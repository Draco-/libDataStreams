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
 
DP_basic.py
#=====================================================================================================
A basic class to model a processing chain of data.
The data processor (DP) gets data records from a data source (DS) or another
data processor, which is prior in the processing chain and manipulates the data
according its function (filtering, mapping of fields, adding fields, calculations
on a record level ...)

Like the data source, the data processor keeps statistical information about the
status and the number of data processed so far

For the use within a larger data processing context, the DP_basic is designed to
provide a python iterator. So subsequent processing objects are able to pull a new
record, as needed (we keep this pull strategy throughout the whole project)

This basic data source class is meant to be extended for various types of data
sources
"""
#==============================================================================================================
# Import section
#==============================================================================================================


#==============================================================================================================
# class DP_basic
#==============================================================================================================
class DP_basic:
	"""The basic data processor class
	
	This class is just like an interface description. It is not meant to be used
	by itself. Rather use this class to implement data source classes with specific
	data sources
	"""
	
	#==============================================================================================================
	# Basic methods
	#==============================================================================================================
	def __init__(self, name='not named'):
		"""Initialize the data processor object
		"""
		#Setting required instance variables
		self.dp_name = name					#the identifying name of the data processor
		self.dp_fetchedRows = 0				#the number of rows/records fetched from previous data source / processor
		self.dp_providedRows = 0			#the number of rows/records providet to the next object in chain
		self.dp_limitRows = -1				#the maximum number of rows the processor will produce
											# set to -1 for no limitation
		self.dp_statInfo = False			#Flag to signal, that each record shall keep statistical information
		self.dp_datasource = None			#Data source, to provide records for the processor

	def __iter__(self):
		"""The __iter__ method is required to design the object as an iterator
		object. As the object itself provides the next() method, the object 
		itself is a interator object
		"""
		return self

	# Unlike the data sources a data processor has no open() and close() method, because it depends on a given data source. There is no
	# need to explicitly enable the processing chain to open an close its underlying data source, as these objects can be controlled
	# by themselves
	
	def next(self):
		"""Provides the next data record
		
		In most cases this data record has to be fetched from the previous data source/processor
		in the processing chain
		"""
		#The method does all the basic testing for availability of new records. 
		if self.dp_limitRows > 0 and self.ds_providedRows >= self.ds_limitRows:
			raise StopIteration
		
		try:
			rec = self._get_next_record()
		except StopIteration:
			raise StopIteration
		except:
			a = 1/0 #Used to signal an Error -- replace with a more suitable reaction
		
		self.dp_providedRows += 1
		
		#if flag is set, enrich the record with statisitcal information from data processor object
		if self.dp_statInfo:
			rec[self.dp_name + ' dp_providedRows'] = self.dp_providedRows
			rec[self.dp_name + ' dp_fetchedRows'] = self.dp_fetchedRows
		return rec
		
	def reset(self):
		"""Enables the application to reset the processor to a defined status
		
		This not necessary for processors, that do not store records for further
		processing
		"""
		self._reset_processor()
		self.dp_fetchedRows = 0
		self.dp_providedRows = 0
		
	def get_name(self):
		"""Returns the identifying name of the object
		"""
		return self.dp_name


	def set_datasource(self, datasource):
		"""Sets the required data source for the processor
		
		This data source must be either a data_source object (or one of its
		derivated classes) or a data_processor object
		"""
		self.dp_datasource = datasource

	def get_providedRows(self):
		"""Returns the number of rows/records provided so far
		"""
		return self.dp_providedRows

	def get_fetchedRows(self):
		"""Returns the number of rows/records fetched from previous object so far
		"""
		return self.dp_fetchedRows

	def get_statInfo(self):
		"""Get the flag for statistical information in every
		record
		"""
		return self.dp_statInfo

	def set_statInfo(self, flag):
		"""Set the flag for statistical information in every
		record
		"""
		self.dp_statInfo = flag
		
	def get_limitRows(self):
		"""Return the actual value of dp_limitRows from the object
		"""
		return self.dp_limitRows
		
	def set_limitRows(self, limit):
		"""Set the value for dp_limitRows to limit
		
		a limit of -1 means, no limitation
		"""
		self.dp_limitRows = limit
		
		
	#==============================================================================================================
	# Methods that are meant to be overwritten, when a special data processor is implemented
	#==============================================================================================================
	def _reset_processor(self):
		"""Enables the processor to be reset to a defined status
		
		It's not necessary to overwrite this, when the processor doesn't store
		records for further processing
		
		It's not necessary to reset the statistical values of the object
		"""
		pass
		
	def _get_next_record(self):
		"""Get the next record, that is provided by the unterlying
		data source
		"""
		# fetch the next record from the datasource
		rec = self.dp_datasource.next()
		self.dp_fetchedRows += 1
		# if processing of the record is required, do it here
		processed_rec = self._process_new_record(rec)
		return processed_rec
		
	def _process_new_record(self, rec):
		"""Do all necessary processing of the given record
		"""
		return rec
		
