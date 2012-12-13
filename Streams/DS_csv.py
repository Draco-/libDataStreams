"""
DS_csv.py

A data source class to extend DS_basic
This extension class uses the DS_basic data source class to model a data source, that is
based on a csv text file.
"""
#==============================================================================================================
# Import section
#==============================================================================================================
import string
from DS_basic import DS_basic

#==============================================================================================================
# class DS_csv
#==============================================================================================================
class DS_csv(DS_basic):
    """Implements a data source, that uses a csv file to create
    the stream of records
    """

    #==============================================================================================================
    # The modified __init__()  method
    #==============================================================================================================
    def __init__(self, name='not named'):
        DS_basic.__init__(self, name)

        self.ds_file = None                 #a file object, where the data source gets the data
        self.ds_fldSep = ';'                #the field separator to be used in the csv data source
        self.ds_filename = None             #the file name string of the underlying data file

    #==============================================================================================================
    # Methods that are specific for the derived class DS_csv
    #==============================================================================================================
    def get_fldSep(self):
        """Returns the actual field separator used, within the csv file
        """
        return self.ds_fldSep
    
    def set_fldSep(self, sep):
        """Set the field separator, used within the csv file
        record
        """
        self.ds_fldSep = sep
        
    #==============================================================================================================
    # Methods that are meant to be overwritten, when a special data source is implemented
    #==============================================================================================================
    def _open_data_source(self, *args):
        """Overrides method from class data_source
        
        Opens a given file for data input
        """
        if len(args) != 0:
            self.ds_filename = args[0]
            self.ds_file = open(args[0], 'r')
        else:
            self.ds_file = open(self.ds_filename, 'r')

        
    def _close_data_source(self):
        """Overrides method from class data_source
        
        Closes the input file of the object
        """
        if self.ds_file != None:
            self.ds_file.close()
        self.ds_file = None
        
    def _get_next_record(self):
        """Overrides method form class data_source
        
        Gets the next line from the underlying file
        """
        # Read line from text file
        line = self.ds_file.readline()
        if line == '':
            raise StopIteration
        
        # keep processed bytes up to date
        self.ds_processedBytes += len(line) 
        
        # extract fields from read line
        line = line.lstrip()
        line = line.rstrip()
        
        fList = string.split(line, self.ds_fldSep)
        
        # build record
        record = {}
        count = 0
        record.__setitem__("Field {0:d}".format(count), line)
        count += 1
        
        for field in fList:
            record.__setitem__("Field {0:d}".format(count), field)
            count += 1
        
        # finished
        return record




