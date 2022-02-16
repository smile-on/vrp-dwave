from vrp_data import VRPData

# formulates VRP problem
from vrp_solution import VRPSolution


class VRPCapacitated(VRPData):

    # formulates VRP problem
    def __init__(self, data: VRPData):
        self.copy(data)
        pass

    status = None

    def find_solution(self) -> VRPSolution:
        return None
