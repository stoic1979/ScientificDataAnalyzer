

"""

 <attr>
                <attrlabl>sepal_leng</attrlabl>
                <attrdef>Att def</attrdef>
                <attrdefs>Producer defined</attrdefs>
                <attrdomv>
                    <rdom>
                        <rdommin>4.3</rdommin>
                        <rdommax>7.9</rdommax>
                    </rdom>
                </attrdomv>
            </attr>


"""


from lxml import etree

# create XML 
root = etree.Element('attr')

# Make a new document tree
doc = etree.ElementTree(root)

# another child with text
child = etree.Element('attrdef')
child.text = 'Producer defined'
root.append(child)
# another child with text
child = etree.Element('attrlabl')
child.text = '4.3'
root.append(child)

# another child with text
child = etree.Element('attrdef')
child.text = '4.3'
root.append(child)

# another child with text
child = etree.Element('attrdomv')
child.text = '4.7'
root.append(child)
 
# another child with text
child = etree.Element('rdommin')
child.text = '4.3'
root.append(child)

# another child with text
child = etree.Element('rdommax')
child.text = '7.9' 
root.append(child)

# pretty string
s = etree.tostring(root, pretty_print=True)
print (s)

# Save to XML file
outFile = open('output.xml', 'w')
doc.write(outFile, xml_declaration=True, encoding='utf-16') 
