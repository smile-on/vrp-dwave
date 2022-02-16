from vrp_data import VRPData

# formulates VRP problem
from vrp_solution import VRPSolution, SolutionStatus


class VRPCapacitated(VRPData):

    # formulates VRP problem
    def __init__(self, data: VRPData):
        self.copy(data)
        pass

    status = SolutionStatus.UNKNOWN

    def find_solution(self) -> VRPSolution:
        self.formulate()
        self.solve()
        if self.status == SolutionStatus.FOUND:
            # todo read solution
            pass
        return None

    def formulate(self):
        pass

    def solve(self):
        pass
