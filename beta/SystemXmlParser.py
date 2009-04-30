#import orbitSystem
#import random
#import dircache
#import random
#import math
#import sys
#import os
#import copy
import xml.parsers
from xml.parsers import expat
#import psyco
#psyco.full()
# Element and XML2Obj classes adapted from O'Rielly's 'Python Cookbook'
class Element(object):
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes
        self.cdata = ''
        self.children = []
    def addChild(self, element):
        self.children.append(element)
    def getAttribute(self, key):
        return self.attributes.get(key)
    def getData(self):
        return self.cdata
    def getElements(self, name=''):
        if name:
            return [c for c in self.children if c.name == name]
        else:
            return list(self.children)

class Xml2Obj(object):
    def __init__(self):
        ''' XML to Object converter '''
        self.root = None
        self.nodeStack = []
    def StartElement(self, name, attributes):
        'Expat start element event handler'
        element = Element(name.encode(), attributes)
        if self.nodeStack:
            parent = self.nodeStack[-1]
            parent.addChild(element)
        else:
            self.root = element
        self.nodeStack.append(element)
    def EndElement(self, name):
        'Expat character data event handler'
        self.nodeStack[-1].pop()
    def CharacterData(self, data):
        'Expat character data event handler'
        if data.strip():
            data = data.encode()
            element = self.nodeStack[-1]
            element.cdata += data            
    def  Parse(self, filename):
        Parser = expat.ParserCreate()
        Parser.StartElementHandler = self.StartElement
        #Parser.EndElementHandler = self.EndElement
        Parser.CharacterDataHandler = self.CharacterData
        ParserStatus = Parser.Parse(open(filename).read(), 1)
        return self.root
    
parser = Xml2Obj()
root_element = parser.Parse('extrasolar.xml')
##            
##class SystemXmlParser():
##    def __init__(self):
##        self.allSystems = []
##        self.xmlString = ""
##    def __init__(self, newXmlString):
##        self.allSystems = []
##        self.xmlString = newXmlString
##        
