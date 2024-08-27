import pandas as pd 

LIWC_PATH = "LIWCperWORD_normalized.csv"
PITCH_PATH = "pitch_words.csv"

liwc_df = pd.read_csv(LIWC_PATH)
pitch_df = pd.read_csv(PITCH_PATH)

merged = pd.merge(pitch_df, liwc_df, on=["clip"], how="inner")
merged.to_csv("merged_vectors.csv", index=False)
