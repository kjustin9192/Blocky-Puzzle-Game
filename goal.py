"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Goal class hierarchy.
"""

from typing import List, Tuple
from block import Block


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class BlobGoal(Goal):
    """A goal to create the largest connected blob of this goal's target
    colour, anywhere within the Block.
    """

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <pos> is the index within <board>.
        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
           -1  if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        # When <pos> is out of bound.
        if pos[0] < 0 or pos[0] >= len(board) or \
                        pos[1] < 0 or pos[1] >= len(board):
            return 0

        if visited[pos[0]][pos[1]] == -1:
            if board[pos[0]][pos[1]] == self.colour:
                visited[pos[0]][pos[1]] = 1
                return 1 + self._undiscovered_blob_size(
                    (pos[0] - 1, pos[1]),
                    board,
                    visited
                ) + self._undiscovered_blob_size(
                    (pos[0] + 1, pos[1]),
                    board,
                    visited
                ) + self._undiscovered_blob_size(
                    (pos[0], pos[1] - 1),
                    board,
                    visited
                ) + self._undiscovered_blob_size(
                    (pos[0], pos[1] + 1),
                    board,
                    visited
                )
            else:
                visited[pos[0]][pos[1]] = 0
                return 0
        else:
            return 0

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.
        The player's score is the number of unit cells in the largest blob of
        targeted colour.

        The score is always greater than or equal to 0.
        """
        flat_board = board.flatten()
        len_flat_board = len(flat_board)

        check_visited = []
        for i in range(len_flat_board):
            column = []
            for j in range(len_flat_board):
                column.append(-1)
            check_visited.append(column)

        # find the score on the largest blob.
        result = 0
        for i in range(len_flat_board):
            for j in range(len_flat_board):
                score_ij = self._undiscovered_blob_size(
                    (i, j), flat_board, check_visited
                )
                result = max(result, score_ij)
        return result

    def description(self) -> str:
        """Return a brief description of this goal.
        """
        return "Create a large group of connected blocks to win!"


class PerimeterGoal(Goal):
    """A goal to have as many unit cells as possible on the outer perimeter
    of the board.
    """

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.
        Scores 1 for each unit cell on the outer perimeter. Scores double for
        unit cells at the corners.

        The score is always greater than or equal to 0.
        """
        result = 0
        flat_board = board.flatten()
        for column_lst in flat_board:
            if column_lst[0] == self.colour:
                result += 1
            if column_lst[-1] == self.colour:
                result += 1
        for colours1 in flat_board[0]:
            if colours1 == self.colour:
                result += 1
        for colours2 in flat_board[-1]:
            if colours2 == self.colour:
                result += 1
        return result

    def description(self) -> str:
        """Return a brief description of this goal.
        """
        return "Have as many unit cells as possible on the outer perimeter!"


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer'
        ],
        'max-attributes': 15
    })
