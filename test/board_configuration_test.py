import unittest

from src.util.board_configuration import BoardConfiguration

class BoardConfigurationTest(unittest.TestCase):
    def test_construction(self):
        # Wrong ones
        self.assertRaises(Exception, BoardConfiguration)
        self.assertRaises(Exception, BoardConfiguration, row_count=-1)
        self.assertRaises(Exception, BoardConfiguration, col_count=-1)
        self.assertRaises(Exception, BoardConfiguration, row_count=0)
        self.assertRaises(Exception, BoardConfiguration, col_count=0)
        self.assertRaises(Exception, BoardConfiguration, row_count=3, col_count=-1)
        self.assertRaises(Exception, BoardConfiguration, row_count=-1, col_count=3)

        # OK ones
        board = BoardConfiguration(row_count=3, col_count=10)
        self.assertEqual(board.row_count, 3)
        self.assertEqual(board.col_count, 10)
        self.assertEqual(len(board.board), board.row_count)
        self.assertEqual(len(board.board[0]), board.col_count)
        for row in board.board:
            for cell in row:
                self.assertEqual(cell, 0)

    def test_access_board(self):
        board = BoardConfiguration(3, 3)

        # Wrong ones
        self.assertRaises(Exception, board.set_board)
        self.assertRaises(Exception, board.set_board, row=2)
        self.assertRaises(Exception, board.set_board, col=2)
        self.assertRaises(Exception, board.set_board, value=1)
        self.assertRaises(Exception, board.set_board, row=2, col=2)
        self.assertRaises(Exception, board.set_board, row=2, col=2, value=10)
        self.assertRaises(Exception, board.set_board, row=3, col=3, value=0)

        # OK ones
        board.set_board(row=2, col=2, value=1)
        self.assertEqual(board.get_board(row=2, col=2), 1)
        board.set_board(row=2, col=2, value=0)
        self.assertEqual(board.get_board(row=2, col=2), 0)
