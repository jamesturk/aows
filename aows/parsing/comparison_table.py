import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pages_per_second = {
    "lxml": 44,
    "BeautifulSoup[html.parser]": 5,
    "BeautifulSoup[html5lib]": 3,
    "BeautifulSoup[lxml]": 7,
    "Selectolax[modest]": 56,
    "Selectolax[lexbor]": 43,
}

max_rps = 91
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
# plt.plot(range(1, max_rps, 5), [50] * 18, "--", color="grey")
fig.set_ylabel(r"% of time in parser")
fig.set_xlabel("Requests per second")

plt.title("RPS vs. % of time in parser")
plt.savefig(
    "docs/img/rps_vs_time.png",
    dpi=150,
    #    bbox_inches=mpl.transforms.Bbox([[0, 0], [8.3, 4.6]]),
)
