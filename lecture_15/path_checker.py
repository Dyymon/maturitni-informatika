import numpy as np
from typing import Tuple


class PathChecker:
    def __init__(self, maze: np.ndarray):
        self.grid = np.asarray(maze)
        if self.grid.ndim != 2:
            raise ValueError("maze must be a 2D array.")

    def evaluate_path(
        self,
        path: np.ndarray,
        start: np.ndarray,
        goal: np.ndarray
    ) -> Tuple[bool, str]:

        path = np.asarray(path)
        start = np.asarray(start)
        goal = np.asarray(goal)

        if path.ndim != 2 or path.shape[1] != 2:
            return False, "path must have shape (n, 2)."

        if start.shape != (2,) or goal.shape != (2,):
            return False, "start and goal must have shape (2,)."

        if len(path) == 0:
            return False, "path is empty."

        if not np.array_equal(start, path[0]):
            return False, "start is not at the beginning of the path."

        if not np.array_equal(goal, path[-1]):
            return False, "goal is not at the end of the path."

        inside, location = self.is_path_in_maze(path)
        if not inside:
            return False, f"path is outside the maze at {location} in the path."

        free, location = self.is_path_free(path)
        if not free:
            return False, f"collision present at {location} in the path."

        continuous, location = self.is_path_continuous(path)
        if not continuous:
            return False, f"path is cut at {location} in the path."

        loopless, location = self.is_loopless(path)
        if not loopless:
            return False, f"path is looping at {location} in the path."

        return True, "path is valid"

    def is_path_in_maze(self, path: np.ndarray) -> Tuple[bool, np.ndarray | None]:
        for p in path:
            if not (0 <= p[0] < self.grid.shape[0] and 0 <= p[1] < self.grid.shape[1]):
                return False, p
        return True, None

    def is_path_free(self, path: np.ndarray) -> Tuple[bool, np.ndarray | None]:
        for p in path:
            if self.grid[p[0], p[1]] != 0:
                return False, p
        return True, None

    @staticmethod
    def is_path_continuous(path: np.ndarray) -> Tuple[bool, np.ndarray | None]:
        directions = np.array([
            [-1, 1], [0, 1], [1, 1],
            [-1, 0],         [1, 0],
            [-1, -1], [0, -1], [1, -1]
        ])

        for i, p in enumerate(path[:-1]):
            if not np.any(np.all(directions == (path[i + 1] - p), axis=1)):
                return False, p

        return True, None

    @staticmethod
    def is_loopless(path: np.ndarray) -> Tuple[bool, np.ndarray | None]:
        seen = set()
        for p in path:
            t = tuple(p)
            if t in seen:
                return False, p
            seen.add(t)
        return True, None



if __name__ == "__main__":
    from mazes import maze_10x10_1
    checker = PathChecker(maze_10x10_1)
    start = np.array([0, 0])
    goal = np.array([2, 1])

    # Example bad path (collision / broken step etc.)
    path = np.array([[0, 0], [0, 1], [1, 1], [0, 1], [1, 1], [2, 1]])

    ok, report = checker.evaluate_path(path, start, goal)
    print(ok)
    print(report)