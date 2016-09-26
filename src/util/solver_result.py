class SolverResult(object):
    def __init__(self):
        self.board_config = None
        self.is_satisfiable = False
        self.latest_solution = []
        self.solution = []
        self.metadata = ''
