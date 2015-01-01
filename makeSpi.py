#!/usr/bin/python
import json
import sys

spi_file = "spi.json"
data = {}
fields = [ ("sort","6 digit sort code (no spaces or hyphens)"), ("account","8 digit account number"), ("codes","your online pin number") , ("mem_day","2 digit day of month of your memorable date") , ("mem_month","2 digit month of year of your memorable date") , ("mem_year","4 digit year of your memorable date") , ("first_school","first school") , ("last_school","last school") , ("memorable_name","memorable name") , ("place_of_birth","place of birth") ]
for field in fields:
    print "%s:" % field[1]
    data[field[0]] = sys.stdin.readline().strip()

f = open(spi_file, 'w')
json.dump(data,f)
print "written spi data to %s, now do: chmod 400 %s" % (spi_file,spi_file)
