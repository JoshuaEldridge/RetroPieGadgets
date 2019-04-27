#!/usr/bin/python


from lxml import etree
infile = open("gamelist.xml", 'r')

context = etree.iterparse(infile, events=("start", "end"))
#context = etree.iterparse(infile, events=("start", "end"), tag="name")

for event, element in context:
    if event == "start":
        print element.tag, element.text
#        print 'Event:', event
#        print 'Element Tag:', element.tag
#        print 'Element Text:', element.text
#        print 'Element Items', element.items()
#    print 'Previous Element', element.getprevious()
#    print 'Parent Element', element.getparent()

infile.close()
