# This is a main Python script to run VRP model.
import time

from vrp_capacitated import VRPCapacitated
from vrp_data import load_vrp_data


def run_vrp(name):
    print(f'VRP start {name}')
    try:
        data = load_vrp_data()
        vrp = VRPCapacitated(data)
        start = time.monotonic()
        solution = vrp.find_solution()
        run_seconds = time.monotonic() - start
        print(f'run_seconds {run_seconds:0,.4f}')
        if solution is None:
            print('solution is NOT found.')
        else:
            print('solution is found.')
            print(solution.to_string())
        print(f'VRP done {name}')
    except ValueError as e:
        print(f'VRP ERROR: {e}')


if __name__ == '__main__':
    # expected solution  [[0, 3, 1], [0, 2]]
    run_vrp('first')
