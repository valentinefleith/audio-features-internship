import pandas as pd
import argparse


def main(part, method):
    csv_file = pd.read_csv(
        f"data_exploration/new_csvfiles/{part}/{part[:3].upper()}_{method}.csv", sep=";"
    )
    gender = pd.read_csv("data_exploration/MT_gender.csv", sep=";")
    scores_with_gender = csv_file.set_index("Input.name").join(gender.set_index("ID"))
    women_scores = scores_with_gender.query("`H/F` == 'F'")
    men_scores = scores_with_gender.query("`H/F` == 'H'")
    women_scores.to_csv(
        f"data_exploration/new_csvfiles/{part}/{part[:3].upper()}_{method}_F.csv",
        sep=";",
    )
    men_scores.to_csv(
        f"data_exploration/new_csvfiles/{part}/{part[:3].upper()}_{method}_H.csv",
        sep=";",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--part", choices=["beginning", "middle", "end", "full"])
    parser.add_argument(
        "-m", "--aggregation_method", choices=["mean", "rms", "hmeans"], required=True
    )
    args = parser.parse_args()
    if args.part is None:
        args.part = "full"

    main(args.part, args.aggregation_method)
