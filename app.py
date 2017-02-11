import sys
import os
from PyQt5 import QtGui, QtCore, uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox, QListWidgetItem
from PyQt5.uic import loadUi

from utils import getFileFromDialog

from constants import *
from csv_reader import CsvReader
from xml_writer import XmlWriter
from attribute_info import AttributeInfo
from data_info import DataInfo

DIRPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))


class Window(QMainWindow):
    """
    Main GUI class for application
    """

    csv_path = None

    #
    # dict for storing attibutes data
    # as associative dict of col/attr name and AttributeInfo
    #
    attrs = {}

    def __init__(self):
        QWidget.__init__(self)

        # loaind ui from xml
        uic.loadUi(os.path.join(DIRPATH, 'app.ui'), self)

        # button event handlers
        self.btnXmlTemplate.clicked.connect(self.handleXmlTemplate)
        self.btnBrowseData.clicked.connect(self.handleBrowseData)
        self.btnSave.clicked.connect(self.handleSave)
        self.btnSaveClose.clicked.connect(self.handleSaveClose)
        self.btnCancel.clicked.connect(self.handleCancel)

        # attribute definition and definition source change event handlers
        self.teAttributeDef1.textChanged.connect(self.handleAttributeDefChanged1)
        self.teAttributeSource1.textChanged.connect(self.handleAttributeSourceChanged1)

        self.teAttributeDef2.textChanged.connect(self.handleAttributeDefChanged2)
        self.teAttributeSource2.textChanged.connect(self.handleAttributeSourceChanged2)

        self.teAttributeDef3.textChanged.connect(self.handleAttributeDefChanged3)
        self.teAttributeSource3.textChanged.connect(self.handleAttributeSourceChanged3)

        # ENUMERATED data change event handlers
        self.teEnumDef.textChanged.connect(self.enumDefinitionChanged)
        self.teEnumSrc.textChanged.connect(self.enumSourceChanged)
        self.lstEnumUnique.currentItemChanged.connect(self.enumUniqueChanged)

        # RANGE min, max, unit, resolution data change event handlers
        self.teRangeMin.textChanged.connect(self.handleRangeMinChanged)
        self.teRangeMax.textChanged.connect(self.handleRangeMaxChanged)
        self.teUnit.textChanged.connect(self.handleUnitChanged)
        self.teResolution.textChanged.connect(self.handleResolutionChanged)

        # CODESET name and source change event handler
        self.teCodesetName.textChanged.connect(self.handleCodesetNameChanged)
        self.teCodesetSource.textChanged.connect(self.handleCodesetSourceChanged)

        # UNREPRESENTABLE desc filed change event handler
        self.teUnreprDesc.textChanged.connect(self.handleUnreprensentableChanged)

        # radio buttons signal handlers
        self.rbEnumerated.toggled.connect(self.fieldTypeChanged)
        self.rbRange.toggled.connect(self.fieldTypeChanged)
        self.rbCodeset.toggled.connect(self.fieldTypeChanged)
        self.rbUnrepresentable.toggled.connect(self.fieldTypeChanged)

        # convenience dict of radio button names and objects
        self.dict_rbs = { ENUMERATED: self.rbEnumerated,
                RANGE: self.rbRange,
                CODESET: self.rbCodeset,
                UNREPRESENTABLE: self.rbUnrepresentable }

        # adding listener for left side list's item changed
        self.lstItems.currentItemChanged.connect(self.attributeChanged)

        # gui setup
        self.setupGui()
	
    def setupGui(self):
        """
        Initialize gui and defualt values etc
        """

        # default initialization of GUI
        self.lblMeasurementDesc.setText(TXT_MEASUREMENT_DESC)

        # setting desc for domain detail labels for dunamic widgets
        self.lblEnumeratedDomain.setText(TXT_ENUMERATED_DOMAIN)
        self.lblRangeDomain.setText(TXT_RANGE_DOMAIN)
        self.lblCodesetDomain.setText(TXT_CODESET_DOMAIN)
        self.lblUnrepresentableDomain.setText(TXT_UNPRESENTABLE_DOMAIN)

        # default field type select in ui is 'enumerated'
        self.field_type = ENUMERATED

        # default field type is 'enumerated'
        self.rbEnumerated.setChecked(True)

        # overview text
        self.teOverview.setText(TXT_OVERVIEW)

        # citation text
        self.teCitation.setText(TXT_CITATION)

    def ensureAttributeType(self):
        if not self.lstItems.count():
            self.attr_type = None
            return

        if not self.lstItems.currentItem():
            self.lstItems.setCurrentRow(0)
        self.attr_type = self.lstItems.currentItem().text()

    def attributeChanged(self):
        """
        Function dynamically shows widgets on right side of tab 2
        Whenever an item is selected/changed on lest side list.

        Radio buttons on right side are automatically selected,
        depending upon the values of attribute's column in csv file
        """

        self.ensureAttributeType()
        if not self.attr_type:
            print "[WARNING] attributeChanged() :: not attr type !!!"
            return

        self.refresh_enumerated_list_values()

        ################################################
        #                                              #
        # Enable/disable radio buttons on right side   #
        # depending upon the data of select attribute  #
        # associated with a column in csv file         #
        #                                              #
        ################################################

        if not self.csv_reader:
            print "[WARNING] :: No csv loaded to read values"
            return

        # if attributes dict is not initialized not need to continue
        if not self.attrs:
            print "[WARNING] attributeChanged() :: attributes dict is not initialized"

            # first time - default vals
            self.teAttributeDef1.setText("%s %s" % (ATTRIBUTE_DEFINITION, self.attr_type))
            self.teAttributeSource1.setText("%s %s" % (DATA_SOURCE, self.attr_type))

            self.teAttributeDef2.setText("%s %s" % (ATTRIBUTE_DEFINITION, self.attr_type))
            self.teAttributeSource2.setText("%s %s" % (DATA_SOURCE, self.attr_type))

            self.teAttributeDef3.setText("%s %s" % (ATTRIBUTE_DEFINITION, self.attr_type))
            self.teAttributeSource3.setText("%s %s" % (DATA_SOURCE, self.attr_type))
            return

        ####################################################
        #                                                  #
        # Fill UI with information from selected attribute #
        #                                                  #
        ####################################################

        attr = self.attrs[self.attr_type]

        # update text fields for attribute definition and definition source
        # from values in the current attribute
        self.teAttributeDef1.setText(attr.defn1)
        self.teAttributeSource1.setText(attr.dsrc1)

        self.teAttributeDef2.setText(attr.defn2)
        self.teAttributeSource2.setText(attr.dsrc2)

        self.teAttributeDef3.setText(attr.defn3)
        self.teAttributeSource3.setText(attr.dsrc3)

        ucnt = self.csv_reader.number_of_Uvalues_per_col(self.attr_type)
        dtype = str(attr.dtype)

        # checking/selecting radio button depending upon the type 
        # determined for given cols datatype and unique counts
        ft = self.det_rb_type(self.attr_type)
        ft = attr.field_type
        if ft:
            self.dict_rbs[ft].setChecked(True)
        else:
            print "WARNING :: No radio buttion selected for '%s'" % self.attr_type

            #FIXME - unchecking all radio buttons or suggest me what to do !!!!
            self.uncheck_all_radio_buttons()

        self.showCurrentAttributeDataInWidgets()

    def uncheck_all_radio_buttons(self):
        for k,v in self.dict_rbs.iteritems():
            self.dict_rbs[k].setChecked(False)

    def show_range_widget(self):
	self.widRange.setHidden(False)
	self.horizontalLayout.addWidget(self.widRange)

    def show_codeset_widget(self):
	self.widCodeset.setHidden(False)
	self.horizontalLayout.addWidget(self.widCodeset)

    def show_unrepresentable_widget(self):
	self.widUnrepresentable.setHidden(False)
	self.horizontalLayout.addWidget(self.widUnrepresentable)

    def show_enumerated_widget(self):
	self.widEnumerated.setHidden(False)
	self.horizontalLayout.addWidget(self.widEnumerated)

    def handleXmlTemplate(self):
        """
        Browse and select the input xml file
        """
        print('Xml Template')

        filenames = getFileFromDialog()
        self.teXmlTemplate.setText(filenames[0])

    def handleBrowseData(self):
        """
        Browse and read the input csv file
        """

        # set old one to null
        self.csv_reader = None
        self.attr_type = None
        self.attrs = {}
        self.lstItems.clear()
        self.lstEnumUnique.clear()
        self.field_type = None

        filenames = getFileFromDialog()
        self.teBrowseData.setText(filenames[0])

        # creating csv reader
        self.csv_path = filenames[0]
        self.csv_reader = CsvReader(self.csv_path)

        # adding list items on left side
        for col in self.csv_reader.get_col_pd_names():
            self.lstItems.addItem(col)

        # select first row if there are elements in list
        if self.lstItems.count() > 0:
            self.lstItems.setCurrentRow(0)
            self.attr_type = self.lstItems.currentItem().text()

        self.refresh_enumerated_list_values()

        self.populate_attributes_data()

        self.showCurrentAttributeDataInWidgets()

    def det_rb_type(self, col):
        """
        Function determines the radio button type depending upon 
        the datatype and count of unique values in the given col in csv

        return: ENUMERATED, RANGE, CODESET, UNREPRESENTABLE

        Note:
        Function raise an exception if rb type can't be determined
        """

        ucnt = self.csv_reader.number_of_Uvalues_per_col(col)
        dtype = str(self.csv_reader.det_datatypes_col(col))

        print "+--> Unique count of '%s' is %d" % (col, ucnt)
        print "+--> Data type of '%s' is %s" % (col, dtype)

        # checking float64 columns for radio buttons
        if dtype == "float64":

            """
            Unrepresentable if the unique values are less than 23 and
            the datatype is float64. 
            """
            if ucnt < 23:
                return UNREPRESENTABLE

            """
            Range radio button to be selected if there are 23-40 unique vales
            and the datatype is float64.  
            """
            if ucnt >= 23 and ucnt <= 40:
                return RANGE

            """
            Codeset radio button to be selected if there are more than 40 unique
            values and the datatype is float64.  
            """
            if ucnt > 40:
                return CODESET

            #FIXME
            # what to return in else case ?????

        # checking object columns for radio buttons
        if dtype == "object":

            """
            Enumerated if the datatype is 'object' and there are less than 20
            unique values.
            """
            if ucnt < 20:
                return ENUMERATED

        ################################################
        #                                              #
        # NOTE                                         #
        # Default is UNREPRESENTABLE type when we cant #
        # Determine radio button type as above         #
        #                                              #
        ################################################
        return UNREPRESENTABLE

    def populate_attributes_data(self):
        """
        Function populates attributes info in data structure

        i.e. 
        a python dict for AttributeInfo objects and their associated data
        """

        # clearing previous data from dict
        self.attrs = {}
        self.attr_type = None

        firstTime = True

        # create attribute info for each col in csv
        for col in self.csv_reader.get_col_pd_names():
            print "[INFO] populating data for: %s" % col

            # creating attribute info
            ai = AttributeInfo( col )
            ai.field_type = self.det_rb_type(col)

            # ensure field type
            if not ai.field_type:
                print "[WARNING] :: cant populate attribute info for '%s', as field type is null" % col
                continue

            #FIXME or add a fallback field type UNREPRESENTABLE !

            ai.set_unique_count( self.csv_reader.number_of_Uvalues_per_col(col) )
            ai.set_data_type( self.csv_reader.det_datatypes_col(col) )
            ai.set_defn1("%s %s" % (ATTRIBUTE_DEFINITION, col) )
            ai.set_dsrc1("%s %s" % (DATA_SOURCE, col) )

            ai.rmin = self.csv_reader.get_col_min(col)
            ai.rmax = self.csv_reader.get_col_max(col)

            ai.en_unique_index = 0
            ai.en_unique_val = ai.rmin

            # check radio button and set val for range min/max textboxes for first attribute
            if firstTime:
                firstTime = False
                self.dict_rbs[ai.field_type].setChecked(True)
                self.teRangeMax.setText(str(ai.rmax))
                self.teRangeMin.setText(str(ai.rmin))

            # lets see the attribute info
            ai.show()
            
            # keeping attribute info in dict
            self.attrs[col] = ai

    def refresh_enumerated_list_values(self):
        self.lstEnumUnique.clear()

        if not self.csv_reader:
            print "[WARNING] :: No csv loaded to read values"
            return

        if not self.attr_type:
            print "[WARNING] :: refresh_enumerated_list_values() cant find current attribute"
            return

        # adding unique values in enumerated widget's list widget
        for val in self.csv_reader.get_unique_values_col( self.attr_type ):
            self.lstEnumUnique.addItem( str(val) )

        if self.attrs:
            attr = self.attrs[self.attr_type]
            if attr.en_unique_val:
                self.lstEnumUnique.setCurrentRow(attr.en_unique_index)
                return

        # select first row if there are elements in list
        elif self.lstEnumUnique.count() > 0:
            self.lstEnumUnique.setCurrentRow( 0 )

    def handleSave(self):

        if not self.teXmlTemplate.toPlainText():
            print "[ERROR] :: XML output not specified"
            self.show_msgbox("Error", "Output Xml file not specified !")
            return

        ##########################################################
        #                                                        #
        #  Create xml writer and pass ui to it , XML Writer will #
        #  fetch data from ui and save/update in the output xml  #
        #                                                        #
        ##########################################################
        self.xml_writer = XmlWriter(self.teXmlTemplate.toPlainText())
        self.xml_writer.save(self.attrs, self.teCitation.toPlainText(), self.teCitation.toPlainText())

    def handleSaveClose(self):
	print "Save and Close"
        self.handleSave()
        QApplication.quit()

    def handleCancel(self):
	print "Cancel"
        QApplication.quit()

    def fieldTypeChanged(self):

	self.widRange.setHidden(True)
	self.widCodeset.setHidden(True)
	self.widUnrepresentable.setHidden(True)
	self.widEnumerated.setHidden(True)

        # remove all widgets from horizontal layout
	for i in reversed(range(self.horizontalLayout.count())): 
            self.horizontalLayout.removeWidget(self.horizontalLayout.itemAt(i).widget())

        if self.rbEnumerated.isChecked():
            self.field_type = ENUMERATED
            self.show_enumerated_widget()

        if self.rbRange.isChecked():
            self.field_type = RANGE
            self.show_range_widget()

        if self.rbCodeset.isChecked():
            self.field_type = CODESET
            self.show_codeset_widget()

        if self.rbUnrepresentable.isChecked():
            self.field_type = UNREPRESENTABLE
            self.show_unrepresentable_widget()

        ################################################
        #                                              #
        # Update field type of selected attribute when #
        # a radio button is changed                    #
        #                                              #
        ################################################

        # if attributes dict is not initialized not need to continue
        if not self.attrs:
            print "[WARNING] fieldTypeChanged() :: attributes dict is not initialized"
            return

        # beacuse of async signal/slot for various ui elements
        # would be good to perform this check
        if not self.attr_type and self.lstItems.count() > 0:
            self.attr_type = self.lstItems.currentItem().text()

        self.printAttrs()

        self.attrs[self.attr_type].field_type = self.field_type
        self.showCurrentAttributeDataInWidgets()

    def printAttrs(self):
        """
        convenience funciton to watch attributes
        """
        print "-------------[ Attributes ]-------------------"
        for k,v in self.attrs.iteritems():
            print k, v
        print "----------------------------------------------"

    def showCurrentAttributeDataInWidgets(self):
        """
        Function display the data of current selected
        attribute in the dynamic widgets on the right side
        """

        if not self.attr_type:
            return

        print "[showCurrentAttributeDataInWidgets]"

        attr = self.attrs[self.attr_type]

        # showing data in enumerated widget
        if attr.en_def:
            self.teEnumDef.setText(attr.en_def)
        else:
            self.teEnumDef.setText("")

        if attr.en_src:
            self.teEnumSrc.setText(attr.en_src)
        else:
            self.teEnumSrc.setText("")

        if attr.en_unique_val:
            self.lstEnumUnique.setCurrentRow(attr.en_unique_index)

        # showing data in range widget
        if attr.rmin:
            self.teRangeMin.setText(str(attr.rmin))
        else:
            self.teRangeMin.setText("")

        if attr.rmax:
            self.teRangeMax.setText(str(attr.rmax))
        else:
            self.teRangeMax.setText("")

        if attr.unit:
            self.teUnit.setText(str(attr.unit))
        else:
            self.teUnit.setText("")

        if attr.resolution:
            self.teResolution.setText(str(attr.resolution))
        else:
            self.teResolution.setText("")

        # showing data in codeset widget
        if attr.cs_name:
            self.teCodesetName.setText(str(attr.cs_name))
        else:
            self.teCodesetName.setText("")

        if attr.cs_src:
            self.teCodesetSource.setText(str(attr.cs_src))
        else:
            self.teCodesetSource.setText("")

        # showing data unrepresentable widget
        if attr.ur_desc:
            self.teUnreprDesc.setText(str(attr.ur_desc))
        else:
            self.teUnreprDesc.setText("")

    def handleAttributeDefChanged1(self):
        """
        Function is called when ever data is changed in "attribute definition 1" text box
        """

        # if attributes dict is not initialized not need to continue
        if not self.attrs:
            print "[WARNING] handleAttributeDefChanged1() :: attributes dict is not initialized"
            return

        self.ensureAttributeType()

        # update definition value for current attribute
        self.attrs[self.attr_type].defn1 = self.teAttributeDef1.toPlainText()

    def handleAttributeDefChanged2(self):
        """
        Function is called when ever data is changed in "attribute definition 2" text box
        """

        # if attributes dict is not initialized not need to continue
        if not self.attrs:
            print "[WARNING] handleAttributeDefChanged2() :: attributes dict is not initialized"
            return

        self.ensureAttributeType()

        # update definition value for current attribute
        self.attrs[self.attr_type].defn2 = self.teAttributeDef2.toPlainText()

    def handleAttributeDefChanged3(self):
        """
        Function is called when ever data is changed in "attribute definition 3" text box
        """

        # if attributes dict is not initialized not need to continue
        if not self.attrs:
            print "[WARNING] handleAttributeDefChanged3() :: attributes dict is not initialized"
            return

        self.ensureAttributeType()

        # update definition value for current attribute
        self.attrs[self.attr_type].defn3 = self.teAttributeDef3.toPlainText()

    def enumDefinitionChanged(self):
        """
        Function is called when ever data is changed in enumerated definition
        """

        # if attributes dict is not initialized not need to continue
        if not self.attrs:
            print "[warning] enumDefinitionChanged() :: attributes dict is not initialized"
            return

        self.ensureAttributeType()

        # update definition source value for current attribute
        self.attrs[self.attr_type].en_def = self.teEnumDef.toPlainText()

    def enumSourceChanged(self):
        """
        Function is called when ever data is changed in enumerated value
        """

        # if attributes dict is not initialized not need to continue
        if not self.attrs:
            print "[warning] enumSourceChanged() :: attributes dict is not initialized"
            return

        self.ensureAttributeType()

        # update definition source value for current attribute
        self.attrs[self.attr_type].en_src = self.teEnumSrc.toPlainText()

    def enumUniqueChanged(self):
        """
        Function is called when ever data is changed in enumerated unique list
        """

        print "enumUniqueChanged cnt: ", self.lstEnumUnique.count()

        # if attributes dict is not initialized not need to continue
        if not self.attrs:
            print "[WARNING] enumUniqueChanged() :: attributes dict is not initialized"
            return

        if not self.lstEnumUnique.count():
            print "[WARNING] enumUniqueChanged() :: lst is empty"
            return


        if not self.lstEnumUnique.currentItem():
            print "[WARNING] enumUniqueChanged() :: lst has not item selected"
            return

        self.ensureAttributeType()

        # update enum unique value for current attribute
        self.attrs[self.attr_type].en_unique_index = self.lstEnumUnique.currentRow()
        self.attrs[self.attr_type].en_unique_val = self.lstEnumUnique.currentItem().text()

    def handleAttributeSourceChanged1(self):
        """
        Function is called when ever data is changed in "attribute definition source 1" text box
        """

        # if attributes dict is not initialized not need to continue
        if not self.attrs:
            print "[warning] handleAttributeSourceChanged1() :: attributes dict is not initialized"
            return

        self.ensureAttributeType()

        # update definition source value for current attribute
        self.attrs[self.attr_type].dsrc1 = self.teAttributeSource1.toPlainText()

    def handleAttributeSourceChanged2(self):
        """
        Function is called when ever data is changed in "attribute definition source 2" text box
        """

        # if attributes dict is not initialized not need to continue
        if not self.attrs:
            print "[warning] handleAttributeSourceChanged2() :: attributes dict is not initialized"
            return

        self.ensureAttributeType()

        # update definition source value for current attribute
        self.attrs[self.attr_type].dsrc2 = self.teAttributeSource2.toPlainText()

    def handleAttributeSourceChanged3(self):
        """
        Function is called when ever data is changed in "attribute definition source 3" text box
        """

        # if attributes dict is not initialized not need to continue
        if not self.attrs:
            print "[warning] handleAttributeSourceChanged3() :: attributes dict is not initialized"
            return

        self.ensureAttributeType()

        # update definition source value for current attribute
        self.attrs[self.attr_type].dsrc3 = self.teAttributeSource3.toPlainText()

    def handleRangeMinChanged(self):
        """
        Function is called when ever range min is changed
        """
        
        print "[handleRangeMinChanged] range min: ", self.teRangeMin.toPlainText()

        # if attributes dict is not initialized not need to continue
        if not self.attrs:
            print "[WARNING] handleRangeMinChanged() :: attributes dict is not initialized"
            return

        self.ensureAttributeType()

        # update range min value for current attribute
        self.attrs[self.attr_type].rmin = self.teRangeMin.toPlainText()

    def handleRangeMaxChanged(self):
        """
        Function is called when ever range max is changed
        """
        print "[handleRangeMaxChanged] range max: ", self.teRangeMax.toPlainText()

        # if attributes dict is not initialized not need to continue
        if not self.attrs:
            print "[WARNING] handleRangeMaxChanged() :: attributes dict is not initialized"
            return

        self.ensureAttributeType()

        # update range max value for current attribute
        self.attrs[self.attr_type].rmax = self.teRangeMax.toPlainText()

    def handleUnitChanged(self):
        """
        Function is called when ever range unit is changed
        """
        print "[handleUnitChanged] range unit: ", self.teUnit.toPlainText()

        # if attributes dict is not initialized not need to continue
        if not self.attrs:
            print "[WARNING] handleUnitChanged() :: attributes dict is not initialized"
            return

        self.ensureAttributeType()

        # update range unit value for current attribute
        self.attrs[self.attr_type].unit = self.teUnit.toPlainText()

    def handleResolutionChanged(self):
        """
        Function is called when ever range resolution is changed
        """
        print "[handleResolutionChanged] resolution: ", self.teResolution.toPlainText()

        # if attributes dict is not initialized not need to continue
        if not self.attrs:
            print "[WARNING] handleResolutionChanged() :: attributes dict is not initialized"
            return

        self.ensureAttributeType()

        # update range resolution value for current attribute
        self.attrs[self.attr_type].resolution = self.teResolution.toPlainText()

    def handleCodesetNameChanged(self):
        """
        Function is called when ever codeset name is changed
        """
        print "[handleCodesetNameChanged] codeset name: ", self.teCodesetName.toPlainText()

        # if attributes dict is not initialized not need to continue
        if not self.attrs:
            print "[WARNING] handleCodesetNameChanged() :: attributes dict is not initialized"
            return

        self.ensureAttributeType()

        # update codeset name
        self.attrs[self.attr_type].cs_name = self.teCodesetName.toPlainText()

    def handleCodesetSourceChanged(self):
        """
        Function is called when ever codeset source is changed
        """
        print "[handleCodesetSourceChanged] codeset source: ", self.teCodesetName.toPlainText()

        # if attributes dict is not initialized not need to continue
        if not self.attrs:
            print "[WARNING] handleCodesetSourceChanged() :: attributes dict is not initialized"
            return

        self.ensureAttributeType()

        # update codeset source
        self.attrs[self.attr_type].cs_src = self.teCodesetSource.toPlainText()

    def handleUnreprensentableChanged(self):
        """
        Function is called when ever UNREPRESENTABLE desc is changed
        """
        print "[handleUnreprensentableChanged] unrepresentable: ", self.teUnreprDesc.toPlainText()

        # if attributes dict is not initialized not need to continue
        if not self.attrs:
            print "[WARNING] handleUnreprensentableChanged() :: attributes dict is not initialized"
            return

        self.ensureAttributeType()

        # update unrepresentable value for current attribute
        self.attrs[self.attr_type].ur_desc = self.teUnreprDesc.toPlainText()

    def show_msgbox(self, title, text):
        """
        Function for showing error/info message box
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information) 
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
	
        retval = msg.exec_()
        print "[INFO] Value of pressed message box button:", retval


##############################################################################
#                                                                            #
#                                 MAIN                                       #
#                                                                            #
##############################################################################
if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.resize(1240, 820)	
    window.show()
    sys.exit(app.exec_())
