# Author: Sam Baird
# GitHub username: OSU-S13BAIRD
# Date: 03/15/2026
# Class: INTRO TO COMPUTER SCIENCE II (CS_162_400_W2026)
# Description: Contains Piece, Pika, Trilobite, Wombat, Beluga, and AnimalGame classes
#              for simulating an animal-themed abstract board game on a 7x7 grid with
#              two players (tangerine and amethyst) and capture-the-beluga win condition.


class Piece:
    """Base class for all game pieces. Stores color and position."""

    def __init__(self, color, position):
        self.__color = color        # 'tangerine' or 'amethyst'
        self.__position = position  # e.g. 'a1'

    def get_color(self):
        return self.__color

    def get_position(self):
        return self.__position

    def set_position(self, position):
        self.__position = position

    def get_legal_moves(self, board):
        """To be implemented by each subclass. Returns a list of legal target squares."""
        raise NotImplementedError


class Pika(Piece):
    """
    Orthogonal, distance 4, sliding.
    Can also move 1 square diagonally.
    """

    def __init__(self, color, position):
        super().__init__(color, position)

    def get_legal_moves(self, board):
        moves = []
        col, row = _parse_pos(self.get_position())

        # orthogonal sliding up to 4
        for dc, dr in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            for dist in range(1, 5):
                nc, nr = col + dc * dist, row + dr * dist
                if not _in_bounds(nc, nr):
                    break
                target_pos = _make_pos(nc, nr)
                occupant = board.get(target_pos)
                if occupant is None:
                    moves.append(target_pos)
                elif occupant.get_color() != self.get_color():
                    moves.append(target_pos)
                    break   # can't slide past
                else:
                    break   # blocked by friendly

        # 1 square diagonal (alternate move)
        for dc, dr in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            nc, nr = col + dc, row + dr
            if _in_bounds(nc, nr):
                target_pos = _make_pos(nc, nr)
                occupant = board.get(target_pos)
                if occupant is None or occupant.get_color() != self.get_color():
                    moves.append(target_pos)

        return moves


class Trilobite(Piece):
    """
    Diagonal, distance 2, sliding.
    Can also move 1 square orthogonally.
    """

    def __init__(self, color, position):
        super().__init__(color, position)

    def get_legal_moves(self, board):
        moves = []
        col, row = _parse_pos(self.get_position())

        # diagonal sliding up to 2
        for dc, dr in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for dist in range(1, 3):
                nc, nr = col + dc * dist, row + dr * dist
                if not _in_bounds(nc, nr):
                    break
                target_pos = _make_pos(nc, nr)
                occupant = board.get(target_pos)
                if occupant is None:
                    moves.append(target_pos)
                elif occupant.get_color() != self.get_color():
                    moves.append(target_pos)
                    break
                else:
                    break

        # 1 square orthogonal (alternate move)
        for dc, dr in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nc, nr = col + dc, row + dr
            if _in_bounds(nc, nr):
                target_pos = _make_pos(nc, nr)
                occupant = board.get(target_pos)
                if occupant is None or occupant.get_color() != self.get_color():
                    moves.append(target_pos)

        return moves


class Wombat(Piece):
    """
    Orthogonal, distance 1, jumping.
    With distance 1 the sliding/jumping distinction doesn't matter.
    Can also move 1 square diagonally (same distance, so effectively 8-directional).
    """

    def __init__(self, color, position):
        super().__init__(color, position)

    def get_legal_moves(self, board):
        moves = []
        col, row = _parse_pos(self.get_position())

        # 1 step in any direction (orthogonal primary + diagonal alternate)
        for dc, dr in [(0, 1), (0, -1), (1, 0), (-1, 0),
                       (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            nc, nr = col + dc, row + dr
            if _in_bounds(nc, nr):
                target_pos = _make_pos(nc, nr)
                occupant = board.get(target_pos)
                if occupant is None or occupant.get_color() != self.get_color():
                    moves.append(target_pos)

        return moves


class Beluga(Piece):
    """
    Diagonal, distance 3, jumping.
    Must jump exactly 3 squares diagonally (cannot be blocked mid-path).
    Can also move 1 square orthogonally.
    """

    def __init__(self, color, position):
        super().__init__(color, position)

    def get_legal_moves(self, board):
        moves = []
        col, row = _parse_pos(self.get_position())

        # exactly 3 squares diagonal, jumping (ignores pieces in the way)
        for dc, dr in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            nc, nr = col + dc * 3, row + dr * 3
            if _in_bounds(nc, nr):
                target_pos = _make_pos(nc, nr)
                occupant = board.get(target_pos)
                if occupant is None or occupant.get_color() != self.get_color():
                    moves.append(target_pos)

        # 1 square orthogonal (alternate move)
        for dc, dr in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nc, nr = col + dc, row + dr
            if _in_bounds(nc, nr):
                target_pos = _make_pos(nc, nr)
                occupant = board.get(target_pos)
                if occupant is None or occupant.get_color() != self.get_color():
                    moves.append(target_pos)

        return moves


# ---------------------------------------------------------------------------
# Helper functions (module-level, not inside any class)
# ---------------------------------------------------------------------------

def _parse_pos(pos):
    """Convert algebraic notation like 'b3' to (col_int, row_int) with 0-based index."""
    col = ord(pos[0]) - ord('a')   # 'a'->0, 'b'->1, ... 'g'->6
    row = int(pos[1]) - 1          # '1'->0, '2'->1, ... '7'->6
    return col, row


def _make_pos(col, row):
    """Convert 0-based (col, row) back to algebraic notation."""
    return chr(col + ord('a')) + str(row + 1)


def _in_bounds(col, row):
    return 0 <= col <= 6 and 0 <= row <= 6


# ---------------------------------------------------------------------------
# AnimalGame
# ---------------------------------------------------------------------------

class AnimalGame:
    """
    Manages state for the animal-themed abstract board game.

    Board layout uses a dict keyed by algebraic position strings ('a1' ... 'g7').
    Tangerine pieces start in row 1, amethyst in row 7.
    Piece order (columns a-g): pika, trilobite, wombat, beluga, wombat, trilobite, pika
    Tangerine moves first.
    """

    def __init__(self):
        self.__board = {}           # pos -> Piece
        self.__turn = 'tangerine'
        self.__game_state = 'UNFINISHED'
        self.__setup_board()

    def __setup_board(self):
        """Place all pieces in their starting positions."""
        piece_order = [Pika, Trilobite, Wombat, Beluga, Wombat, Trilobite, Pika]
        cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

        for i, cls in enumerate(piece_order):
            tan_pos = cols[i] + '1'
            ame_pos = cols[i] + '7'
            self.__board[tan_pos] = cls('tangerine', tan_pos)
            self.__board[ame_pos] = cls('amethyst', ame_pos)

    def get_game_state(self):
        """Returns 'UNFINISHED', 'TANGERINE_WON', or 'AMETHYST_WON'."""
        return self.__game_state

    def make_move(self, from_pos, to_pos):
        """
        Attempt to move the piece at from_pos to to_pos.
        Returns True on success, False if the move is illegal or the game is over.
        """
        if self.__game_state != 'UNFINISHED':
            return False

        piece = self.__board.get(from_pos)

        # must be a piece belonging to the current player
        if piece is None or piece.get_color() != self.__turn:
            return False

        # check if to_pos is in the piece's legal moves
        legal = piece.get_legal_moves(self.__board)
        if to_pos not in legal:
            return False

        # execute the move
        captured = self.__board.get(to_pos)
        self.__board.pop(from_pos)
        self.__board[to_pos] = piece
        piece.set_position(to_pos)

        # check win condition
        if captured is not None and isinstance(captured, Beluga):
            if captured.get_color() == 'amethyst':
                self.__game_state = 'TANGERINE_WON'
            else:
                self.__game_state = 'AMETHYST_WON'

        # advance turn only if game is still going
        if self.__game_state == 'UNFINISHED':
            self.__turn = 'amethyst' if self.__turn == 'tangerine' else 'tangerine'

        return True

    def print_board(self):
        """Optional display helper — useful for testing."""
        abbrev = {
            'Pika': 'Pi', 'Trilobite': 'Tr', 'Wombat': 'Wo', 'Beluga': 'Be'
        }
        print('  ' + '  '.join('abcdefg'))
        for row in range(6, -1, -1):
            line = str(row + 1) + ' '
            for col in range(7):
                pos = _make_pos(col, row)
                piece = self.__board.get(pos)
                if piece is None:
                    line += ' . '
                else:
                    letter = abbrev[type(piece).__name__]
                    color_tag = 'T' if piece.get_color() == 'tangerine' else 'A'
                    line += color_tag + letter
            print(line)
        print(f"Turn: {self.__turn}  State: {self.__game_state}\n")
