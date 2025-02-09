from __future__ import print_function
__author__ = 'Leanne Whitmore'
__email__ = 'lwhitmo@sandia.gov'
__description__ = 'Tests pubchem compounds'

import re
import os
import unittest
from Pubchem import pubchem_compounds as pc
from Database import query as Q
from Database import initialize_database as init_db
from Database import build_kbase_db as bkdb
PATH = os.path.dirname(os.path.abspath(__file__))
PPATH = re.sub('/Pubchem/tests', '', PATH)

if os.path.isfile(PATH+'/test.db') is True:
    os.remove(PATH+'/test.db')
init_db.Createdb(PATH+'/test.db', False)
bkdb.BuildKbase(PATH+'/data', PPATH+'/Database/data/KbasetoKEGGCPD.txt',
                PPATH+'/Database/data/KbasetoKEGGRXN.txt', False,
                PATH+'/test.db', 'bio')
DB = Q.Connector(PATH+'/test.db')

class PubchemTests(unittest.TestCase):
    def setUp(self):
        """Initialize before every test."""
        print ("Initializing tests")
        self.PC = pc.PubchemConnector(DB)

    def tearDown(self):
        """Clean up after each test."""
        print ("Clearing out test suite")
        del self.PC

    def test_get_ID_from_pubchem(self):
        '''Testing retrieval of database ID for a compound from a pubchem ID'''
        print ("Testing retrieval of database ID for a compound from a pubchem ID")
        kbid = self.PC.get_ID_from_pubchemID('71089297', False)
        self.assertIn('cpdA_c0', kbid)
        self.assertIn('cpdD_c0', kbid)

    def test_get_ID_from_name(self):
        '''Testing retrieval of database ID for a compound from a general name'''
        print ("Testing retrieval of database ID for a compound from a general name")
        kbid = self.PC.get_ID_from_name('CPDA')
        self.assertEqual(kbid, 'cpdA_c0')

if __name__ == '__main__':
    unittest.main(exit=False)
    os.remove(PATH+'/test.db')
