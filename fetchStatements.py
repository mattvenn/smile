#!/usr/bin/python
import json
import re
import argparse
import mechanize
import ipdb
import csv
import os

from parseTable import TableParser

def store_body(body,file_name):
    if args.store:
        f = open("html/" + file_name,'w')
        f.write(body)
        f.close()

def new_statement(statement_number):
    return not os.path.exists(get_statement_path(statement_number))

def get_statement_path(statement_number):
    return "%s/%s/account%d/statement%s.csv" % (args.account_path, args.account_type, args.account_num,statement_number)

def parse_table(body,statement_number):
    if re.compile("logged out").search(body):
        print "problem fetching statement %s, logged out" % statement_number
        exit(1)
    if re.compile("the statement you requested isn't available online").search(body):
        print "problem fetching statement %s, too old!" % statement_number
        return

    #parse the table
    p = TableParser(args.account_type)
    p.feed(body) 
    data = p.data
    if args.verbose:
        print "parsed %d lines of data" % len(data)
    if len(data):
        #write to csv file
        with open(get_statement_path(statement_number), 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for line in data:
                writer.writerow(line)
        csvfile.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="login to smile and download statements")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--all', action='store_const', dest='all', const="True", help="download all statements")
    group.add_argument('--recent', action='store_const', dest='recent', const=True, help="download most recent")

    parser.add_argument('--store', action='store_const', dest='store', const='True', help="store all html files")
    parser.add_argument('--noverbose', action='store_const', const=False, dest='verbose', default=True, help="verbose")
    parser.add_argument('--spi-file', action='store', dest='spi_file', help="spi details", required = True)
    parser.add_argument('--account-path', action='store', dest='account_path', help="where to store statements", default = "/home/mattvenn/work/finances/accounts/")
    parser.add_argument('--account-type', action='store', dest='account_type', help="savings or current", default = "current")
    parser.add_argument('--account-num', action='store', type=int, dest='account_num', default=0, help="which account num")
    
    args = parser.parse_args()

    try:
        f = open(args.spi_file)
        spi = json.load(f)
    except:
        print "couldn't get spi details from", args.spi_file
        exit(1)

    br = mechanize.Browser()
    br.open("https://banking.smile.co.uk/SmileWeb/start.do")
    if args.verbose:
        print "got login form"
    br.select_form(name="loginForm")
    br["sortCode"] = spi["sort"]
    br["accountNumber"] = spi["account"]

    body = br.submit().read()
    store_body(body,"passcode.html")

    if args.verbose:
        print "doing pass code"

    count = 0
    first = True
    second = False

    br.select_form(name="passCodeForm")
    if br.form.controls[1].name != "firstPassCodeDigit":
        print "can't find the select for 1st"
        exit(1)
    if br.form.controls[2].name != "secondPassCodeDigit":
        print "can't find the select for 2nd"
        exit(1)

    for number in ["first", "second", "third", "fourth" ]:
        regex = re.compile("%s digit" % number)
        if regex.search(body):
            if first:
                br.form["firstPassCodeDigit"] = [spi["codes"][count]]
                if args.verbose:
                    print "asked for digit #%d" % count
                second = True
                first = False
            elif second:
                br.form["secondPassCodeDigit"] = [spi["codes"][count]]
                if args.verbose:
                    print "asked for digit #%d" % count
        count += 1
            
    body = br.submit().read()
    store_body(body,"spi.html")

    if args.verbose:
        print "spi"

    #this one is the memorable date, name etc
    br.select_form(name="loginSpiForm")

    if re.compile("memorable date").search(body):
        if args.verbose:
            print "memorable date"
        br.form["memorableDay"] = spi["mem_day"]
        br.form["memorableMonth"] = spi["mem_month"]
        br.form["memorableYear"] = spi["mem_year"]
    elif re.compile("place of birth").search(body):
        if args.verbose:
            print "place of birth"
        br.form["birthPlace"] = spi["place_of_birth"]
    elif re.compile("lastschool").search(body):
        if args.verbose:
            print "last school"
        br.form["lastSchool"] = spi["last_school"]
    elif re.compile("firstschool").search(body):
        if args.verbose:
            print "first school"
        br.form["firstSchool"] = spi["first_school"]
    elif re.compile("memorable name").search(body):
        if args.verbose:
            print "memorable name"
        br.form["memorableName"] = spi["memorable_name"]
    else:
        print "don't know this SPI"
        ipdb.set_trace()
        exit(1)

    body = br.submit().read()

    #there may be a message we have to read
    for form in br.forms():
        if form.name == 'linearButtonNavigationForm':
            if args.verbose:
                print "message to read"
            br.select_form(name="linearButtonNavigationForm")
            body = br.submit().read()
    """
    if re.compile("important|making some changes|new online banking|contact details",re.IGNORECASE).search(body):
        if args.verbose:
            print "message to read"
        store_body(body,"message.html")
        br.select_form(name="linearButtonNavigationForm")
        body = br.submit().read()
    """

    #now should be logged in
    if not re.compile("your account was last accessed").search(body):
        print "don't seem to be logged in"
        exit(1)

    store_body(body,"accounts.html")
    if args.verbose:
        print "logged in"

    if args.verbose:
        print "fetching details for account #%d" % args.account_num

    #main current account
    if args.account_type == 'current':
        regex = r"current account"
    elif args.account_type == 'savings':
        regex = r"savings account"
    else:
        print "unknown account type ", args.account_type
        exit(1)

    body = br.follow_link(text_regex=regex, nr=args.account_num).read()
    store_body(body,"accountpage.html")

    #previous statements
    body = br.follow_link(text='previous statements[IMG]').read()
    store_body(body,"previousStatements.html")

    #get all statements
    available_statements = list(br.links(text_regex=r"^\d+$"))
    num_available_statements = len(available_statements)

    if args.all:
        for statement_num in range(num_available_statements):
            #get new list of all the links every request
            link = list(br.links(text_regex=r"^\d+$"))[statement_num]
            statement_number = link.text

            if args.verbose:
                print "retrieving statement %s of %d available statements" % (statement_number, num_available_statements)

            body = br.follow_link(link).read()
            parse_table(body,statement_number)

            #have to go back to the index page to get new page urls
            br.follow_link(text="previous statements[IMG]")

    elif args.recent:
        #get most recent of previous statement
        statement_link = available_statements[0]
        statement_number = statement_link.text

        #check if we need to download it
        if new_statement(statement_number):
            if args.verbose:
                print "retrieving statement %s of %d available statements" % (statement_number, num_available_statements)
            body = br.follow_link(statement_link).read()
            store_body(body,"mostrecentStatement")
            parse_table(body,statement_number)
        else:
            if args.verbose:
                print "no new statements"

    #logout
    finish = br.follow_link(text_regex=r"log off", nr=0).read()
    store_body(finish,"logout.html")
    if args.verbose:
        print "logged out"

