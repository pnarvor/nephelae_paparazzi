#! /usr/bin/python3 

from defusedxml.ElementTree import parse as xml_parse

filepath = "/home/pnarvor/work/nephelae/soft/paparazzi/var/aircrafts/Flash/flight_plan.xml"

blocks = {}
with open(filepath, 'r') as fplanFile:
     xmlBlocks = xml_parse(fplanFile).getroot().find('flight_plan').find('blocks').getchildren()
     for b in xmlBlocks:
         blocks[int(b.get('no'))] = b.get('name')



