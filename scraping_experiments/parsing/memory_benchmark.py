from .implementations import Lxml, BSoup
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

# lx = Lxml()
# bs_hp = BSoup("html.parser")
# bs_h5 = BSoup("html5lib")
# bs_lx = BSoup("lxml")

# example = "html5test"
# a = [lx.load_dom(example) for _ in range(100)]
# b = [bs_hp.load_dom(example) for _ in range(100)]
# c = [bs_h5.load_dom(example) for _ in range(100)]
# d = [bs_lx.load_dom(example) for _ in range(100)]


def draw_graph():
    # stats based on running above through memray
    memray_stats = [
        {"parser": "lxml", "example": "python", "mem": 16.8},
        {"parser": "BeautifulSoup[html.parser]", "example": "python", "mem": 38.2},
        {"parser": "BeautifulSoup[html5lib]", "example": "python", "mem": 38.3},
        {"parser": "BeautifulSoup[lxml]", "example": "python", "mem": 47.9},
        {"parser": "lxml", "example": "asha_bhosle", "mem": 19.4},
        {"parser": "BeautifulSoup[html.parser]", "example": "asha_bhosle", "mem": 55.3},
        {"parser": "BeautifulSoup[html5lib]", "example": "asha_bhosle", "mem": 55.3},
        {"parser": "BeautifulSoup[lxml]", "example": "asha_bhosle", "mem": 52.4},
        {"parser": "lxml", "example": "html5test x100", "mem": 8.3},
        {
            "parser": "BeautifulSoup[html.parser]",
            "example": "html5test x100",
            "mem": 14.2,
        },
        {"parser": "BeautifulSoup[html5lib]", "example": "html5test x100", "mem": 15.2},
        {"parser": "BeautifulSoup[lxml]", "example": "html5test x100", "mem": 19.6},
    ]

    df = pd.DataFrame(memray_stats)
    sns.set_theme()
    fig = sns.barplot(data=df, x="example", y="mem", hue="parser")
    fig.set_ylabel(r"Memory (MiB)")
    fig.set_xlabel("Example HTML")

    plt.title("Memory Comparison")
    plt.savefig(
        "img/memory_usage.png",
        dpi=200,
        #    bbox_inches=mpl.transforms.Bbox([[0, 0], [8.3, 4.6]]),
    )


draw_graph()
