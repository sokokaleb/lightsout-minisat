import os

from src.util.board_configuration import BoardConfiguration
from src.util.dimacs import Dimacs
from src.util.solver_result import SolverResult

class LightsOutMinisatWrapper(object):
    def __init__(self,
            exec_command='minisat',
            in_file_path='/tmp/lightsout_in',
            out_file_path='/tmp/lightsout_out',
            meta_file_path='/tmp/lightsout_meta'):
        self.exec_command = exec_command
        self.in_file_path = in_file_path
        self.out_file_path = out_file_path
        self.meta_file_path = meta_file_path

    def solve(self, board_config=None, latest_result=None):
        if (board_config is None) or not isinstance(board_config, BoardConfiguration):
            raise Exception('board_config should be filled with an object of BoardConfiguration!')
        if (latest_result is not None) and not isinstance(latest_result, SolverResult):
            raise Exception('latest_result should be an instance of SolverResult!')

        if latest_result is not None:
            board_config_in_dimacs = self.board_to_dimacs(board_config, latest_result.solution)
        else:
            board_config_in_dimacs = self.board_to_dimacs(board_config)
        
        in_file = open(self.in_file_path, 'w')
        in_file.write(board_config_in_dimacs.to_string())
        in_file.close()

        command = '{0} {1} {2} > {3}'.format(self.exec_command, self.in_file_path, self.out_file_path, self.meta_file_path)
        os.system(command)
        
        result = SolverResult()
        result.board_config_in_dimacs = board_config

        out_file = open(self.out_file_path, 'r')
        out_lines = out_file.readlines()
        out_file.close()

        sat_status = out_lines[0].strip()

        if sat_status == 'SAT':
            result.is_satisfiable = True
            out_res = out_lines[1].split()
            out_res = [int(sol) for sol in out_res[board_config_in_dimacs.literal_count // 2 : -1]]
            result.latest_solution = out_res
            if latest_result is not None:
                result.solutions = latest_result.solutions
            result.solutions.append(result.latest_solution)
            meta_file = open(self.meta_file_path, 'r')
            meta_res = meta_file.read()
            meta_file.close()
            result.metadata = meta_res
        
        return result

    def board_to_dimacs(self, board_config=None, received_solution=[]):
        if (board_config is None) or not isinstance(board_config, BoardConfiguration):
            raise Exception('board_config should be filled with an object of BoardConfiguration!')

        result = Dimacs(literal_count=board_config.row_count * board_config.col_count * 2)
        
        # Insert inputs first
        for i in xrange(0, board_config.row_count):
            for j in xrange(0, board_config.col_count):
                tile_index = i * board_config.col_count + j + 1;
                if board_config.get_board(i, j) == 1:
                    result.add_clause([tile_index])
                else:
                    result.add_clause([-tile_index])

        # Construct constraints
        for i in xrange(0, board_config.row_count):
            for j in xrange(0, board_config.col_count):
                tile_index = i * board_config.col_count + j;
                valid_tiles = [tile_index] + WrapperHelper.get_surrounding_tiles(tile_index, board_config)
                valid_tiles = [item + 1 for item in valid_tiles]
                for mask in xrange(2 ** len(valid_tiles)):
                    processed_mask = bin(mask)[2:].zfill(len(valid_tiles))
                    if processed_mask.count('1') % 2 == 0: # We want even number of negative multipliers
                        result.add_clause([a * b for a, b in zip(valid_tiles, [(-1) ** int(bit) for bit in processed_mask])])

        # Add found solution to find another solution
        for soln in received_solution:
            result.add_clause(soln)

        return result

class WrapperHelper(object):
    @staticmethod
    def get_surrounding_tiles(tile_index=None, board_config=None):
        if (tile_index is None) or (board_config is None):
            raise Exception('tile_index and board_config should be filled!')
        if not isinstance(board_config, BoardConfiguration):
            raise Exception('board_config should be an instance of BoardConfiguration!')

        # We number [1, row_count * col_count] for each tile's state (0 for off
        # and 1 for on), and the number [row_count * col_count + 1, 2 * row_count
        # * col_count] for the "pressed" tiles.
        # Hence we need an offset to ease access to the "pressed" literals.
        OFFSET = board_config.row_count * board_config.col_count
        if not (0 <= tile_index < OFFSET):
            raise Exception('tile_index is out of bound!')
        MOVEMENT_SCALAR = [0, 1, -1, board_config.col_count, -board_config.col_count]

        return [OFFSET + tile_index + m_scalar \
                for m_scalar in MOVEMENT_SCALAR \
                if 1 <= tile_index + m_scalar + 1 <= OFFSET and \
                WrapperHelper.same_row_or_column(tile_index, tile_index + m_scalar, board_config)]

    @staticmethod
    def same_row_or_column(tile_index_0=None, tile_index_1=None, board_config=None):
        if (tile_index_0 is None) or (tile_index_1 is None) or (board_config is None):
            raise Exception('tile_index_0, tile_index_1, and board_config should be filled!')
        if not isinstance(board_config, BoardConfiguration):
            raise Exception('board_config should be an instance of BoardConfiguration!')
        return ((tile_index_0 % board_config.col_count == tile_index_1 % board_config.col_count) or \
            (tile_index_0 // board_config.col_count == tile_index_1 // board_config.col_count))

    @staticmethod
    def literals_to_board(literals=[], board_config=None):
        if board_config is None:
            raise Exception('board_config should be filled!')
        if not isinstance(board_config, BoardConfiguration):
            raise Exception('board_config should be an instance of BoardConfiguration!')

        OFFSET = board_config.row_count * board_config.col_count
        res = [[0 for _ in xrange(board_config.col_count)] for _ in xrange(board_config.row_count)]
        for literal in literals:
            if literal > 0:
                literal -= 1 + OFFSET
                row, col = literal // board_config.col_count, literal % board_config.col_count
                res[row][col] = 1
        
        return res
