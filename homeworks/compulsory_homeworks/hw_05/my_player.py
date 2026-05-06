import numpy as np
from typing import Optional, Tuple


class StudentBot:
    def __init__(self, name: str = "My Student Bot"):
        self.name = name

    def choose_move(
        self,
        board: np.ndarray,
        player: int,
        win_length: int
    ) -> Optional[Tuple[int, int]]:

        empty_cells = np.argwhere(board == 0)

        if len(empty_cells) == 0:
            return None

        row, col = empty_cells[0]
        return int(row), int(col)