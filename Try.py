"""
Tic-Tac-Toe (Human vs AI)
Author: ChatGPT
Description:
    A terminal-based Tic-Tac-Toe game against an optimal AI.
    Designed with clean structure, input validation, and safe coding practices.
"""

from __future__ import annotations
from typing import List, Optional, Tuple
import math


Board = List[str]


class GameError(Exception):
    """Custom exception for game-related errors."""


def create_board() -> Board:
    """Create a new empty Tic-Tac-Toe board."""
    return [" "] * 9


def display_board(board: Board) -> None:
    """Print the game board in a human-friendly format."""
    print("\n")
    for row in range(3):
        start = row * 3
        print(" " + " | ".join(board[start:start + 3]))
        if row < 2:
            print("---+---+---")
    print("\n")


def available_moves(board: Board) -> List[int]:
    """Return list of indices that are free."""
    return [i for i, value in enumerate(board) if value == " "]


def make_move(board: Board, position: int, player: str) -> None:
    """
    Place a move on the board.

    Raises:
        GameError: if move is invalid.
    """
    if position not in range(9):
        raise GameError("Position must be between 1 and 9.")

    if board[position] != " ":
        raise GameError("That position is already taken.")

    board[position] = player


def check_winner(board: Board, player: str) -> bool:
    """Check if a player has won."""
    win_patterns = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    return any(all(board[i] == player for i in pattern) for pattern in win_patterns)


def is_draw(board: Board) -> bool:
    """Check if the game is a draw."""
    return " " not in board


def minimax(board: Board, depth: int, maximizing: bool) -> Tuple[int, Optional[int]]:
    """
    Minimax algorithm for optimal AI move selection.

    Returns:
        Tuple of (score, move)
    """
    if check_winner(board, "O"):
        return 10 - depth, None
    if check_winner(board, "X"):
        return depth - 10, None
    if is_draw(board):
        return 0, None

    if maximizing:
        best_score = -math.inf
        best_move = None
        for move in available_moves(board):
            board[move] = "O"
            score, _ = minimax(board, depth + 1, False)
            board[move] = " "
            if score > best_score:
                best_score = score
                best_move = move
        return best_score, best_move
    else:
        best_score = math.inf
        best_move = None
        for move in available_moves(board):
            board[move] = "X"
            score, _ = minimax(board, depth + 1, True)
            board[move] = " "
            if score < best_score:
                best_score = score
                best_move = move
        return best_score, best_move


def get_human_move(board: Board) -> int:
    """Prompt and validate human move."""
    while True:
        try:
            raw = input("Choose a position (1-9): ").strip()
            position = int(raw) - 1
            if position not in available_moves(board):
                raise GameError("Invalid move.")
            return position
        except ValueError:
            print("Please enter a valid number.")
        except GameError as exc:
            print(exc)


def ai_move(board: Board) -> int:
    """Determine AI move using minimax."""
    _, move = minimax(board, 0, True)
    if move is None:
        raise GameError("AI failed to determine a move.")
    return move


def game_loop() -> None:
    """Main game loop."""
    board = create_board()
    print("Welcome to Tic-Tac-Toe!")
    print("You are X, AI is O.")
    display_board(board)

    while True:
        # Human turn
        move = get_human_move(board)
        make_move(board, move, "X")
        display_board(board)

        if check_winner(board, "X"):
            print("You win! 🎉")
            break
        if is_draw(board):
            print("It's a draw!")
            break

        # AI turn
        move = ai_move(board)
        make_move(board, move, "O")
        print("AI moves...")
        display_board(board)

        if check_winner(board, "O"):
            print("AI wins!")
            break
        if is_draw(board):
            print("It's a draw!")
            break


def main() -> None:
    """Program entry point with safe execution handling."""
    try:
        game_loop()
    except KeyboardInterrupt:
        print("\nGame interrupted safely.")
    except Exception as exc:
        print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
