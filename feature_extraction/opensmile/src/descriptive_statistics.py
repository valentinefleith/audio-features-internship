import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json
from sklearn.preprocessing import StandardScaler


FEAT_DIR_PATH = "./features"


def rescale_feature_df(feature_df):
    scaler = StandardScaler()
    standardized_features = scaler.fit_transform(feature_df.iloc[:, 1:])
    standardized_df = pd.concat(
        [
            feature_df.iloc[:, 0],
            pd.DataFrame(standardized_features, columns=feature_df.iloc[:, 1:].columns),
        ],
        axis=1,
    )
    return standardized_df
    # print(standardized_df.describe().round(6))


def get_most_least_uniform_feats(df):
    variances = df.iloc[:, 1:].var()
    most_uniform_feat = variances.idxmin()
    least_uniform_feat = variances.idxmax()
    return most_uniform_feat, least_uniform_feat


def plot_distribution(df, most_uniform_feat, least_uniform_feat, category):
    plt.figure(figsize=(14, 6))
    # distribution of the most uniform feature
    plt.subplot(1, 2, 1)
    sns.histplot(df[most_uniform_feat], kde=True)
    plt.title(
        f"Distribution of the most uniform feature of {category} features : {most_uniform_feat}"
    )
    # distribution of the least uniform feature
    plt.subplot(1, 2, 2)
    sns.histplot(df[least_uniform_feat], kde=True)
    plt.title(
        f"Distribution of the least uniform feature of {category} features: {least_uniform_feat}"
    )
    plt.tight_layout()
    plt.show()


def main():
    feature_files = glob.glob(f"{FEAT_DIR_PATH}/csv_files/*.csv")
    stats_files = os.path.join(FEAT_DIR_PATH, "stats", "standardized")
    os.makedirs(stats_files, exist_ok=True)
    categories = [os.path.basename(file).split(".")[0] for file in feature_files]
    for i, file in enumerate(feature_files):
        feature_df = pd.read_csv(file)
        # feature_df.describe().to_csv(f"{stats_files}/{categories[i]}_stats.csv")
        standardized_df = rescale_feature_df(feature_df)
        # standardized_df.describe().to_csv(f"{stats_files}/{categories[i]}_stats.csv")
        most_uniform_feat, least_uniform_feat = get_most_least_uniform_feats(
            standardized_df
        )
        plot_distribution(
            standardized_df, most_uniform_feat, least_uniform_feat, categories[i]
        )


if __name__ == "__main__":
    main()
