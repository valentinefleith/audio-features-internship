"""
The extract_features.py script extracts eGeMAPS (extended Geneva Minimalistic Acoustic Parameter Set) features from a directory of audio files and saves the resulting feature set to a CSV file. The script leverages the OpenSMILE toolkit through the opensmile Python library.

To run this script:
python3 extract_features.py /path/to/corpus_dir

It requires a "wav" subdirectory in the directory.

Also possible to perform the creation of several csv depending on the categories defined in the 'categories.py' file. To do so, run with the same command as before but add a third argument, for example:
python3 extract_features.py /path/to/corpus_dir -c
"""


import sys
import opensmile
import glob
import pandas as pd
from categories import CATEGORIES


def split_feature_categories(features):
    for cat, feat in CATEGORIES.items():
        only_category = pd.concat([features["file"], features[feat]], axis=1)
        only_category.to_csv(f"features_{cat}.csv")


def create_csv(features, to_split=False):
    all_features = pd.concat(features).reset_index()
    all_features = all_features.drop(columns=["start", "end"])
    all_features["file"] = (
        all_features["file"].str.split("/").str[-1].str.split("_").str[-1]
    )
    print(all_features)
    if to_split:
        return split_feature_categories(all_features)
    all_features.to_csv("features.csv")


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 extract_features.py /path/to/corpus_dir")
    audio_paths = glob.glob(f"{sys.argv[1]}/wav/*.wav")
    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.eGeMAPSv02,
        feature_level=opensmile.FeatureLevel.Functionals,
    )
    features = []
    for audio in audio_paths:
        features.append(smile.process_file(audio))
    to_split = len(sys.argv) > 2
    create_csv(features, to_split=to_split)


if __name__ == "__main__":
    main()
