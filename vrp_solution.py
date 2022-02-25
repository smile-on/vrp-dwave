# represents a solution of the VRP problem.
from enum import Enum


class SolutionStatus(Enum):
    UNKNOWN = 'not defined'
    CONFLICT = 'conflict is detected'
    INFEASIBLE = 'infeasible'
    FOUND = 'solution has been found'


class VRPSolution:

    def __init__(self, routes, cost):
        """Interpret the sample found in terms of routes
        Args:
            routes [[0, 3, 1], [0, 2]] """""
        self.routes = routes
        self.total_cost = 0
        for r in routes:
            s1 = None
            for s2 in r:
                if s1 is not None:
                    self.total_cost += cost[s1][s2]
                s1 = s2

    def str(self) -> str:
        """describe the solution"""
        return f' routes {self.routes.__str__()} \n total cost {self.total_cost}'
