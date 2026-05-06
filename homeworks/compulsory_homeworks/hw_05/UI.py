import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from typing import Optional, Protocol, Tuple, List
import random
import numpy as np

from my_player import StudentBot


# ==============================
# Core game model
# ==============================

class MoveSource(Protocol):
    name: str

    def choose_move(
        self,
        board: np.ndarray,
        player: int,
        win_length: int
    ) -> Optional[Tuple[int, int]]:
        ...


@dataclass
class GameConfig:
    rows: int = 10
    cols: int = 10
    win_length: int = 4


class GameState:
    def __init__(self, config: GameConfig):
        self.config = config
        self.board = np.zeros((config.rows, config.cols), dtype=int)

        self.current_player = 1
        self.winner: Optional[int | str] = None
        self.winning_cells: List[Tuple[int, int]] = []
        self.move_count = 0

    def reset(self) -> None:
        self.board[:, :] = 0
        self.current_player = 1
        self.winner = None
        self.winning_cells = []
        self.move_count = 0

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.config.rows and 0 <= col < self.config.cols

    def is_legal_move(self, row: int, col: int) -> bool:
        return (
            self.in_bounds(row, col)
            and self.board[row, col] == 0
            and self.winner is None
        )

    def legal_moves(self) -> List[Tuple[int, int]]:
        positions = np.argwhere(self.board == 0)
        return [tuple(pos) for pos in positions]

    def apply_move(self, row: int, col: int) -> bool:
        if not self.is_legal_move(row, col):
            return False

        self.board[row, col] = self.current_player
        self.move_count += 1

        winner, winning_cells = self.check_winner_from(row, col)

        if winner is not None:
            self.winner = winner
            self.winning_cells = winning_cells
        elif self.move_count == self.config.rows * self.config.cols:
            self.winner = "Draw"
        else:
            self.current_player = 2 if self.current_player == 1 else 1

        return True

    def check_winner_from(
        self,
        row: int,
        col: int
    ) -> Tuple[Optional[int], List[Tuple[int, int]]]:

        player = self.board[row, col]

        if player == 0:
            return None, []

        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
        ]

        for dr, dc in directions:
            line = [(row, col)]

            r, c = row + dr, col + dc
            while self.in_bounds(r, c) and self.board[r, c] == player:
                line.append((r, c))
                r += dr
                c += dc

            r, c = row - dr, col - dc
            while self.in_bounds(r, c) and self.board[r, c] == player:
                line.insert(0, (r, c))
                r -= dr
                c -= dc

            if len(line) >= self.config.win_length:
                return player, line[:self.config.win_length]

        return None, []


# ==============================
# Player / bot implementations
# ==============================

class HumanPlayer:
    def __init__(self, name: str = "Human"):
        self.name = name

    def choose_move(
        self,
        board: np.ndarray,
        player: int,
        win_length: int
    ) -> Optional[Tuple[int, int]]:
        return None


class RandomBot:
    def __init__(self, name: str = "Random Bot"):
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

        row, col = random.choice(empty_cells)
        return int(row), int(col)

# ==============================
# GUI
# ==============================

class TicTacToeApp:
    PLAYER_OPTIONS = {
        "Human": HumanPlayer,
        "Random Bot": RandomBot,
        "Student Bot": StudentBot,
    }

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Generalized Tic Tac Toe")

        self.config = GameConfig(rows=10, cols=10, win_length=4)
        self.game = GameState(self.config)

        self.player_x: MoveSource = HumanPlayer("Player 1")
        self.player_o: MoveSource = HumanPlayer("Player 2")

        self.cell_buttons: List[List[tk.Button]] = []
        self.auto_play_job = None

        self.build_controls()
        self.build_board()
        self.update_status()
        self.maybe_run_program_turn()

    def build_controls(self) -> None:
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(control_frame, text="Rows").grid(row=0, column=0)
        self.rows_var = tk.IntVar(value=self.config.rows)
        ttk.Spinbox(control_frame, from_=3, to=20, textvariable=self.rows_var, width=5).grid(row=0, column=1)

        ttk.Label(control_frame, text="Cols").grid(row=0, column=2)
        self.cols_var = tk.IntVar(value=self.config.cols)
        ttk.Spinbox(control_frame, from_=3, to=20, textvariable=self.cols_var, width=5).grid(row=0, column=3)

        ttk.Label(control_frame, text="Win Length").grid(row=0, column=4)
        self.win_var = tk.IntVar(value=self.config.win_length)
        ttk.Combobox(
            control_frame,
            values=[3, 4, 5],
            textvariable=self.win_var,
            width=5,
            state="readonly"
        ).grid(row=0, column=5)

        ttk.Label(control_frame, text="Mode").grid(row=1, column=0)
        self.mode_var = tk.StringVar(value="Player vs Player")

        mode_box = ttk.Combobox(
            control_frame,
            textvariable=self.mode_var,
            values=["Player vs Player", "Player vs PC", "PC vs PC"],
            state="readonly",
            width=16,
        )
        mode_box.grid(row=1, column=1, columnspan=2)
        mode_box.bind("<<ComboboxSelected>>", self.on_mode_changed)

        ttk.Label(control_frame, text="Player 1").grid(row=1, column=3)
        self.x_player_var = tk.StringVar(value="Human")
        self.x_player_box = ttk.Combobox(
            control_frame,
            textvariable=self.x_player_var,
            values=list(self.PLAYER_OPTIONS.keys()),
            state="readonly",
            width=12,
        )
        self.x_player_box.grid(row=1, column=4)

        ttk.Label(control_frame, text="Player 2").grid(row=1, column=5)
        self.o_player_var = tk.StringVar(value="Human")
        self.o_player_box = ttk.Combobox(
            control_frame,
            textvariable=self.o_player_var,
            values=list(self.PLAYER_OPTIONS.keys()),
            state="readonly",
            width=12,
        )
        self.o_player_box.grid(row=1, column=6)

        self.apply_mode_preset()

        ttk.Button(control_frame, text="New Game", command=self.start_new_game).grid(row=0, column=6, padx=8)
        ttk.Button(control_frame, text="Step Bot", command=self.step_program_turn).grid(row=0, column=7, padx=8)

        self.auto_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(control_frame, text="Auto-run bots", variable=self.auto_var).grid(row=1, column=7)

        self.status_var = tk.StringVar(value="")
        ttk.Label(
            control_frame,
            textvariable=self.status_var,
            font=("Arial", 11, "bold")
        ).grid(row=0, column=8, rowspan=2, padx=8)

    def build_board(self) -> None:
        if hasattr(self, "board_frame"):
            self.board_frame.destroy()

        self.board_frame = ttk.Frame(self.root, padding=10)
        self.board_frame.pack(side=tk.TOP)

        self.cell_buttons = []

        for r in range(self.game.config.rows):
            row_buttons = []

            for c in range(self.game.config.cols):
                btn = tk.Button(
                    self.board_frame,
                    text="",
                    width=3,
                    height=1,
                    font=("Arial", 14, "bold"),
                    command=lambda rr=r, cc=c: self.on_cell_clicked(rr, cc),
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                row_buttons.append(btn)

            self.cell_buttons.append(row_buttons)

    def on_mode_changed(self, event=None) -> None:
        self.apply_mode_preset()

    def apply_mode_preset(self) -> None:
        mode = self.mode_var.get()

        if mode == "Player vs Player":
            self.x_player_var.set("Human")
            self.o_player_var.set("Human")
        elif mode == "Player vs PC":
            self.x_player_var.set("Human")
            self.o_player_var.set("Student Bot")
        elif mode == "PC vs PC":
            self.x_player_var.set("Student Bot")
            self.o_player_var.set("Random Bot")

    def make_player(self, kind: str, player_number: int) -> MoveSource:
        cls = self.PLAYER_OPTIONS[kind]
        return cls(name=f"{kind} ({player_number})")

    def start_new_game(self) -> None:
        rows = self.rows_var.get()
        cols = self.cols_var.get()
        win_length = self.win_var.get()

        if win_length > max(rows, cols):
            messagebox.showerror(
                "Invalid settings",
                "Win length must be <= rows or cols."
            )
            return

        self.cancel_scheduled_turn()

        self.config = GameConfig(rows=rows, cols=cols, win_length=win_length)
        self.game = GameState(self.config)

        self.player_x = self.make_player(self.x_player_var.get(), 1)
        self.player_o = self.make_player(self.o_player_var.get(), 2)

        self.build_board()
        self.refresh_board()
        self.update_status()
        self.maybe_run_program_turn()

    def current_source(self) -> MoveSource:
        return self.player_x if self.game.current_player == 1 else self.player_o

    def on_cell_clicked(self, row: int, col: int) -> None:
        if self.game.winner is not None:
            return

        source = self.current_source()

        if not isinstance(source, HumanPlayer):
            return

        if self.game.apply_move(row, col):
            self.refresh_board()
            self.update_status()
            self.maybe_run_program_turn()

    def step_program_turn(self) -> None:
        if self.game.winner is not None:
            return

        source = self.current_source()

        if isinstance(source, HumanPlayer):
            return

        move = source.choose_move(
            self.game.board.copy(),
            self.game.current_player,
            self.game.config.win_length
        )

        if move is None:
            return

        row, col = move

        if not self.game.apply_move(row, col):
            messagebox.showerror(
                "Invalid move",
                f"{source.name} returned illegal move: {move}"
            )
            return

        self.refresh_board()
        self.update_status()
        self.maybe_run_program_turn()

    def maybe_run_program_turn(self) -> None:
        self.cancel_scheduled_turn()

        if self.game.winner is not None:
            return

        source = self.current_source()

        if isinstance(source, HumanPlayer):
            return

        if self.auto_var.get():
            self.auto_play_job = self.root.after(250, self.step_program_turn)

    def cancel_scheduled_turn(self) -> None:
        if self.auto_play_job is not None:
            self.root.after_cancel(self.auto_play_job)
            self.auto_play_job = None

    def refresh_board(self) -> None:
        winning_set = set(self.game.winning_cells)

        symbols = {
            0: "",
            1: "X",
            2: "O",
        }

        for r in range(self.game.config.rows):
            for c in range(self.game.config.cols):
                value = int(self.game.board[r, c])
                btn = self.cell_buttons[r][c]

                btn.configure(text=symbols[value])

                if (r, c) in winning_set:
                    btn.configure(bg="#90EE90")
                else:
                    btn.configure(bg=self.root.cget("bg"))

    def update_status(self) -> None:
        if self.game.winner == "Draw":
            self.status_var.set("Draw")
        elif self.game.winner is not None:
            self.status_var.set(f"Winner: Player {self.game.winner}")
        else:
            source = self.current_source()
            self.status_var.set(
                f"Turn: Player {self.game.current_player} ({source.name})"
            )


def main() -> None:
    root = tk.Tk()
    app = TicTacToeApp(root)
    app.refresh_board()
    root.mainloop()


if __name__ == "__main__":
    main()