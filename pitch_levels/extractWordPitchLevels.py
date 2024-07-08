import sys
import glob
import parselmouth as pm
import textgrids as tgt


PITCH_LEVELS = {"high": "H", "low": "L", "highrise": "HR", "highfall": "HF"}


class Word:
    """
    Represents a word with its associated TextGrid index and time intervals.

    Attributes:
        word (str): The text of the word.
        tgt_index (int): The index of the word in the TextGrid.
        xmin (float): The start time of the word.
        xmax (float): The end time of the word.
    """

    def __init__(self, word, index):
        self.word = word.text
        self.tgt_index = index
        self.xmin = word.xmin
        self.xmax = word.xmax

    def __repr__(self):
        return f"Word(word={self.word}, index={self.tgt_index}, xmin={self.xmin}, xmax={self.xmax})"

    def __str__(self):
        return f"Mot: {self.word}\nIndex: {self.tgt_index}\nXmin: {self.xmin}\nXmax: {self.xmax}"


def already_stored(word_text, word_list):
    """
    Checks if a word is already in the list of words.

    Args:
        word_text (str): The text of the word to check.
        word_list (list): The list of Word objects.

    Returns:
        bool: True if the word is already in the list, False otherwise.
    """
    for word in word_list:
        if word.word == word_text:
            return True
    return False


def find_words_in_intervals(time_intervals, words):
    """
    Finds words within specified time intervals.

    Args:
        time_intervals (list): List of tuples containing start and end times.
        words (list): List of word intervals from TextGrid.

    Returns:
        list: List of Word objects found within the specified time intervals.
    """
    word_list = []
    for start, end in time_intervals:
        for index, word in enumerate(words):
            if word.xmin <= start and end <= word.xmax:
                if not already_stored(word.text, word_list):
                    word_list.append(Word(word, index))
                break
    return word_list


def extract_words_by_pitch_level(level, transcript_paths, pitch_paths):
    """
    Extracts words from transcripts based on specified pitch levels.

    Args:
        level (str): The pitch level to filter by (e.g., "high", "low").
        transcript_paths (list): List of paths to transcript TextGrid files.
        pitch_paths (list): List of paths to pitch level TextGrid files.

    Returns:
        list: A list of lists containing Word objects for each transcript.
    """
    words_by_pitch_level = []
    for transcript_path, pitch_path in zip(transcript_paths, pitch_paths):
        words = tgt.TextGrid(transcript_path)["words"]
        pitch_intervals = tgt.TextGrid(pitch_path)["polytonia"]
        time_intervals = [
            (interval.xmin, interval.xmax)
            for interval in pitch_intervals
            if interval.text.lower() == PITCH_LEVELS[level].lower()
        ]
        words_by_pitch_level.append(find_words_in_intervals(time_intervals, words))
    return words_by_pitch_level


def main():
    """
    Main function to extract words from TextGrid files based on pitch levels.
    """
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 extractWordPitchLevels.py /path/to/corpus")

    textgrid_paths = glob.glob(f"{sys.argv[1]}/*.TextGrid")
    transcript_paths = sorted(
        [path for path in textgrid_paths if not path.endswith("polytonia.TextGrid")]
    )
    pitch_paths = sorted(
        [path for path in textgrid_paths if path.endswith("polytonia.TextGrid")]
    )

    for level in PITCH_LEVELS.keys():
        words_by_level = extract_words_by_pitch_level(
            level, transcript_paths, pitch_paths
        )
        for words in words_by_level:
            print(f"{level.capitalize()} :")
            print(words)


if __name__ == "__main__":
    main()
