import sys
import spacy
import glob
import textgrids as tgt


def tokenize_with_spacy(file):
    with open(file, "r") as f:
        text = f.read().lower().replace("\n", " ").replace("-", " ")
    nlp = spacy.load("fr_core_news_sm")
    doc = nlp(text)
    tokens = [token.text for token in doc if token.text not in ",?.- "]
    i = 0
    while i < len(tokens):
        if tokens[i].endswith("'"):
            tokens[i] += tokens[i + 1]
            tokens.pop(i + 1)
        i += 1
    return tokens


def main():
    """
    Main function to extract words from TextGrid files based on pitch levels.
    """
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 extractWordPitchLevels.py /path/to/corpus")
    transcript_paths = sorted(glob.glob(f"{sys.argv[1]}/*.txt"))
    textgrid_paths = glob.glob(f"{sys.argv[1]}/*.TextGrid")
    aligned_tgt_paths = sorted(
        [path for path in textgrid_paths if not path.endswith("polytonia.TextGrid")]
    )
    # print(transcript_paths)
    # print(aligned_tgt_paths)
    for transcript, textgrid in zip(transcript_paths, aligned_tgt_paths):
        mfa_tokens = [
            word.text for word in tgt.TextGrid(textgrid)["words"] if word.text != ""
        ]
        spacy_tokens = tokenize_with_spacy(transcript)
        print(f"FOR FILE {transcript}")
        print(f"MFA TOKENS:\n {len(mfa_tokens)}\n")
        print(f"SPACY TOKENS:\n {len(spacy_tokens)}\n")


if __name__ == "__main__":
    main()
