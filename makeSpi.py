import json
data = {
    "sort" : "1",
    "account" : "1",
    "codes" : [ "1","1","1","1"],
    "mem_day" : "1",
    "mem_month" : "1",
    "mem_year" : "1",
    "first_school" : "1",
    "last_school" : "1",
    "memorable_name" : "1",
    "place_of_birth" : "1",
    }
print json.dumps(data)
