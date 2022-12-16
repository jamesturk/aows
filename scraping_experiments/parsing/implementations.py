from abc import ABC, abstractmethod
import pathlib
import lxml.html
from bs4 import BeautifulSoup, Tag


class Base(ABC):
    examples = ["asha_bhosle", "html5test", "nba", "pyindex"]

    def __init__(self):
        self.html = {}
        for example in self.examples:
            self.html[example] = (
                pathlib.Path("testdata") / f"{example}.html"
            ).read_text()

    @abstractmethod
    def parse_dom(self, html):
        pass

    @abstractmethod
    def find_tags(self, tree, tag):
        pass

    @abstractmethod
    def all_nodes(self, tree):
        pass

    @abstractmethod
    def all_text(self, tree):
        pass

    def pre_parse(self):
        # Pre-parse the HTML to allow us to benchmark individual selections
        self.root = {}
        for name, html in self.html.items():
            self.root[name] = self.load_dom(name)

    def extract_text(self, example):
        nodes = self.find_tags(self.root[example], "ul")
        return "".join(self.all_text(node) for node in nodes)


class Lxml(Base):
    def parse_dom(self, html):
        return lxml.html.fromstring(html)

    def find_tags(self, tree, tag):
        return tree.xpath(f"//{tag}")

    def all_nodes(self, tree):
        return [e for e in tree.iter()]

    def all_text(self, tree):
        return tree.text_content()

    # benchmarks 1-5

    def load_dom(self, example):
        return lxml.html.fromstring(self.html[example])

    def links_natural(self, example):
        return self.root[example].xpath("//a/@href")

    def links_css(self, example):
        return self.root[example].cssselect("a[href]")

    def count_elements(self, example):
        elements = []

        def count(element):
            if isinstance(element, lxml.html.HtmlElement):
                elements.append(element.tag)
                for child in element.getchildren():
                    count(child)

        count(self.root[example])
        return elements
        # return list(self.root[example].iter())

    def __repr__(self):
        return "lxml.html"


class BSoup(Base):
    def __init__(self, parser):
        super().__init__()
        self.parser = parser

    def parse_dom(self, html):
        return BeautifulSoup(html, self.parser)

    def find_tags(self, tree, tag):
        return tree.find_all(tag)

    def all_nodes(self, tree):
        return [e for e in tree.recursiveChildGenerator() if isinstance(e, Tag)]

    def all_text(self, tree):
        return tree.get_text()

    # benchmarks 1-5

    def load_dom(self, example):
        return BeautifulSoup(self.html[example], self.parser)

    def links_natural(self, example):
        return self.root[example].find_all("a", href=True)

    def links_css(self, example):
        return self.root[example].select("a[href]")

    def count_elements(self, example):
        elements = []

        def count(element):
            if isinstance(element, Tag):
                elements.append(element.name)
                for child in getattr(element, "children", []):
                    count(child)

        count(self.root[example])
        return elements
        # return list(self.root[example].recursiveChildGenerator())

    def __repr__(self):
        return f"BeautifulSoup[{self.parser}]"
