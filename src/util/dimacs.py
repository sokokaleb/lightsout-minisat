class Dimacs(object):
    def __init__(self, literal_count=0, clause_count=0, clauses=[]):
        if (literal_count < 0) or (clause_count < 0):
            raise Exception('clause_count and literal_count should be non-negative!')
        if clause_count != len(clauses):
            raise Exception('clause_count isn\'t equal to the number of clauses in clauses!')
        self.literal_count = literal_count
        self.clause_count = clause_count
        self.clauses = list(clauses)

    def add_clause(self, clause=None):
        if clause is None:
            raise Exception('clause shouldn\'t be empty!')
        self.clauses.append(clause)
        self.clause_count += 1

    def to_string(self):
        result = 'p cnf {0} {1}\n'.format(self.literal_count, self.clause_count)
        for clause in self.clauses:
            tmp = ''
            for literal in clause:
                tmp += '{0} '.format(literal)
            tmp += '0\n'
            result += tmp
        return result
