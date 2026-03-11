import numpy as np

class Planner:

    def __init__(self, grid: np.ndarray):
        self.grid = grid

    def plan(self, start: np.ndarray, goal: np.ndarray)->np.ndarray:

        return start