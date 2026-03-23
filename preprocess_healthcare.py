'''
preprocess_healthcare.py
  Author(s): Jasper Bungay (1384647), Lincoln Fiser (1385739), Harveen Harveen (1337280)

  Project: Team Project
  Date of Last Update: Mar 23, 2026.

  Functional Summary
        This code preprocesses a Statistics Canda healthcare CSV file by cleaning and extracting specific 
        data from the year of choice (2019). It handles inconsistent formatting by eliminating information 
        that won't be valuable to the program, and filtering out irrelavent values. 

     Commandline Parameters: 2
        argv[1] = preprocess_healthcare.py
        argv[2] = <input_healthcare_csv>

     References:
        * Statistics Canada - Access to A Regular Healthcare Provider.
           https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310009616&pickMembers%5B0%5D=1.7&pickMembe
           rs%5B1%5D=3.1&cubeTimeFrame.startYear=2019&cubeTimeFrame.endYear=2020&referencePeriods=20190101%2C
           20200101

'''
import sys
import csv

def main(argv):
   
    # CHECK COMMAND LINE ARGUMENTS
   
    # The program expects the healthcare CSV file
    # Validates Input, Ensures the user provided a filename when running the code
    if len(argv) < 2:
        print("Usage: python preprocess_healthcare.py <input_healthcare_csv>")
        sys.exit(1)

    healthcare_filename = argv[1]
    output_filename = "Databases/healthcare_2020_cleaned.csv"

    
    # OPEN INPUT FILE
   
    # utf-8-sig is used because StatCan CSV files
    # may contain a special character at the start
    try:
        infile = open(healthcare_filename, newline='', encoding="utf-8-sig")
    except IOError:
        print(f"Error: Could not open {healthcare_filename}")
        sys.exit(1)

    reader = csv.reader(infile)

    
    # CREATE OUTPUT FILE
   
    # The cleaned file will only keep the fields
    # needed for the merge step
    # Creates a new file to save only the data we actually need
    try:
        outfile = open(output_filename, "w", newline='', encoding="utf-8")
    except IOError:
        print(f"Error: Could not create {output_filename}")
        infile.close()
        sys.exit(1)

    writer = csv.writer(outfile)
    writer.writerow(["REF_DATE", "GEO", "VALUE"]) # Define new, simple header

    count = 0              # number of rows written
    current_geo = ""       # keeps track of the current province

    
    # PROCESS EACH ROW
    
    # The healthcare file is not in normal column format.
    # It looks like:
    #
    # "Newfoundland and Labrador","Total, 12 years and over","Both sexes","Percent","2019","87.5"
    # ,,,,"2020","86.7"
    # ,,,,"2021","87.5"
    #
    # So:
    # - the province appears only on the first row
    # - the next rows reuse that province with blank cells
    for row in reader:
        # Skip empty or very short rows
        if len(row) < 6:
            continue

        first_col = row[0].strip()
        ref_date = row[4].strip()
        value = row[5].strip()

        # Stop when footnotes begin
        if first_col == "Footnotes:":
            break

        # Skip non-data header rows
        if first_col in [
            "",
            "Geography",
            "Indicators",
            "How to cite: Statistics Canada. Table 13-10-0096-01  Health characteristics, annual estimates, inactive"
        ]:
            pass
        else:
            # Update current province when a new one appears
            current_geo = first_col

        # Keep only 2020 rows with a province and a value
        if current_geo != "" and ref_date == "2020" and value != "":
            writer.writerow(["2020", current_geo, value])
            count += 1

   
    # CLOSE FILES
 
    infile.close()
    outfile.close()

    print(f"Success! Created {output_filename} with {count} rows.")



if __name__ == "__main__":
    main(sys.argv)
