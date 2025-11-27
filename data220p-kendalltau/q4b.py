import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Productivity_Rating.csv")
df = df[["clean_author_name", "score"]]

top10 = df.sort_values(by="score", ascending=False).head(10)
top10 = top10.iloc[::-1]

bars = plt.barh(top10["clean_author_name"], top10["score"])

plt.xlabel("Score")
plt.ylabel("Author")
plt.title("Top 10 Authors by Productivity")

for bar in bars:
    width = bar.get_width()
    plt.text(
        width - 0.1,
        bar.get_y() + bar.get_height() / 2,
        f"{width:.2f}",
        va="center",
        ha="left",
        fontsize=9
    )

plt.tight_layout()
plt.show()



# python -m venv venv