import parselmouth as pm
import textgrids as tgt
import numpy as np
import pandas as pd
import glob
from tqdm import tqdm

CORPUS_PATH = "../../corpus/wav/full"
SAMPLE_PATH = "../../corpus/sample/wav"
SCORES_PATH = "../../corpus/MT_aggregated_ratings.csv"
TEXTGRID_PATH = "../../prosogram/corpus"


def calculate_intensity_peaks_rate(sound, intensity_threshold, intensity_values):
    intensity_peaks = np.sum(intensity_values > intensity_threshold)
    return intensity_peaks / sound.duration

def calculate_pause_stats(id, sound):
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


class Audio:
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
            f"Audio(id={self.id}, pitch={self.avg_pitch:.2f} Hz, intensity={self.avg_intensity:.2f} dB, "
            f"intensity_peaks_rate={self.intensity_peaks_rate:.2f} peaks/sec, "
            f"pitch_variation={self.pitch_variation:.2f} Hz, "
            f"intensity_variation={self.intensity_variation:.2f} dB, "
            f"avg_len_pause={self.avg_len_pause:.2f} s, "
            f"pause_rate={self.pause_rate:.2f} pause/sec)"
        )

    @staticmethod
    def new(filename):
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
        return Audio(
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
    scores = pd.read_csv(SCORES_PATH)
    return scores.query("`clip` == 'full' and `aggregationMethod` == 'mean'")[
        ["id", "persuasiveness"]
    ]


def main():
    audio_filepaths = glob.glob(f"{CORPUS_PATH}/*.wav")
    audio_features = []
    for audio_file in tqdm(audio_filepaths):
        audio_features.append(Audio.new(audio_file).__dict__)
    audio_features_df = pd.DataFrame(audio_features)
    print(audio_features_df)
    merged = pd.merge(audio_features_df, get_scores(), on="id").sort_values(by="id")
    print(merged)
    merged.to_csv("../../corpus/merged_audio_features.csv", index=False)


if __name__ == "__main__":
    main()