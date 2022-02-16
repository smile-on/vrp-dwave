import numpy as np


# VRPData defines VRP problem
class VRPData:
    n_stops = 0
    capacity_stop = np.zeros(n_stops, dtype=int)
    n_vans = 2
    capacity_van = np.zeros(n_vans, dtype=int)
    n_nodes = 3
    cost = np.zeros((n_stops, n_stops), dtype=np.double)

    # copy constructor
    def copy(self, data):
        self.n_stops = data.n_stops
        self.capacity_stop = np.copy(data.capacity_stop)
        self.n_vans = data.n_vans
        self.capacity_van = np.copy(data.capacity_van)
        self.n_nodes = data.n_nodes
        self.cost = np.copy(data.cost)
        self.integrity_check()

    # integrity checks on internal data structures
    def integrity_check(self):
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
