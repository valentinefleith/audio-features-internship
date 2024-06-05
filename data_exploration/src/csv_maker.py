"""
This script processes and analyzes ratings data from a CSV file. It calculates and aggregates scores using either mean or RMS (Root Mean Square) methods for various dimensions of answers. The script is designed to handle different parts of video clips (beginning, middle, end, full) and produces a consolidated DataFrame with aggregated scores.
The script only prints the csv but can also save it (commented line in main()).

To run this script:
python3 csv_maker.py -p <part> -m <aggregation_method>

You can run:
python3 csv_maker.py -h
to see what are the required arguments. Method is mandatory, but default part is full.
"""


import pandas as pd
import numpy as np
import argparse

ANNOTATION_PATH = "raw_data/annotations.csv"
DIMENSIONS = [
    "Answer.Competence",
    "Answer.Engagement",
    "Answer.Persuasiveness",
    "Answer.Global",
]


def get_ratings_by_raters(df, rating_dimension):
    rater1 = df.query("index % 3 == 0").reset_index(drop=True)[[rating_dimension]]
    rater2 = df.query("index % 3 == 1").reset_index(drop=True)[[rating_dimension]]
    rater3 = df.query("index % 3 == 2").reset_index(drop=True)[[rating_dimension]]
    return [rater1, rater2, rater3]


def get_mean_scores(ratings):
    scores = []
    for dim in DIMENSIONS:
        df = get_ratings_by_raters(ratings, dim)
        concatenated = pd.concat([df[0][[dim]], df[1][[dim]], df[2][[dim]]], axis=1)
        scores.append(concatenated.mean(axis=1))
    mean_scores = pd.concat(scores, axis=1)
    mean_scores.columns = DIMENSIONS
    return mean_scores


def get_harmonic_mean_scores(ratings):
    scores = []
    for dim in DIMENSIONS:
        df = get_ratings_by_raters(ratings, dim)
        concatenated = pd.concat([df[0][[dim]], df[1][[dim]], df[2][[dim]]], axis=1)
        scores.append(len(concatenated.columns) / (1 / concatenated).sum(axis=1))
    harmonic_mean_scores = pd.concat(scores, axis=1)
    harmonic_mean_scores.columns = DIMENSIONS
    return harmonic_mean_scores


def get_rms_scores(ratings):
    scores = []
    for dim in DIMENSIONS:
        df = get_ratings_by_raters(ratings, dim)
        concatenated = pd.concat([df[0][[dim]], df[1][[dim]], df[2][[dim]]], axis=1)
        scores.append(np.sqrt((concatenated**2).mean(axis=1)))
    rms_scores = pd.concat(scores, axis=1)
    rms_scores.columns = DIMENSIONS
    return rms_scores


def main(part, method):
    annotations = pd.read_csv(ANNOTATION_PATH, sep=";", encoding="ISO-8859-1")
    ratings = annotations.query("`clip` == @part")[
        [
            "Input.name",
            "Answer.Competence",
            "Answer.Engagement",
            "Answer.Persuasiveness",
            "Answer.Global",
        ]
    ].reset_index(drop=True)
    clip_names = ratings["Input.name"].drop_duplicates().reset_index(drop=True)
    if method == "mean":
        aggregated_scores = get_mean_scores(ratings)
    elif method == "rms":
        aggregated_scores = get_rms_scores(ratings)
    else:
        aggregated_scores = get_harmonic_mean_scores(ratings)
    final_df = pd.concat([clip_names, aggregated_scores], axis=1)
    final_df.insert(1, "clip", part)
    print(final_df)
    # UNCOMMENT TO SAVE THE CSV:
    # final_df.to_csv(
    #     f"data_exploration/new_csvfiles/{part}/{part[:3].upper()}_{method}.csv",
    #     sep=";",
    #     index=False,
    # )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--part", choices=["beginning", "middle", "end", "full"])
    parser.add_argument(
        "-m", "--aggregation_method", choices=["mean", "rms", "hmeans"], required=True
    )
    args = parser.parse_args()
    if args.part is None:
        args.part = "full"

    main(args.part, args.aggregation_method)
