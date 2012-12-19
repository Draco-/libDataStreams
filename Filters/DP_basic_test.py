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
Test the DS_basic class
"""
#==============================================================================================================
# Import section
#==============================================================================================================
import sys
import unittest

sys.path.append('../Streams')
from DS_basic import DS_basic

#==============================================================================================================
# Global values
#==============================================================================================================
if __name__ == '__main__':
	single_test = True
else:
	single_test = False
	
#==============================================================================================================
# Test class initialisation and class variables
#==============================================================================================================
class TestCreateDS_basic(unittest.TestCase):
	def setUp(self):
		print ' Creation of DS_basic object'
		
	def tearDown(self):
		pass
		
	def runTest(self):
		if single_test:
			print '\n  Initialisation of DS_basic object'
		
		self.ds = None
		self.ds = DS_basic('Test')
		assert self.ds != None, 'Could not instantiate an object for the class'

		if single_test:
			print '  Default values for instance variables'

		assert self.ds.ds_name == 'Test', 'Initialisation of Name failed'
		assert self.ds.ds_status == 'closed', 'Initialisation of Status failed'
		assert self.ds.ds_statInfo == False, 'Initialisation of statInfo failed'
		assert self.ds.ds_numRows == 0, 'Initialisation of numRows failes'
		assert self.ds.ds_processedBytes == 0, 'Initialisation of processedBytes failed'
		assert self.ds.ds_limitRows == -1, 'Initialisation of limitRows failed'

		if single_test:
			print '  Get methods for instance variables'
			
		assert self.ds.get_name() == 'Test', 'Method get_name failed'
		assert self.ds.get_status() == 'closed', 'Method get_status failed'
		assert self.ds.get_statInfo() == False, 'Method get_statInfo failed'
		assert self.ds.get_numRows() == 0, 'Method get_numRows failed'
		assert self.ds.get_processedBytes() == 0, 'Method get_processedBytes failed'
		assert self.ds.get_limitRows() == -1, 'Method get_limitRows failed'

		if single_test:
			print '  Set methods for instance variables'
			
		self.ds.set_statInfo(True)
		assert self.ds.ds_statInfo == True, 'Method set_statInfo could not set statInfo'
		self.ds.set_statInfo(False)
		assert self.ds.ds_statInfo == False, 'Method set_statInfo could not reset statInfo'
		
		self.ds.set_limitRows(10)
		assert self.ds.ds_limitRows == 10, 'Method set_limitRows could not set limitRows'
		self.ds.set_limitRows(-1)
		assert self.ds.ds_limitRows == -1, 'Method set_limitRows could not reset limitRows'

#==============================================================================================================
# Test class open / close underlying data source
#==============================================================================================================
class TestOpenCloseDS_basic(unittest.TestCase):
	def setUp(self):
		print '\n Open / close the data source for DS_basic'
		self.ds = None
		self.ds = DS_basic('Test')
		
	def tearDown(self):
		pass
		
	def runTest(self):
		# Low level test, opening and closing of the data source
		if single_test:
			print '  Test opening / closing of data source (low level)'
		
		try:
			self.ds._open_data_source([])
		except:
			print '   Low level method _open_data_source() raised exception'
		
		try:
			self.ds._close_data_source()
		except:
			print '   Low level method _close_data_source() raised exception'
		
		# Function test for open() and close() method
		if single_test:
			print '  Open method for the DS_basic object'
		
		self.ds.open([])
		assert self.ds.ds_status == 'open', 'Method open() could not open the data source'
		self.ds.close()
		assert self.ds.ds_status == 'closed', 'Method close() could not close the data source'
		
#==============================================================================================================
# Test class get next record 
#==============================================================================================================
class TestNextDS_basic(unittest.TestCase):
	def setUp(self):
		print '\n Get next record from DS_basic'
		self.ds = None
		self.ds = DS_basic('Test')
		self.ds.open()
		
	def tearDown(self):
		try:
			self.ds.close()
		except:
			pass
			
	def runTest(self):
		# Low level test, get the next record with _get_next_record method
		if single_test:
			print '  Test _get_next_record (Low level)'
			
		rec = None
		procBytes = self.ds.ds_processedBytes
		try:
			rec = self.ds._get_next_record()
		except:
			print '  Low level method _get_next_record() raised exception'
		assert rec != None, 'Method _get_next_record did not return a record'
		assert rec.__class__.__name__ == 'dict', 'Method _get_next_record did not return a dictionary as record'
		assert self.ds.ds_processedBytes != procBytes, 'Method _get_next_record did not change number of processed Bytes'
		
		if single_test:
			print '  Test next() method - single shot'
			
		rec = None
		try:
			rec = self.ds.next()
		except:
			print '  Method next() raised exception'
		assert rec != None, 'Method next() did not return a record'
		assert rec.__class__.__name__ == 'dict', 'Method next() did not return a dictionary as record'
		assert self.ds.ds_numRows == 1, 'Method next() did not count number of Rows provided'
		assert self.ds.ds_processedBytes == 44, 'Counting of processed Bytes did not work properly'
		
		if single_test:
			print '  Test next() method - repeated calls'

		try:
			count = 0
			while count < 10:
				rec = self.ds.next()
				assert rec != None, 'Method next() did not return a record'
				assert rec.__class__.__name__ == 'dict', 'Method next() did not return a dictionary as record'
				count += 1
		except:
			print '  Test next() method - repeated calls raised exception'
			
		assert self.ds.ds_numRows == 11, 'Method next() did not count number of Rows provided'
		#print self.ds.ds_processedBytes
		assert self.ds.ds_processedBytes == 264, 'Counting of processed Bytes did not work properly'
			


#==============================================================================================================
# Test controll and start up
#==============================================================================================================
def suite():
	print 'Testing DS_basic'
	testSuite=unittest.TestSuite()
	testSuite.addTest(TestCreateDS_basic())
	testSuite.addTest(TestOpenCloseDS_basic())
	testSuite.addTest(TestNextDS_basic())
	return testSuite
    
def main():
	runner = unittest.TextTestRunner()
	runner.run(suite())

    
if __name__ == '__main__':
	main()
