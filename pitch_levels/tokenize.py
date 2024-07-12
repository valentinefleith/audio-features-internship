"""
This module extracts words from TextGrid files based on pitch levels.
It tokenizes transcript text using spaCy and compares it to MFA tokenized words.

Usage:
    python3 extractWordPitchLevels.py /path/to/corpus
"""

import sys
import spacy
import glob
import textgrids as tgt


def tokenize_text(file_path):
    """
    Tokenizes the text in the given file using spaCy.

    Args:
        file_path (str): Path to the text file to be tokenized.

    Returns:
        List[str]: A list of tokens from the text file.
    """
    with open(file_path, "r") as file:
        text = file.read().lower().replace("\n", " ").replace("-", " ")
    
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


def extract_words(corpus_path):
    """
    Extracts words from TextGrid files and compares them with spaCy tokens.

    Args:
        corpus_path (str): Path to the corpus directory containing text and TextGrid files.
    """
    transcript_paths = sorted(glob.glob(f"{corpus_path}/*.txt"))
    textgrid_paths = glob.glob(f"{corpus_path}/*.TextGrid")
    aligned_tgt_paths = sorted(
        [path for path in textgrid_paths if not path.endswith("polytonia.TextGrid")]
    )
    
    for transcript, textgrid in zip(transcript_paths, aligned_tgt_paths):
        mfa_tokens = [
            word.text for word in tgt.TextGrid(textgrid)["words"] if word.text != ""
        ]
        spacy_tokens = tokenize_text(transcript)
        
        print(f"FOR FILE {transcript}")
        print(f"MFA TOKENS:\n {len(mfa_tokens)}\n")
        print(f"SPACY TOKENS:\n {len(spacy_tokens)}\n")


def main():
    """
    Main function to handle the extraction process from the command line.
    """
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 extractWordPitchLevels.py /path/to/corpus")
    
    corpus_path = sys.argv[1]
    extract_words(corpus_path)


if __name__ == "__main__":
    main()
