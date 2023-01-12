import pandas as pd
import seaborn as sns
import matplotlib as mpl
from matplotlib import pyplot as plt

from .implementations import Lxml, BSoup, Parsel, Selectolax, SelectoLexbor


def load_examples(example, N):
    lx = Lxml()
    bs_hp = BSoup("html.parser")
    bs_h5 = BSoup("html5lib")
    bs_lx = BSoup("lxml")
    parsel = Parsel()
    selectolax = Selectolax()
    selectolexbor = SelectoLexbor()

    lx_res = [lx.load_dom(example) for _ in range(N)]
    bs_hp_res = [bs_hp.load_dom(example) for _ in range(N)]
    bs_h5_res = [bs_h5.load_dom(example) for _ in range(N)]
    bs_lx_res = [bs_lx.load_dom(example) for _ in range(N)]
    parsel_res = [parsel.load_dom(example) for _ in range(N)]
    slax_res = [selectolax.load_dom(example) for _ in range(N)]
    slex_res = [selectolexbor.load_dom(example) for _ in range(N)]


def draw_graph():
    # stats based on running above through memray
    memray_stats = [
        # pyindex
        {"parser": "lxml", "example": "pyindex", "mem": 14.9},
        {"parser": "BeautifulSoup[html.parser]", "example": "pyindex", "mem": 39.2},
        {"parser": "BeautifulSoup[html5lib]", "example": "pyindex", "mem": 38.3},
        {"parser": "BeautifulSoup[lxml]", "example": "pyindex", "mem": 48.4},
        {"parser": "parsel", "example": "pyindex", "mem": 14.9},
        {"parser": "selectolax[modest]", "example": "pyindex", "mem": 28.1},
        {"parser": "selectolax[lexbor]", "example": "pyindex", "mem": 20.5},
        # pyindex x 10
        # {"parser": "lxml", "example": "pyindex x 10", "mem": 148.1},
        # {
        #     "parser": "BeautifulSoup[html.parser]",
        #     "example": "pyindex x 10",
        #     "mem": 388.9,
        # },
        # {"parser": "BeautifulSoup[html5lib]", "example": "pyindex x 10", "mem": 383.9},
        # {"parser": "BeautifulSoup[lxml]", "example": "pyindex x 10", "mem": 482.1},
        # {"parser": "parsel", "example": "pyindex x 10", "mem": 152.5},
        # {"parser": "selectolax[modest]", "example": "pyindex x 10", "mem": 281.2},
        # {"parser": "selectolax[lexbor]", "example": "pyindex x 10", "mem": 205.3},
        # asha_bhosle
        {"parser": "lxml", "example": "asha_bhosle", "mem": 15.3},
        {"parser": "BeautifulSoup[html.parser]", "example": "asha_bhosle", "mem": 41.2},
        {"parser": "BeautifulSoup[html5lib]", "example": "asha_bhosle", "mem": 41.2},
        {"parser": "BeautifulSoup[lxml]", "example": "asha_bhosle", "mem": 51.3},
        {"parser": "parsel", "example": "asha_bhosle", "mem": 17.4},
        {"parser": "selectolax[modest]", "example": "asha_bhosle", "mem": 29.1},
        {"parser": "selectolax[lexbor]", "example": "asha_bhosle", "mem": 20.2},
        # html5test x 10
        {"parser": "lxml", "example": "html5test x10", "mem": 2.0},
        {
            "parser": "BeautifulSoup[html.parser]",
            "example": "html5test x10",
            "mem": 1.1,
        },
        {"parser": "BeautifulSoup[html5lib]", "example": "html5test x10", "mem": 2.3},
        {"parser": "BeautifulSoup[lxml]", "example": "html5test x10", "mem": 2.0},
        {"parser": "parsel", "example": "html5test x10", "mem": 0.9},
        {"parser": "selectolax[lexbor]", "example": "html5test x10", "mem": 10.7},
        {"parser": "selectolax[modest]", "example": "html5test x10", "mem": 11.1},
        # html5test x 100
        {"parser": "lxml", "example": "html5test x100", "mem": 8.3},
        {
            "parser": "BeautifulSoup[html.parser]",
            "example": "html5test x100",
            "mem": 14.2,
        },
        {"parser": "BeautifulSoup[html5lib]", "example": "html5test x100", "mem": 15.2},
        {"parser": "BeautifulSoup[lxml]", "example": "html5test x100", "mem": 19.6},
        {"parser": "parsel", "example": "html5test x100", "mem": 8.6},
        {"parser": "selectolax[lexbor]", "example": "html5test x100", "mem": 111},
        {"parser": "selectolax[modest]", "example": "html5test x100", "mem": 107},
    ]

    df = pd.DataFrame(memray_stats)
    sns.set_theme()
    fig = sns.barplot(data=df, x="example", y="mem", hue="parser")
    fig.set_ylabel(r"Memory (MiB)")
    fig.set_xlabel("Example HTML")
    sns.move_legend(fig, "upper left", bbox_to_anchor=(1, 1))

    plt.title("Memory Comparison")
    plt.savefig(
        "docs/img/memory_usage.png",
        dpi=200,
        bbox_inches=mpl.transforms.Bbox([[0, 0], [8.3, 4.6]]),
    )


load_examples(example="html5test", N=1)
# draw_graph()
