import pandas as pd
import itertools

# load ranking function
def load_ranking(csv_path, name_col="university_name", rank_col="ranking"):
    df = pd.read_csv(csv_path)
    return dict(zip(df[name_col], df[rank_col]))

# kendall tau math function
def kendall_tau(rank1, rank2):
    # init counters
    concordant = 0
    discordant = 0
    
    # uni union
    universities = set(rank1) | set(rank2)

    # assign missing rank values to bottom
    max_rank1 = max(rank1.values()) + 1
    max_rank2 = max(rank2.values()) + 1

    # extract rank from uni list
    def r1(u): 
        return rank1.get(u, max_rank1 + 1)
    def r2(u): 
        return rank2.get(u, max_rank2 + 1)

    # calc tau
    for u, v in itertools.combinations(universities, 2):
        rank1_u, rank1_v = r1(u), r1(v)
        rank2_u, rank2_v = r2(u), r2(v)

        if ((rank1_u < rank1_v) and (rank2_u < rank2_v)) or ((rank1_u > rank1_v) and (rank2_u > rank2_v)) or ((rank1_u == rank1_v) and (rank2_u == rank2_v)):
            concordant += 1
        else:
            discordant += 1

    n = len(universities)
    tau = (concordant - discordant) / (n * (n - 1) / 2)
    return tau

# load rankings from sql output
excellence = load_ranking("excellence.csv")
balanced = load_ranking("balanced.csv")
productivity = load_ranking("productivity.csv")

# load usnews rankings from sample data
usnews_df = pd.read_csv("usnews.csv")
usnews_df = usnews_df[usnews_df["rank"] <= 52]
usnews = dict(zip(usnews_df["university_name"], usnews_df["rank"]))

# print results
print("US News vs. Excellence:", kendall_tau(excellence, usnews))
print("US News vs. Balanced:", kendall_tau(balanced, usnews))
print("US News vs. Productivity:", kendall_tau(productivity, usnews))