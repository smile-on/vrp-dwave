from dimod import ConstrainedQuadraticModel, Binary, quicksum
from dwave.system import LeapHybridSampler

from vrp_data import VRPData
# formulates VRP problem
from vrp_solution import VRPSolution, SolutionStatus


class VRPCapacitated(VRPData):

    # formulates VRP problem
    def __init__(self, data: VRPData):
        self.copy(data)
        pass

    def find_solution(self) -> VRPSolution:
        self.formulate()
        self.solve()
        if self.status == SolutionStatus.FOUND:
            # todo read solution
            # solution = [k for k, v in self.best_solution.items() if v == 1]
            return VRPSolution(self.best_solution)
        return None

    status = SolutionStatus.UNKNOWN
    cqm = None
    x = {}  # Boolean[van, node, stop-1]
    best_solution = None  # best infeasible solution if model has conflicts or infeasibility

    def formulate(self):
        self.cqm = ConstrainedQuadraticModel()
        # BinaryArray
        self.x = [[[Binary(f'x_{v}.{n}.{s}') for s in range(1, self.n_stops)] for n in range(self.n_nodes)] for v in
                  range(self.n_vans)]
        # s.t.
        # each stop is visited. Disjoint One-Hot constraint
        for s in range(1, self.n_stops):
            self.cqm.add_discrete([f'x_{v}.{n}.{s}' for n in range(self.n_nodes) for v in range(self.n_vans)],
                                  label=f"stop-has-visit-{s}")
        # each node is assigned to one stop at most
        for v in range(self.n_vans):
            for n in range(self.n_nodes):
                self.cqm.add_constraint(quicksum(self.x[v][n][s - 1] for s in range(1, self.n_stops)) <= 1,
                                        label=f"van-node-one-stop-{v}.{n}")
        # todo add constraint on capacity.
        # obj
        routes = []
        for v in range(self.n_vans):
            # departure
            n = 0
            leg_cost = quicksum(self.cost[0][s] * self.x[v][n][s - 1] for s in range(1, self.n_stops))
            routes.append(leg_cost)
            # cost[s’][s”] * x[v][n-1][s’] * x[v][n][s”]
            for n in range(1, self.n_nodes):
                leg_cost = quicksum(
                    [self.cost[s1][s2] * self.x[v][n - 1][s1 - 1] * self.x[v][n][s2 - 1]
                     for s2 in range(1, self.n_stops) for s1 in range(1, self.n_stops)])
                routes.append(leg_cost)
        # minimize
        self.cqm.set_objective(sum(routes))

    def solve(self):
        # fixme debug model
        with open("../cqm.bin", "wb", buffering=0) as f:
            f.write(self.cqm.to_file().read())
        answer = LeapHybridSampler().sample(self.cqm)  # time_limit=60 sec num_reads=?
        try:
            self.best_solution = answer.filter(lambda d: d.is_feasible).first
            self.status = SolutionStatus.FOUND
            # fixme debug solution decoding
            print(answer)
        except ValueError:
            try:
                self.best_solution = answer.first
                self.status = SolutionStatus.INFEASIBLE
            except ValueError:
                self.best_solution = None
                self.status = SolutionStatus.UNKNOWN
