import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pages_per_second = {
    "lxml": 104,
    "BeautifulSoup[html.parser]": 14,
    "BeautifulSoup[html5lib]": 7,
    "BeautifulSoup[lxml]": 19,
}

max_rps = 126
rows = []
for pages in (11824,):
    for parser, pps in pages_per_second.items():
        for rps in range(1, max_rps, 5):
            time_in_request = pages / rps
            time_in_scrape = pages / pps
            total_time = time_in_request + time_in_scrape
            pct_in_scrape = time_in_scrape / total_time * 100
            pct_in_request = time_in_request / total_time * 100
            rows.append(
                {
                    "time_in_request": time_in_request,
                    "time_in_scrape": time_in_scrape,
                    "pct_in_scrape": pct_in_scrape,
                    "pct_in_request": pct_in_request,
                    "rps": rps,
                    "parser": parser,
                }
            )


df = pd.DataFrame(rows)
sns.set_theme()
fig = sns.lineplot(data=df, x="rps", y="pct_in_scrape", hue="parser")
plt.plot(range(1, max_rps, 5), [50] * 25, "--", color="grey")
fig.set_ylabel(r"% of time in parser")
fig.set_xlabel("Requests per second")

plt.title("RPS vs. % of time in parser")
plt.savefig(
    f"img/rps_vs_time.png",
    dpi=150,
    #    bbox_inches=mpl.transforms.Bbox([[0, 0], [8.3, 4.6]]),
)
