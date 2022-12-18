import pandas as pd
import seaborn as sns
import matplotlib as mpl
from matplotlib import pyplot as plt
import timeit
from .implementations import BSoup, Lxml, Selectolax, SelectoLexbor

methods = [
    ("load_dom", 2),
    ("links_natural", 10),
    ("links_css", 10),
    ("count_elements", 10),
    ("extract_text", 10),
]


def run_all_benchmarks():
    implementations = [
        Lxml(),
        BSoup("html.parser"),
        BSoup("html5lib"),
        BSoup("lxml"),
        Selectolax(),
        SelectoLexbor(),
    ]
    runs = []
    for impl in implementations:
        impl.pre_parse()
        for example in impl.examples:
            for method, count in methods:
                time = timeit.timeit(
                    "method(example)",
                    globals={"method": getattr(impl, method), "example": example},
                    number=count,
                )
                if method == "load_dom":
                    # no length for load_dom
                    results = 1
                else:
                    results = len(getattr(impl, method)(example))
                runs.append(
                    {
                        "implementation": str(impl),
                        "example": example,
                        "method": method,
                        "average_time": time / count,
                        "count": count,
                        "results": results,
                    }
                )
    return pd.DataFrame(runs)


def show_results(df, method, examples=None):
    """
    Show relative times and overall graph for benchmark.
    """
    plt.clf()
    sns.set_theme()
    filtered = df[df.method == method]
    if examples:
        filtered = filtered.loc[(df.example.isin(examples))]
    ax = sns.barplot(filtered, x="example", y="average_time", hue="implementation")
    ax.set_ylabel("Avg. Time (s)")
    ax.set_xlabel("Example HTML")
    ax.set_title(f"{method} (runs={filtered['count'].iloc[0]})")
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))

    means = filtered.groupby("implementation").mean("average_time")
    means /= means.loc["lxml.html"]
    print(means)

    comparison = filtered[["implementation", "example", "results"]]
    comparison = comparison.pivot(
        index="example", columns="implementation", values="results"
    )
    print(comparison.to_markdown(index=True))

    # save image to file
    plt.savefig(
        f"docs/img/{method}.png",
        dpi=150,
        bbox_inches=mpl.transforms.Bbox([[0, 0], [8.3, 4.6]]),
    )


bdf = run_all_benchmarks()

for func, _ in methods:
    show_results(bdf, func, ["asha_bhosle", "pyindex"])
