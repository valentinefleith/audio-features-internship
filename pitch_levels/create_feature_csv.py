import pandas as pd
import glob
import os


def add_line(feature_csv, profile_path):
    """
    Adds a new line of data from a TSV file to the feature_csv DataFrame and appends an ID column.

    Parameters:
    - feature_csv (pd.DataFrame): The DataFrame to which the new line will be added.
    - profile_path (str): The file path of the TSV file to be read.

    Returns:
    - pd.DataFrame: The updated DataFrame with the new line and ID column appended.
    """
    profile_id = os.path.basename(profile_path).replace(".txt", "").split("_")[0]
    profile_data = pd.read_csv(profile_path, sep="\t")
    profile_data["ID"] = profile_id
    return pd.concat([feature_csv, profile_data], ignore_index=True)


def main():
    """
    Main function that processes all TSV files in the 'prosodic_profiles' directory,
    concatenates them into a single DataFrame, adds an ID column, and saves the result as a CSV file.
    """
    profiles = glob.glob("prosodic_profiles/*.txt")
    feature_csv = pd.DataFrame()

    for profile in profiles:
        feature_csv = add_line(feature_csv, profile)

    feature_csv.set_index("ID", inplace=True)
    feature_csv.to_csv("combined_features.csv")
    print(feature_csv)


if __name__ == "__main__":
    """
    Entry point of the script. It calls the main function to execute the processing of TSV files.
    """
    main()
