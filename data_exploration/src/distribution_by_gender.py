import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_distribution(men_scores, women_scores, dimension):
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    sns.histplot(women_scores[f"Answer.{dimension.title()}"], kde=True)
    plt.title(f"Distribution of Women scores for {dimension}.")
    plt.subplot(1, 2, 2)
    sns.histplot(men_scores[f"Answer.{dimension.title()}"], kde=True)
    plt.title(f"Distribution of Men scores for {dimension}.")
    plt.tight_layout()
    plt.show()


def main(method, part):
    dimension = ["persuasiveness", "engagement"]
    women_scores = pd.read_csv(f"data_exploration/new_csvfiles/{part}/{part[:3].upper()}_{method}_F.csv", sep=";")
    men_scores = pd.read_csv(f"data_exploration/new_csvfiles/{part}/{part[:3].upper()}_{method}_H.csv", sep=";")
    for dim in dimension:
        plot_distribution(men_scores, women_scores, dim)
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--aggregation_method", choices=["mean", "rms", "hmeans"])
    parser.add_argument("-p", "--part", choices=["beginning", "middle", "end"])
    # parser.add_argument(
    #     "-c",
    #     "--dimension",
    #     choices=["competence", "engagement", "persuasiveness", "global"],
    # )
    args = parser.parse_args()
    if args.aggregation_method is None:
        args.aggregation_method = "rms"
    if args.part is None:
        args.part = "full"
    # if args.dimension is None:
    #     args.dimension = "persuasiveness"
    main(method=args.aggregation_method, part=args.part)
