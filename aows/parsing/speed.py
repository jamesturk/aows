import pandas as pd
import seaborn as sns
import matplotlib as mpl
from matplotlib import pyplot as plt
import timeit
from .implementations import BSoup, Lxml, Selectolax, SelectoLexbor, Parsel

# TODO: regen graphs w/ count = 100, and normalize colors between runs (reordering parsel to last might do the trick)
methods = [
    ("load_dom", 5),
    ("links_natural", 100),
    ("links_css", 100),
    ("count_nodes", 100),
    ("extract_text", 100),
]


def run_all_benchmarks():
    implementations = [
        Lxml(),
        BSoup("html.parser"),
        BSoup("html5lib"),
        BSoup("lxml"),
        Selectolax(),
        SelectoLexbor(),
        Parsel(),
    ]
    runs = []
    for impl in implementations:
        impl.pre_parse()
        for example in impl.examples:
            for method, count in methods:
                if method in impl.skip:
                    continue
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

    print(f"\n\n## {method}")

    means = filtered.groupby("implementation").mean("average_time")
    # exclude near-zero values
    means = means[means.average_time > 0.000001]
    means["normalized"] = means["average_time"] / means["average_time"].min()
    means = means[["average_time", "normalized"]]
    print(means.to_markdown())

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
