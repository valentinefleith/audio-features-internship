import sys
import glob
from dataclasses import dataclass
import parselmouth as pm
import textgrids as tgt


PITCH_LEVELS = {"high": "H", "low": "L"}


class Word:
    def __init__(self, word, i):
        self.word = word.text
        self.index = i
        self.xmin = word.xmin
        self.xmax = word.xmax

    def __repr__(self):
        return f"Word(word={self.word}, index={self.index}, xmin={self.xmin}, xmax={self.xmax})"

    def __str__(self):
        return f"Mot: {self.word}\nIndex: {self.index}\nXmin: {self.xmin}\nXmax: {self.xmax}"


def find_list_of_words(times, words):
    word_list = []
    for time in times:
        for i, word in enumerate(words):
            if word.xmin <= time[0] and time[1] <= word.xmax:
                word_list.append(Word(word, i))
                break
    return sorted(set(word_list), key=lambda x: x.index)


def extract_words_pitch(level, tgt_transcripts, tgt_pitch):
    words_list = []
    for transcript, pitch in zip(tgt_transcripts, tgt_pitch):
        words = tgt.TextGrid(transcript)["words"]
        pitch_levels = tgt.TextGrid(pitch)["polytonia"]
        times = []
        for pitches in pitch_levels:
            if pitches.text == PITCH_LEVELS[level]:
                start = pitches.xmin
                end = pitches.xmax
                # time = (start + end) / 2
                times.append((start, end))
        words_list.append(find_list_of_words(times, words))
    return words_list


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 extractWordPitchLevels.py /path/to/corpus")
    # audio_paths = glob.glob(f"{sys.argv[1]}/*.wav")
    textgrids_paths = glob.glob(f"{sys.argv[1]}/*.TextGrid")
    transcript_tgt = []
    pitch_levels_tgt = []
    for txtgrid in textgrids_paths:
        if txtgrid.endswith("polytonia.TextGrid"):
            pitch_levels_tgt.append(txtgrid)
        else:
            transcript_tgt.append(txtgrid)
    # ids = [path.split('/')[-1].split('.')[0] for path in audio_paths]
    transcript_tgt.sort()
    pitch_levels_tgt.sort()
    words = extract_words_pitch("high", transcript_tgt, pitch_levels_tgt)
    print(words)


if __name__ == "__main__":
    main()
