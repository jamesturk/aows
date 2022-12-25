from abc import ABC, abstractmethod
import pathlib
import lxml.html
from bs4 import BeautifulSoup, Tag
from selectolax.parser import HTMLParser
from selectolax.lexbor import LexborHTMLParser
from parsel import Selector


class Base(ABC):
    examples = ["asha_bhosle", "html5test", "nba", "pyindex"]
    skip = []

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

    @abstractmethod
    def links_natural(self, example):
        pass

    @abstractmethod
    def links_css(self, example):
        pass

    @abstractmethod
    def get_href(self, node):
        pass

    def pre_parse(self):
        # Pre-parse the HTML to allow us to benchmark individual selections
        self.root = {}
        for name, html in self.html.items():
            self.root[name] = self.load_dom(name)

    def count_nodes(self, example):
        return self.all_nodes(self.root[example])

    def extract_text(self, example):
        nodes = self.find_tags(self.root[example], "ul")
        return "".join(self.all_text(node) for node in nodes)

    def load_dom(self, example):
        return self.parse_dom(self.html[example])


class Lxml(Base):
    def parse_dom(self, html):
        return lxml.html.fromstring(html)

    def find_tags(self, tree, tag):
        return tree.xpath(f"//{tag}")

    def all_nodes(self, tree):
        return [e for e in tree.iter()]

    def all_text(self, tree):
        return tree.text_content()

    def links_natural(self, example):
        return self.root[example].xpath("//a[@href]")

    def links_css(self, example):
        return self.root[example].cssselect("a[href]")

    def get_href(self, node):
        return node.attrib["href"]

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

    def links_natural(self, example):
        return self.root[example].find_all("a", href=True)

    def links_css(self, example):
        return self.root[example].select("a[href]")

    def get_href(self, node):
        return node.get("href")

    def __repr__(self):
        return f"BeautifulSoup[{self.parser}]"


class Selectolax(Base):
    def parse_dom(self, html):
        return HTMLParser(html)

    def find_tags(self, tree, tag):
        return tree.css(f"{tag}")

    def all_nodes(self, tree):
        return [e for e in tree.root.traverse()]

    def all_text(self, tree):
        return tree.text()

    def links_natural(self, example):
        return self.root[example].css("a[href]")

    def links_css(self, example):
        return self.root[example].css("a[href]")

    def get_href(self, node):
        return node.attributes["href"]

    def __repr__(self):
        return "Selectolax[modest]"


class SelectoLexbor(Selectolax):
    def parse_dom(self, html):
        return LexborHTMLParser(html)

    def __repr__(self):
        return "Selectolax[lexbor]"


class Parsel(Base):
    skip = ["extract_text", "count_elements"]

    def parse_dom(self, html):
        if isinstance(html, bytes):
            html = html.decode()
        return Selector(html)

    def find_tags(self, tree, tag):
        return tree.css(f"{tag}")

    def all_nodes(self, tree):
        return []
        # return [e for e in tree.xpath("./*")]

    def all_text(self, tree):
        # parsel's documentation shows a .text property but it didn't seem to work
        # and documentation is sparse. it seems the preferred method is to use
        # xpath or css for everything
        raise NotImplementedError()

    def links_natural(self, example):
        return self.root[example].xpath("//a[@href]")

    def links_css(self, example):
        return self.root[example].css("a[href]")

    def get_href(self, node):
        return node.attrib["href"]

    def __repr__(self):
        return "Parsel"
