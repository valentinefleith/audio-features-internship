import glob
import pandas as pd
import textgrids as tgt

TEXTGRIDS_PATH = "../../corpus/alignments"
PITCH_PATH = "../../corpus/polytonia"
SCORES_PATH = "../../corpus/MT_aggregated_ratings.csv"

PITCH_LEVELS = ["none", "L", "M", "H", "B", "T"]


def get_score(id):
    df = pd.read_csv(SCORES_PATH)
    return float(
        df.query("`clip` == 'full' and `aggregationMethod` == 'mean' and `id` == @id")[
            "persuasiveness"
        ].iloc[0]
    )


class Word:
    def __init__(self, text, none, l, m, h, b, t):
        self.text = text
        self.none = none
        self.l = l
        self.m = m
        self.h = h
        self.b = b
        self.t = t

    def get_pitch_vec(self):
        return [self.none, self.l, self.m, self.h, self.b, self.t]

    @staticmethod
    def new(text):
        return Word(text, 0, 0, 0, 0, 0, 0)

    def to_dict(self, clip_id, persuasiveness):
        return {
            "clip": clip_id,
            "persuasiveness": persuasiveness,
            "word": self.text,
            "none": self.none,
            "L": self.l,
            "M": self.m,
            "H": self.h,
            "B": self.b,
            "T": self.t,
        }


class Clip:
    def __init__(self, id, score, words: list[Word]):
        self.id = id
        self.score = score
        self.words = words

    def to_df(self):
        # Convert the Clip to a DataFrame where each Word is a row
        data = [word.to_dict(self.id, self.score) for word in self.words]
        return pd.DataFrame(data)

    @staticmethod
    def new(id, words, pitch_annotations):
        words_list = []
        for word in words:
            if word.text == "":
                continue
            begin, end = word.xmin, word.xmax
            word_instance = Word.new(word.text)
            for annotation in pitch_annotations:
                if annotation.xmin >= begin and annotation.xmax <= end:
                    if "h" in annotation.text.lower():
                        word_instance.h = 1
                    elif "m" in annotation.text.lower():
                        word_instance.m = 1
                    elif "b" in annotation.text.lower():
                        word_instance.b = 1
                    elif "t" in annotation.text.lower():
                        word_instance.t = 1
                    else:
                        word_instance.none = 1
                    break
            words_list.append(word_instance)
        return Clip(id, get_score(id), words_list)


def main():
    transcriptions = sorted(glob.glob(f"{TEXTGRIDS_PATH}/*.TextGrid"))
    pitch_levels = sorted(glob.glob(f"{PITCH_PATH}/*.TextGrid"))
    words_dataframes = []

    for transcript, pitch_level in zip(transcriptions, pitch_levels):
        words = tgt.TextGrid(transcript)["words"]
        pitch_annotations = tgt.TextGrid(pitch_level)["polytonia"]
        id = transcript.split("/")[-1].split(".")[0]
        words_dataframes.append(Clip.new(id, words, pitch_annotations).to_df())

    # Merge all dataframes into a single dataframe
    final_df = pd.concat(words_dataframes, ignore_index=True)

    final_df.to_csv("output.csv", index=False)
    print(final_df)


if __name__ == "__main__":
    main()
