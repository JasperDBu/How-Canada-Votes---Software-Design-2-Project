#!/usr/bin/env python

'''
extract_column_match_case_insensitive
  Author(s): Jasper Bungay (1384647), Lincoln Fiser (1385739), Harveen Harveen (1337280)

  Project: Data Extractor Script (Iteration 0)
  Date of Last Update: Feb 23, 2026.

  Functional Summary
        Extract rows from a .CSV file based on matching a case-insensitive string
        within a given column identified by index

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

class region:
    def __init__(self, name):
        self.name = name
    total_seats = 0
    NHPI_percent = 0
    Lib_seats = 0
    CPC_seats = 0
    BQ_seats = 0
    NDP_seats = 0
    GP_seats = 0


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
        region("ontario"),
        region("quebec"),
        region("british columbia"),
        region("prarie region"),
        region("atlantic region")
        ]

    

    region_dict = {
        "ontario" : "ontario",
        "quebec" : "quebec",
        "british columbia" : "british columbia",
        "prarie region" : ["manitoba", "saskaatchewan", "alberta"],
        "atlantic region" : ["newfoundland and labrador", "prince edward island", "nova scotia", "newbrunswick"]
        }

    NHPI_parsing( NHPI_filename, year_period, NHPI_method_to_match, regions)

    for geo_region in regions:
        print(f"Percent calulated for {geo_region.name} is {geo_region.NHPI_percent}")
    #
    #   End of Function
    #



def NHPI_parsing(filename, year_period, NHPI_method_to_match, regions):

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

    #
    # Create a CSV (Comma Separated Value) reader based on this
    # open file handle.  We can use the reader in a loop iteration
    # in order to access each line in turn.
    #
    reader = csv.reader(infile)


    header = None
    line_number = 0
    column_number = 0
    first_column_index_to_search = 0
    second_column_index_to_search = 0
    third_column_index_to_search = 0
    fourth_column_index_to_search = 0

    end_date = "2025-04"
    start_date =f"{ 2025 - year_period }-04"

    NHPI_first_search = "New Housing Price Indexes"
    NHPI_second_search = "REF_DATE"
    NHPI_third_search = "Value"
    NHPI_fourth_search = "Geo"


    #
    #   Parse each line of data from the CSV reader, which will break   
    #   the lines into fields based on the comma delimiter.
    #
    #   The field for each line are stored in a different row data array
    #   for each line of the data.
    #
    #   We then take the data and assign them into a "tuple" which we
    #   can store in the data array for later use
    #
    for row in reader:

        line_number += 1

        # if the header value is not yet set, process the header
        # information
        if header is None:

            # Goes through header row and finds the column_index_to_search by matching strings
            for column in row:
                if first_column_index_to_search != 0 and second_column_index_to_search != 0 and third_column_index_to_search and fourth_column_index_to_search != 0:
                    break

                try:
                    if NHPI_first_search.lower() in column.lower():
                        first_column_index_to_search = column_number
                except ValueError as err:
                    print(f"Error: string to match '{NHPI_first_search}' is not a string",
                        file=sys.stderr)
                    sys.exit(1)
                
                try:
                    if NHPI_second_search.lower() in column.lower():
                        second_column_index_to_search = column_number
                except ValueError as err:
                    print(f"Error: string to match '{NHPI_second_search}' is not a string",
                        file=sys.stderr)
                    sys.exit(1) 
                
                try:
                    if NHPI_third_search.lower() in column.lower():
                        third_column_index_to_search = column_number
                except ValueError as err:
                    print(f"Error: string to match '{NHPI_third_search}' is not a string",
                        file=sys.stderr)
                    sys.exit(1) 
                
                try:
                    if NHPI_fourth_search.lower() in column.lower():
                        fourth_column_index_to_search = column_number
                except ValueError as err:
                    print(f"Error: string to match '{NHPI_fourth_search}' is not a string",
                        file=sys.stderr)
                    sys.exit(1) 
                column_number += 1
            
            header = row


        else:
            # here we process the data rows

            # make sure that the row is long enough
            if len(row) <= first_column_index_to_search and len(row) <= second_column_index_to_search:
                print(f"Error: requested field {first_column_index_to_search} and {second_column_index_to_search}",
                    f"from line {line_number} which",
                    f"only contains {len(row)} fields",
                        file=sys.stderr)
                sys.exit(1)

            # Obtain the value from the indicated field
            try:
                #Removes case-sensitive search
                first_row_data_to_check = row[first_column_index_to_search].lower()
            except ValueError as err:
                print(f"Error: row data '{row[first_column_index_to_search]}' is not a string",
                        file=sys.stderr)
                sys.exit(1)
                
            try:
                second_row_data_to_check = row[second_column_index_to_search].lower()
            except ValueError as err:
                print(f"Error: row data '{row[second_column_index_to_search]}' is not a string",
                        file=sys.stderr)
                sys.exit(1)
            
            try:
                third_row_data_to_check = row[third_column_index_to_search].lower()
            except ValueError as err:
                print(f"Error: row data '{row[third_column_index_to_search]}' is not a string",
                        file=sys.stderr)
                sys.exit(1)
            
            try:
                fourth_row_data_to_check = row[fourth_column_index_to_search].lower()
            except ValueError as err:
                print(f"Error: row data '{row[fourth_column_index_to_search]}' is not a string",
                        file=sys.stderr)
                sys.exit(1)

            # The "in" keyword allows us to search for a substring
            # within another string
            if NHPI_method_to_match in first_row_data_to_check:
                if start_date in second_row_data_to_check:
                    try:
                        start = float(third_row_data_to_check)
                    except ValueError as err:
                        print(f"Error: string to int '{second_row_data_to_check}' is not a number",
                            file=sys.stderr)
                        sys.exit(1)
                elif end_date in second_row_data_to_check: 
                    try:
                        end = float(third_row_data_to_check)
                    except ValueError as err:
                        print(f"Error: string to int '{third_row_data_to_check}' is not a number",
                            file=sys.stderr)
                        sys.exit(1)    
                    for geo_region in regions:
                        if fourth_row_data_to_check in geo_region.name:
                            geo_region.NHPI_percent = round(end - start, 1)

                
    # close the input file
    infile.close()



##
## Call our main function, passing the system argv as the parameter
##
if __name__ == "__main__": main(sys.argv)


#
#   End of Script
#
