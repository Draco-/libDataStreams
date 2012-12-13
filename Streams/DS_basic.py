"""
DS_basic.py

A basic class to model various data sources.
A data source in this project is defined as an object, that is able to contact a file,
database, input facility and so on and to provide data as a series of records.
Each record consists of a list of fields, holding the values and their classification
information.

In addition the DS_basic keeps some statistical information such as status of the
connection, number of generated records, number of processed bytes and so on.

For the use within a larger data processing context, the DS_basic is designed to
provide a python iterator. So subsequent processing objects are able to pull a new
record, as needed (we keep this pull strategy throughout the whole project)

This basic data source class is meant to be extended for various types of data
sources
"""
#==============================================================================================================
# Import section
#==============================================================================================================


#==============================================================================================================
# class DS_basic
#==============================================================================================================
class DS_basic:
    """The basic data_source class
    
    This class is just like an interface description. It is not meant to be used
    by itself. Rather use this class to implement data source classes with specific
    data sources
    """
    
    #==============================================================================================================
    # Basic methods
    #==============================================================================================================
    def __init__(self, name='not named'):
        """Initialize the data source object
        """
        #Setting required instance variables
        self.ds_name = name                 #the identifying name of the data source
        self.ds_numRows = 0                 #the number of rows/records generated
        self.ds_processedBytes = 0          #the number of processed bytes so far
        self.ds_limitRows = -1              #the maximum number of rows the iterator will produce
                                            # set to -1 for no limitation
        self.ds_status = 'closed'           #a status information for the data_source
        self.ds_statInfo = False            #Flag to signal, that each record shall keep statistical information    
    
    def __iter__(self):
        """The __iter__ method is required to design the object as an iterator
        object. As the object itself provides the next() method, the object 
        itself is a interator object
        """
        return self
        
    def open(self, *args):
        """Initialize and open the underlying data source
        """
        # As the opening of various data sources depends on the type of data source, we use an additional
        #method for opening this source. This method is meant to be overwritten, when the class is extended
        #try
        self._open_data_source(*args)
        #except
        self.ds_status = 'open'
        
    def close(self):
        """Close the underlying data source
        """
        # As the closing of various data sources depends on the type of data source, we use an additional
        #method for closing this source. This method is meant to be overwritten, when the class is extended
        #try
        self._close_data_source()
        #except
        self.ds_status = 'closed'

    def next(self):
        """Provides the next data record from the source thus implementing
        the interface for python iterators
        
        Returns a record object each time the method is called
        """
        #The method does all the basic testing for availability of new records. 
        if self.ds_status != 'open':
            raise StopIteration                         #should be replaced by a Datasource not open Exeption
        if self.ds_limitRows > 0 and self.ds_numRows >= self.ds_limitRows:
            raise StopIteration
        
        #try
        rec = self._get_next_record()
        #except
        
        self.ds_numRows += 1
        #if flag is set, enrich the record with statisitcal information from data source object
        if self.ds_statInfo:
            rec['ds_numRows'] = self.ds_numRows
            rec['ds_processedBytes'] = self.ds_processedBytes
            rec['ds_name'] = self.ds_name
        return rec
        
    def reset(self):
        """Reset the data source object.
        
        This means, close the underlying data source and reopen it again to be
        able to provide the same record stream as before.
        Additionally all statistics are reset
        """
        self.close()
        self.ds_status = 'closed'
        self.ds_numRows = 0
        self.ds_processedBytes = 0
        self.open()
        self.ds_status = 'open'
        
    def get_name(self):
        """Returns the identifying name of the object
        """
        return self.ds_name

    def get_status(self):
        """Returns the status information for the object
        """
        return self.ds_status
        
    def get_numRows(self):
        """Returns the number of rows provided so far
        """
        return self.ds_numRows
        
    def get_processedBytes(self):
        """Returns the number of bytes processed so far
        """
        return self.ds_processedBytes
        
    def get_statInfo(self):
        """Get the flag for statistical information in every
        record
        """
        return self.ds_statInfo

    def set_statInfo(self, flag):
        """Set the flag for statistical information in every
        record
        """
        self.ds_statInfo = flag
        
    def get_limitRows(self):
        """Return the actual value of ds_limitRows from the object
        """
        return self.ds_limitRows
        
    def set_limitRows(self, limit):
        """Set the value for ds_limitRows to limit
        
        a limit of -1 means, no limitation
        """
        self.ds_limitRows = limit
        
        
    #==============================================================================================================
    # Methods that are meant to be overwritten, when a special data source is implemented
    #==============================================================================================================
    def _open_data_source(self, *args):
        """Initialize and open the underlying data source for
        the actual object
        """
        #We pass this here, because there is no idea, how this is to be done in a special data source
        pass
        
    def _close_data_source(self):
        """Close down the underlying data source for the
        actual object
        """
        #We pass this here, because there is no idea, how this is to be done in a special data source
        pass

    def _get_next_record(self):
        """Get the next record, that is provided by the unterlying
        data source
        """
        #In order to keep the ds_processedBytes accurate, it is necessary, to add up this value here
        #==============================================================================================================
        self.ds_processedBytes += len('dummy record from ') + len(self.ds_name)

        #Implement logic to get a new record from the underlying data source here
        #==============================================================================================================
        return {'value':('dummy record from ' + self.ds_name)}




    
