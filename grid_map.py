import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class MazePlotter:
    """
    Grid maze plotter.

    grid: (N, N) np.array, 0 = free, 1 = obstacle
    start: (x, y) tuple or array-like
    goal:  (x, y) tuple or array-like

    Coordinates are interpreted as (x, y) where:
      - x is column index in [0, N-1]
      - y is row index in [0, N-1]
    """

    def __init__(
        self,
        grid: np.ndarray,
        start,
        goal,
        path: np.ndarray | None = None,
        live: bool = False,
        cell_size: float = 6.0,
        title: str = "Grid Maze",
    ):
        self.grid = np.asarray(grid)
        if self.grid.ndim != 2 or self.grid.shape[0] != self.grid.shape[1]:
            raise ValueError("grid must be a 2D square array (N x N).")
        self.N = self.grid.shape[0]

        self.start = self._to_xy(start, name="start")
        self.goal = self._to_xy(goal, name="goal")

        self.live = bool(live)
        self.title = title

        self.fig, self.ax = plt.subplots(figsize=(cell_size, cell_size))
        self._setup_base_plot()

        # Plot initial items
        self._draw_start_goal()
        if path is not None:
            self.plot_path(path, color="blue", linewidth=2.5, markersize=3, label="path")

        self._finalize_show()

    # ---------- public API ----------

    def show(self):
        """Show the plot (non-blocking if live=True)."""
        if self.live:
            plt.show(block=False)
        else:
            plt.show()

    def plot_path(
        self,
        path: np.ndarray,
        color: str = "blue",
        linewidth: float = 2.5,
        markersize: float = 0.0,
        label: str | None = None,
        zorder: int = 5,
    ):
        """
        Plot a path (K x 2) of (x, y) coords.
        In live mode this updates immediately.
        """
        pts = self._validate_path(path)
        (line,) = self.ax.plot(
            pts[:, 0],
            pts[:, 1],
            color=color,
            linewidth=linewidth,
            marker="o" if markersize > 0 else None,
            markersize=markersize if markersize > 0 else None,
            label=label,
            zorder=zorder,
        )
        self._refresh()
        return line

    def add_overlay(
        self,
        coords: np.ndarray,
        color: str = "blue",
        kind: str = "line",
        linewidth: float = 2.0,
        markersize: float = 6.0,
        alpha: float = 1.0,
        label: str | None = None,
        zorder: int = 6,
    ):
        """
        Live overlay helper.

        coords: (K, 2) array of (x, y)
        kind:
          - "line"  : connect points with lines
          - "scatter": scatter points
          - "points" : alias for scatter

        Returns the created artist.
        """
        pts = self._validate_path(coords)

        kind = kind.lower()
        if kind in ("scatter", "points"):
            artist = self.ax.scatter(
                pts[:, 0], pts[:, 1],
                s=markersize**2 / 2.0,
                c=color,
                alpha=alpha,
                label=label,
                zorder=zorder,
            )
        elif kind == "line":
            (artist,) = self.ax.plot(
                pts[:, 0], pts[:, 1],
                color=color,
                linewidth=linewidth,
                alpha=alpha,
                label=label,
                zorder=zorder,
            )
        else:
            raise ValueError("kind must be one of: 'line', 'scatter', 'points'.")

        self._refresh()
        return artist

    def clear_overlays(self, keep_start_goal: bool = True):
        """
        Remove plotted overlays (paths/scatters). Optionally keep start/goal.
        """
        # Wipe axis and redraw base
        self.ax.cla()
        self._setup_base_plot()
        if keep_start_goal:
            self._draw_start_goal()
        self._refresh()

    def update_grid(self, new_grid: np.ndarray, redraw: bool = True):
        """
        Replace the grid. If redraw=True, it refreshes the plot.
        """
        new_grid = np.asarray(new_grid)
        if new_grid.shape != (self.N, self.N):
            raise ValueError(f"new_grid must have shape {(self.N, self.N)}")
        self.grid = new_grid
        if redraw:
            self.clear_overlays(keep_start_goal=True)

    # ---------- internal helpers ----------

    def _setup_base_plot(self):
        # Colormap: free=white, obstacle=black
        cmap = ListedColormap(["white", "black"])

        # Use origin="lower" so y increases upward like standard Cartesian coords
        self.ax.imshow(
            self.grid,
            cmap=cmap,
            origin="lower",
            interpolation="none",
            vmin=0,
            vmax=1,
            extent=(-0.5, self.N - 0.5, -0.5, self.N - 0.5),
            zorder=0,
        )

        # Grid lines at cell boundaries
        self.ax.set_xticks(np.arange(-0.5, self.N, 1), minor=True)
        self.ax.set_yticks(np.arange(-0.5, self.N, 1), minor=True)
        self.ax.grid(which="minor", linestyle="-", linewidth=0.6, alpha=0.35)

        # Major ticks centered on cells (0..N-1)
        self.ax.set_xticks(np.arange(0, self.N, 1))
        self.ax.set_yticks(np.arange(0, self.N, 1))

        self.ax.set_xlim(-0.5, self.N - 0.5)
        self.ax.set_ylim(-0.5, self.N - 0.5)
        self.ax.set_aspect("equal")
        self.ax.set_title(self.title)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")

    def _draw_start_goal(self):
        sx, sy = self.start
        gx, gy = self.goal

        # Start: green, Goal: red
        self.ax.scatter([sx], [sy], s=120, c="green", edgecolors="k", linewidths=0.8, zorder=10, label="start")
        self.ax.scatter([gx], [gy], s=120, c="red",   edgecolors="k", linewidths=0.8, zorder=10, label="goal")

    def _to_xy(self, pt, name="point"):
        arr = np.asarray(pt).reshape(-1)
        if arr.size != 2:
            raise ValueError(f"{name} must be length-2 (x, y).")
        x, y = int(arr[0]), int(arr[1])
        self._check_in_bounds(x, y, name=name)
        return (x, y)

    def _check_in_bounds(self, x: int, y: int, name="coord"):
        if not (0 <= x < self.N and 0 <= y < self.N):
            raise ValueError(f"{name} ({x}, {y}) out of bounds for N={self.N}.")

    def _validate_path(self, path: np.ndarray):
        pts = np.asarray(path)
        if pts.ndim != 2 or pts.shape[1] != 2:
            raise ValueError("path/coords must be a (K, 2) array of (x, y).")
        # Coerce to float for plotting, but validate bounds as ints
        for i, (x, y) in enumerate(pts):
            xi, yi = int(x), int(y)
            self._check_in_bounds(xi, yi, name=f"coords[{i}]")
        return pts.astype(float)

    def _finalize_show(self):
        # Nice legend if labels exist
        handles, labels = self.ax.get_legend_handles_labels()
        if labels:
            self.ax.legend(loc="upper right", framealpha=0.9)

        if self.live:
            plt.ion()
            plt.show(block=False)
            self._refresh()
        else:
            # In non-live mode, don't auto-block here; user can call show()
            pass

    def _refresh(self):
        # Redraw immediately if live
        if self.live:
            self.fig.canvas.draw_idle()
            self.fig.canvas.flush_events()
            plt.pause(0.001)

if __name__ == "__main__":

    N = 10
    grid = np.zeros((N, N), dtype=int)
    grid[3:8, 4] = 1

    start = (0, 0)
    goal = (9, 9)

    path = np.array(
        [[0, 0], [1, 0], [2, 0], [3, 0], [4, 1], [5, 2], [6, 3], [7, 4], [8, 5], [9, 6],
         [9, 7], [9, 8], [9, 9]])

    mp = MazePlotter(grid, start, goal, path=path, live=True, title="My Maze")
    mp.show()

    # Later: update live with a new overlay in purple
    new_segment = np.array([[3, 3], [4, 3], [5, 3], [6, 3]])
    mp.add_overlay(new_segment, color="purple", kind="line", linewidth=3)

    # Or scatter explored nodes in orange
    explored = np.array([[1, 1], [1, 2], [2, 2], [3, 2]])
    mp.add_overlay(explored, color="orange", kind="scatter", markersize=5)