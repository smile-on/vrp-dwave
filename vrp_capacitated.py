from dimod import ConstrainedQuadraticModel, Binary, quicksum
from dwave.system import LeapHybridCQMSampler

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
            return self.decode_solution()
        return None

    status = SolutionStatus.UNKNOWN
    cqm = None
    best_sample = None  # can be the best infeasible solution if model has conflicts or infeasibility

    def formulate(self):
        self.cqm = ConstrainedQuadraticModel()
        # x = Boolean[van, node, stop-1]
        x = [[[Binary(f'x_{v}.{n}.{s}') for s in range(1, self.n_stops)] for n in range(self.n_nodes)] for v in
             range(self.n_vans)]
        # s.t.
        # each stop is visited. Disjoint One-Hot constraint
        for s in range(1, self.n_stops):
            self.cqm.add_discrete([f'x_{v}.{n}.{s}' for n in range(self.n_nodes) for v in range(self.n_vans)],
                                  label=f"stop-has-visit-{s}")
        # each node is assigned to one stop at most
        for v in range(self.n_vans):
            for n in range(self.n_nodes):
                self.cqm.add_constraint(quicksum(x[v][n][s - 1] for s in range(1, self.n_stops)) <= 1,
                                        label=f"van-node-one-stop-{v}.{n}")
        # todo add constraint on capacity.
        # obj
        routes = []
        for v in range(self.n_vans):
            # departure leg
            n = 0
            leg_cost = quicksum(self.cost[0][s] * x[v][n][s - 1] for s in range(1, self.n_stops))
            routes.append(leg_cost)
            # move leg = cost[s’][s”] * x[v][n-1][s’] * x[v][n][s”]
            for n in range(1, self.n_nodes):
                leg_cost = quicksum(
                    [self.cost[s1][s2] * x[v][n - 1][s1 - 1] * x[v][n][s2 - 1]
                     for s2 in range(1, self.n_stops) for s1 in range(1, self.n_stops)])
                routes.append(leg_cost)
        # minimize
        self.cqm.set_objective(quicksum(routes))

    def solve(self):
        # self.model_dump_to("../self.cqm.bin")
        sampler = LeapHybridCQMSampler()
        answer = sampler.sample_cqm(self.cqm)  # time_limit=5 sec num_reads=?
        try:
            self.best_sample = answer.filter(lambda d: d.is_feasible).first.sample
            self.status = SolutionStatus.FOUND
        except ValueError:
            try:
                self.best_sample = answer.first.sample
                self.status = SolutionStatus.INFEASIBLE
            except ValueError:
                self.best_sample = None
                self.status = SolutionStatus.UNKNOWN

    def decode_solution(self) -> VRPSolution:
        """Interpret the sample found in terms of routes."""
        routes = []
        for v in range(self.n_vans):
            route = [0]
            for n in range(self.n_nodes):
                for s in range(1, self.n_stops):
                    # best_sample.sample['x']
                    if self.best_sample[f'x_{v}.{n}.{s}'] > 0:
                        route.append(s)
                        break
                pass
            pass
            routes.append(route)
        pass
        return VRPSolution(routes, self.cost)

    def model_dump_to(self, file_name: str):
        """Write dump of the cqm model into the file for debugging purpose."""
        with open(file_name, "wb", buffering=0) as f:
            f.write(self.cqm.to_file().read())
