"""
This script generates descriptive statistic tables in LaTeX format for CSV files containing data, with each file representing different aggregation methods. It is designed to be run from the command line, taking a directory path containing the CSV files as input. Dirname must be "full", "beginning", "middle" or "end", and each csv file should represent one aggregation method.
This script reads csv, computes descriptive statistics and print it. It offers the possibily to save those statistics in a latex file (commented in the script).

Usage example:
    python3 src/statistic_tables.py new_csvfiles/full

"""

import argparse
import pandas as pd
import glob


def create_statistic_table(filename, method, part):
    df = pd.read_csv(filename, sep=";")
    print(f"Stats for method : {method}")
    stats = df.describe()
    print(stats, "\n")
    # UNCOMMENT TO SAVE LATEX FILE
    # table = stats.style.to_latex().replace("%", "\%")
    # with open(f"tables/{part}/{part[:3].upper()}_{method}.tex", "w") as f:
    #     f.write(table)


def main(directory):
    filenames = glob.glob(f"{directory}/*.csv")
    methods = [file.split("/")[-1].split(".")[0].split("_")[-1] for file in filenames]
    part = directory.split("/")[-1]
    for i, method in enumerate(methods):
        create_statistic_table(filenames[i], method, part)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory", help="directory containing csv files with every aggregation method"
    )
    args = parser.parse_args()
    main(args.directory)
