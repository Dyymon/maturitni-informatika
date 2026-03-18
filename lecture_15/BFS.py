import numpy as np
from collections import deque

from grid_map import MazePlotter


def bfs_grid(grid: np.ndarray, start, goal):
    """
    Breadth-first search on a 4-neighbor grid using [i, j] coordinates.

    grid[i, j]:
      - 0 = free
      - 1 = obstacle

    start, goal:
      - [i, j]

    Returns:
      - path as (K, 2) np.array of [i, j]
      - None if no path exists
    """
    grid = np.asarray(grid)
    n_rows, n_cols = grid.shape

    start = np.asarray(start, dtype=int)
    goal = np.asarray(goal, dtype=int)

    si, sj = int(start[0]), int(start[1])
    gi, gj = int(goal[0]), int(goal[1])

    def in_bounds(i, j):
        return 0 <= i < n_rows and 0 <= j < n_cols

    def is_free(i, j):
        return grid[i, j] == 0

    if not in_bounds(si, sj) or not in_bounds(gi, gj):
        raise ValueError("start/goal out of bounds")
    if not is_free(si, sj) or not is_free(gi, gj):
        return None

    q = deque([(si, sj)])
    parent = {(si, sj): None}

    while q:
        i, j = q.popleft()

        if (i, j) == (gi, gj):
            path = []
            cur = (i, j)
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return np.array(path, dtype=int)

        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if in_bounds(ni, nj) and is_free(ni, nj) and (ni, nj) not in parent:
                parent[(ni, nj)] = (i, j)
                q.append((ni, nj))

    return None


def bfs_grid_live(grid: np.ndarray, start, goal, plotter=None, pause: float = 0.05):
    """
    BFS with live visualization using MazePlotter.

    Uses the same style as your Planner:
      - explored: orange filled cells
      - frontier: dodgerblue filled cells
      - current:  purple filled cell
      - final path: limegreen line + markers

    Coordinates are [i, j].
    """
    grid = np.asarray(grid)
    n_rows, n_cols = grid.shape

    start = np.asarray(start, dtype=int)
    goal = np.asarray(goal, dtype=int)

    si, sj = int(start[0]), int(start[1])
    gi, gj = int(goal[0]), int(goal[1])

    def in_bounds(i, j):
        return 0 <= i < n_rows and 0 <= j < n_cols

    def is_free(i, j):
        return grid[i, j] == 0

    if not in_bounds(si, sj) or not in_bounds(gi, gj):
        raise ValueError("start/goal out of bounds")
    if not is_free(si, sj) or not is_free(gi, gj):
        return None

    q = deque([(si, sj)])
    parent = {(si, sj): None}
    explored = set()

    frontier_artist = None
    explored_artist = None
    current_artist = None

    while q:
        i, j = q.popleft()
        explored.add((i, j))

        if plotter is not None:
            if frontier_artist is not None:
                frontier_artist.remove()
            if explored_artist is not None:
                explored_artist.remove()
            if current_artist is not None:
                current_artist.remove()

            explored_pts = np.array(list(explored), dtype=int)
            if explored_pts.size > 0:
                explored_artist = plotter.add_overlay(
                    explored_pts,
                    color="orange",
                    kind="cells",
                    alpha=0.35,
                    label="explored",
                    zorder=2,
                )
            else:
                explored_artist = None

            frontier_pts = np.array(list(q), dtype=int)
            if frontier_pts.size > 0:
                frontier_artist = plotter.add_overlay(
                    frontier_pts,
                    color="dodgerblue",
                    kind="cells",
                    alpha=0.45,
                    label="frontier",
                    zorder=4,
                )
            else:
                frontier_artist = None

            current_artist = plotter.add_overlay(
                np.array([[i, j]], dtype=int),
                color="purple",
                kind="cells",
                alpha=0.85,
                label="current",
                zorder=6,
            )

            if plotter.live:
                import matplotlib.pyplot as plt
                plt.pause(pause)

        if (i, j) == (gi, gj):
            path = []
            cur = (i, j)
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            path = np.array(path, dtype=int)

            if plotter is not None:
                if current_artist is not None:
                    current_artist.remove()

                plotter.add_overlay(
                    path,
                    color="limegreen",
                    kind="line",
                    linewidth=3.0,
                    alpha=1.0,
                    label="path",
                    zorder=9,
                )
                plotter.add_overlay(
                    path,
                    color="limegreen",
                    kind="scatter",
                    markersize=4,
                    alpha=1.0,
                    zorder=10,
                )

            return path

        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if in_bounds(ni, nj) and is_free(ni, nj) and (ni, nj) not in parent:
                parent[(ni, nj)] = (i, j)
                q.append((ni, nj))

    return None


# ------------------- Example -------------------
if __name__ == "__main__":
    import time
    from mazes import maze_20x20_1
    from path_checker import PathChecker

    maze = maze_20x20_1
    checker = PathChecker(grid=maze)

    start = np.array([0, 0])
    goal = np.array([19, 19])

    plotter = MazePlotter(
        grid=maze,
        start=start,
        goal=goal,
        live=True,
        title="BFS progress / frontier / explored / path",
    )

    path = bfs_grid_live(maze, start, goal, plotter=plotter, pause=0.05)

    plotter.show()
    print(path)
    print(checker.evaluate_path(path, start=start, goal=goal) if path is not None else "No path")
    time.sleep(100)