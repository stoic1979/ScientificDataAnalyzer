#
# class to encapsulate attribute info for attributes
# like sepal_length, sepal_width, petal_length, petal_length, species etc
#

from constants import *

class AttributeInfo:

    """
    depending upon field type, the attribute info will be changed

    field type can be enumerated, range, codeset, unrepresentable
    """
    field_type = None

    # range params
    rmin = None
    rmax = None
    unit = None
    resolution = None

    # codeset params
    cs_name = None
    cs_src = None

    # unrepresentable params
    ur_desc = None

    # enumerated params
    en_unique_val = None
    en_def = None
    en_src = None
    en_unique_index = 0

    # general params
    ucnt = 0  # unique count
    dtype = None # data type

    # attribute definition and definition source
    defn1 = None
    dsrc1 = None
    defn2 = None
    dsrc2 = None
    defn3 = None
    dsrc3 = None

    def __init__(self, title):
        """
        attribute title will be fetched from csv,
        and assigned to AttributeInfo

        for example, title can be sepal_length, petal_width, species etc
        """
        self.title = title

    def set_enumerated_params(self, en_unique_index, en_unique_val, en_def, en_src):
        assert self.field_type == ENUMERATED, "ERROR :: Cant set '%s' params when field_type is '%s'" % (ENUMERATED, self.field_type)

        self.en_unique_index = en_unique_index
        self.en_unique_val = en_unique_val
        self.en_def = en_def
        self.en_src = en_src

    def set_range_params(self, rmin, rmax, unit, resolution):
        assert self.field_type == RANGE, "ERROR :: Cant set '%s' params when field_type is '%s'" % (RANGE, self.field_type)

        self.rmin = rmin
        self.rmax = rmax
        self.unit = unit
        self.resolution = resolution

    def set_codeset_params(self, name, src):
        assert self.field_type == CODESET, "ERROR :: Cant set '%s' params when field_type is '%s'" % (CODESET, self.field_type)

        self.cs_name = name
        self.cs_src = src

    def set_unrepresentable_params(self, desc):
        assert self.field_type == UNREPRESENTABLE, "ERROR :: Cant set '%s' params when field_type is '%s'" % (UNREPRESENTABLE, self.field_type)

        self.ur_desc = desc

    def set_unique_count(self, val):
        self.ucnt = val

    def set_data_type(self, val):
        self.dtype = val

    def set_defn1(self, val):
        self.defn1 = val

    def set_dsrc1(self, val):
        self.dsrc1 = val
    
    def show(self):
        assert self.field_type, "Field type not set for AttributeInfo"

        print "\n=============[ %s ]===============" % self.title
        print ">> Field Type: %s <<" % self.field_type
        print "Unique Count . . . . : %s" % str(self.ucnt)
        print "Data Type .  . . . . : %s" % str(self.dtype)
        print "Definition 1 . . . . : %s" % str(self.defn1)
        print "Definition Source 1. : %s" % str(self.dsrc1)
        print "Definition 2 . . . . : %s" % str(self.defn2)
        print "Definition Source 2. : %s" % str(self.dsrc2)
        print "Definition 3 . . . . : %s" % str(self.defn3)
        print "Definition Source 3. : %s" % str(self.dsrc3)

        if self.field_type == ENUMERATED:
            print "Unique Index . . .  . : %s" % str(self.en_unique_index)
            print "Unique Value . . .  . : %s" % str(self.en_unique_val)
            print "Definition of Value . : %s" % str(self.en_def)
            print "Source of Value . . . : %s" % str(self.en_src)
            return

        if self.field_type == RANGE:
            print "Range Min . . : %s" % str(self.rmin)
            print "Range Max . . : %s" % str(self.rmax)
            print "Measure Unit .: %s" % str(self.unit)
            print "Rersolution . : %s" % str(self.resolution)
            return

        if self.field_type == CODESET:
            print "Codeset Name . . : %s" % str(self.cs_name)
            print "Codeset Source . : %s" % str(self.cs_src)
            return

        if self.field_type == UNREPRESENTABLE:
            print "Description of Values Recroded : %s" % str(self.ur_desc)


##############################################################################
#                                                                            #
#                                 MAIN                                       #
#                                                                            #
##############################################################################
if __name__ == '__main__':

    from csv_reader import CsvReader

    #some quick tests
    reader = CsvReader("./iris.csv")

    # test ENUMERATED vals
    for col in reader.get_col_pd_names():
        ai = AttributeInfo(col)
        ai.field_type = ENUMERATED
        ai.set_enumerated_params(1, 5.5, "Some definition of value", "Some source of value")
        ai.show()

    # test RANGE vals
    for col in reader.get_col_pd_names():
        ai = AttributeInfo(col)
        ai.field_type = RANGE
        ai.set_range_params(3.4, 5.6, "cms", "some resolution")
        ai.show()

    # test CODESET vals
    for col in reader.get_col_pd_names():
        ai = AttributeInfo(col)
        ai.field_type = CODESET
        ai.set_codeset_params("MAF TIGER", "Some features")
        ai.show()

    # test UNREPRESENTABLE vals
    for col in reader.get_col_pd_names():
        ai = AttributeInfo(col)
        ai.field_type = UNREPRESENTABLE
        ai.set_unrepresentable_params("Some description")
        ai.show()
