import pandas as pd

CSV_PATH = "extreme_words.csv"

def main():
    df = pd.read_csv(CSV_PATH)
    colere = df.query("`LIWC` == 'colère' and `Persuasiveness` <= 3.0")
    colere.to_csv("low_high_words/colere_low.csv", index=False)

    bottom = df.query("`LIWC` == 'colère' and `Pitch` == 'B'")
    bottom.to_csv("low_high_words/bottom_colere.csv", index=False)

    juron = df.query("`LIWC` == 'juron' and `Pitch` == 'M'")
    juron.to_csv("low_high_words/juron_middle_highscore.csv", index=False)

    pronomimp = df.query("`LIWC` == 'pronomimp' and `Pitch` == 'B'")
    pronomimp.to_csv("low_high_words/pronomimp_mid.csv", index=False)


    print(df.query("`LIWC` == 'colère' and `Pitch` == 'H'"))
    

if __name__ == "__main__":
    main()
