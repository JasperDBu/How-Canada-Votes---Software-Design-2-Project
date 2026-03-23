'''
visualize_healthcare_turnout.py
  Author(s): Jasper Bungay (1384647), Lincoln Fiser (1385739), Harveen Harveen (1337280)

  Project: Team Project
  Date of Last Update: Mar 23, 2026.

  Functional Summary
        The purpose of this code is to take the merged data that has been gathered, and input it
        onto a visual graph using PYPLOT from matplot lib to generate a scatter plot so data can
        be compared and contrasted a solution can be reached to see effects on each province. 

     Commandline Parameters: 2
        argv[1] = visualize_healthcare_turnout.py 
        argv[2]: Databases/healthcare_turnout_merged.csv

     References:
        * Statistics Canada - Access to A Regular Healthcare Provider.
           https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310009616&pickMembers%5B0%5D=1.7&pickMembe
           rs%5B1%5D=3.1&cubeTimeFrame.startYear=2019&cubeTimeFrame.endYear=2020&referencePeriods=20190101%2C
           20200101

        * Election

'''


import sys
import csv
import matplotlib.pyplot as plt

def main(argv):
    
    # CHECK INPUT
    
    if len(argv) < 2:
        print("Usage: python visualize_healthcare_turnout.py <merged_csv>")
        sys.exit(1)

    input_file = argv[1]
    output_file = "Databases/healthcare_vs_turnout.png"

    regions = []
    healthcare_access = []
    voter_turnout = []

    
    # READ DATA
    
    try:
        infile = open(input_file, newline='', encoding="utf-8")
    except IOError:
        print(f"Error: Could not open {input_file}")
        sys.exit(1)

    reader = csv.DictReader(infile)

    for row in reader:
        regions.append(row["GEO"])
        healthcare_access.append(float(row["HC_ACCESS_2020"]))
        voter_turnout.append(float(row["VOTER_TURNOUT_2019"]))

    infile.close()

   
    # CREATE SCATTER PLOT
    
    plt.figure(figsize=(10, 6))
    plt.scatter(healthcare_access, voter_turnout)

    # Add labels (province names)
    for i in range(len(regions)):
        plt.text(
            healthcare_access[i] + 0.1,
            voter_turnout[i] + 0.1,
            regions[i],
            fontsize=8
        )

    plt.xlabel("Healthcare Access (%)")
    plt.ylabel("Voter Turnout (%)")
    plt.title("Healthcare Access vs Voter Turnout (2019-2020)")
    plt.grid(True)
    plt.tight_layout()

   
    # SAVE FILE 
    
    plt.savefig(output_file)

    print(f"Graph saved as {output_file}")


if __name__ == "__main__":
    main(sys.argv)
