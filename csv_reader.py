#
# wrapper script for reading csv file using pandas
#

import pandas as pd


class CsvReader:

    def __init__(self, filepath):
        print("[CsvReader] initialized with file: %s" % filepath)

        self.filepath = filepath

    def get_unique_values_col(self, colName):
        df = pd.read_csv(self.filepath)
        return sorted(df[colName].unique())

    def number_of_Uvalues_per_col(self, colName=None):
        """
        Function to get number of unique values count of given colName

        If colName is not specified,
        then it will return unique value count of of all columns
        """
        length_col_list= []
        df = pd.read_csv(self.filepath)

        # col index
        index = 0

        for i in df:
            col_length = len(pd.unique(df[i]))
            length_col_list.append(col_length)

            # if colName is specified, return its unique count
            if colName:
                if index == self.get_col_index(colName):
                    # return unique count of colName
                    return col_length
            index +=1

        if colName:
            # oops, we were not able to find unique count of colName
            raise Exception("Failed to find unique count for column '%s'" % colName)

        # return unique count of all cols
        return length_col_list

    def det_datatypes_col(self, colName=None):
        """
        Function to get data types of colName. 
        
        If colName is not specified,
        then it will return data type of all columns
        """
        df = pd.read_csv(self.filepath)
        datatype_col = []

        # col index
        index = 0

        for i in df:
            dType = df.dtypes[i]
            datatype_col.append(dType)

            # if colName is specified, return its datatype
            if colName:
                if index == self.get_col_index(colName):
                    # return datatype of colName
                    return dType
            index +=1

        if colName:
            # oops, we were not able to find datatype of colName
            raise Exception("Failed to find datatype for column '%s'" % colName)

        # return datatype of all cols
        return datatype_col

    def get_col_pd_names(self):
        """
        Function to get col names
        """
        df = pd.read_csv(self.filepath)
        pd_col_names = []

        for i in df:
            colName = i
            pd_col_names.append(colName)
        return pd_col_names 

    def get_col_max(self, colName):
        """
        Function to get max value from a col
        """
        df = pd.read_csv(self.filepath)
        return df[colName].max()

    def get_col_min(self, colName):
        """
        Function to get min value from a col
        """
        df = pd.read_csv(self.filepath)
        return df[colName].min()

    def get_col_index(self, colName):
        """
        Function for get index of given col in the header
        """
        index  = 0
        for col in self.get_col_pd_names():
            if col == colName:
                return index
            index += 1

        # this should never happen !!!
        raise Exception("Column '%s'not found in csv" % colName)

##############################################################################
#                                                                            #
#                                 MAIN                                       #
#                                                                            #
##############################################################################
if __name__ == '__main__':

    #some quick tests
    reader = CsvReader("./iris.csv")

    # test reading values from columns
    for col in reader.get_col_pd_names():
        print ("Unique values of col '%s': %s" % (col, reader.get_unique_values_col(col)))
        print (col, " max: ", reader.get_col_max(col))
        print (col, " min: ", reader.get_col_min(col))
        print ("Colum index for '%s' is %d" % (col, reader.get_col_index(col)))
        print ("Colum datatype for '%s' is %s" % (col, reader.det_datatypes_col(col)))
        print ("Unique Count for '%s' is %s" % (col, reader.number_of_Uvalues_per_col(col)))

    # check unique values
    print("Unique values per col: %s" % reader.number_of_Uvalues_per_col())

    # check data types
    print("Data types col: %s" % reader.det_datatypes_col())

    # col names
    print("Col pd names: %s" % reader.get_col_pd_names())
