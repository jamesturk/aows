# Comparing BeautifulSoup and lxml

The two main libraries for parsing HTML in Python are [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) and [lxml](http://lxml.de/).

Beautiful Soup is not actually a parser in itself, but a wrapper around a number of different parsers. It's [documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser) explains how to pick a parser.  The default parser is [html.parser](https://docs.python.org/3/library/html.parser.html), which is part of the Python standard library. You can also use [lxml](http://lxml.de/) or `html5lib`.

The conventional wisdom about these parsers is roughly:

| Parser | Language | Speed | How Lenient? |
| --- | --- | --- | --- |
| html.parser | C | Slow | Moderately |
| lxml | C | Fast | Moderately |
| html5lib | Python | Slowest | Extremely |

We'll take a look at real world examples to see how true this is.  
Also "lenient" is tough to define, so we'll look at how each parser handles some common HTML errors and see how big of a factor leniency plays.

We'll compare these along several dimensions:

* Speed
* Leniency
* Ease of Use
* Features
* Memory Usage

## Test Data & Environment

For the speed and memory usage tests I grabbed four sample pages:

* [Python Documentation Full Index](https://docs.python.org/3/genindex-all.html) - A fairly large page with lots of links.
* [List of 2021-22 NBA Transactions](https://en.wikipedia.org/wiki/List_of_2021%E2%80%9322_NBA_season_transactions) - A very large Wikipedia page with a huge table.
* [List of Hindi songs recorded by Asha Bhosle](https://en.wikipedia.org/wiki/List_of_Hindi_songs_recorded_by_Asha_Bhosle) - At the time of writing, the largest Wikipedia page.
* [HTML5 Test Page](https://html5test.com/index.html) - A moderately sized page with lots of HTML5 features.

All benchmarks were evaluated on my MacBook Pro (2021) with an Apple M1 Processor running Python 3.10.7.

## Speed Comparison

While it is generally true that scrapers are limited by the speed of the connection to the target website, the speed of different parsers can have a significant impact on the performance of your scraper.

Or perhaps you are working on a complex scraper, and decided it is a good idea to cache copies of the pages locally and run your scraper against those. This will allow you to test your scraper without having to wait for the target website to respond.
If you are using this strategy, you will quickly find that the speed of your scraper is now limited by the speed of your parser.

To test the speed of the parsers, I wrote a benchmarking script which you can see [here](#TODO).

### Benchmark #1 - Parsing HTML

The first benchmark simply parses the HTML of the four pages using each of the parsers.

lxml:
```python
root = lxml.html.fromstring(html)
```
BeautifulSoup:
```python
root = BeautifulSoup(html, 'lxml')
  # or 'html.parser' or 'html5lib'
```

![Parse Benchmark 1](speed-benchmark1.png)
![Parse Benchmark 2](speed-benchmark2.png)

You can see the relative speeds are fairly consistent between the four implementations.

As you can see, lxml is significantly faster than the others.  Even when BeautifulSoup is using lxml as the parser, it is about 10x slower than using lxml directly.

Relative Speeds:

| Parser | Speed |
| --- | --- |
| lxml | 1.0 |
| BeautifulSoup (lxml) | 10x |
| BeautifulSoup (html.parser) | 14x |
| BeautifulSoup (html5lib) | 33x |

### Benchmark #2 - Extracting Links

This benchmark uses a native method to extract all of the links from the pages.

lxml:

```python
links = root.xpath('//a/@href')
```

BeautifulSoup:

```python
links = root.find_all('a', href=True)
```

### Benchmark #3 - Extracting Links (CSS)

This benchmark uses CSS Selectors to extract all of the links from the pages.

lxml:

```python
links = root.cssselect('a[href]')
```

**Note: lxml does not support CSS Selectors natively.  It uses the [cssselect](https://pypi.org/project/cssselect/) library.  This library is written in Python and is not as fast as lxml's native XPath implementation.**

BeautifulSoup:

```python
# select all a tags with an href attribute
links = root.select('a[href]')
```

### Benchmark #4 - Counting Elements

For this benchmark we'll walk the DOM tree and count the number of elements.

lxml:

```python
count = 0
for _ in root.iter():
    count += 1
```

BeautifulSoup:

```python
count = 0
for _ in root.recursiveChildGenerator():
    count += 1
```

### Benchmark #5 - Extracting Text

Finally, we'll use each parser's built in text extraction function to extract the text from the pages.

lxml:

```python
text = root.text_content()
```

BeautifulSoup:

```python
text = root.get_text()
```
