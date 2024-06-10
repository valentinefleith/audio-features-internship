"""
This script converts MP4 video files to WAV audio files. It processes all MP4 files in a specified directory and saves the converted WAV files to a destination directory.

To run this script:
python3 mp4_to_wav.py /path/to/video_dir

/path/to/video_dir: The path to the directory containing the MP4 files to be converted. The script expects the MP4 files to be located in a subdirectory named mp4 within this directory. The converted WAV files will be saved in a subdirectory named wav.

pydub library is required.
"""

import sys
import os
import glob
import pandas as pd
from pydub import AudioSegment

PARTS = ["beg", "end", "mid", "full"]
ACCENTS = {
    "è": "e",
    "é": "e",
    "ë": "e",
    "é": "e",
    "ç": "c",
    "É": "E",
    "Á": "A",
    "ï": "i",
}


def find_right_name(filepath, dest_path, df_ids):
    filename = filepath.split("/")[-1]
    filepart = filepath.split("/")[-2]
    for accent, no_accent in ACCENTS.items():
        if accent in filename:
            filename = filename.replace(accent, no_accent)
    if filepart == "original":
        return None
    for part in PARTS:
        if filepath.split("/")[-2].startswith(part):
            dest_path += f"{part}/"
    try:
        name_path = df_ids.query("`Name` == @filename")["subname"].values[0]
    except IndexError:
        print(f"\nERROR: {filename} not found.\n")
        return None
    dest_path += name_path
    return dest_path + ".wav"


def save_as_wav_files(video_paths, dest_path, df_ids):
    os.makedirs(dest_path, exist_ok=True)
    for part in PARTS:
        os.makedirs(dest_path + part, exist_ok=True)
    df_ids = pd.concat(
        [
            df_ids.rename(str.lower, axis="columns"),
            df_ids["Name"].str.replace("_transcript.txt", ".mp4"),
        ],
        axis=1,
    )
    for filepath in video_paths:
        name = find_right_name(filepath, dest_path, df_ids)
        if name is None:
            continue
        print(name, end="\n")
        # name = filepath.split("/")[-1].split(".")[0]
        sound = AudioSegment.from_file(filepath, format="mp4")
        sound.export(name, format="wav")


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 mp4_to_wav.py /path/do/video_dir")
    id_path = f"{sys.argv[1]}/transcripts_ID_list_modif.csv"
    video_paths = glob.glob(f"{sys.argv[1]}/mp4/*/*/*.mp4")
    df_ids = pd.read_csv(id_path, sep=";")
    save_as_wav_files(video_paths, f"{sys.argv[1]}/wav/", df_ids)


if __name__ == "__main__":
    main()
