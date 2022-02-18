# represents a solution of the VRP problem.
from enum import Enum


class SolutionStatus(Enum):
    UNKNOWN = 'not defined'
    CONFLICT = 'conflict is detected'
    INFEASIBLE = 'infeasible'
    FOUND = 'solution has been found'


class VRPSolution:

    def __init__(self, sample):
        self.sample = sample

    def str(self) -> str:
        return self.sample.str()
