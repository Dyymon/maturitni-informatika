import numpy as np
from collections import deque
import matplotlib.pyplot as plt

from grid_map import MazePlotter

def bfs_grid(grid: np.ndarray, start, goal):
    """
    Breadth-first search on a 4-neighbor grid.
    grid: (N,N) with 0 free, 1 obstacle
    start/goal: (x,y)
    Returns: path as (K,2) np.array of (x,y), or None if no path
    """
    grid = np.asarray(grid)
    N = grid.shape[0]
    sx, sy = int(start[0]), int(start[1])
    gx, gy = int(goal[0]), int(goal[1])

    def in_bounds(x, y): return 0 <= x < N and 0 <= y < N
    def is_free(x, y): return grid[y, x] == 0  # (x,y) -> grid[row=y, col=x]

    if not in_bounds(sx, sy) or not in_bounds(gx, gy):
        raise ValueError("start/goal out of bounds")
    if not is_free(sx, sy) or not is_free(gx, gy):
        return None

    q = deque([(sx, sy)])
    parent = {(sx, sy): None}

    while q:
        x, y = q.popleft()
        if (x, y) == (gx, gy):
            # reconstruct
            path = []
            cur = (x, y)
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return np.array(path, dtype=int)

        for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny) and is_free(nx, ny) and (nx, ny) not in parent:
                parent[(nx, ny)] = (x, y)
                q.append((nx, ny))

    return None


def bfs_grid_live(grid: np.ndarray, start, goal, plotter, pause=0.01):
    """
    BFS with live visualization using your MazePlotter class.
      - frontier: light blue
      - explored: blue

    plotter must be a MazePlotter created with live=True.
    Returns: path as (K,2) np.array, or None
    """
    grid = np.asarray(grid)
    N = grid.shape[0]
    sx, sy = int(start[0]), int(start[1])
    gx, gy = int(goal[0]), int(goal[1])

    def in_bounds(x, y): return 0 <= x < N and 0 <= y < N
    def is_free(x, y): return grid[y, x] == 0

    if not in_bounds(sx, sy) or not in_bounds(gx, gy):
        raise ValueError("start/goal out of bounds")
    if not is_free(sx, sy) or not is_free(gx, gy):
        return None

    # Create TWO scatter artists once, then update their offsets each step.
    # Frontier = light blue, Explored = blue
    frontier_sc = plotter.add_overlay(np.array([[sx, sy]]), color="#7FDBFF", kind="scatter", markersize=5, alpha=0.9, label="frontier")
    explored_sc = plotter.add_overlay(np.empty((0, 2), dtype=int), color="blue", kind="scatter", markersize=5, alpha=0.9, label="explored")

    q = deque([(sx, sy)])
    parent = {(sx, sy): None}
    explored = set()

    while q:
        # --- update frontier visualization (queue contents) ---
        frontier_pts = np.array(list(q), dtype=float) if len(q) else np.empty((0, 2), dtype=float)
        frontier_sc.set_offsets(frontier_pts)

        # pop
        x, y = q.popleft()
        explored.add((x, y))

        # --- update explored visualization ---
        explored_pts = np.array(list(explored), dtype=float) if len(explored) else np.empty((0, 2), dtype=float)
        explored_sc.set_offsets(explored_pts)

        # refresh
        plotter.fig.canvas.draw_idle()
        plotter.fig.canvas.flush_events()
        plt.pause(pause)

        if (x, y) == (gx, gy):
            # reconstruct + draw final path
            path = []
            cur = (x, y)
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            path = np.array(path, dtype=int)
            plotter.plot_path(path, color="blue", linewidth=2.5, markersize=0, label="path")
            return path

        for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny) and is_free(nx, ny) and (nx, ny) not in parent:
                parent[(nx, ny)] = (x, y)
                q.append((nx, ny))

    return None


# ------------------- Example -------------------
if __name__ == "__main__":
    # Make a toy maze
    N = 20
    grid = np.zeros((N, N), dtype=int)
    grid[3:17, 10] = 1
    grid[10, 10] = 0  # a gap

    start = (2, 2)
    goal = (18, 18)

    # Use your MazePlotter class from earlier (must be in scope)
    mp = MazePlotter(grid, start, goal, live=True, title="BFS Visualization")
    mp.show()

    path = bfs_grid_live(grid, start, goal, mp, pause=0.02)

    print("Path length:" if path is not None else "No path.", None if path is None else len(path))