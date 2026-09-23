import numpy as np

class Planner:

    def __init__(self, grid: np.ndarray):
        """
        initialize the planner

        :param grid: 2D numpy array where 1 = obstacle, 0 = free space
        """
        self.grid = grid

    def plan(self, start: np.ndarray, goal: np.ndarray)->np.ndarray:
        """
        will return the planned path from start to goal

        :param start: 1D numpy array of i, j position of start in the grid ie grid[i][j]
        :param goal: 1D numpy array of i, j position of goal in the grid ie grid[i][j]
        :return: 2D numpy array of i, j positions of planned path
        """

        return np.array([start, goal])