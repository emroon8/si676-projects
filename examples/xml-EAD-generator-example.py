import xml.etree.ElementTree as ET
try:
    from lxml import etree
except:
    print('lxml not working')

print('''\n
This demonstrates generation of a valid XML document to
create an EAD-encoded finding aid for the "Superior Papers".
A sample challenge would be to add in prompts for the user
to add certain elements, such as the title, publisher, notes, etc.
And to create a more dynamic, program-enabled creation of a dynamic EAD doc.
An additional challenge would be to add a schema declaration in a processing instruction,
per XML protocols https://www.w3.org/TR/xml-model/xml-model.xml\n''')

#============= set up input/output files
fout = input('Enter a file name for output (suggest "superior-papers-auto-generated.xml"): ') 

#============= set up namespaces
EAD3_ns = 'http://ead3.archivists.org/schema/'
DC_ns = 'http://purl.org/dc/elements/1.1/'
DCTERMS_ns = 'http://purl.org/dc/terms/'
XSI_ns = 'http://www.w3.org/2001/XMLSchema-instance'
XHTML_ns = ''

ns = {
    'ead' : EAD3_ns,
    'dc'  : DC_ns,
    'dcterms': DCTERMS_ns,
    'xsi' : XSI_ns
}

# helper to add namespace delcarations with subelement tags, 
# this helps with use of the QName function in lxml
def ead(tag):
    '''
    This function takes a string representing an EAD tag name and adds the qualifying namespace
    '''
    return etree.QName(EAD3_ns, tag)

#============= Get the data 
# IDEA: modify this script to ask for input

#============= Create the XML tree and elements
# this demo uses the lxml E factory to create the tree and subelements

# IDEA: create functions to generate separate sections/elements, 
# e.g., def buildControl(recordID, instanceURL):
# etc... 

# set a root element, use .QName to set namespace
rootName = etree.QName(EAD3_ns, 'ead')
root = etree.Element(rootName, nsmap=ns)
# TODO: add in the XSD as a processing instruction
#root.append(etree.ProcessingInstruction('xml-model', 'href="https://loc.gov/ead/ead3_undeprecated.dtd" type="application/xml-dtd"'))
# assign root element to an Element Tree object
finding_aid = etree.ElementTree(root)

# create subelements
control = etree.SubElement(root, ead('control'), attrib = {'countryencoding':'iso3166-1','dateencoding':'iso8601','langencoding':'iso639-2b'}, nsmap=ns)
archdesc = etree.SubElement(root, ead('archdesc'), attrib = {'level':'collection','audience':'external'}, nsmap=ns)

# build CONTROL element
# recordID
recordID = etree.SubElement(control, ead('recordid'), attrib = {'instanceurl':'http://jajohnst.si.umich.edu/fake-ead.xml'}, nsmap=ns)
recordID.text = '1234'

# filedesc
filedesc = etree.SubElement(control, ead('filedesc'))

titlestmt = etree.SubElement(filedesc, ead('titlestmt'))
titleproper = etree.SubElement(titlestmt, ead('titleproper'))
titleproper.text = 'A Finding Aid for the Superior Papers'

publicationstmt = etree.SubElement(filedesc, ead('publicationstmt'))
publisher = etree.SubElement(publicationstmt, ead('publisher'))
publisher.text = 'University of Michigan School of Information'
date = etree.SubElement(publicationstmt, ead('date'), attrib={'normal':'2022-09-01'})
date.text = 'September 2022'

# maintenancestatus (required)
maintenancestatus = etree.SubElement(control, ead('maintenancestatus'), attrib={'value':'new'})

# build ARCHDESC element
# top-level digital ID element for identifying information about collection
did1 = etree.SubElement(archdesc, ead('did'))
repository = etree.SubElement(did1, ead('repository'))
corpname = etree.SubElement(repository, ead('corpname'))
part1 = etree.SubElement(corpname, ead('part'))
part1.text = 'University of Michigan'
part2 = etree.SubElement(corpname, ead('part'))
part2.text = 'School of Information'

# comment about all the stuff that's missing
did1.append(etree.Comment('somewhere around here would be additional information like scope, bioghist, and contents lists'))

# bioghist
bioghist = etree.SubElement(archdesc, ead('bioghist'))
bioghist.text = 'This collection is a superior collection of papers for a superior organization and individual.'

# dsc - description of subordinate contents, ie, contents list
dsc1 = etree.SubElement(archdesc, ead('dsc'), attrib={'dsctype':'otherdsctype', 'audience':'external'})
c01 = etree.SubElement(dsc1, ead('c01'), attrib={'level':'series'})
c01.text = 'Business Records'
c02 = etree.SubElement(dsc1, ead('c02'), attrib={'level':'series'})
c02.text = 'Correspondence'
c03 = etree.SubElement(dsc1, ead('c03'), attrib={'level':'file', 'audience':'internal'})
c03.text = 'Personal File'

#============= Write the XML - this uses lxml and pretty print to make a more readable output
finding_aid.write(fout, xml_declaration=True, encoding='utf-8', method='xml', pretty_print=True)