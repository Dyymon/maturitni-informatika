import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection


class MazePlotter:
    """
    Grid maze plotter using matrix indexing convention.

    grid[i, j]:
      - i = row index
      - j = column index

    So any point [i, j] refers to the same cell as maze[i, j] or maze[i][j].

    grid: 2D np.array
      - 0 = free
      - 1 = obstacle

    start, goal:
      - length-2 coordinates in [i, j] format

    path:
      - (K, 2) array of [i, j] coordinates
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
        if self.grid.ndim != 2:
            raise ValueError("grid must be a 2D array.")
        self.n_rows, self.n_cols = self.grid.shape

        self.start = self._to_ij(start, name="start")
        self.goal = self._to_ij(goal, name="goal")

        self.live = bool(live)
        self.title = title

        self.fig, self.ax = plt.subplots(figsize=(cell_size, cell_size))
        self._setup_base_plot()

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
        Plot a path given as (K, 2) array of [i, j] coords.
        """
        pts = self._validate_path(path)
        x, y = self._ij_to_xy(pts)

        (line,) = self.ax.plot(
            x,
            y,
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
        edgecolor: str | None = None,
    ):
        """
        Add overlay using [i, j] coordinates.

        kind:
          - "line"
          - "scatter"
          - "points" : alias for scatter
          - "cells"
          - "fill"   : alias for cells
        """
        pts = self._validate_path(coords)
        x, y = self._ij_to_xy(pts)

        kind = kind.lower()

        if kind in ("scatter", "points"):
            artist = self.ax.scatter(
                x,
                y,
                s=markersize**2 / 2.0,
                c=color,
                alpha=alpha,
                label=label,
                zorder=zorder,
            )

        elif kind == "line":
            (artist,) = self.ax.plot(
                x,
                y,
                color=color,
                linewidth=linewidth,
                alpha=alpha,
                label=label,
                zorder=zorder,
            )

        elif kind in ("cells", "fill"):
            patches = []
            for i, j in pts:
                # cell centered at (j, i), so lower-left corner is (j-0.5, i-0.5)
                rect = Rectangle((j - 0.5, i - 0.5), 1.0, 1.0)
                patches.append(rect)

            artist = PatchCollection(
                patches,
                facecolor=color,
                edgecolor=edgecolor if edgecolor is not None else "none",
                linewidth=linewidth,
                alpha=alpha,
                zorder=zorder,
            )

            if label is not None:
                artist.set_label(label)

            self.ax.add_collection(artist)

        else:
            raise ValueError("kind must be one of: 'line', 'scatter', 'points', 'cells', 'fill'.")

        self._refresh()
        return artist

    def clear_overlays(self, keep_start_goal: bool = True):
        """Remove overlays and redraw the base maze."""
        self.ax.cla()
        self._setup_base_plot()
        if keep_start_goal:
            self._draw_start_goal()
        self._refresh()

    def update_grid(self, new_grid: np.ndarray, redraw: bool = True):
        """Replace the grid and optionally redraw."""
        new_grid = np.asarray(new_grid)
        if new_grid.shape != (self.n_rows, self.n_cols):
            raise ValueError(f"new_grid must have shape {(self.n_rows, self.n_cols)}")
        self.grid = new_grid
        if redraw:
            self.clear_overlays(keep_start_goal=True)

    # ---------- internal helpers ----------

    def _setup_base_plot(self):
        cmap = ListedColormap(["white", "black"])

        self.ax.imshow(
            self.grid,
            cmap=cmap,
            origin="lower",
            interpolation="none",
            vmin=0,
            vmax=1,
            extent=(-0.5, self.n_cols - 0.5, -0.5, self.n_rows - 0.5),
            zorder=0,
        )

        self.ax.set_xticks(np.arange(-0.5, self.n_cols, 1), minor=True)
        self.ax.set_yticks(np.arange(-0.5, self.n_rows, 1), minor=True)
        self.ax.grid(which="minor", linestyle="-", linewidth=0.6, alpha=0.35)

        self.ax.set_xticks(np.arange(0, self.n_cols, 1))
        self.ax.set_yticks(np.arange(0, self.n_rows, 1))

        self.ax.set_xlim(-0.5, self.n_cols - 0.5)
        self.ax.set_ylim(-0.5, self.n_rows - 0.5)
        self.ax.set_aspect("equal")
        self.ax.set_title(self.title)
        self.ax.set_xlabel("j (column)")
        self.ax.set_ylabel("i (row)")

    def _draw_start_goal(self):
        si, sj = self.start
        gi, gj = self.goal

        self.ax.scatter(
            [sj], [si],
            s=120, c="green", edgecolors="k",
            linewidths=0.8, zorder=10, label="start"
        )
        self.ax.scatter(
            [gj], [gi],
            s=120, c="red", edgecolors="k",
            linewidths=0.8, zorder=10, label="goal"
        )

    def _to_ij(self, pt, name="point"):
        arr = np.asarray(pt).reshape(-1)
        if arr.size != 2:
            raise ValueError(f"{name} must be length-2 [i, j].")
        i, j = int(arr[0]), int(arr[1])
        self._check_in_bounds(i, j, name=name)
        return (i, j)

    def _check_in_bounds(self, i: int, j: int, name="coord"):
        if not (0 <= i < self.n_rows and 0 <= j < self.n_cols):
            raise ValueError(
                f"{name} [{i}, {j}] out of bounds for grid shape {self.grid.shape}."
            )

    def _validate_path(self, path: np.ndarray):
        pts = np.asarray(path)
        if pts.ndim != 2 or pts.shape[1] != 2:
            raise ValueError("path/coords must be a (K, 2) array of [i, j].")

        for k, (i, j) in enumerate(pts):
            ii, jj = int(i), int(j)
            self._check_in_bounds(ii, jj, name=f"coords[{k}]")

        return pts.astype(float)

    def _ij_to_xy(self, pts: np.ndarray):
        """
        Convert array of [i, j] points into plotting coordinates:
          x = j
          y = i
        """
        x = pts[:, 1]
        y = pts[:, 0]
        return x, y

    def _finalize_show(self):
        handles, labels = self.ax.get_legend_handles_labels()
        if labels:
            self.ax.legend(loc="upper right", framealpha=0.9)

        if self.live:
            plt.ion()
            plt.show(block=False)
            self._refresh()

    def _refresh(self):
        if self.live:
            self.fig.canvas.draw_idle()
            self.fig.canvas.flush_events()
            plt.pause(0.001)


if __name__ == "__main__":
    n = 10
    grid = np.zeros((n, n), dtype=int)

    # obstacle at grid[i, j]
    grid[3:8, 4] = 1

    start = (0, 0)   # [i, j]
    goal = (9, 9)    # [i, j]

    # Path is now explicitly [i, j]
    path = np.array([
        [0, 0],
        [0, 1],
        [0, 2],
        [0, 3],
        [1, 4],
        [2, 5],
        [3, 6],
        [4, 7],
        [5, 8],
        [6, 9],
        [7, 9],
        [8, 9],
        [9, 9],
    ])

    mp = MazePlotter(grid, start, goal, path=path, live=True, title="Maze ([i, j] indexing)")
    mp.show()

    # Another line overlay in [i, j]
    new_segment = np.array([
        [3, 3],
        [3, 4],
        [3, 5],
        [3, 6],
    ])
    mp.add_overlay(new_segment, color="purple", kind="line", linewidth=3)

    # Scatter explored nodes in [i, j]
    explored = np.array([
        [1, 1],
        [2, 1],
        [2, 2],
        [2, 3],
    ])
    mp.add_overlay(explored, color="orange", kind="scatter", markersize=5)