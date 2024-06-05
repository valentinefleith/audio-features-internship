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
from pydub import AudioSegment


def save_as_wav_files(video_paths, dest_path):
    os.makedirs(dest_path, exist_ok=True)
    for filepath in video_paths:
        name = filepath.split("/")[-1].split(".")[0]
        sound = AudioSegment.from_file(filepath, format="mp4")
        sound.export(f"{dest_path}/{name}.wav", format="wav")


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 mp4_to_wav.py /path/do/video_dir")
    video_paths = glob.glob(f"{sys.argv[1]}/mp4/*.mp4")
    save_as_wav_files(video_paths, f"{sys.argv[1]}/wav")


if __name__ == "__main__":
    main()
