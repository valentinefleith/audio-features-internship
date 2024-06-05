"""
The extract_features.py script extracts eGeMAPS (extended Geneva Minimalistic Acoustic Parameter Set) features from a directory of audio files and saves the resulting feature set to a CSV file. The script leverages the OpenSMILE toolkit through the opensmile Python library.

To run this script:
python3 extract_features.py /path/to/corpus_dir

It requires a "wav" subdirectory in the directory.
"""


import sys
import opensmile
import glob
import pandas as pd


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 extract_features.py /path/to/corpus_dir")
    audio_paths = glob.glob(f"{sys.argv[1]}/wav/*.wav")
    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.eGeMAPSv02,
        feature_level=opensmile.FeatureLevel.Functionals,
    )
    features = []
    for audio in audio_paths:
        features.append(smile.process_file(audio))
    all_features = pd.concat(features)
    all_features.to_csv(f"features.csv")


if __name__ == "__main__":
    main()
