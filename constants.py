#
# script for storing constant definitions for project
#

##########################################################################
#                                                                        #
#                      Field Type Constants                              #
#                                                                        #
##########################################################################

ENUMERATED = "Enumerated"
RANGE = "Range"
CODESET = "Codeset"
UNREPRESENTABLE = "Unrepresentable"


##########################################################################
#                                                                        #
#                         Attribute Types                                #
#                                                                        #
##########################################################################

SEPAL_LENGTH = "sepal_length"
SEPAL_WIDTH = "sepal_width"
PETAL_LENGTH = "petal_length"
PETAL_WIDTH = "petal_width"
SPECIES = "species"


##########################################################################
#                                                                        #
#                      Attribute Definitions                             #
#                                                                        #
##########################################################################

ATTRIBUTE_DEFINITION = "This is attribute definition for"
ATTRIBUTE_SOURCE = "This is attribute definition for"


##########################################################################
#                                                                        #
#                      Definition Sources                                #
#                                                                        #
##########################################################################

DATA_SOURCE = "Producer defined for"


##########################################################################
#                                                                        #
# Field Type Labels for enumerated, range, codeset and unrepresentable   #
#                                                                        #
##########################################################################

TXT_ENUMERATED_DOMAIN = "This attribute type should be used when a finite set of values exist as possible " \
        "entries for a field. Provide a definition for each possible entry. All value that " \
        "appear in the filed will be an entry from the enumerated list." \
        "\n\n" \
        "Example: a field name \"RoadType\". Possible values are \"Heavy Duty\". \"Light Duty\", and \"Trail\". " \
        "Three value definitions would be provided that clearly explain the criteria forerach of the three " \
        "classifications."

TXT_RANGE_DOMAIN = "This attribute should be used when value entries will fall within some numeric range. The Range " \
        "Minimum should represent in minimum value recorded in the field. The Range Maximum should represent the " \
        "maximum value recorded in the field. (In some cases, these values could also represent the minimum and " \
        "maximum values that could possible be recorded for the field, although this is usually a little useful). " \
        "Include units when relevant."

TXT_CODESET_DOMAIN = "This text should be used when the values in a field represent entries from an established set of " \
        "codes. If this domain type is used, the authoritative reference that defines the values and their definitions " \
        "needs to reference (include a URL, publication citation, etc.) " \
        "\n\n" \
        "Examples: Zip code, U.S. Census FIPS codes, established industry abbrevations/codes etc."

TXT_UNPRESENTABLE_DOMAIN = "This attribute should be used for any attribute value that is not a codeset, an enumerated somain, or a range. When " \
        "uncertain about which domain type should be used, this is often a good option. Clearly explain what a field represnts to" \
        "assist future data users. If a description is simple, it may be appropriate to have the same text in the 'Attribute Definition'" \
        "and the free text description of the field. " \
        "\n\n" \
        "Example: name of a data technician, dates, notes, free text descriptions/entries, etc."


##########################################################################
#                                                                        #
#           Dict with field types and their descriptions                 #
#                                                                        #
##########################################################################

DICT_FIELD_TYPES = {ENUMERATED: TXT_ENUMERATED_DOMAIN,
        RANGE: TXT_RANGE_DOMAIN,
        CODESET: TXT_CODESET_DOMAIN,
        UNREPRESENTABLE: TXT_UNPRESENTABLE_DOMAIN}


##########################################################################
#                                                                        #
#                Text For Measurement Description                        #
#                                                                        #
##########################################################################

TXT_MEASUREMENT_DESC = "*Measurement resolution is the smallest unit to which measurements are taken. " \
        "This usually corresponds to the number of decimal places captured in the min/max values. " \
        "(Whole number values: resolution 1, A value of 75.242: resolution = .001)"


##########################################################################
#                                                                        #
#                   Overview And Citation Texts                          #
#                                                                        #
##########################################################################

TXT_OVERVIEW = "The entity and attribute information provided here describes the tabular data associated " \
        "with the data set. Please review the detailed description that provided(the individual attribute " \
        "descriptions) for information on the values that appear as fields/table entries of the data set. " \
        "\n\nHere what is defined. "

TXT_CITATION = "The entity and attributes information was generated by the individual and/or agency " \
        "identified as the originator of the data set. Please review the rest of the metadata record " \
        "for additional details and information."
