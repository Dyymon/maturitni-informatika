import numpy as np

class Planner:

    def __init__(self, grid: np.ndarray):
        self.grid = grid

    def plan(self, start: np.ndarray, goal: np.ndarray)->np.ndarray:

        return np.array([start])

if __name__ == "__main__":
    from mazes import maze_10x10_1
    from path_checker import PathChecker
    planner = Planner(grid=maze_10x10_1)
    checker = PathChecker(maze=maze_10x10_1)

    start = np.array([0,0])
    goal = np.array([9,9])

    path = planner.plan(start, goal)
    print(checker.evaluate_path(path, start=start, goal=goal))


