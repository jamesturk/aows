from abc import ABC, abstractmethod
import pathlib
import lxml.html
from bs4 import BeautifulSoup
import timeit


class Comparison(ABC):

    examples = ["asha_bhosle", "example", "nba", "python"]

    def __init__(self):
        self.html = {}
        for example in self.examples:
            self.html[example] = (
                pathlib.Path("testdata") / f"{example}.html"
            ).read_text()

    @abstractmethod
    def load_dom(self):
        pass


class Lxml(Comparison):
    def load_dom(self, example):
        return lxml.html.fromstring(self.html[example])

    def __repr__(self):
        return "lxml.html"


class BSoup(Comparison):
    def __init__(self, parser):
        super().__init__()
        self.parser = parser

    def load_dom(self, example):
        return BeautifulSoup(self.html[example], self.parser)

    def __repr__(self):
        return f"BeautifulSoup[{self.parser}]"


def run_speed_test(obj, method, number):
    for example in Comparison.examples:
        result = timeit.timeit(
            "method(example)",
            globals={"method": getattr(obj, method), "example": example},
            number=number,
        )
        print(obj, example, "\n", result)


ll = Lxml()
bs_hp = BSoup("html.parser")
bs_html5 = BSoup("html5lib")
bs_lxml = BSoup("lxml")

# run_speed_test(ll, "load_dom", 10)
# run_speed_test(bs_hp, "load_dom", 10)
run_speed_test(bs_html5, "load_dom", 10)
run_speed_test(bs_lxml, "load_dom", 10)

# ll.run_speed_test(ll.load_dom)
# bs.run_speed_test(bs.load_dom)
