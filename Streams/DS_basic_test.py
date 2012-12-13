"""
DS_basic_test.py

Test suite for the DS_basic class
"""

import unittest
import DS_basic

class TestCreateDS_basic(unittest.TestCase):
    def setUp(self):
        #print 'Initialisation of DS_basic'
        self.ds = None

    def tearDown(self):
        pass

    # Tests, if it is possible to create an instance of the class
    def runTest(self):
        self.ds = DS_basic.DS_basic('Test')
        assert self.ds != None, 'Could not instantiate DS_basic'
        #Test the instance variables, that should have been set during creation of the instance
        assert self.ds.ds_name == 'Test', 'Initialisation of Name failed'
        assert self.ds.ds_status == 'closed', 'Initialisation of Status failed'
        assert self.ds.ds_statInfo == False, 'Initialisation of statInfo failed'
        assert self.ds.ds_numRows == 0, 'Initialisation of numRows failes'
        assert self.ds.ds_processedBytes == 0, 'Initialisation of processedBytes failed'
        assert self.ds.ds_limitRows == -1, 'Initialisation of limitRows failed'

        #Test the usage of get set methods for instance variables
        assert self.ds.get_name() == 'Test', 'Method get_name failed'
        assert self.ds.get_status() == 'closed', 'Method get_status failed'
        assert self.ds.get_statInfo() == False, 'Method get_statInfo failed'

        statInfo = self.ds.get_statInfo()
        self.ds.set_statInfo(not statInfo)
        assert self.ds.get_statInfo() == True, 'Method set_statInfo failed'
        self.ds.set_statInfo(statInfo)

        assert self.ds.get_numRows() == 0, 'Method get_numRows failed'
        assert self.ds.get_processedBytes() == 0, 'Method get_processedBytes failed'
        assert self.ds.get_status() == 'closed', 'Method get_status failed'

        limitRows = self.ds.get_limitRows()
        self.ds.set_limitRows(10)
        assert self.ds.get_limitRows() == 10, 'Method get_limitRows failed'
        self.ds.set_limitRows(limitRows)


class TestOpenDS_basic(unittest.TestCase):
    def setUp(self):
        #print 'Open the DS_basic object'
        self.ds = None
        self.ds = DS_basic.DS_basic('Test')

    def tearDown(self):
        pass

    # Tests, if it is possible to open the basic data source
    def runTest(self):
        assert self.ds.ds_status == 'closed', 'Object creation started with wrong status'
        self.ds.open()

        assert self.ds.ds_name == 'Test', 'Object is changed after open()'
        assert self.ds.ds_status == 'open', 'Could not open DS_basic object'


class TestCloseDS_basic(unittest.TestCase):
    def setUp(self):
        #print 'Close the DS_basic object'
        self.ds = None
        self.ds = DS_basic.DS_basic('Test')
        self.ds.open()


    def tearDown(self):
        pass

    # Test, if the close of the data source works
    def runTest(self):
        assert self.ds.ds_status == 'open', 'Setup for TestCloseDS_basic set wrong status'

        self.ds.close()
        assert self.ds.ds_status == 'closed', 'Could not close DS_basic object'


class TestNextDS_basic(unittest.TestCase):
    def setUp(self):
        #print 'Get next record from DS_basic'
        self.ds = None
        self.ds = DS_basic.DS_basic('Test')
        self.ds.open()

    def tearDown(self):
        pass

    def runTest(self):
        rec = None
        rec = self.ds.next()

        assert rec != None, 'DS_basic returned no record'
        assert self.ds.ds_status == 'open', 'DS_basic closed after one record'
        assert self.ds.ds_numRows == 1, 'Counting of records did not work'
        assert self.ds.ds_processedBytes == 22, 'Counting of processed bytes did not work'

        count = 0
        while count < 10:
            rec = self.ds.next()
            count += 1

        assert rec != None, 'DS_basic did not return 11nth record'
        assert self.ds.ds_numRows == 11, 'Counting of records did not work'
        assert self.ds.ds_processedBytes == 242, 'Counting of processed bytes did not work'        


class TestRowLimitDS_basic(unittest.TestCase):
    def setUp(self):
        #print 'Test row limiting of DS_basic'
        self.ds = None
        self.ds = DS_basic.DS_basic('Test')
        self.ds.open()
        
    def tearDown(self):
        pass

    def runTest(self):
        self.ds.next()
        assert self.ds.ds_numRows == 1, 'Counting of records did not work'

        self.ds.set_limitRows(10)
        assert self.ds.ds_limitRows == 10, 'Could not set row limit properly'

        count = 0
        while count < 9:
            self.ds.next()
            count += 1

        assert self.ds.get_numRows() == 10, 'Counting of records did not work'

        try:
            self.ds.next()
        except StopIteration:
            pass
        else:
            self.fail("DS_basic doesn't raise StopIteration when finished")


class TestResetDS_basic(unittest.TestCase):
    def setUp(self):
        #print 'Test the reset method of DS_basic'
        self.ds = None
        self.ds = DS_basic.DS_basic('Test')
        self.ds.open()

    def tearDown(self):
        pass

    def runTest(self):
        count = 0
        while count < 10:
            self.ds.next()
            count += 1

        assert self.ds.get_numRows() == 10, 'Counting of records did not work'
        assert self.ds.ds_status == 'open', 'DS_basic closed unexpectedly'

        self.ds.reset()
        assert self.ds.ds_status == 'open', 'DS_basic did not reopen after reset'
        assert self.ds.ds_name == 'Test', 'Name has changed unexpectedly'
        assert self.ds.ds_numRows == 0, 'Reinitialisation of numRows failes'
        assert self.ds.ds_processedBytes == 0, 'Reinitialisation of processedBytes failed'
        

class TestRecordDS_basic(unittest.TestCase):
    def setUp(self):
        #print 'Test record returned by DS_basic'
        self.ds = None
        self.ds = DS_basic.DS_basic('Test')
        self.ds.open()

    def tearDown(self):
        pass

    def runTest(self):
        rec = self.ds.next()
        assert isinstance(rec, dict), 'Returned record is not a dictionary'
        try:
            field = rec['value']
        except:
            self.fail('Returned record has unexpected content')
        else:
            assert field == 'dummy record from Test', 'Returned record has unexpected value'

        self.ds.set_statInfo(True)
        assert self.ds.ds_statInfo == True, 'Could not set statInfo to True'

        rec = self.ds.next()
        assert isinstance(rec, dict), 'Returned record is not a dictionary'
        try:
            field = rec['value']
            numRows = rec['ds_numRows']
            processedBytes = rec['ds_processedBytes']
            name = rec['ds_name']
        except:
            self.fail('Returned record has unexpected content')
        else:
            assert field == 'dummy record from Test', 'Returned record has unexpected value'
            assert numRows == 2, 'Returned record has unexpected numRows'
            assert processedBytes == 44, 'Returned record has unexpected processedBytes'
            assert name == 'Test', 'Returned record has unexpected name'


        



        
        

        
def suite():
    print 'Testing DS_basic'
    testSuite=unittest.TestSuite()
    testSuite.addTest(TestCreateDS_basic())
    testSuite.addTest(TestOpenDS_basic())
    testSuite.addTest(TestCloseDS_basic())
    testSuite.addTest(TestNextDS_basic())
    testSuite.addTest(TestRowLimitDS_basic())
    testSuite.addTest(TestResetDS_basic())
    testSuite.addTest(TestRecordDS_basic())
    return testSuite
    
def main():
    runner = unittest.TextTestRunner()
    runner.run(suite())

    
if __name__ == '__main__':
    main()
