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
 
EP_field_to_str.py
#=====================================================================================================
Class EP_field_to_str is used to convert a field value to a string with given
length and format
To do this, a formating information has to be given together with the value, or the
default format for this value type is used
"""
#==============================================================================================================
# Import section
#==============================================================================================================
import sys
import re

#==============================================================================================================
# class EP_field_to_str
#==============================================================================================================
class EP_field_to_str:
	"""
	A class to convert a given value to a string with the given format
	"""
	# Definition of default formats
	type_str = re.compile('(.*)')
	
	types = [type_str]
	
	def __init__(self):
		pass
		
	def format_string(self, value, format=None):
		
		if format == None:
			form = self.formats[self.types[0]]
		else:
			form = format
		result = form[1].format(value)
		result = self.truncate_string(result, form[2])
		return result
	
	def truncate_string(self, string, length):
	
		if len(string.strip()) > length:
			return string.strip()[0: length - 4] + ' ...'
		else:
			return string.strip() + ' ' * (length - len(string.strip()))
			

	formats = {types[0]:(format_string,'{0:<s}',20,)}
