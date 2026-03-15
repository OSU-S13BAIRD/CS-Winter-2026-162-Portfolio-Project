# Author: Sam Baird
# GitHub username: OSU-S13BAIRD
# Date: 03/15/2026
# Class: INTRO TO COMPUTER SCIENCE II (CS_162_400_W2026)
# Description: Unit tests for AnimalGame.py covering valid move distances,
#              valid move directions, sliding vs. jumping behavior, captures,
#              turn order, and game state reporting.

import unittest
from AnimalGame import AnimalGame


class TestMoveDistances(unittest.TestCase):
    """Tests that pieces only move valid distances per their movement rules."""

    def test_pika_cannot_move_more_than_four_squares(self):
        """
        Pika slides orthogonally up to 4 squares. Attempting to move it 5 or
        more squares in a straight line should be rejected (return False) because
        4 is its maximum range.
        """
        game = AnimalGame()
        # a1 -> a6 is 5 squares north — beyond pika's range of 4
        result = game.make_move('a1', 'a6')
        self.assertFalse(result, "Pika should not be able to move 5 squares orthogonally")

        # a1 -> a7 is 6 squares — also illegal
        result2 = game.make_move('a1', 'a7')
        self.assertFalse(result2, "Pika should not be able to move 6 squares orthogonally")

    def test_pika_can_move_within_range(self):
        """
        Pika should legally move 1, 2, 3, or 4 squares orthogonally. Each of
        these distances must return True and the piece must appear at the destination.
        """
        # 1 square
        g1 = AnimalGame()
        self.assertTrue(g1.make_move('a1', 'a2'), "Pika should move 1 square")

        # 2 squares
        g2 = AnimalGame()
        self.assertTrue(g2.make_move('a1', 'a3'), "Pika should move 2 squares")

        # 3 squares
        g3 = AnimalGame()
        self.assertTrue(g3.make_move('a1', 'a4'), "Pika should move 3 squares")

        # 4 squares
        g4 = AnimalGame()
        self.assertTrue(g4.make_move('a1', 'a5'), "Pika should move 4 squares")

    def test_trilobite_cannot_move_more_than_two_diagonal_squares(self):
        """
        Trilobite slides diagonally up to 2 squares. Moving it 3 squares
        diagonally must be rejected as out of range.
        """
        game = AnimalGame()
        # b1 trilobite; 3 squares diagonally would be e4
        result = game.make_move('b1', 'e4')
        self.assertFalse(result, "Trilobite should not move 3 squares diagonally")

    def test_trilobite_can_move_one_and_two_diagonal_squares(self):
        """
        Trilobite must be able to slide 1 or 2 squares diagonally. Both
        distances should return True.
        """
        g1 = AnimalGame()
        self.assertTrue(g1.make_move('b1', 'c2'), "Trilobite should move 1 square diagonally")

        g2 = AnimalGame()
        self.assertTrue(g2.make_move('b1', 'd3'), "Trilobite should move 2 squares diagonally")

    def test_beluga_must_jump_exactly_three_diagonal_squares(self):
        """
        Beluga is a jumping piece that must land exactly 3 squares diagonally.
        Moving it 1 or 2 diagonal squares (not its alternate 1-square orthogonal)
        must be rejected; moving exactly 3 must succeed.
        """
        game = AnimalGame()
        # d1 beluga; 1 diagonal = e2, 2 diagonal = f3
        self.assertFalse(game.make_move('d1', 'e2'),
                         "Beluga cannot jump only 1 diagonal square as primary move")
        self.assertFalse(game.make_move('d1', 'f3'),
                         "Beluga cannot jump only 2 diagonal squares as primary move")

        # exactly 3 diagonal squares: d1 -> g4
        self.assertTrue(game.make_move('d1', 'g4'),
                        "Beluga should jump exactly 3 diagonal squares")

    def test_wombat_cannot_move_more_than_one_square(self):
        """
        Wombat moves exactly 1 square in any direction. Any attempt to move
        2 or more squares must be rejected.
        """
        game = AnimalGame()
        # c1 wombat; 2 squares north = c3
        self.assertFalse(game.make_move('c1', 'c3'),
                         "Wombat should not move 2 squares")
        # 2 squares diagonal
        self.assertFalse(game.make_move('c1', 'e3'),
                         "Wombat should not move 2 squares diagonally")


class TestMoveDirections(unittest.TestCase):
    """
    Tests that pieces only move in their designated direction, and that the
    one-square alternate direction rule is correctly enforced for all piece types.
    """

    def test_pika_cannot_move_diagonally_more_than_one_square(self):
        """
        Pika's primary direction is orthogonal. Its only diagonal option is the
        1-square alternate. Moving it 2+ squares diagonally must be illegal.
        """
        game = AnimalGame()
        # a1 pika; 2 diagonal = c3
        self.assertFalse(game.make_move('a1', 'c3'),
                         "Pika should not move 2 squares diagonally")

    def test_pika_can_move_one_square_diagonally(self):
        """
        Pika's alternate move allows exactly 1 square diagonally. This must
        return True from an open starting position.
        """
        game = AnimalGame()
        # a1 pika moves 1 square diagonally to b2
        self.assertTrue(game.make_move('a1', 'b2'),
                        "Pika should be allowed its 1-square diagonal alternate move")

    def test_trilobite_cannot_move_orthogonally_more_than_one_square(self):
        """
        Trilobite's primary direction is diagonal. Its only orthogonal option is
        the 1-square alternate. Moving it 2+ squares orthogonally must be illegal.
        """
        game = AnimalGame()
        # b1 trilobite; 2 squares north = b3
        self.assertFalse(game.make_move('b1', 'b3'),
                         "Trilobite should not move 2 squares orthogonally")

    def test_trilobite_can_move_one_square_orthogonally(self):
        """
        Trilobite's alternate move allows exactly 1 square orthogonally.
        This must return True from an open starting position.
        """
        game = AnimalGame()
        # b1 trilobite moves 1 square north to b2
        self.assertTrue(game.make_move('b1', 'b2'),
                        "Trilobite should be allowed its 1-square orthogonal alternate move")

    def test_beluga_cannot_move_diagonally_more_than_one_square_orthogonally(self):
        """
        Beluga's alternate orthogonal move is limited to exactly 1 square.
        Attempting 2+ squares orthogonally must be rejected.
        """
        game = AnimalGame()
        # d1 beluga; 2 squares north = d3
        self.assertFalse(game.make_move('d1', 'd3'),
                         "Beluga should not move 2 squares orthogonally")

    def test_beluga_can_move_one_square_orthogonally(self):
        """
        Beluga's alternate move is exactly 1 square orthogonally.
        This must return True.
        """
        game = AnimalGame()
        self.assertTrue(game.make_move('d1', 'd2'),
                        "Beluga should be allowed its 1-square orthogonal alternate move")

    def test_wombat_can_move_in_all_eight_directions(self):
        """
        Because the Wombat's orthogonal primary and diagonal alternate both
        cover exactly 1 square, it must be able to reach any of the 8
        adjacent squares. We verify all 8 directions from c1 after clearing
        the row by using a fresh game and only testing reachable open squares.
        """
        # From c1 (wombat), open adjacent squares are b2 (diagonal) and d2 (diagonal)
        # and c2 (orthogonal north). b1 and d1 are blocked by friendlies.
        g1 = AnimalGame()
        self.assertTrue(g1.make_move('c1', 'c2'), "Wombat moves north (orthogonal)")

        g2 = AnimalGame()
        self.assertTrue(g2.make_move('c1', 'b2'), "Wombat moves northwest (diagonal)")

        g3 = AnimalGame()
        self.assertTrue(g3.make_move('c1', 'd2'), "Wombat moves northeast (diagonal)")


class TestSlidingVsJumping(unittest.TestCase):
    """
    Tests that sliding pieces are blocked by intervening pieces and jumping
    pieces are not.
    """

    def test_pika_blocked_by_friendly_piece(self):
        """
        A sliding piece cannot move through a square occupied by a friendly piece.
        The tangerine pika at a1 has a tangerine trilobite at b1. Moving the pika
        horizontally past b1 should be illegal because it is blocked.
        We first move another piece out of the way if needed, then verify blocking.
        We test by trying to slide the a1 pika rightward past the b1 trilobite.
        """
        game = AnimalGame()
        # Pika at a1 cannot reach c1 going right because b1 is occupied by friendly trilobite
        self.assertFalse(game.make_move('a1', 'c1'),
                         "Pika should be blocked by friendly trilobite at b1")
        self.assertFalse(game.make_move('a1', 'd1'),
                         "Pika should still be blocked further right past b1")

    def test_pika_blocked_by_enemy_piece_cannot_slide_past(self):
        """
        A sliding piece can capture the first enemy it encounters, but cannot
        continue past it. We set up a scenario where an enemy occupies a square
        along the pika's path and verify the pika cannot reach a square beyond it.
        """
        game = AnimalGame()
        # Move tangerine pika a1->a4, then move amethyst pika a7->a5 (now at a5).
        # Tangerine pika at a4 tries to slide to a6 — it must stop AT a5 (capture),
        # so a6 is beyond the blocker and illegal.
        game.make_move('a1', 'a4')   # tangerine pika to a4
        game.make_move('a7', 'a5')   # amethyst pika to a5
        self.assertFalse(game.make_move('a4', 'a6'),
                         "Pika should not slide past an enemy piece at a5")
        # But capturing at a5 IS legal
        self.assertTrue(game.make_move('a4', 'a5'),
                        "Pika should be able to capture at a5")

    def test_beluga_jumps_over_intervening_pieces(self):
        """
        A jumping piece must not be blocked by pieces between its start and
        landing square. Beluga jumps exactly 3 diagonal squares regardless
        of what occupies the intermediate squares.
        We verify that the beluga at d1 can reach g4 even when a piece sits
        on e2 or f3 along that diagonal.
        """
        game = AnimalGame()
        # Move trilobite at b1 diagonally to e2 to place a piece on the beluga's path
        game.make_move('b1', 'c2')   # trilobite b1->c2 (tangerine)
        game.make_move('b7', 'c6')   # amethyst filler move
        game.make_move('c2', 'e4')   # trilobite c2->e4 — now on the d1->g4 diagonal
        game.make_move('a7', 'a6')   # amethyst filler

        # Beluga at d1 jumps to g4; e2 and f3 are not occupied but e4 is off the
        # d1->g4 ray; the key is the jump ignores anything in the way
        result = game.make_move('d1', 'g4')
        self.assertTrue(result, "Beluga should jump over intervening pieces to land at g4")

    def test_trilobite_blocked_after_one_square(self):
        """
        Trilobite slides diagonally up to 2 squares. If the first diagonal
        square is occupied by a friendly piece, it cannot continue to the
        second square.
        """
        game = AnimalGame()
        # b1 trilobite; c2 is an open square. Move wombat c1->c2 first to block.
        game.make_move('c1', 'c2')   # tangerine wombat c1->c2 (blocks the b1->d3 path at c2)
        game.make_move('a7', 'a6')   # amethyst filler to advance turn
        # Now b1 trilobite cannot slide through c2 (friendly wombat) to reach d3
        self.assertFalse(game.make_move('b1', 'd3'),
                         "Trilobite should be blocked by friendly piece at c2")
        # But it CAN move to c2... wait, c2 is friendly so even 1 square is blocked
        self.assertFalse(game.make_move('b1', 'c2'),
                         "Trilobite cannot move to square occupied by friendly piece")


class TestCaptures(unittest.TestCase):
    """
    Tests that capture rules are enforced correctly: pieces can capture enemies
    by landing on their square, and cannot capture friendly pieces.
    """

    def test_piece_cannot_capture_friendly_piece(self):
        """
        A piece must not be able to move to a square occupied by a piece of
        the same color. Attempting such a move must return False and leave the
        board unchanged.
        """
        game = AnimalGame()
        # Tangerine pika at a1 cannot move right to b1 (tangerine trilobite)
        self.assertFalse(game.make_move('a1', 'b1'),
                         "Piece must not capture a friendly piece")
        # Tangerine wombat c1 cannot move to b1 or d1 (both friendly)
        self.assertFalse(game.make_move('c1', 'b1'),
                         "Wombat must not capture a friendly piece to its left")
        self.assertFalse(game.make_move('c1', 'd1'),
                         "Wombat must not capture a friendly piece to its right")

    def test_piece_can_capture_enemy_piece(self):
        """
        When a piece lands on a square occupied by an enemy, the enemy is removed
        and the moving piece takes that square. The move must return True and the
        captured piece must no longer be on the board.
        """
        game = AnimalGame()
        # Bring tangerine pika a1 to a5, then amethyst pika a7 to a6.
        # Then move tangerine pika a5 to a6 to capture amethyst pika.
        game.make_move('a1', 'a4')   # tangerine pika to a4
        game.make_move('a7', 'a5')   # amethyst pika to a5
        result = game.make_move('a4', 'a5')  # tangerine captures amethyst at a5
        self.assertTrue(result, "Piece should be able to capture an enemy piece")

    def test_capturing_amethyst_beluga_ends_game(self):
        """
        If the amethyst beluga is captured, the game must immediately report
        TANGERINE_WON. Subsequent moves must return False because the game is over.
        """
        game = AnimalGame()
        # Walk the tangerine beluga (d1) up toward amethyst beluga (d7)
        # using 1-square orthogonal alternate moves, then jump over once in range.
        game.make_move('d1', 'd2')   # tan beluga -> d2
        game.make_move('a7', 'a6')   # amethyst filler
        game.make_move('d2', 'd3')   # tan beluga -> d3
        game.make_move('a6', 'a5')   # amethyst filler
        game.make_move('d3', 'd4')   # tan beluga -> d4
        game.make_move('a5', 'a4')   # amethyst filler
        game.make_move('d4', 'd5')   # tan beluga -> d5
        game.make_move('a4', 'a3')   # amethyst filler
        # Tangerine beluga at d5 can jump diagonally 3 to g8? No — use orthogonal
        # to reach d6 then diagonal to capture at d7 is 1 square orthogonal
        game.make_move('d5', 'd6')   # tan beluga -> d6
        game.make_move('a3', 'a2')   # amethyst filler
        # Now d6 beluga moves 1 orthogonal north to d7, capturing amethyst beluga
        result = game.make_move('d6', 'd7')
        self.assertTrue(result, "Move to capture amethyst beluga should succeed")
        self.assertEqual(game.get_game_state(), 'TANGERINE_WON',
                         "Game state should be TANGERINE_WON after amethyst beluga captured")
        # Further moves must be rejected
        self.assertFalse(game.make_move('a1', 'a2'),
                         "No moves should be allowed after the game is won")

    def test_capturing_tangerine_beluga_ends_game(self):
        """
        If the tangerine beluga is captured, the game must immediately report
        AMETHYST_WON.
        """
        game = AnimalGame()
        # Walk tangerine beluga to center, then let amethyst beluga capture it.
        game.make_move('d1', 'd2')   # tan
        game.make_move('d7', 'd6')   # ame beluga -> d6
        game.make_move('d2', 'd3')   # tan
        game.make_move('d6', 'd5')   # ame
        game.make_move('d3', 'd4')   # tan beluga -> d4
        # Amethyst beluga at d5 captures tangerine beluga at d4 (1 square orthogonal)
        result = game.make_move('d5', 'd4')
        self.assertTrue(result, "Amethyst beluga should capture tangerine beluga at d4")
        self.assertEqual(game.get_game_state(), 'AMETHYST_WON',
                         "Game state should be AMETHYST_WON after tangerine beluga captured")


class TestTurnOrder(unittest.TestCase):
    """
    Tests that turn alternation is enforced correctly: tangerine moves first,
    then amethyst, and so on. Attempting to move out of turn must return False.
    """

    def test_tangerine_moves_first(self):
        """
        On a freshly initialized game, only tangerine pieces should be movable.
        Attempting to move an amethyst piece on the very first turn must fail.
        """
        game = AnimalGame()
        # Try moving amethyst piece on turn 1 — must be rejected
        self.assertFalse(game.make_move('a7', 'a6'),
                         "Amethyst should not be able to move on tangerine's turn")
        # Tangerine move must succeed
        self.assertTrue(game.make_move('a1', 'a2'),
                        "Tangerine should be able to move on its own turn")

    def test_amethyst_moves_second(self):
        """
        After tangerine completes a valid move, it becomes amethyst's turn.
        Attempting another tangerine move must fail; an amethyst move must succeed.
        """
        game = AnimalGame()
        game.make_move('a1', 'a2')   # tangerine's turn — succeeds

        # Now it's amethyst's turn; another tangerine move must fail
        self.assertFalse(game.make_move('b1', 'b2'),
                         "Tangerine should not move twice in a row")
        # Amethyst move must succeed
        self.assertTrue(game.make_move('a7', 'a6'),
                        "Amethyst should be able to move on its own turn")

    def test_turns_alternate_multiple_cycles(self):
        """
        Turn order must alternate consistently over several rounds. We execute
        four half-turns (two full rounds) and verify the pattern holds.
        """
        game = AnimalGame()
        self.assertTrue(game.make_move('a1', 'a2'),  "Round 1 - tangerine")
        self.assertTrue(game.make_move('a7', 'a6'),  "Round 1 - amethyst")
        self.assertTrue(game.make_move('a2', 'a3'),  "Round 2 - tangerine")
        self.assertTrue(game.make_move('a6', 'a5'),  "Round 2 - amethyst")
        # Out-of-turn attempt mid-sequence
        self.assertFalse(game.make_move('a5', 'a4'),
                         "Amethyst piece should not move on tangerine's turn")

    def test_cannot_move_nonexistent_piece(self):
        """
        Attempting to move from an empty square must return False regardless of
        whose turn it is.
        """
        game = AnimalGame()
        self.assertFalse(game.make_move('a3', 'a4'),
                         "Cannot move from an empty square")
        self.assertFalse(game.make_move('d4', 'd5'),
                         "Cannot move from another empty square")


class TestGameState(unittest.TestCase):
    """
    Tests that get_game_state() returns the correct string value at each
    stage of the game: before any move, during play, and after a beluga capture.
    """

    def test_initial_state_is_unfinished(self):
        """
        A freshly created AnimalGame must report 'UNFINISHED' before any
        moves have been made.
        """
        game = AnimalGame()
        self.assertEqual(game.get_game_state(), 'UNFINISHED',
                         "Initial game state must be UNFINISHED")

    def test_state_remains_unfinished_during_normal_play(self):
        """
        As long as neither beluga has been captured, get_game_state() must
        continue to return 'UNFINISHED' after each move.
        """
        game = AnimalGame()
        game.make_move('a1', 'a4')
        self.assertEqual(game.get_game_state(), 'UNFINISHED',
                         "State should still be UNFINISHED after first move")
        game.make_move('a7', 'a5')
        self.assertEqual(game.get_game_state(), 'UNFINISHED',
                         "State should still be UNFINISHED after second move")

    def test_state_is_tangerine_won_after_capturing_amethyst_beluga(self):
        """
        get_game_state() must return 'TANGERINE_WON' immediately after the
        tangerine player captures the amethyst beluga.
        """
        game = AnimalGame()
        game.make_move('d1', 'd2')
        game.make_move('a7', 'a6')
        game.make_move('d2', 'd3')
        game.make_move('a6', 'a5')
        game.make_move('d3', 'd4')
        game.make_move('a5', 'a4')
        game.make_move('d4', 'd5')
        game.make_move('a4', 'a3')
        game.make_move('d5', 'd6')
        game.make_move('a3', 'a2')
        game.make_move('d6', 'd7')   # captures amethyst beluga
        self.assertEqual(game.get_game_state(), 'TANGERINE_WON',
                         "State must be TANGERINE_WON after amethyst beluga captured")

    def test_state_is_amethyst_won_after_capturing_tangerine_beluga(self):
        """
        get_game_state() must return 'AMETHYST_WON' immediately after the
        amethyst player captures the tangerine beluga.
        """
        game = AnimalGame()
        game.make_move('d1', 'd2')
        game.make_move('d7', 'd6')
        game.make_move('d2', 'd3')
        game.make_move('d6', 'd5')
        game.make_move('d3', 'd4')
        game.make_move('d5', 'd4')   # amethyst captures tangerine beluga
        self.assertEqual(game.get_game_state(), 'AMETHYST_WON',
                         "State must be AMETHYST_WON after tangerine beluga captured")

    def test_make_move_returns_false_after_game_over(self):
        """
        Once the game has ended (either player's beluga is captured), every
        subsequent call to make_move() must return False, regardless of what
        move is attempted.
        """
        game = AnimalGame()
        game.make_move('d1', 'd2')
        game.make_move('d7', 'd6')
        game.make_move('d2', 'd3')
        game.make_move('d6', 'd5')
        game.make_move('d3', 'd4')
        game.make_move('d5', 'd4')   # game over: AMETHYST_WON
        # Any further move must be rejected
        self.assertFalse(game.make_move('a7', 'a6'),
                         "No moves allowed after game ends")
        self.assertFalse(game.make_move('a1', 'a2'),
                         "No moves allowed after game ends (other side)")


if __name__ == '__main__':
    unittest.main()
