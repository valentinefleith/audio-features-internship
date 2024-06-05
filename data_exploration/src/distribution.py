"""
This script processes and visualizes ratings data from a CSV file. It provides options to plot the distribution of raw ratings, mean ratings, or RMS (Root Mean Square) ratings for specific dimensions (competence, engagement, persuasiveness) of answers, filtered by different parts of a clip (beginning, middle, end).

To run this script :
python3 distribution.py -t <plottype> -p <part> -c <dimension>

You can run :
python3 distribution.py -h
to see what are the required arguments. If no arguments are specified, default values are : -t raw, -p full, -c persuasiveness.

Don't hesitate to update the path of the annotation file according to your file structure before running it!
"""


import pandas as pd
import argparse
import matplotlib.pyplot as plt
import numpy as np

ANNOTATION_PATH = "raw_data/annotations.csv"


def get_ratings_by_raters(df, rating_dimension):
    rater1 = df.query("index % 3 == 0")[rating_dimension]
    rater2 = df.query("index % 3 == 1")[rating_dimension]
    rater3 = df.query("index % 3 == 2")[rating_dimension]
    return [rater1, rater2, rater3]


def plot_distribution_raw(df, rating_dimension):
    bins = np.linspace(0, 7, 8) - 0.5
    plt.hist(
        get_ratings_by_raters(df, rating_dimension),
        bins,
        label=["rater 1", "rater 2", "rater 3"],
    )
    plt.legend(loc="upper right")
    plt.title(f"Distribution of Ratings of {rating_dimension.split('.')[1]} by raters")
    plt.show()


def plot_distribution_means(df):
    dimensions = ["Answer.Competence", "Answer.Engagement", "Answer.Persuasiveness"]
    averages = []
    for rating_dimension in dimensions:
        ratings = get_ratings_by_raters(df, rating_dimension)
        concatenated = pd.concat(
            [
                ratings[0].reset_index()[[rating_dimension]],
                ratings[1].reset_index()[[rating_dimension]],
                ratings[2].reset_index()[[rating_dimension]],
            ],
            axis=1,
        )
        averages.append(concatenated.mean(axis=1))
    bins = np.linspace(1, 5, 9)
    plt.hist(averages, bins, label=dimensions, rwidth=0.90)
    plt.legend(loc="upper left")
    plt.title("Distribution of Average of every dimension")
    plt.show()


def plot_distribution_rms(df):
    dimensions = ["Answer.Competence", "Answer.Engagement", "Answer.Persuasiveness"]
    rms_values = []
    for rating_dimension in dimensions:
        ratings = get_ratings_by_raters(df, rating_dimension)
        concatenated = pd.concat(
            [
                ratings[0].reset_index()[[rating_dimension]],
                ratings[1].reset_index()[[rating_dimension]],
                ratings[2].reset_index()[[rating_dimension]],
            ],
            axis=1,
        )
        rms_values.append(np.sqrt((concatenated**2).mean(axis=1)))
    bins = np.linspace(1, 5, 9)
    plt.hist(rms_values, bins, label=dimensions, rwidth=0.90)
    plt.legend(loc="upper left")
    plt.title("Distribution of RMS of every dimension")
    plt.show()


def plot_distribution_harmonic_mean(df):
    dimensions = ["Answer.Competence", "Answer.Engagement", "Answer.Persuasiveness"]
    harmonic_means = []
    for rating_dimension in dimensions:
        ratings = get_ratings_by_raters(df, rating_dimension)
        concatenated = pd.concat(
            [
                ratings[0].reset_index()[[rating_dimension]],
                ratings[1].reset_index()[[rating_dimension]],
                ratings[2].reset_index()[[rating_dimension]],
            ],
            axis=1,
        )
        harmonic_means.append(
            len(concatenated.columns) / (1 / concatenated).sum(axis=1)
        )
    bins = np.linspace(1, 5, 9)
    plt.hist(harmonic_means, bins, label=dimensions, rwidth=0.90)
    plt.legend(loc="upper left")
    plt.title("Distribution of Harmonic means of every dimension")
    plt.show()


def main(plottype, part, dimension):
    ratings = pd.read_csv(ANNOTATION_PATH, sep=";", encoding="ISO-8859-1")
    ratings = ratings.query("`clip` == @part")[
        [
            "Answer.Competence",
            "Answer.Engagement",
            "Answer.Persuasiveness",
        ]
    ].reset_index()
    rating_dimension = "Answer." + dimension.title()
    if plottype == "raw":
        plot_distribution_raw(ratings, rating_dimension)
    elif plottype == "means":
        plot_distribution_means(ratings)
    elif plottype == "rms":
        plot_distribution_rms(ratings)
    elif plottype == "hmeans":
        plot_distribution_harmonic_mean(ratings)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--plottype", choices=["raw", "means", "rms", "hmeans"])
    parser.add_argument("-p", "--part", choices=["beginning", "middle", "end"])
    parser.add_argument(
        "-c",
        "--dimension",
        choices=["competence", "engagement", "persuasiveness", "global"],
    )
    args = parser.parse_args()
    if args.plottype is None:
        args.plottype = "raw"
    if args.part is None:
        args.part = "full"
    if args.dimension is None:
        args.dimension = "persuasiveness"
    main(plottype=args.plottype, part=args.part, dimension=args.dimension)
