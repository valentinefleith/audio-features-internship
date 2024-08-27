"""
This module processes a dataset of word-level features, including pitch and LIWC categories, 
to analyze and visualize the relationship between these features and persuasiveness scores. 
The resulting visualization shows the average persuasiveness across different pitch and LIWC categories.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CSV_PATH = "merged_vectors.csv"


def filter_dataframe(df, dimension, liwc_columns, pitch_columns):
    """
    Filters the DataFrame to include only the relevant columns for analysis.

    Parameters:
        df (pd.DataFrame): The original DataFrame containing the data.
        dimension (str): The dimension to be analyzed (e.g., 'persuasiveness').
        liwc_columns (list): List of LIWC category column names.
        pitch_columns (list): List of pitch category column names.

    Returns:
        pd.DataFrame: A filtered DataFrame containing only the target columns.
    """
    # Select relevant columns: clip, word, dimension (e.g., 'persuasiveness'), and LIWC & pitch columns
    target_columns = ["clip", "word", f"{dimension}"]
    target_columns.extend(pitch_columns)
    target_columns.extend(liwc_columns)
    filtered_df = df[target_columns]
    return filtered_df


def reshape_data(filtered_df, liwc_columns, pitch_columns):
    """
    Reshapes the filtered DataFrame to prepare data for plotting.

    Parameters:
        filtered_df (pd.DataFrame): The DataFrame filtered to include only relevant columns.
        liwc_columns (list): List of LIWC category column names.
        pitch_columns (list): List of pitch category column names.

    Returns:
        pd.DataFrame: A DataFrame containing the reshaped data, grouped by pitch and LIWC categories, 
                      with average persuasiveness and count of occurrences.
    """
    plot_data = []
    for _, row in filtered_df.iterrows():
        word = row["word"]
        persuasiveness = row["persuasiveness"]
        # Check each pitch category for a match
        for pitch in pitch_columns:
            if row[pitch] == 1:  # If the word has this pitch category
                # Check each LIWC category for a match
                for liwc in liwc_columns:
                    if row[liwc] == 1:  # If the word belongs to this LIWC category
                        plot_data.append([pitch, liwc, persuasiveness])

    # Convert the list into a DataFrame
    plot_df = pd.DataFrame(plot_data, columns=["Pitch", "LIWC", "Persuasiveness"])

    # Group by Pitch and LIWC to calculate the average persuasiveness and count occurrences
    grouped_df = plot_df.groupby(["Pitch", "LIWC"], as_index=False).agg(
        AvgPersuasiveness=("Persuasiveness", "mean"),
        Count=("Persuasiveness", "size"),  # Count the number of occurrences
    )
    return grouped_df


def plot_dataframe(plot_df):
    """
    Plots the average persuasiveness across pitch and LIWC categories using a scatter plot.

    Parameters:
        plot_df (pd.DataFrame): The DataFrame containing the data to be plotted, 
                                with columns for Pitch, LIWC, AvgPersuasiveness, and Count.
    """
    # Initialize the figure
    plt.figure(figsize=(14, 8))

    # Create a scatter plot using seaborn for better color mapping
    scatter_plot = sns.scatterplot(
        x="LIWC",
        y="Pitch",
        hue="AvgPersuasiveness",
        palette="viridis",
        data=plot_df,
        alpha=0.8,
        size="Count",
        sizes=(50, 500),
    )

    # Set plot labels and title
    plt.xlabel("LIWC Categories")
    plt.ylabel("Pitch Categories")
    plt.title("Average Persuasiveness Across Pitch and LIWC Categories")
    plt.xticks(rotation=90)  # Rotate x-axis labels for readability
    plt.grid(True)

    # Handle legend for persuasiveness color mapping
    h, l = scatter_plot.get_legend_handles_labels()
    legend1 = plt.legend(
        h[: len(set(plot_df["AvgPersuasiveness"])) + 1],
        l[: len(set(plot_df["AvgPersuasiveness"])) + 1],
        loc="upper left",
        bbox_to_anchor=(1.0, 1),
        borderaxespad=0.0,
    )
    scatter_plot.add_artist(legend1)

    # Handle legend for the size mapping (Count)
    plt.legend(
        h[len(set(plot_df["AvgPersuasiveness"])) + 1 :],
        l[len(set(plot_df["AvgPersuasiveness"])) + 1 :],
        loc="upper left",
        bbox_to_anchor=(1.0, 0.7),
        borderaxespad=0.0,
    )

    # Display the plot
    plt.show()

def find_extreme_words(filtered_df, liwc_columns, pitch_columns, min_persuasiveness, max_persuasiveness):
    """
    Finds words and their related LIWC categories that fall within a specified persuasiveness range.

    Parameters:
        filtered_df (pd.DataFrame): The DataFrame containing the data.
        liwc_columns (list): List of LIWC category column names.
        pitch_columns (list): List of pitch category column names.
        min_persuasiveness (float): The minimum persuasiveness score to filter by.
        max_persuasiveness (float): The maximum persuasiveness score to filter by.

    Returns:
        pd.DataFrame: A DataFrame of words with their corresponding LIWC categories, 
                      pitch categories, clips, and persuasiveness scores within the specified range.
    """
    extreme_words = []

    for _, row in filtered_df.iterrows():
        word = row["word"]
        clip = row["clip"]
        persuasiveness = row["persuasiveness"]
        
        if min_persuasiveness >= persuasiveness or persuasiveness >= max_persuasiveness:
            for pitch in pitch_columns:
                if row[pitch] == 1:  # If the word has this pitch category
                    for liwc in liwc_columns:
                        if row[liwc] == 1:  # If the word belongs to this LIWC category
                            extreme_words.append([word, clip, pitch, liwc, persuasiveness])

    # Convert the list into a DataFrame
    extreme_words_df = pd.DataFrame(extreme_words, columns=["Word", "Clip", "Pitch", "LIWC", "Persuasiveness"])
    
    return extreme_words_df


def display_extreme_words(extreme_words_df):
    """
    Displays the words, pitch, and LIWC categories with extreme persuasiveness.

    Parameters:
        extreme_words_df (pd.DataFrame): DataFrame containing the extreme words and their categories.
    """
    if extreme_words_df.empty:
        print("No words found within the specified persuasiveness range.")
    else:
        print("Words with extreme persuasiveness scores:")
        print(extreme_words_df)
        extreme_words_df.to_csv("extreme_words.csv")


def main():
    """
    Main function that orchestrates the filtering, reshaping, and plotting of the data.

    The function reads the dataset from a CSV file, filters it to include only relevant LIWC 
    and pitch categories, reshapes the data for analysis, and then visualizes the average 
    persuasiveness across the different categories. It also finds and displays words with 
    extreme persuasiveness scores.
    """
    # Load the dataset from the CSV file
    df = pd.read_csv(CSV_PATH)
    
    liwc_columns = df.columns[
        df.columns.get_loc("BigWords") : df.columns.get_loc("remplisseur") + 1
    ]
    
    pitch_columns = [
        "none",
        "L",
        "M",
        "H",
        "B",
        "T",
    ]

    # Filter the DataFrame for relevant columns
    filtered_df = filter_dataframe(df, "persuasiveness", liwc_columns, pitch_columns)
    
    # Reshape the data for plotting
    plot_df = reshape_data(filtered_df, liwc_columns, pitch_columns)
    # print(plot_df)
    
    # Plot the reshaped data
    plot_dataframe(plot_df)
    
    # Find and display words with extreme persuasiveness
    min_persuasiveness = 2.5
    max_persuasiveness = 4.8
    extreme_words_df = find_extreme_words(filtered_df, liwc_columns, pitch_columns, min_persuasiveness, max_persuasiveness)
    display_extreme_words(extreme_words_df)


if __name__ == "__main__":
    main()
