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




##
## Mainline function
##
def main(argv):
    #
    #   Check that we have been given the right number of parameters,
    #   and store the single command line argument in a variable with
    #   a better name
    #
    if len(argv) != 4:
        print("Usage: extract_column.py <column to search> <string to search for> <input csv file name>")
        sys.exit(1)

    # Puts all strings to search to lower for case-insensitive search
    try:
        column_name_to_search = argv[1].lower()
    except ValueError as err:
        print(f"Error: column index '{argv[1]}' is not a string",
                file=sys.stderr)
        sys.exit(1)

    try:
        column_data_to_match = argv[2].lower()
    except ValueError as err:
        print(f"Error: string to match '{argv[1]}' is not a string",
                file=sys.stderr)
        sys.exit(1)    
    filename = argv[3]


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


    #
    # Create a CSV (Comma Separated Value) reader *writer* that will
    # output to standard output.  Using this writer to format our
    # output will ensure that the structure is correct and output
    # fields get quoted properly.
    writer = csv.writer(sys.stdout)


    header = None
    line_number = 0
    column_index_to_search = 0

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
                try:
                    if column_name_to_search in column.lower():
                        break
                    column_index_to_search += 1
                except ValueError as err:
                    print(f"Error: string to match '{argv[1]}' is not a string",
                        file=sys.stderr)
                    sys.exit(1) 
            
            header = row
            writer.writerow(header)

        else:
            # here we process the data rows

            # make sure that the row is long enough
            if len(row) < column_index_to_search:
                print(f"Error: requested field {column_index_to_search}",
                    f"from line {line_number} which",
                    f"only contains {len(row)} fields",
                        file=sys.stderr)
                sys.exit(1)

            # Obtain the value from the indicated field
            try:
                #Removes case-sensitive search
                row_data_to_check = row[column_index_to_search].lower()
            except ValueError as err:
                print(f"Error: row data '{argv[1]}' is not a string",
                        file=sys.stderr)
                sys.exit(1) 

            # The "in" keyword allows us to search for a substring
            # within another string
            if column_data_to_match in row_data_to_check:
                writer.writerow(row)

    # close the input file
    infile.close()


    #
    #   End of Function
    #

##
## Call our main function, passing the system argv as the parameter
##
if __name__ == "__main__": main(sys.argv)


#
#   End of Script
#
