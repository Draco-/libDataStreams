# coding=utf-8
"""
 Copyright (C) 2012 Jürgen Baumeister

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
DS_basic_test.py
#=====================================================================================================
Test suite for the DS_basic class
"""

import unittest
import DS_csv

class TestCreateDS_csv(unittest.TestCase):
    def setUp(self):
        #print 'Initialisation of DS_csv'
        self.ds = None

    def tearDown(self):
        pass

    # Tests, if it is possible to create an instance of the class
    def runTest(self):
        self.ds = DS_csv.DS_csv('Test')
        assert self.ds != None, 'Could not instantiate DS_basic'
    #Test the instance variables, that should have been set during creation of the instance
        assert self.ds.ds_name == 'Test', 'Initialisation of Name failed'
        assert self.ds.ds_status == 'closed', 'Initialisation of Status failed'
        assert self.ds.ds_statInfo == False, 'Initialisation of statInfo failed'
        assert self.ds.ds_numRows == 0, 'Initialisation of numRows failes'
        assert self.ds.ds_processedBytes == 0, 'Initialisation of processedBytes failed'
        assert self.ds.ds_limitRows == -1, 'Initialisation of limitRows failed'

        #Additional test for derived class DS_csv
        assert self.ds.ds_file == None, 'Instance variable ds_file not initialized'
        assert self.ds.ds_fldSep == ';', 'Field separator not set correctly'
        

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

        #Additional test for derived class DS_csv
        assert self.ds.get_fldSep() == ';', 'Method get fldSep failed'

        fldSep = self.ds.get_fldSep()
        self.ds.set_fldSep(':')
        assert self.ds.get_fldSep() == ':', 'Method set fldSep failed'
        self.ds.set_fldSep(fldSep)


class TestOpenDS_basic(unittest.TestCase):
    def setUp(self):
        #print 'Open the DS_csv object'
        #self.wd = 'c:/Dokumente und Einstellungen/BaumeiJu01/Eigene Dateien/Geschäft/080 Organisation/Privat/Python/'
        self.wd = '../Testdata/'
        self.csv = 'DS_csv_testdata.csv'

        self.ds = None
        self.ds = DS_csv.DS_csv('Test')

    def tearDown(self):
        try:
            self.ds.ds_file.close()
        except:
            pass

    # Tests, if it is possible to open the basic data source
    def runTest(self):
        assert self.ds.ds_status == 'closed', 'Object creation started with wrong status'
        assert self.ds.ds_file == None, 'Object creation started with ds_file already set'
        self.ds.open(self.wd + self.csv)

        assert self.ds.ds_file != None, 'Open method did not open a file'
        assert self.ds.ds_status == 'open', 'Could not open DS_basic object'


class TestCloseDS_basic(unittest.TestCase):
    def setUp(self):
        #print 'Close the DS_basic object'
        #self.wd = 'c:/Dokumente und Einstellungen/BaumeiJu01/Eigene Dateien/Geschäft/080 Organisation/Privat/Python/'
        self.wd = '../Testdata/'
        self.csv = 'DS_csv_testdata.csv'

        self.ds = None
        self.ds = DS_csv.DS_csv('Test')
        self.ds.open(self.wd + self.csv)

    def tearDown(self):
        try:
            self.ds.ds_file.close()
        except:
            pass


    # Test, if the close of the data source works
    def runTest(self):
        assert self.ds.ds_status == 'open', 'Setup for TestCloseDS_csv set wrong status'
        assert self.ds.ds_file != None, 'Setup for TestCloseDS_csv has not opened a file'

        self.ds.close()
        assert self.ds.ds_status == 'closed', 'Could not close DS_basic object'
        assert self.ds.ds_file == None, 'Could not close the underlying csv file'


class TestNextDS_basic(unittest.TestCase):
    def setUp(self):
        #print 'Get next record from DS_basic'
        #self.wd = 'c:/Dokumente und Einstellungen/BaumeiJu01/Eigene Dateien/Geschäft/080 Organisation/Privat/Python/'
        self.wd = '../Testdata/'
        self.csv = 'DS_csv_testdata.csv'

        self.ds = None
        self.ds = DS_csv.DS_csv('Test')
        self.ds.open(self.wd + self.csv)

    def tearDown(self):
        try:
            self.ds.ds_file.close()
        except:
            pass

    def runTest(self):
        rec = None
        rec = self.ds.next()

        assert rec != None, 'DS_basic returned no record'
        assert self.ds.ds_status == 'open', 'DS_basic closed after one record'
        assert self.ds.ds_numRows == 1, 'Counting of records did not work'
        #print self.ds.ds_processedBytes
        assert self.ds.ds_processedBytes == 221, 'Counting of processed bytes did not work'

        count = 0
        while count < 10:
            rec = self.ds.next()
            count += 1

        assert rec != None, 'DS_basic did not return 11nth record'
        assert self.ds.ds_numRows == 11, 'Counting of records did not work'
        #print self.ds.ds_processedBytes
        assert self.ds.ds_processedBytes == 1289, 'Counting of processed bytes did not work'        


class TestRowLimitDS_basic(unittest.TestCase):
    def setUp(self):
        #print 'Test row limiting of DS_basic'
        #self.wd = 'c:/Dokumente und Einstellungen/BaumeiJu01/Eigene Dateien/Geschäft/080 Organisation/Privat/Python/'
        self.wd = '../Testdata/'
        self.csv = 'DS_csv_testdata.csv'

        self.ds = None
        self.ds = DS_csv.DS_csv('Test')
        self.ds.open(self.wd + self.csv)
        
    def tearDown(self):
        try:
            self.ds.ds_file.close()
        except:
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
        #self.wd = 'c:/Dokumente und Einstellungen/BaumeiJu01/Eigene Dateien/Geschäft/080 Organisation/Privat/Python/'
        self.wd = '../Testdata/'
        self.csv = 'DS_csv_testdata.csv'

        self.ds = None
        self.ds = DS_csv.DS_csv('Test')
        self.ds.open(self.wd + self.csv)
 
    def tearDown(self):
        try:
            self.ds.ds_file.close()
        except:
            pass

    def runTest(self):
        #print 'Running the test'
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

        rec = self.ds.next()
        assert rec['Field 0'][0:10] == 'Material;M', 'First record not returned correctly'
        

class TestRecordDS_basic(unittest.TestCase):
    def setUp(self):
        #print 'Test record returned by DS_basic'
        #self.wd = 'c:/Dokumente und Einstellungen/BaumeiJu01/Eigene Dateien/Geschäft/080 Organisation/Privat/Python/'
        self.wd = '../Testdata/'
        self.csv = 'DS_csv_testdata.csv'

        self.ds = None
        self.ds = DS_csv.DS_csv('Test')
        self.ds.open(self.wd + self.csv)

    def tearDown(self):
        try:
            self.ds.ds_file.close()
        except:
            pass

    def runTest(self):
        rec = self.ds.next()
        assert isinstance(rec, dict), 'Returned record is not a dictionary'
        #print len(rec)
        assert len(rec) == 25, 'Record not returned correctly'
        try:
            field = rec['Field 0']
        except:
            self.fail('Returned record has unexpected content')
        else:
            assert rec['Field 0'][0:10] == 'Material;M', 'Returned record has unexpected value'

        self.ds.set_statInfo(True)
        assert self.ds.ds_statInfo == True, 'Could not set statInfo to True'

        rec = self.ds.next()
        assert isinstance(rec, dict), 'Returned record is not a dictionary'
        try:
            field = rec['Field 0'][0:10]
            numRows = rec['ds_numRows']
            processedBytes = rec['ds_processedBytes']
            name = rec['ds_name']
        except:
            self.fail('Returned record has unexpected content')
        else:
            assert field == '220105;50 ', 'Returned record has unexpected value'
            assert numRows == 2, 'Returned record has unexpected numRows'
            #print self.ds.get_processedBytes()
            assert processedBytes == 303, 'Returned record has unexpected processedBytes'
            assert name == 'Test', 'Returned record has unexpected name'


        



        
        

        
def suite():
    print 'Testing DS_csv'
    testSuite=unittest.TestSuite()
    testSuite.addTest(TestCreateDS_csv())
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
