import sys
import csv

def standardize_name(name):
    
    # STANDARDIZE PROVINCE NAMES
    
    # This helps match names between both files
    name = str(name).strip()

    replacements = {
        "N.L.": "Newfoundland and Labrador",
        "P.E.I.": "Prince Edward Island",
        "B.C.": "British Columbia",
        "N.W.T.": "Northwest Territories",
        "PEI": "Prince Edward Island",
        "NFLD.": "Newfoundland and Labrador",
        "NWT": "Northwest Territories"
    }

    return replacements.get(name, name)


def load_healthcare(filename):
    
    # LOAD CLEANED HEALTHCARE DATA
   
    # Reads the cleaned file and stores it in a
    # dictionary like:
    # { "Ontario": "90.6", "Quebec": "78.5", ... }
    data = {}

    try:
        infile = open(filename, newline='', encoding="utf-8")
    except IOError:
        print(f"Error: Could not open {filename}")
        sys.exit(1)

    reader = csv.DictReader(infile)

    for row in reader:
        geo = standardize_name(row.get("GEO", ""))
        value = row.get("VALUE", "").strip()

        if geo != "" and value != "":
            data[geo] = value

    infile.close()
    return data


def main(argv):
    
    # CHECK COMMAND LINE ARGUMENTS
   
    # The program expects:
    # 1. cleaned healthcare CSV
    # 2. turnout CSV
    if len(argv) < 3:
        print("Usage: python merge_healthcare_turnout.py <healthcare_csv> <turnout_csv>")
        sys.exit(1)

    healthcare_file = argv[1]
    turnout_file = argv[2]
    output_file = "Databases/healthcare_turnout_merged.csv"

    # Load healthcare data first
    healthcare_data = load_healthcare(healthcare_file)

    
    # OPEN TURNOUT FILE
   
    try:
        turnout_in = open(turnout_file, newline='', encoding="utf-8-sig")
    except IOError:
        print(f"Error: Could not open {turnout_file}")
        sys.exit(1)

    try:
        merged_out = open(output_file, "w", newline='', encoding="utf-8")
    except IOError:
        print(f"Error: Could not create {output_file}")
        turnout_in.close()
        sys.exit(1)

    reader = csv.DictReader(turnout_in)

    # The turnout file has:
    # Province, Percentage of Voter Turnout 2019
    writer = csv.DictWriter(
        merged_out,
        fieldnames=["GEO", "HC_ACCESS_2019", "VOTER_TURNOUT_2019"]
    )
    writer.writeheader()

    count = 0

    
    # MERGE THE TWO FILES
    
    for row in reader:
        province = standardize_name(row.get("Province", ""))
        turnout = row.get("Percentage of Voter Turnout 2019", "").strip()

        # Only write rows where:
        # 1. province exists in healthcare data
        # 2. turnout value is not empty
        if province in healthcare_data and turnout != "":
            writer.writerow({
                "GEO": province,
                "HC_ACCESS_2019": healthcare_data[province],
                "VOTER_TURNOUT_2019": turnout
            })
            count += 1

    turnout_in.close()
    merged_out.close()

    print(f"Success! Created {output_file} with {count} rows.")



# RUN PROGRAM

if __name__ == "__main__":
    main(sys.argv)