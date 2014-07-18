#!/usr/bin/python
import json
import sys

spi_file = "spi.json"
data = {}
fields = [ "sort", "account", "codes" , "mem_day" , "mem_month" , "mem_year" , "first_school" , "last_school" , "memorable_name" , "place_of_birth" ]
for field in fields:
    print "%s:" % field
    data[field] = sys.stdin.readline().strip()

f = open(spi_file, 'w')
json.dump(data,f)
print "written spi data to %s, now do: chmod 400 %s" % (spi_file,spi_file)
