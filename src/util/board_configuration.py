class BoardConfiguration(object):
    def __init__(self, row_count=None, col_count=None):
        if (row_count is None) or (col_count is None):
            raise Exception('Board dimension should be properly set!')
        if (row_count < 1) or (col_count < 1):
            raise Exception('Board dimension should be positive!')
        self.row_count = row_count
        self.col_count = col_count
        self.board = [[False for _ in xrange(col_count)] for _ in xrange(row_count)]

    def set_board(self, row=None, col=None, value=None):
        if (value is None) or not isinstance(value, bool):
            raise Exception('Value should be set to either False (off) or True (on)!')
        self.check_range(row=row, col=col)
        self.board[row][col] = value

    def toggle_board(self, row=None, col=None):
        self.check_range(row=row, col=col)
        self.set_board(row=row, col=col, value=(not self.board[row][col]))

    def get_board(self, row=None, col=None):
        self.check_range(row=row, col=col)
        return self.board[row][col]

    def clear_board(self):
        for i in xrange(self.row_count):
            for j in xrange(self.col_count):
                self.board[i][j] = False

    def is_done(self):
        is_done = True
        for row in self.board:
            for item in row:
                is_done = is_done & item
        return is_done

    def check_range(self, row, col):
        if not (0 <= row < self.row_count) or not (0 <= col < self.col_count):
            raise Exception('(row, col) is out of bound!')

