#!/usr/bin/env python

import sys
import csv

def main(argv):
    # Requirement: Input healthcare CSV via command line
    if len(argv) < 2:
        print("Usage: python healthcare_by_voting.py <input_healthcare_csv>")
        sys.exit(1)

    healthcare_filename = argv[1]
    output_filename = "healthcare_2019_ontario_all_ages.csv"

    try:
        # 'utf-8-sig' is used to handle the encoding from StatCan files
        infile = open(healthcare_filename, newline='', encoding="utf-8-sig")
    except IOError as err:
        print(f"Error: Could not open {healthcare_filename}")
        sys.exit(1)

    reader = csv.DictReader(infile)
    
    try:
        outfile = open(output_filename, 'w', newline='', encoding="utf-8")
        # Creating exactly the three columns you requested
        fieldnames = ["REF_DATE", "GEO", "VALUE"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
    except IOError as err:
        print(f"Error: Could not create output file")
        sys.exit(1)

    count = 0
    for row in reader:
        # FILTERS:
        # 1. Only 2019 baseline
        # 2. Only Ontario
        # 3. Only Percentages (this ignores the 'Number of persons' rows)
        # 4. Only the specific healthcare access indicator
        if (row['REF_DATE'] == "2019" and 
            row['GEO'] == "Ontario" and 
            row['Characteristics'] == "Percent" and 
            row['Indicators'] == "Has a regular healthcare provider"):
            
            writer.writerow({
                "REF_DATE": row['REF_DATE'],
                "GEO": row['GEO'],
                "VALUE": row['VALUE']
            })
            count += 1

    infile.close()
    outfile.close()
    
    print(f"Success! Created {output_filename} with {count} rows.")

if __name__ == "__main__":
    main(sys.argv)