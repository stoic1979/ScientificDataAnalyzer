#
# wrapper script for generating xml output
#

from lxml import etree
from io import StringIO
from constants import *

class XmlWriter:

    def __init__(self, filepath):

        print("[XmlWriter] initialized with file: %s" % filepath)

        self.filepath = filepath
        self.tree = etree.parse(self.filepath)
        print("[XmlWriter] Input XML:-\n", etree.tostring(self.tree.getroot(), pretty_print=True))

    def create_overview_element(self, des, cit):
        overview = etree.Element('overview')

        eaover = etree.Element('eaover')
        eaover.text = des

        eadetcit = etree.Element('eadetcit')
        eadetcit.text = cit

        overview.append(eaover)
        overview.append(eadetcit)

        return overview

    def create_detailed_element(self, attrs):
        detailed = etree.Element('detailed')

        for attr_type, a in attrs.iteritems():
            attr = etree.Element('attr')

            # label
            attrlabl = etree.Element("attrlabl")
            attrlabl.text = a.title

            #######################################################
            #                                                     #
            # Write attribute definitions and source 1,2,3 to XML #
            #                                                     #
            #######################################################

            # definition 1
            attrdef1 = etree.Element("attrdef1")
            attrdef1.text = a.defn1

            # definition source 1
            attrdefs1 = etree.Element("attrdefs1")
            attrdefs1.text = a.dsrc1

            # definition 2
            attrdef2 = etree.Element("attrdef2")
            attrdef2.text = a.defn2

            # definition source 2
            attrdefs2 = etree.Element("attrdefs2")
            attrdefs2.text = a.dsrc2

            # definition 3
            attrdef3 = etree.Element("attrdef3")
            attrdef3.text = a.defn3

            # definition source 3
            attrdefs3 = etree.Element("attrdefs3")
            attrdefs3.text = a.dsrc3

            # field type - enumberated, range, codeset or unrepresentable
            attrdomv = etree.Element("attrdomv")

            if a.field_type == ENUMERATED:
                edom = etree.Element("edom")
                edomv = etree.Element("edomv")
                edomvd = etree.Element("edomvd")
                edomvds = etree.Element("edomvds")

                edomv.text = a.en_unique_val
                edomvd.text = a.en_def
                edomvds.text = a.en_src

                edom.append(edomv)
                edom.append(edomvd)
                edom.append(edomvds)

                attrdomv.append(edom)

            if a.field_type == RANGE:
                rdom = etree.Element("rdom")

                # min
                rdommin = etree.Element("rdommin")
                rdommin.text = str(a.rmin)

                # max
                rdommax = etree.Element("rdommax")
                rdommax.text = str(a.rmax)

                rdom.append(rdommin)
                rdom.append(rdommax)
                attrdomv.append(rdom)

            if a.field_type == CODESET:
                codesetd = etree.Element("codesetd")

                # codeset name
                codesetn = etree.Element("codesetn")
                codesetn.text = a.cs_name

                # codeset source
                codesets = etree.Element("codesets")
                codesets.text = a.cs_src

                codesetd.append(codesetn)
                codesetd.append(codesets)
                attrdomv.append(codesetd)

            if a.field_type == UNREPRESENTABLE:
                udom = etree.Element("udom")
                udom.text = a.ur_desc
                attrdomv.append(udom)

            attr.append(attrlabl)

            attr.append(attrdef1)
            attr.append(attrdef2)
            attr.append(attrdef3)

            attr.append(attrdefs1)
            attr.append(attrdefs2)
            attr.append(attrdefs3)

            attr.append(attrdomv)
            detailed.append(attr)
        return detailed

    def create_status_element(self, di):
        status = etree.Element('status')
        progress = etree.Element('progress')
        progress.text = di.progress

        update = etree.Element('update')
        update.text = di.update

        status.append(progress)
        status.append(update)

        return status

    def create_accconst_element(self, di):
        accconst = etree.Element('accconst')
        accconst.text = di.accconst

        return accconst

    def create_useconst_element(self, di):
        useconst = etree.Element('useconst')
        useconst.text = di.useconst

        return useconst

    def save(self, attrs, des, cit):
        """
        function reads the data from GUI elements and
        save/updates the xml

        param ui: reference to Qt MainWindow from app.py
        """

        root = self.tree.getroot()
        new_root = etree.Element(root.tag)
        metadata = root

        for child in root:
            if child.tag == "eainfo":
                continue
            else:
                eainfo = etree.Element('eainfo')
                eainfo.append(self.create_detailed_element(attrs))
                eainfo.append(self.create_overview_element(des, cit))
                new_root.append(eainfo)

            new_root.append(child)

        output_xml = etree.tostring(new_root, pretty_print=True)
        print("[XmlWriter] Input XML:-\n", output_xml)

        # writing to input xml file
        f = open(self.filepath, "w")
        f.write(output_xml)
        f.close()


##############################################################################
#                                                                            #
#                                 MAIN                                       #
#                                                                            #
##############################################################################
if __name__ == '__main__':
    #some quick tests
    writer = XmlWriter("./test.xml")

    writer.save({})
