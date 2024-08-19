import parselmouth as pm
import numpy as np
import glob
from tqdm import tqdm

CORPUS_PATH = "../../corpus/wav/full"
SAMPLE_PATH = "../../corpus/sample/wav"


def calculate_intensity_peaks_rate(sound, intensity_threshold, intensity_values):
    intensity_peaks = np.sum(intensity_values > intensity_threshold)
    return intensity_peaks / sound.duration


class Audio:
    def __init__(self, id, avg_pitch, avg_intensity, intensity_peaks_rate):
        self.id = id
        self.avg_pitch = avg_pitch
        self.avg_intensity = avg_intensity
        self.intensity_peaks_rate = intensity_peaks_rate

    def __repr__(self):
        return f"Audio(id={self.id}, pitch={self.avg_pitch:.2f}, intensity={self.avg_intensity:.2f}, intensity_peaks_rate={self.intensity_peaks_rate:.2f})"

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
        return Audio(id, average_pitch, average_intensity, intensity_peaks_rate)


def main():
    audio_filepaths = glob.glob(f"{SAMPLE_PATH}/*.wav")
    file_list = []
    for audio_file in tqdm(audio_filepaths):
        file_list.append(Audio.new(audio_file))
    print(file_list)


if __name__ == "__main__":
    main()
