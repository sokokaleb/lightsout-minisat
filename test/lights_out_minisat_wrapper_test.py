import unittest

from src.lights_out_minisat_wrapper import LightsOutMinisatWrapper, WrapperHelper
from src.util.board_configuration import BoardConfiguration
from src.util.solver_result import SolverResult

class LightsOutMinisatWrapperTest(unittest.TestCase):
    def setUp(self):
        self.wrapper = LightsOutMinisatWrapper()

    def test_board_to_dimacs(self):
        board_config = BoardConfiguration(row_count=2, col_count=3)
        self.assertRaises(Exception, self.wrapper.board_to_dimacs)
        self.assertRaises(Exception, self.wrapper.board_to_dimacs, board_config=1)
        
        dimacs = self.wrapper.board_to_dimacs(board_config)
        self.assertEqual(dimacs.literal_count, 2 * 3 * 2)
        self.assertEqual(dimacs.clause_count, 2 * 3 + 4 * 8 + 2 * 16)
        self.assertEqual(dimacs.clause_count, len(dimacs.clauses))

        dimacs = self.wrapper.board_to_dimacs(board_config, [[1, 2, 3]])
        self.assertEqual(dimacs.literal_count, 2 * 3 * 2)
        self.assertEqual(dimacs.clause_count, 2 * 3 + 4 * 8 + 2 * 16 + 1)
        self.assertEqual(dimacs.clause_count, len(dimacs.clauses))

    def test_solve(self):
        board_config = BoardConfiguration(row_count=3, col_count=3)
        self.assertRaises(Exception, self.wrapper.solve)
        self.assertRaises(Exception, self.wrapper.solve, board_config=1)
        self.assertRaises(Exception, self.wrapper.solve, board_config=board_config, latest_result=1)

        result = self.wrapper.solve(board_config=board_config)
        self.assertIsInstance(result, SolverResult)
        self.assertTrue(result.is_satisfiable)

        unsolvable_board_config = BoardConfiguration(row_count=2, col_count=3)
        unsolvable_board_config.set_board(row=0, col=0, value=1)
        result = self.wrapper.solve(board_config=unsolvable_board_config)
        self.assertIsInstance(result, SolverResult)
        self.assertFalse(result.is_satisfiable)

class WrapperHelperTest(unittest.TestCase):
    def setUp(self):
        self.board_config = BoardConfiguration(row_count=3, col_count=3)

    def test_same_row_or_column(self):
        self.assertRaises(Exception, WrapperHelper.same_row_or_column);
        self.assertRaises(Exception, WrapperHelper.same_row_or_column, tile_index_0=0, tile_index_1=1);
        self.assertRaises(Exception, WrapperHelper.same_row_or_column, board_config=self.board_config);

        self.assertTrue(WrapperHelper.same_row_or_column(tile_index_0=4, tile_index_1=1, board_config=self.board_config))
        self.assertTrue(WrapperHelper.same_row_or_column(tile_index_0=4, tile_index_1=4, board_config=self.board_config))
        self.assertTrue(WrapperHelper.same_row_or_column(tile_index_0=4, tile_index_1=7, board_config=self.board_config))
        self.assertTrue(WrapperHelper.same_row_or_column(tile_index_0=4, tile_index_1=3, board_config=self.board_config))
        self.assertTrue(WrapperHelper.same_row_or_column(tile_index_0=4, tile_index_1=5, board_config=self.board_config))
        self.assertFalse(WrapperHelper.same_row_or_column(tile_index_0=4, tile_index_1=0, board_config=self.board_config))

    def test_get_surrounding_tiles(self):
        self.assertRaises(Exception, WrapperHelper.get_surrounding_tiles)
        self.assertRaises(Exception, WrapperHelper.get_surrounding_tiles, board_config=10)

        self.assertItemsEqual(WrapperHelper.get_surrounding_tiles(tile_index=0, board_config=self.board_config), [9, 10, 12])
        self.assertItemsEqual(WrapperHelper.get_surrounding_tiles(tile_index=4, board_config=self.board_config), [10, 12, 13, 14, 16])

    def test_literals_to_board(self):
        self.assertRaises(Exception, WrapperHelper.literals_to_board)
        self.assertRaises(Exception, WrapperHelper.literals_to_board, board_config=10)

        board_config = BoardConfiguration(3, 3)
        literals = [10, 11, 12, 13, -14, 15, 16, 17, 18]
        result = WrapperHelper.literals_to_board(literals=literals, board_config=board_config)
        self.assertEqual(len(result), board_config.row_count)
        self.assertEqual(len(result[0]), board_config.col_count)
        self.assertEqual(result, [[1, 1, 1], [1, 0, 1], [1, 1, 1]])
