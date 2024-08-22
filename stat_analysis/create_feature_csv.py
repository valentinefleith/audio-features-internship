"""
This module extracts acoustic features from audio files and combines them with persuasiveness scores.
It processes audio files to calculate various features such as pitch, intensity, pause statistics, etc.,
and then merges these features with pre-existing scores to produce a combined dataset.
"""

import parselmouth as pm
import textgrids as tgt
import numpy as np
import pandas as pd
import glob
from tqdm import tqdm

CORPUS_PATH = "../../corpus/wav/full"
SAMPLE_PATH = "../../corpus/sample/wav"
SCORES_PATH = "../../corpus/MT_aggregated_ratings.csv"
TEXTGRID_PATH = "../../corpus/alignments"


def calculate_intensity_peaks_rate(sound, intensity_threshold, intensity_values):
    """
    Calculate the rate of intensity peaks in the sound signal.

    Parameters:
        sound (pm.Sound): The sound object representing the audio file.
        intensity_threshold (float): The threshold above which an intensity value is considered a peak.
        intensity_values (np.ndarray): Array of intensity values over time.

    Returns:
        float: The rate of intensity peaks per second in the sound.
    """
    intensity_peaks = np.sum(intensity_values > intensity_threshold)
    return intensity_peaks / sound.duration


def calculate_pause_stats(id, sound):
    """
    Calculate the average length and rate of pauses in the audio based on the TextGrid annotations.

    Parameters:
        id (str): The identifier of the audio file (used to locate the corresponding TextGrid file).
        sound (pm.Sound): The sound object representing the audio file.

    Returns:
        tuple: A tuple containing the average length of pauses (float) and the pause rate per second (float).
    """
    try:
        textgrid = tgt.TextGrid(f"{TEXTGRID_PATH}/{id}.TextGrid")
    except FileNotFoundError:
        print(f"file not found: {id}")
        return 0, 0
    words = textgrid["words"]
    pauses = []
    for word in words:
        if word.text == "":
            pauses.append(word.xmax - word.xmin)
    avg_len_pause = np.mean(pauses)
    pause_rate = len(pauses) / sound.duration
    return avg_len_pause, pause_rate


class Features:
    """
    A class to represent and store various acoustic features of an audio file.
    Parameters:
        id (str): The identifier of the audio file.
        avg_pitch (float): The average pitch of the audio in Hertz.
        avg_intensity (float): The average intensity of the audio in decibels.
        intensity_peaks_rate (float): The rate of intensity peaks per second.
        pitch_variation (float): The standard deviation of pitch values (pitch variation).
        intensity_variation (float): The standard deviation of intensity values (intensity variation).
        avg_len_pause (float): The average length of pauses in seconds.
        pause_rate (float): The rate of pauses per second.
    """

    def __init__(
        self,
        id,
        avg_pitch,
        avg_intensity,
        intensity_peaks_rate,
        pitch_variation,
        intensity_variation,
        avg_len_pause,
        pause_rate,
    ):
        self.id = id
        self.avg_pitch = avg_pitch
        self.avg_intensity = avg_intensity
        self.intensity_peaks_rate = intensity_peaks_rate
        self.pitch_variation = pitch_variation
        self.intensity_variation = intensity_variation
        self.avg_len_pause = avg_len_pause
        self.pause_rate = pause_rate

    def __repr__(self):
        return (
            f"Features(id={self.id}, pitch={self.avg_pitch:.2f} Hz, intensity={self.avg_intensity:.2f} dB, "
            f"intensity_peaks_rate={self.intensity_peaks_rate:.2f} peaks/sec, "
            f"pitch_variation={self.pitch_variation:.2f} Hz, "
            f"intensity_variation={self.intensity_variation:.2f} dB, "
            f"avg_len_pause={self.avg_len_pause:.2f} s, "
            f"pause_rate={self.pause_rate:.2f} pause/sec)"
        )

    @staticmethod
    def new(filename):
        """
        Create a new Features object from an audio file.

        Parameters:
            filename (str): The path to the audio file.

        Returns:
            Features: A Features object containing the calculated features of the audio.
        """
        sound = pm.Sound(filename)
        id = filename.split("/")[-1].split(".")[0]
        # calculate averages
        pitch_values = sound.to_pitch().selected_array["frequency"]
        # we remove unvoiced pitch values (usually 0 Hz)
        average_pitch = np.mean(pitch_values[pitch_values > 0])

        intensity_values = sound.to_intensity().values[0]
        average_intensity = np.mean(intensity_values)

        # calculate intensity peaks rate
        intensity_peaks_rate = calculate_intensity_peaks_rate(
            sound, average_intensity, intensity_values
        )

        pitch_variation = np.std(pitch_values)
        intensity_variation = np.std(intensity_values)

        avg_len_pause, pause_rate = calculate_pause_stats(id, sound)
        return Features(
            id,
            average_pitch,
            average_intensity,
            intensity_peaks_rate,
            pitch_variation,
            intensity_variation,
            avg_len_pause,
            pause_rate,
        )


def get_scores():
    """
    Retrieve the persuasiveness scores for the audio clips.

    Returns:
        pd.DataFrame: A DataFrame containing the IDs and persuasiveness scores of the audio clips.
    """
    scores = pd.read_csv(SCORES_PATH)
    return scores.query("`clip` == 'full' and `aggregationMethod` == 'mean'")[
        ["id", "persuasiveness"]
    ]


def main():
    """
    Main function to extract audio features from files, merge them with persuasiveness scores, and save the result.

    The function processes all audio files in the specified corpus directory, extracts their features, and merges
    these features with pre-existing scores into a single DataFrame. The result is then saved to a CSV file.
    """
    audio_filepaths = glob.glob(f"{CORPUS_PATH}/*.wav")
    audio_features = []
    for audio_file in tqdm(audio_filepaths):
        audio_features.append(Features.new(audio_file).__dict__)
    audio_features_df = pd.DataFrame(audio_features)
    print(audio_features_df)
    merged = pd.merge(audio_features_df, get_scores(), on="id").sort_values(by="id")
    print(merged)
    merged.to_csv("merged_audio_features.csv", index=False)


if __name__ == "__main__":
    main()
