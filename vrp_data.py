import numpy as np


class VRPData:
    """VRPData completely defines VRP problem."""

    n_stops = 0
    capacity_stop = np.zeros(n_stops, dtype=int)
    n_vans = 0
    capacity_van = np.zeros(n_vans, dtype=int)
    n_nodes = 0
    cost = np.zeros((n_stops, n_stops), dtype=np.double)

    def copy(self, other):
        """Makes this VRPData instance a full copy of the other VRPData object."""
        self.n_stops = other.n_stops
        self.capacity_stop = np.copy(other.capacity_stop)
        self.n_vans = other.n_vans
        self.capacity_van = np.copy(other.capacity_van)
        self.n_nodes = other.n_nodes
        self.cost = np.copy(other.cost)
        self.integrity_check()

    def integrity_check(self):
        """Performs data integrity checks on internal data structures."""
        capacity_stop_shape = (self.n_stops,)
        if self.capacity_stop.shape != capacity_stop_shape:
            raise ValueError(
                f'capacity_stop.shape {self.capacity_stop.shape} expected {capacity_stop_shape}')
        capacity_van_shape = (self.n_vans,)
        if self.capacity_van.shape != capacity_van_shape:
            raise ValueError(f'capacity_van.shape {self.capacity_van.shape} expected {capacity_van_shape}')
        if sum(self.capacity_stop) > sum(self.capacity_van):
            raise ValueError(f' sum capacity_stop {sum(self.capacity_stop)} > capacity_van {sum(self.capacity_van)}')


def load_vrp_data() -> VRPData:
    """A toy VRP problem as defined at https://github.com/smile-on/ortools-samples ."""
    data = VRPData()
    data.n_stops = 4
    data.capacity_stop = np.array([0, 1, 1, 1], dtype=int)
    data.n_vans = 2
    data.capacity_van = np.array([2, 2], dtype=int)
    data.n_nodes = 3
    data.cost = np.array([
        [0, 5, 3, 6],
        [5, 0, 8, 1],
        [3, 8, 0, 4],
        [6, 1, 4, 0],
    ], dtype=np.double)
    data.integrity_check()
    return data
