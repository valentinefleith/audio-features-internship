import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CSV_PATH = "merged_vectors.csv"


def filter_dataframe(df, dimension, liwc_columns, pitch_columns):
    # Filter out relevant data
    target_columns = ["word", f"{dimension}"]
    target_columns.extend(pitch_columns)
    target_columns.extend(liwc_columns)
    filtered_df = df[target_columns]
    return filtered_df


def reshape_data(filtered_df, liwc_columns, pitch_columns):
    plot_data = []
    for _, row in filtered_df.iterrows():
        word = row["word"]
        persuasiveness = row["persuasiveness"]
        for pitch in pitch_columns:
            if row[pitch] == 1:  # If the word has this pitch category
                for liwc in liwc_columns:
                    if row[liwc] == 1:  # If the word belongs to this LIWC category
                        plot_data.append([pitch, liwc, persuasiveness])

    plot_df = pd.DataFrame(plot_data, columns=["Pitch", "LIWC", "Persuasiveness"])

    # Group by Pitch and LIWC to calculate the average persuasiveness and count occurrences
    grouped_df = plot_df.groupby(["Pitch", "LIWC"], as_index=False).agg(
        AvgPersuasiveness=("Persuasiveness", "mean"),
        Count=("Persuasiveness", "size"),  # Count the number of occurrences
    )
    return grouped_df


def plot_dataframe(plot_df):
    # Plotting
    plt.figure(figsize=(14, 8))

    # Using seaborn for better color mapping
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

    plt.xlabel("LIWC Categories")
    plt.ylabel("Pitch Categories")
    plt.title("Average Persuasiveness Across Pitch and LIWC Categories")
    plt.xticks(rotation=90)  # Rotate x-axis labels for readability
    plt.grid(True)

    h, l = scatter_plot.get_legend_handles_labels()
    legend1 = plt.legend(
        h[: len(set(plot_df["AvgPersuasiveness"])) + 1],
        l[: len(set(plot_df["AvgPersuasiveness"])) + 1],
        loc="upper left",
        bbox_to_anchor=(1.0, 1),
        borderaxespad=0.0,
    )
    scatter_plot.add_artist(legend1)

    plt.legend(
        h[len(set(plot_df["AvgPersuasiveness"])) + 1 :],
        l[len(set(plot_df["AvgPersuasiveness"])) + 1 :],
        loc="upper left",
        bbox_to_anchor=(1.0, 0.7),
        borderaxespad=0.0,
    )

    plt.show()


def main():
    df = pd.read_csv(CSV_PATH)
    # LIWC categories start from 'BigWords' to 'Emoji' (assuming continuous columns)
    liwc_columns = df.columns[
        df.columns.get_loc("BigWords") : df.columns.get_loc("Emoji") + 1
    ]
    pitch_columns = [
        "none",
        "L",
        "M",
        "H",
        "B",
        "T",
    ]  # Assuming these are the pitch categories

    filtered_df = filter_dataframe(df, "persuasiveness", liwc_columns, pitch_columns)
    plot_df = reshape_data(filtered_df, liwc_columns, pitch_columns)
    plot_dataframe(plot_df)


if __name__ == "__main__":
    main()
