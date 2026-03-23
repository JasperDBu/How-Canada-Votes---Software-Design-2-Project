#!/usr/bin/env python

'''
NHPI_by_voting_results.py
  Author(s): Jasper Bungay (1384647), Lincoln Fiser (1385739), Harveen Harveen (1337280)

  Project: Team Project
  Date of Last Update: Mar 22, 2026.

  Functional Summary
        This code parses two data files into usable data to answer if housing price affects the voting results of the 
        45th General Election. We use the NHPI data table and the voting results by electorial districts to complete this question.
        The data will be parsed into region obects that will hold onto some information that we will be using. For instance, total seats each region has,
        how many seats each party recieved. Finally, the code creates a grouped bar chart to visualize our data and will help us confirm
        any patterns showing.

     Commandline Parameters: 3
        argv[1] = string column identity
        argv[2] = string to match
        argv[3] = name of the input csv file

     References:
        * Statistics Canada (2025): "Job vacancies, payroll
            employees, job vacancy rate, and average offered
            hourly wage by industry sub-sector, quarterly,
            unadjusted for seasonality", Table: 14-10-0442-01,
            https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410044201
        * Government of Canada (2025): "44th General Election:
            Official Voting Results", Record ID:
            065439a9-c194-4259-9c95-245a852be4a1
            https://open.canada.ca/data/en/dataset/065439a9-c194-4259-9c95-245a852be4a1
'''


#
#   Packages and modules
#

# The 'sys' module gives us access to system tools, including the
# command line parameters, as well as standard input, output and error
import sys

# The 'csv' module gives us access to a tool that will read CSV
# (Comma Separated Value) files and provide us access to each of
# the fields on each line in turn
import csv

import matplotlib.pyplot as plt

import pandas as pd


# Class definition for regions, this is where all the collected values will be kept. 
class region:
    def __init__(self, name):
        self.name = name
        self.total_seats = 0
        self.NHPI_percent = 0
        self.party_seats = {
                "Liberal" : 0,
                "Conservative" : 0,
                "Bloc Q" : 0,
                "New Democratic" : 0,
                "Green" : 0
            }
    


##
## Mainline function
##
def main(argv):
    #
    #   Check that we have been given the right number of parameters,
    #   and store the single command line argument in a variable with
    #   a better name
    #
    if len(argv) != 5:
        print("Usage: NHPI_by_voting_results.py <Housing price index method to filter> <Year period to filter> <input csv file name for voting data set> <input csv file name for housing price index data set>")
        sys.exit(1)

    # Puts all strings to search to lower for case-insensitive search
    try:
        NHPI_method_to_match = argv[1].lower()
    except ValueError as err:
        print(f"Error: column index '{argv[1]}' is not a string",
                file=sys.stderr)
        sys.exit(1)

    try:
        year_period = int(argv[2])
        if year_period > 3:
            print(f"Error: year period is out of range '{argv[2]}' range is 1 - 3")
    except ValueError as err:
        print(f"Error: year period '{argv[2]}' is not an int",
                file=sys.stderr)
        sys.exit(1)    

    
    voting_filename = argv[3]
    NHPI_filename = argv [4]


    regions = [
        region("Ontario"),
        region("Quebec"),
        region("British Columbia"),
        region("Prarie Region"),
        region("Atlantic Region")
        ]


    region_dict = {
        "ontario" : ["ontario"],
        "quebec" : ["quebec"],
        "british columbia" : ["british columbia"],
        "prarie region" : ["manitoba", "saskaatchewan", "alberta"],
        "atlantic region" : ["newfoundland and labrador", "prince edward island", "nova scotia", "newbrunswick"]
        }


    NHPI_parsing( NHPI_filename, year_period, NHPI_method_to_match, regions)

    vote_parsing( voting_filename, regions, region_dict )


    for geo_region in regions:
        number_to_percent(geo_region)
        print(f"Percent calulated for {geo_region.name} is {geo_region.NHPI_percent}")
        print(f"Total Seats: {geo_region.total_seats}")
        print(f"Liberals: {geo_region.party_seats["Liberal"]}")
        print(f"CPC: {geo_region.party_seats["Conservative"]}")
        print(f"BQ: {geo_region.party_seats["Bloc Q"]}")
        print(f"NDP: {geo_region.party_seats["New Democratic"]}")
        print(f"GP: {geo_region.party_seats["Green"]}")

    visualization(regions, year_period, NHPI_method_to_match)


def NHPI_parsing(filename, year_period, NHPI_method_to_match, regions):

    infile = open_csv_file(filename)

    # Using csv.reader to read the csv file and seperate it into rows
    reader = csv.reader(infile)

    #variables for csv markers
    header = None
    line_number = 0

    #Constants for target year period start date and end date
    END_DATE = "2025-04"
    START_DATE =f"{ 2025 - year_period }-04"

    #
    for row in reader:

        line_number += 1

        # if the header value is not yet set, process the header
        # information
        if header is None:

            header = row

            NHPI = header_column_search_index(header, "New Housing Price Indexes")
            REF_DATE = header_column_search_index(header, "Ref_date")
            VALUE = header_column_search_index(header, "Value")
            GEO = header_column_search_index(header, "Geo")

        else:
            # here we process the data rows

            # make sure that the row is long enough
            if len(row) != len(header):
                print(f"Error: invalid row on line {line_number}",
                        file=sys.stderr)
                sys.exit(1)

            # Obtain the value from 'New House Price Index' field
            nhpi_data = retrieve_data(row, NHPI)
                
            if NHPI_method_to_match in nhpi_data:

                ref_date_data = retrieve_data(row, REF_DATE)

                try:
                    value_data = float(retrieve_data(row, VALUE))
                except ValueError as err:
                    print(f"Error: {row[VALUE]} is not a number : {err}",
                            file=sys.stderr)
                    sys.exit(1)

                if START_DATE in ref_date_data:

                    start = value_data

                elif END_DATE in ref_date_data: 

                    end = value_data

                    geo_data = retrieve_data(row, GEO)
                    
                    for geo_region in regions:
                        if geo_data in geo_region.name.lower():
                            geo_region.NHPI_percent = round(end - start, 1)
                            break
                
    # close the input file
    infile.close()


def vote_parsing(filename, regions, region_dict):

    infile = open_csv_file(filename)

    header = None
    line_number = 0

    reader = csv.reader(infile)

    for row in reader:

        if header is None:

            header = row

            PROVINCE = header_column_search_index(header, "Province")
            ELECTED = header_column_search_index(header, "Elected Candidate")

        else:

            # make sure that the row is long enough
            if len(row) != len(header):
                print(f"Error: invalid row on line {line_number}",
                        file=sys.stderr)
                sys.exit(1) 

            region_data = find_key_by_value(region_dict, retrieve_data(row, PROVINCE))

            if region_data != None:
                for geo_region in regions:
                    if region_data in geo_region.name.lower():
                        seat_data = retrieve_data(row, ELECTED)
                        increment_if_match(geo_region, seat_data)

    infile.close()


def visualization(regions, year_period, NHPI_method):

    df = build_dataframe(regions)

    plot_cols = ["NHPI", "LIB", "CPC", "BQ", "NDP", "GP"]

    df.plot(x="Region",
            y=plot_cols,
            kind="bar",
            stacked=False,
            title=f'Regional Housing Price Change, {year_period}, {NHPI_method}, and Party Seat Percentage in the 45th Election'
            )
    
    plt.ylabel("Percentage (%)")

    plt.tight_layout()
    plt.show()


##
##  open_csv_file:
##  This function takes a file name and opens a csv file and returns the opened file. This function also has error checks.
##
def open_csv_file(filename):
    #
    # Open the input file.  The encoding argument
    # indicates that we want to handle the BOM (if present)
    # by simply ignoring it.
    #
    # The "newline=''" argument ensures correct handling of
    # the input data if the values within quoted strings of
    # the CSV format themselves contain newlines.  Please
    # see footnote 1 on the Python.org `csv` library documentation:
    #    https://docs.python.org/3/library/csv.html#id4
    #
    try:
        infile = open(filename, newline='', encoding="utf-8-sig")

    except IOError as err:
        # Here we are using the python format() function.
        # The arguments passed to format() are placed into
        # the string it is called on in the order in which
        # they are given.
        print("Unable to open csv file '{}' : {}".format(
                filename, err), file=sys.stderr)
        sys.exit(1)

    return infile


##
##  header_column_search_index: 
##  This function takes a header row and the target field. It finds the column index of the target field using 
##  the header row to match a case-insensitive check   
##
def header_column_search_index( header, target):

    column_number = 0
    target = target.lower()
    
    for column in header:
        try:
            if target in column.lower():
                return column_number
            else:
                column_number += 1
        except ValueError as err:
            print(f"Error: string to match '{column}' is not a string : {err}",
                file=sys.stderr)
            sys.exit(1)
    
    print(f"Error: could not find '{target}' column in header row", file=sys.stderr)
    sys.exit(1)
    
        

def retrieve_data(row, index):
    try:
        data = row[index].lower()
    except ValueError as err:
        print(f"Error: row data '{row[index]}' is not a string : {err}",
                file=sys.stderr)
        sys.exit(1)
    return data




def find_key_by_value(dict, target):
    target = target.lower()
    for key, values in dict.items():
        for items in values:
            if items in target:
                return key
    return None


def increment_if_match(geo_region, target):
    for key in geo_region.party_seats:
        if key.lower() in target:
            geo_region.party_seats[key] += 1
            geo_region.total_seats += 1
            return
    print(f"Error: could not find '{target}' in region.party_seats. ")


def number_to_percent(geo_region):
    for key in geo_region.party_seats:
        geo_region.party_seats[key] = round(( geo_region.party_seats[key] / geo_region.total_seats ) * 100, 1) 

    #  class region:
        # def __init__(self, name):
        #     self.name = name
        #     self.total_seats = 0
        #     self.NHPI_percent = 0
        #     self.party_seats = {
        #             "Liberal" : 0,
        #             "Conservative" : 0,
        #             "Bloc Q" : 0,
        #             "New Democratic" : 0,
        #             "Green" : 0
        #         }

def build_dataframe(regions):
    rows = []
    for r in regions:
        row = {
            "Region": r.name,
            "NHPI": r.NHPI_percent,
            "LIB": r.party_seats["Liberal"],
            "CPC": r.party_seats["Conservative"],
            "BQ": r.party_seats["Bloc Q"],
            "NDP": r.party_seats["New Democratic"],
            "GP": r.party_seats["Green"]
        }
        rows.append(row)

    return pd.DataFrame(rows, columns=['Region', 'NHPI', 'LIB', 'CPC', 'BQ', 'NDP', 'GP'])






    
        
    


##
## Call our main function, passing the system argv as the parameter
##
if __name__ == "__main__": main(sys.argv)


#
#   End of Script
#
