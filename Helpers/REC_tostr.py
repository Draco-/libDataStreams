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
 
REC_tostr.py
#=====================================================================================================
A helper module.
Provides functions and a class REC_tostr to convert a given record (dictionary)
to a readable string, that can be printed
"""
#==============================================================================================================
# Import section
#==============================================================================================================


#==============================================================================================================
# Global functions for formatting
#==============================================================================================================
def form_str(value):
	"""Formats a given string
	"""
	return '{0:<s}'.format(value)
	
def form_int(value):
	"""Formats a given integer
	"""
	return '{0:> ,d}'.format(value)
	
def form_float(value):
	"""Formats a given float
	"""
	return '{0:> n}'.format(value)
	
def form_uni(value):
	try:
		string = value.encode('latin_1','replace')
	except:
		string = '?unitxt?'
		
	return '{0:<s}'.format(string)
	
def form_unknown(value):
	"""Formats a given value, if there
	is no information about its format
	"""
	return value.__class__.__name__

def form_none(value):
	return '.'
	
#==============================================================================================================
# class REC_tostr
#==============================================================================================================
class REC_tostr:
	"""A basic class to convert a given record into a printable string
	"""
	def_formats = {	'str':[form_str, None],
					'unicode':[form_uni, None],
					'int':[form_int, 8],
					'float':[form_float, 10],
					'NoneType':[form_none,1]}
	
	def __init__(self, formats = {}):
		self.formats = formats						# Internal format definition dictionary
		self.fieldlist = []							# Internal fieldlist for formatting of many records

	def get_formats(self):
		"""Get the internal format definition dictionary
		"""
		return self.formats
	
	def set_formats(self, formats = {}):
		"""Set the internal format definition dictionary
		if formats is omitted, self.formats is set to {}
		and the default formats from the class are used
		"""
		self.formats = formats
		
	def get_fieldlist(self):
		"""Get the internal fieldlist
		"""
		return self.fieldlist
		
	def set_fieldlist(self, fieldlist):
		"""Set the internal fieldlist
		"""
		self.fieldlist = fieldlist
		
	def get_default_formats(self):
		"""Get the default internal format definition dictionary
		"""
		return REC_tostr.def_formats
		
	def rec_str(self, record, fieldlist = None):
		string = ""
		# If no fieldlist is given
		if fieldlist == None:
			# If fieldlist is set for the object we take this list
			if self.fieldlist != []:
				fields = self.fieldlist
			# Otherwise we only have the fieldlist from the record
			else:
				fields = record.keys()
		# If a fieldlist is given, we take this list
		else:
			fields = fieldlist
		
		for field in fields:
			# If the entry in the fieldlist is a list, the first entry is the fieldname
			if isinstance(field, list):
				key = field[0]
			# Otherwise the entry is the fieldname itself
			else:
				key = field
			
			# If the fieldname is present in the record, we can use this value for formatting
			if key in record.keys():
				value = record[key]
			# Otherwise the field is not defined in the actual record
			else:
				value = 'n.d.'
			
			string = string + self.formatField(value, field) + '|'
		
		return string
		
	def formatField(self, fieldvalue, fieldinfo):
		type = fieldvalue.__class__.__name__
		if type in self.formats.keys():
			format = self.formats[type]
		elif type in REC_tostr.def_formats.keys():
			format = REC_tostr.def_formats[type]
		else:
			format = [form_unknown, None]
		
		element = format[0](fieldvalue)
		element = self._limit_str(element, format[1])
		
		return element
			

	def _limit_str(self, string, length):
		if length == None:
			return string
			
		if len(string) <= length:
			result = (' ' * (length - len(string))) + string
		if len(string) > length:
			result = '*' * length
			
		return result