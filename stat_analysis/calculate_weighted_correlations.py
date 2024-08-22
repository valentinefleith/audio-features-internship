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

    :param x: 1D array of the first variable.
    :param y: 1D array of the second variable.
    :param w: 1D array of weights corresponding to each observation.
    :return: Weighted Pearson correlation coefficient.
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
    features_df = pd.read_csv(CSV_PATH)
    persuasiveness_scores = features_df["persuasiveness"]
    freq = persuasiveness_scores.value_counts()
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
