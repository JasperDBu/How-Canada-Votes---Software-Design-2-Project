#!/usr/bin/env python


#   NHPI_by_voting_results.py
#   Author(s): Jasper Bungay (1384647), Lincoln Fiser (1385739), Harveen Harveen (1337280)

#   Project: Team Project
#   Date of Last Update: Mar 22, 2026.

#   Functional Summary
#         This code parses two data files into usable data to answer if housing price affects the voting results of the 
#         45th General Election. We use the NHPI data table and the voting results by electorial districts to complete this question.
#         The data will be parsed into region obects that will hold onto some information that we will be using. For instance, total seats each region has,
#         how many seats each party recieved. Finally, the code creates a grouped bar chart to visualize our data and will help us confirm
#         any patterns showing.

#      Commandline Parameters: 4
#         argv[1] = NHPI method column identity
#         argv[2] = integer year period
#         argv[3] = name of the voting input csv file
#         argv[4] = name of the NHPI input csv file

#      Commandline Example: 
#         Windows:
#             python .\NHPI_by_voting_results.py house 1 .\Databases\45th_election_voting_results.csv .\Databases\New_Housing_Price_Index.csv
#         MacOS:
#             python3 NHPI_by_voting_results.py house 1 Databases/45th_election_voting_results.csv Databases/New_Housing_Price_Index.csv

#      References:
#         * Statistics Canada – New Housing Price Index, monthly, by geographical region
#           https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810020501&pickMembers%5B0%5D=1.1&cubeTimeFrame.startMonth=01&cubeTimeFrame.startYear=2025&cubeTimeFrame.endMonth=01&cubeTimeFrame.endYear=2026&referencePeriods=20250101%2C20260101

#         * Elections Canada – Voting results by electoral district for the 45th General Election
#           https://www.elections.ca/content.aspx?section=res&dir=rep/off/45gedata&document=summary&lang=e



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

# The 'plt' module gives us access to tools that allow us to create graphs
import matplotlib.pyplot as plt

# The 'pd' module allows us to use data that is formatted in a table manner. This is usefull for
# creating a visualization.
import pandas as pd

# The 'np' module allows us work with matrices or in other words, data that have been formatted with pd.
import numpy as np


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
    #   a better name.
    #
    if len(argv) != 5:
        print("Usage: NHPI_by_voting_results.py <Housing price index method to filter> <Year period to filter> <input csv file name for voting data set> <input csv file name for housing price index data set>")
        sys.exit(1)

    # Puts all strings to search to lower for case-insensitive search.
    try:
        NHPI_method_to_match = argv[1].lower()
    except ValueError as err:
        print(f"Error: column index '{argv[1]}' is not a string",
                file=sys.stderr)
        sys.exit(1)

    # takes year period argument and checks if it is a valid input.
    try:
        year_period = int(argv[2])
        if year_period > 3:
            print(f"Error: year period is out of range '{argv[2]}' range is 1 - 3")
    except ValueError as err:
        print(f"Error: year period '{argv[2]}' is not an int",
                file=sys.stderr)
        sys.exit(1)    


    # creating variables for the file names.
    voting_filename = argv[3]
    NHPI_filename = argv [4]

    # creating an array of regions to keep all 5 different regions in the data base.
    regions = [
        region("Ontario"),
        region("Quebec"),
        region("British Columbia"),
        region("Prarie Region"),
        region("Atlantic Region")
        ]

    # creating a dictionary that allows us to key provinces to their geographical region.
    region_dict = {
        "ontario" : ["ontario"],
        "quebec" : ["quebec"],
        "british columbia" : ["british columbia"],
        "prarie region" : ["manitoba", "saskaatchewan", "alberta"],
        "atlantic region" : ["newfoundland and labrador", "prince edward island", "nova scotia", "newbrunswick"]
        }


    # This function parses the NHPI data base into our region objects.
    NHPI_parsing( NHPI_filename, year_period, NHPI_method_to_match, regions)

    # This function parses the voting results into our region objects.
    vote_parsing( voting_filename, regions, region_dict )

    # This loops through the array of region objects and transforms the data and prints out the contents of the data.
    for geo_region in regions:
        # This function turns the count of seats distributed to the parties into a percent based on the amount of seats distributed to each party.
        number_to_percent(geo_region)

        # prints out the contents of the region objects.
        print(f"Percent calulated for {geo_region.name} is {geo_region.NHPI_percent}")
        print(f"Liberals: {geo_region.party_seats["Liberal"]}%")
        print(f"CPC: {geo_region.party_seats["Conservative"]}%")
        print(f"BQ: {geo_region.party_seats["Bloc Q"]}%")
        print(f"NDP: {geo_region.party_seats["New Democratic"]}%")
        print(f"GP: {geo_region.party_seats["Green"]}%")

    # This function creates a grouped bar chart of the gathered and transformed data.
    visualization(regions, year_period, NHPI_method_to_match)


## NHPI_parsing: 
##   This function parses the data from the New Housing Price Index data table to the array of region objects.
## Parameter: 
##   filename: [string] this is the name of the NHPI data table
##   year_period: [int] this is the specified amount of years the user want to calculate
##   NHPI_method_to_match: [string] this is the specified NHPI method the user would like to filter out and calculate
##   regions: [array of regions (objects)] this is the array of region objects where we will keep the data parsed.
## Output: 
##   The data parsed will be kept inside the region objects. This function will calculate the NHPI value change from the start date and
##   end date of the year period.
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


## vote_parsing: 
##   This function parses the data from the New Housing Price Index data table to the array of region objects.
## Parameter: 
##   filename: [string] this is the name of the NHPI data table
##   NHPI_method_to_match: [string] this is the specified NHPI method the user would like to filter out and calculate
##   regions: [array of regions (objects)] this is the array of region objects where we will keep the data parsed.
## Output: 
##   The data parsed will be kept inside the region objects. This function will count amount of seats given to each party in each region

def vote_parsing(filename, regions, region_dict):

    # This will open the file
    infile = open_csv_file(filename)

    # this is to keep track of the header row
    header = None
    line_number = 0

    # uses csv.reader to split the csv data into an array
    reader = csv.reader(infile)

    for row in reader:

        if header is None:

            header = row

            # Finds the index of the given column fields
            PROVINCE = header_column_search_index(header, "Province")
            ELECTED = header_column_search_index(header, "Elected Candidate")

        else:

            # make sure that the row is long enough
            if len(row) != len(header):
                print(f"Error: invalid row on line {line_number}",
                        file=sys.stderr)
                sys.exit(1) 

            # This matches the province data to a region
            region_data = find_key_by_value(region_dict, retrieve_data(row, PROVINCE))

            # if the province was matched it will increment the total seats given in the region and increment the elected party
            if region_data != None:
                for geo_region in regions:
                    if region_data in geo_region.name.lower():
                        seat_data = retrieve_data(row, ELECTED)
                        increment_if_match(geo_region, seat_data)

    # This closes the file
    infile.close()


## visualization:
##   This function will create a grouped bar chart to visualize the collected data
## Parameters:
##   regions: [array of regions(objects)] This is an array of region objects
##   year_period: [int] this is the specified amount of years the user want to calculate
##   NHPI_method: [string] this is the specified NHPI method the user would like to filter out and calculate
## Output:
##   This will create a new png file of the created graph. This file is called "NHPI_by_voting_results_visualization.png"
def visualization(regions, year_period, NHPI_method):

    # This function build the data frame that we will be using to plot our data
    df = build_dataframe(regions)

    # This names the columns of the group bar
    plot_cols = ["NHPI", "LIB", "CPC", "BQ", "NDP", "GP"]

    # This chooses the colours for the bars
    colors = {
        "NHPI": "brown",
        "LIB": "red",
        "CPC": "deepskyblue",
        "BQ": "blue",
        "NDP": "orangered",
        "GP": "green"
    }

    #This Creates a blank canvas for us to work in
    plt.figure(figsize=(12, 6))

    # This creates the amount of sections we have for regions in the x axis
    x = np.arange(len(df["Region"]))
    width = 0.12

    # Draw each bar group
    for i, col in enumerate(plot_cols):
        plt.bar(
            x + i * width,
            df[col],
            width=width,
            label=col,
            color=colors[col]
        )

    # Horizontal zero line
    plt.axhline(0, color="black", linewidth=1)

    # Light gridlines
    plt.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.7)

    # Y-axis ticks every 5
    ymin = df[plot_cols].min().min()
    ymax = df[plot_cols].max().max()
    plt.yticks(np.arange(np.floor(ymin/5)*5, np.ceil(ymax/5)*5 + 1, 5))

    # X axis labels centered under groups
    plt.xticks(
        x + width * (len(plot_cols)-1) / 2,
        df["Region"],
        rotation=0
    )

    # This creates the labels and title
    plt.ylabel("Percentage (%)")
    plt.title(
        f"Regional Housing Price Change, {year_period} year period, {NHPI_method} pricing, and Party Seat Percentage in the 45th Election"
        )
    plt.legend()
    plt.tight_layout()

    # This saves the graph as a  PNG
    plt.savefig("NHPI_by_voting_results_visualization.png", dpi=300)
    plt.close()



##
## open_csv_file:
##    This function takes a file name and opens a csv file and returns the opened file. This function also has error checks.
## Parameter:
##   filename: [string] name of a file
def open_csv_file(filename):
    
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
## header_column_search_index: 
##   This function takes a header row and the target field. It finds the column index of the target field using 
##   the header row to match a case-insensitive check
## Parameter:
##   header: [row from csv.reader] this is usually the header row
##   target: [string] this is the name of the target column field
## output:
##   This function outputs the index number of the target column field
def header_column_search_index( header, target):

    column_number = 0

    # This is used for case-insensitive checks
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
    

## retrieve_data:
##   This function gets the data from the target column field in the given row.
## Parameter:
##   row: [row from csv.reader] 
##   index: [int] this is the index of the target column field
## Output:
##   This returns the data retrieved from the target column field
def retrieve_data(row, index):
    try:
        # This checks if the data is valid.
        data = row[index].lower()
    except ValueError as err:
        print(f"Error: row data '{row[index]}' is not a string : {err}",
                file=sys.stderr)
        sys.exit(1)
    return data


## find_key_by_value:
##   This function searches through the values of the dictionary. If the target matches any values it will give back the key that contains the value.
## parameters:
##   dict: [dictionary] this is usually the dictonary of regions to provinces
##   target: [string] This is the target value that we want to match with the dictionary
## Output:
##   This function outputs the key where the target matches the value. If there is no match it will return None
def find_key_by_value(dict, target):
    # This turns the match to case-insensitive
    target = target.lower()
    # checks through the values of the keys 
    for key, values in dict.items():
        for items in values:
            if items in target:
                return key
    return None


## increment_if_match:
##   This function will increment the value of a key when the target matches the key.
## parameters:
##   geo_region: [object] this is a region object
##   target: [string] this is the target used to match
## output:
##   This code will output nothing but it will increment the value of a key.
def increment_if_match(geo_region, target):
    for key in geo_region.party_seats:
        if key.lower() in target.lower():
            geo_region.party_seats[key] += 1
            geo_region.total_seats += 1
            return
    print(f"Error: could not find '{target}' in region.party_seats. ")
    sys.exit(1)


## number_to_percent:
##   This function will turn the party seat count to a percent using the total seats in the region
## parameters:
##   geo_region: [object] this is a region object
## Output:
##   this code will output nothing but it will change a value from a number to a percent.
def number_to_percent(geo_region):
    total = geo_region.total_seats
    for key in geo_region.party_seats:
        geo_region.party_seats[key] = round(( geo_region.party_seats[key] / geo_region.total_seats ) * 100, 1) 


## build_dataframe:
##   This code will turn the given array into a data frame that will be used for the visualization
## parameters:
##   regions: [array of objects] this is an array of region objects.
## Output:
##   This function will return the new dataframe
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
