#!/usr/bin/python
import xml.etree.ElementTree as ET
import sys
from collections import defaultdict
dict1={}
from prettytable import PrettyTable
x=PrettyTable()


parameters_to_print=['id','name','uuid','memory','vcpu','inter-type','inter-address','inter-dev','disk-dev','disk-serial']

x.field_names=parameters_to_print
#inputfile = ET.parse(sys.argv[1])
#root=inputfile.getroot()

def parsing_each_file(inputfilename):
    root=inputfilename.getroot()
    domainid=root.attrib['id']
    dict1.setdefault(domainid,{})['id']=domainid
    for value in ['name','uuid','memory','vcpu']:
        for child in root.iter(value):
            dict1[domainid][value]=child.text
    
    for interfacechild in root.findall('devices/interface'):
        for key,value in interfacechild.attrib.items():
            dict1[domainid]['inter-'+key]=value
        for eachparameter in interfacechild.getchildren():
            if eachparameter.attrib:
                for key,value in eachparameter.attrib.items():
                    dict1[domainid]['inter-'+key]=value
    
    for node in root.findall('devices/disk'):
        for key,value in node.attrib.items():
            dict1[domainid]['disk-'+key]=value
        for parameters in node.getchildren():
            if parameters.attrib:
                for key,value in parameters.attrib.items():
                    dict1[domainid]['disk-'+key]=value
            else:
                if parameters.text:
                    dict1[domainid]['disk-serial']=parameters.text
    for key,value in dict1.items():
        x.add_row([value.get(eachparameter) for eachparameter in parameters_to_print])
    print(dict1)

#x.field_names=parameters_to_print
#for key,value in dict1.items():
#    x.add_row([value.get(eachparameter) for eachparameter in parameters_to_print])
#print(x)

for eachinputfile in sys.argv[1:]:
    inputfilename1=ET.parse(eachinputfile)
    parsing_each_file(inputfilename1)
