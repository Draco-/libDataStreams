"""
DS_basic_test.py

Test suite for the DS_basic class
"""

import unittest
import DS_xlsx

class TestCreateDS_xlsx(unittest.TestCase):
    def setUp(self):
        print 'Initialisation of DS_xlsx'
        self.ds = None

    def tearDown(self):
        pass

    # Tests, if it is possible to create an instance of the class
    def runTest(self):
        self.ds = DS_xlsx.DS_xlsx('Test')
        assert self.ds != None, 'Could not instantiate DS_basic'
        #Test the instance variables, that should have been set during creation of the instance
        assert self.ds.ds_name == 'Test', 'Initialisation of Name failed'
        assert self.ds.ds_status == 'closed', 'Initialisation of Status failed'
        assert self.ds.ds_statInfo == False, 'Initialisation of statInfo failed'
        assert self.ds.ds_numRows == 0, 'Initialisation of numRows failes'
        assert self.ds.ds_processedBytes == 0, 'Initialisation of processedBytes failed'
        assert self.ds.ds_limitRows == -1, 'Initialisation of limitRows failed'

        #Additional test for derived class DS_xlsx
        assert self.ds.ds_file == None, 'Instance variable ds_file not initialized'
        assert self.ds.ds_filename == None, 'Instance varialbe ds_filename not initialized'
        assert self.ds.ds_table == None, 'Instance variable ds_table not initialized'
        assert self.ds.ds_tablename == None, 'Instance variable ds_tablename not initialized'
        

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

        #Additional test for derived class DS_xlsx
        assert self.ds.get_filename() == None, 'Method get filename failed'
        filename = self.ds.get_filename()
        self.ds.set_filename('Test Filename')
        assert self.ds.get_filename() == 'Test Filename', 'Variable filename could not be set correctly'
        self.ds.set_filename(filename)

        assert self.ds.get_tablename() == None, 'Method get tablename failed'
        tablename = self.ds.get_tablename()
        self.ds.set_tablename('Test Tablename')
        assert self.ds.get_tablename() == 'Test Tablename', 'Variable tablename could not be set correctly'
        self.ds.set_tablename(tablename)


class TestOpenDS_xlsx(unittest.TestCase):
    def setUp(self):
        print 'Open the DS_xlsx object'
        #self.wd = 'c:/Dokumente und Einstellungen/BaumeiJu01/Eigene Dateien/Geschäft/080 Organisation/Privat/Python/'
        self.wd = '../Testdata/'
        self.xlsx = 'DS_xlsx_testdata.xlsm'
        self.tab = 'Table'

        self.ds = None
        self.ds = DS_xlsx.DS_xlsx('Test')

    def tearDown(self):
        pass

    # Tests, if it is possible to open the basic data source
    def runTest(self):
        assert self.ds.ds_status == 'closed', 'Object creation started with wrong status'
        assert self.ds.ds_file == None, 'Object creation started with ds_file already set'
        self.ds.open(self.wd + self.xlsx, self.tab)

        assert self.ds.ds_file != None, 'Open method did not open a file'
        assert self.ds.ds_table != None, 'Open method did not get a sheet object'
        assert self.ds.ds_reader != None, 'Open method did not get a data reader'
        assert self.ds.ds_status == 'open', 'Open status set wrong for the object'


class TestCloseDS_xlsx(unittest.TestCase):
    def setUp(self):
        print 'Close the DS_xlsx object'
        self.wd = 'c:/Dokumente und Einstellungen/BaumeiJu01/Eigene Dateien/Geschäft/080 Organisation/Privat/Python/'
        self.xlsx = 'DS_xlsx_testdata.xlsm'
        self.tab = 'Table'

        self.ds = None
        self.ds = DS_xlsx.DS_xlsx('Test')
        self.ds.open(self.wd + self.xlsx, self.tab)

    def tearDown(self):
        pass


    # Test, if the closing of the data source works
    def runTest(self):
        assert self.ds.ds_file != None, 'Setup did not open a file'
        assert self.ds.ds_table != None, 'Setup did not get a sheet object'
        assert self.ds.ds_reader != None, 'Setup did not get a data reader'
        assert self.ds.ds_status == 'open', 'Open status set wrong for the object'

        self.ds.close()
        assert self.ds.ds_file == None, 'Close method did not close the file'
        assert self.ds.ds_table == None, 'Close method did not close the sheet object'
        assert self.ds.ds_reader == None, 'Close method did not close the data reader'
        assert self.ds.ds_status == 'closed', 'Status set wrong for the object'


class TestNextDS_xlsx(unittest.TestCase):
    def setUp(self):
        print 'Get next record from DS_xlsx'
        self.wd = 'c:/Dokumente und Einstellungen/BaumeiJu01/Eigene Dateien/Geschäft/080 Organisation/Privat/Python/'
        self.xlsx = 'DS_xlsx_testdata.xlsm'
        self.tab = 'Table'

        self.ds = None
        self.ds = DS_xlsx.DS_xlsx('Test')
        self.ds.open(self.wd + self.xlsx, self.tab)

    def tearDown(self):
        pass

    def runTest(self):
        rec = None
        rec = self.ds.next()

        assert rec != None, 'DS_xlsx returned no record'
        assert self.ds.ds_status == 'open', 'DS_xlsx closed after one record'
        assert self.ds.ds_numRows == 1, 'Counting of records did not work'
        #print self.ds.ds_processedBytes
        #assert self.ds.ds_processedBytes == 35, 'Counting of processed bytes did not work'

        count = 0
        while count < 10:
            rec = self.ds.next()
            count += 1

        assert rec != None, 'DS_xlsx did not return 11nth record'
        assert self.ds.ds_numRows == 11, 'Counting of records did not work'
        #print self.ds.ds_processedBytes
        #assert self.ds.ds_processedBytes == 479, 'Counting of processed bytes did not work'        


class TestRowLimitDS_xlsx(unittest.TestCase):
    def setUp(self):
        print 'Test row limiting of DS_xlsx'
        self.wd = 'c:/Dokumente und Einstellungen/BaumeiJu01/Eigene Dateien/Geschäft/080 Organisation/Privat/Python/'
        self.xlsx = 'DS_xlsx_testdata.xlsm'
        self.tab = 'Table'

        self.ds = None
        self.ds = DS_xlsx.DS_xlsx('Test')
        self.ds.open(self.wd + self.xlsx, self.tab)
        
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
            self.fail("DS_xlsx doesn't raise StopIteration when finished")


class TestResetDS_xlsx(unittest.TestCase):
    def setUp(self):
        print 'Test the reset method of DS_xlsx'
        self.wd = 'c:/Dokumente und Einstellungen/BaumeiJu01/Eigene Dateien/Geschäft/080 Organisation/Privat/Python/'
        self.xlsx = 'DS_xlsx_testdata.xlsm'
        self.tab = 'Table'

        self.ds = None
        self.ds = DS_xlsx.DS_xlsx('Test')
        self.ds.open(self.wd + self.xlsx, self.tab)
 
    def tearDown(self):
        pass

    def runTest(self):
        print 'Running the test'
        count = 0
        while count < 15:
            self.ds.next()
            count += 1

        assert self.ds.get_numRows() == 15, 'Counting of records did not work'
        assert self.ds.ds_status == 'open', 'DS_xlsx closed unexpectedly'

        self.ds.reset()
        assert self.ds.ds_status == 'open', 'DS_xlsx did not reopen after reset'
        assert self.ds.ds_name == 'Test', 'Name has changed unexpectedly'
        assert self.ds.ds_numRows == 0, 'Reinitialisation of numRows failes'
        #assert self.ds.ds_processedBytes == 0, 'Reinitialisation of processedBytes failed'
        
        count = 0
        while count < 15:
            self.ds.next()
            count += 1

        rec = self.ds.next()
        #print rec['F'][0:10]
        assert rec['F'][0:10] == '1161316', 'First record not returned correctly'
        

class TestRecordDS_xlsx(unittest.TestCase):
    def setUp(self):
        print 'Test record returned by DS_xlsx'
        self.wd = 'c:/Dokumente und Einstellungen/BaumeiJu01/Eigene Dateien/Geschäft/080 Organisation/Privat/Python/'
        self.xlsx = 'DS_xlsx_testdata.xlsm'
        self.tab = 'Table'

        self.ds = None
        self.ds = DS_xlsx.DS_xlsx('Test')
        self.ds.open(self.wd + self.xlsx, self.tab)

    def tearDown(self):
        pass

    def runTest(self):
        count = 0
        while count < 15:
            self.ds.next()
            count += 1

        rec = self.ds.next()
        assert isinstance(rec, dict), 'Returned record is not a dictionary'
        #print len(rec)
        assert len(rec) == 21, 'Record not returned correctly'
        try:
            field = rec['F']
        except:
            self.fail('Returned record has unexpected content')
        else:
            assert rec['F'][0:10] == '1161316', 'Returned record has unexpected value'

        self.ds.set_statInfo(True)
        assert self.ds.ds_statInfo == True, 'Could not set statInfo to True'

        rec = self.ds.next()
        assert isinstance(rec, dict), 'Returned record is not a dictionary'
        try:
            field = rec['F'][0:10]
            numRows = rec['ds_numRows']
            processedBytes = rec['ds_processedBytes']
            name = rec['ds_name']
        except:
            self.fail('Returned record has unexpected content')
        else:
            #print field
            assert field == '', 'Returned record has unexpected value'
            #print self.ds.ds_numRows
            assert numRows == 17, 'Returned record has unexpected numRows'
            #print self.ds.get_processedBytes()
            #assert processedBytes == 303, 'Returned record has unexpected processedBytes'
            assert name == 'Test', 'Returned record has unexpected name'


        



        
        

        
def suite():
    print 'Testing DS_xlsx'
    testSuite=unittest.TestSuite()
    testSuite.addTest(TestCreateDS_xlsx())
    testSuite.addTest(TestOpenDS_xlsx())
    testSuite.addTest(TestCloseDS_xlsx())
    testSuite.addTest(TestNextDS_xlsx())
    testSuite.addTest(TestRowLimitDS_xlsx())
    testSuite.addTest(TestResetDS_xlsx())
    testSuite.addTest(TestRecordDS_xlsx())
    return testSuite
    
def main():
    runner = unittest.TextTestRunner()
    runner.run(suite())

    
if __name__ == '__main__':
    main()
