from __future__ import print_function
__author__ = 'Leanne Whitmore'
__email__ = 'lwhitmo@sandia.gov'
__description__ = 'Tests cycle.py and addition of cycle constraints,\
                   ensures it obtains correct answers'

import unittest
import re
import os
from copy import deepcopy
from ShortestPath import constraints as co
from Database import query as Q
from Database import initialize_database as init_db
from Database import build_kbase_db as bkdb
from ShortestPath import integerprogram_pulp as ip_pulp

PATH = os.path.dirname(os.path.abspath(__file__))
PPATH = re.sub('/ShortestPath/tests', '', PATH)

if os.path.isfile(PATH+'/test.db') is True:
    os.remove(PATH+'/test.db')

'''GENERATE TEST DATABASE'''
init_db.Createdb(PATH+'/test.db', False)
bkdb.BuildKbase(PATH+'/data2', PPATH+'/Database/data/KbasetoKEGGCPD.txt',
                PPATH+'/Database/data/KbasetoKEGGRXN.txt', False,
                PATH+'/test.db', 'bio')
DB = Q.Connector(PATH+'/test.db')
allrxns = DB.get_all_reactions()
allmets = DB.get_all_compounds()

class CycleTests(unittest.TestCase):
    """Test class"""
    def setUp(self):
        """Initialize before every test."""
        print ("Initializing tests")

    def tearDown(self):
        """Clean up after each test."""
        print ("Clearing out test suite")

    def test_identification_of_cycle_pulp(self):
        """Tests identification of cycles with pulp package"""
        try:
            import pulp
            print ("...Testing identification of cycles with pulp package")
            C = co.ConstructInitialLP(allrxns, allmets, DB, [], True, False)
            IP = ip_pulp.IntergerProgram(DB, 10, 20, 0, 'False',  'False', 30, None)
            inmets = DB.get_compounds_in_model('t1')
            inrxns = DB.get_reactions_in_model('t1')
            osp = IP.run_glpk(C, inmets, inrxns, 'cpdT_c0', 'True')
            for solution in osp:
                cycletest = IP.run_cycle_check(solution)
                self.assertEqual(cycletest, True)
                print ("...Testing that cycle variables and arcs are correct")

        except ImportError:
            print ('pulp package not installed, cannot run tests for this python package')

    def test_identification_of_k_path_pulp(self):
        """Tests identification of cycles with pulp package"""
        try:
            import pulp
            print ("...Testing identification of cycles with pulp package")
            C = co.ConstructInitialLP(allrxns, allmets, DB, [], True, False)
            IP = ip_pulp.IntergerProgram(DB, 10, 20, 1, 'False', 'False', 30, None)
            inmets = DB.get_compounds_in_model('t1')
            inrxns = DB.get_reactions_in_model('t1')
            osp = IP.run_glpk(C, inmets, inrxns, 'cpdT_c0', 'True')
            self.assertEqual(len(osp), 3)
            self.assertEqual(len(osp[-1]), 6)

        except ImportError:
            print ('pulp package not installed, cannot run tests for this python package')

if __name__ == '__main__':
    unittest.main(exit=False)
    os.remove(PATH+'/test.db')
