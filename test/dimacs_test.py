import unittest

from src.util.dimacs import Dimacs

class DimacsTest(unittest.TestCase):
    def test_construct_dimacs(self):
        dimacs = Dimacs()
        self.assertEqual(dimacs.literal_count, 0)
        self.assertEqual(dimacs.clause_count, 0)
        self.assertEqual(dimacs.clauses, [])

        literal_count = 10
        clause_count = 10
        clauses = [[i] for i in xrange(clause_count)]
        dimacs = Dimacs(literal_count=literal_count,
                clause_count=clause_count,
                clauses=clauses)
        self.assertEqual(dimacs.literal_count, literal_count)
        self.assertEqual(dimacs.clause_count, clause_count)
        self.assertEqual(dimacs.clauses, clauses)

        dimacs = Dimacs()
        self.assertRaises(Exception, Dimacs, literal_count=-1)
        self.assertRaises(Exception, Dimacs, clause_count=-1)
        self.assertRaises(Exception, Dimacs, clause_count=10, clauses=[[1], [2]])

    def test_add_clause(self):
        dimacs = Dimacs()
        self.assertRaises(Exception, dimacs.add_clause)
        dimacs.add_clause([1])
        self.assertEqual(dimacs.clauses, [[1]])
        dimacs.add_clause([2])
        self.assertEqual(dimacs.clauses, [[1], [2]])

    def test_to_string(self):
        literal_count = 10
        clause_count = 10
        clauses = [[i] for i in xrange(1, clause_count + 1)]
        dimacs = Dimacs(literal_count=literal_count,
                clause_count=clause_count,
                clauses=clauses)
        self.assertEqual('p cnf 10 10\n1 0\n2 0\n3 0\n4 0\n5 0\n6 0\n7 0\n8 0\n9 0\n10 0\n',
                dimacs.to_string())
