class BoardConfiguration:
    def __init__(self, row_count=None, col_count=None):
        if (row_count is None) or (col_count is None):
            raise Exception('Board dimension should be properly set!')
        if (row_count < 1) or (col_count < 1):
            raise Exception('Board dimension should be positive!')
        self.row_count = row_count
        self.col_count = col_count
        self.board = [[0 for _ in range(col_count)] for _ in range(row_count)]

    def set_board(self, row=None, col=None, value=None):
        if (value is None) or not (0 <= value <= 1):
            raise Exception('Value should be set to either 0 (off) or 1(on)!')
        self.check_range(row=row, col=col)
        self.board[row][col] = value

    def get_board(self, row=None, col=None):
        self.check_range(row=row, col=col)
        return self.board[row][col]

    def check_range(self, row, col):
        if not (0 <= row < self.row_count) or not (0 <= col < self.col_count):
            raise Exception('(row, col) is out of bound!')

