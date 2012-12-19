"""
REC_tostr_test.py

Test Suite for REC_tostr
"""
#==============================================================================================================
# Import section
#==============================================================================================================
import unittest
from REC_tostr import REC_tostr
from REC_tostr import form_str

#==============================================================================================================
# Test classes
#==============================================================================================================

# Sample record for testing
#==============================================================================================================
sr = {'Fld 01 - string':         'Dies ist ein normal langer String',
      'Fld 02 - pinteger':       1234,
      'Fld 03 - ninteger':       -1234,
      'Fld 04 - pfloat':         123.123,
      'Fld 05 - nfloat':         -123.123,
      'Fld 06 - long':           1234567L}

# Creation and setup of the REC_tostr object
#==============================================================================================================
class TestCreateREC_tostr(unittest.TestCase):
	def setUp(self):
		pass
		
	def tearDown(self):
		pass
		
	def runTest(self):
		rp = None
		rp = REC_tostr()
		assert rp != None, 'Could not instantiate REC_tostr object'
		assert rp.formats == {}, 'Internal formats dictionary initialised wrong'


class TestInstanceVariablesREC_tostr(unittest.TestCase):
	def setUp(self):
		self.rp = None
		self.rp = REC_tostr()
		
	def tearDown(self):
		pass
		
	def runTest(self):
		# Instance variable .formats
		assert self.rp.formats == {}, 'Internal formats dictionard initialised wrong'
		self.rp.set_formats({'int':[form_str, None]})
		assert self.rp.formats.__class__.__name__ == 'dict', 'Fail internal formats set wrong'
		assert self.rp.formats['int'] == [form_str, None], 'Fail internal formats with wrong content'
		self.rp.set_formats()
		assert self.rp.formats == {}, 'Fail for setting default formats'
		
		# Class variable def_formats
		cf = REC_tostr.def_formats
		assert self.rp.get_default_formats() == cf, 'Could not get default formats'

		
		

# Test default formatting
#==============================================================================================================
class TestDefaultREC_tostr(unittest.TestCase):
	def setUp(self):
		self.rp = None
		self.rp = REC_tostr()
		
	def tearDown(self):
		pass
		
	def runTest(self):
		# Default formatting (without fieldlist)
		result = self.rp.rec_str(sr)
		print result
		assert result == '1234567|Dies ist ein normal langer String|   123.123|  -1,234|  -123.123|   1,234|', 'Result is not as expected'
		
		# Formatting using fieldlist
		fl = ['Fld 01 - string','Fld 02 - pinteger','Fld 04 - pfloat','xxx']
		result = self.rp.rec_str(sr, fl)
		print result
		assert result == 'Dies ist ein normal langer String|   1,234|   123.123|n.d.|',  'Result is not as expected'
		

#==============================================================================================================
# Test controll and start up
#==============================================================================================================
def suite():
    print 'Testing REC_tostr'
    testSuite=unittest.TestSuite()
    testSuite.addTest(TestCreateREC_tostr())
    testSuite.addTest(TestInstanceVariablesREC_tostr())
    testSuite.addTest(TestDefaultREC_tostr())

    return testSuite
    
def main():
    runner = unittest.TextTestRunner()
    runner.run(suite())

    
if __name__ == '__main__':
    main()
