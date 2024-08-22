"""
This module calculates the weighted Pearson correlation coefficients between various acoustic features 
and persuasiveness scores in a dataset. The correlations are calculated using custom weights based 
on the frequency of persuasiveness scores, and the results are saved to a JSON file.
"""

import pandas as pd
import numpy as np
import json

CSV_PATH = "merged_audio_features.csv"
FEATURES = [
    "avg_pitch",
    "avg_intensity",
    "intensity_peaks_rate",
    "pitch_variation",
    "intensity_variation",
    "avg_len_pause",
    "pause_rate",
]


def weighted_correlation(x, y, w):
    """
    Calculate the weighted Pearson correlation coefficient between two variables.

    Parameters:
        x (np.ndarray or list): 1D array or list of the first variable (e.g., feature values).
        y (np.ndarray or list): 1D array or list of the second variable (e.g., persuasiveness scores).
        w (np.ndarray or list): 1D array or list of weights corresponding to each observation.

    Returns:
        float: The weighted Pearson correlation coefficient between x and y.
    """
    # Convert inputs to numpy arrays
    x = np.array(x)
    y = np.array(y)
    w = np.array(w)
    # Calculate the weighted means
    mean_x = np.average(x, weights=w)
    mean_y = np.average(y, weights=w)
    # Calculate the weighted covariance
    cov_xy = np.sum(w * (x - mean_x) * (y - mean_y)) / np.sum(w)
    # Calculate the weighted standard deviations
    std_x = np.sqrt(np.sum(w * (x - mean_x) ** 2) / np.sum(w))
    std_y = np.sqrt(np.sum(w * (y - mean_y) ** 2) / np.sum(w))
    # Calculate the weighted correlation coefficient
    corr = cov_xy / (std_x * std_y)
    return corr


def main():
    """
    Main function that reads the dataset, calculates weighted correlations between features 
    and persuasiveness scores, and saves the results to a JSON file.

    The function reads feature data and persuasiveness scores from a CSV file, computes weights based on the
    frequency of the persuasiveness scores, and then calculates the weighted correlation for each feature
    against the persuasiveness scores. The correlations are stored in a dictionary and saved as a JSON file.
    """
    # Load the dataset from the CSV file
    features_df = pd.read_csv(CSV_PATH)
    persuasiveness_scores = features_df["persuasiveness"]
    # Calculate the frequency of each persuasiveness score
    freq = persuasiveness_scores.value_counts()
    # Assign weights inversely proportional to the frequency of each score
    weights = persuasiveness_scores.map(lambda x: 1 / freq[x])
    correlations = {}
    for feature in FEATURES:
        correlations[feature] = weighted_correlation(
            features_df[feature], persuasiveness_scores, weights
        )
    with open("correlations.json", "w") as f:
        json.dump(correlations, f)
    print(correlations)


if __name__ == "__main__":
    main()
