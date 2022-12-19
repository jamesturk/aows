# Parsing: Performance

## Speed Comparison

It makes sense to acknowledge that speed is rarely the most important part of choosing a scraping library. While it is generally true that scrapers are limited by the speed of the connection to the target website, the speed of different parsers can have a significant impact on the performance of your scraper.

### #1 - Parsing HTML

The initial parse of the HTML is likely the most expensive part of the scraping process. This benchmark measures the time it takes to parse the HTML using each library.

#### Code

=== "lxml.html"

    ```python
    root = lxml.html.fromstring(html)
    ```
=== "BeautifulSoup"

    ```python
    root = BeautifulSoup(html, 'lxml')
      # or 'html.parser' or 'html5lib'
    ```
=== "Selectolax"

    ```python
    root = selectolax.parser.HTMLParser(html)
    # or selectolax.lexbor.LexborParser(html)
    ```
=== "Parsel"

    ```python
    root = parsel.Selector(html)
    ```

#### Results

![load_dom](/img/load_dom.png)

| implementation             |   average_time |   normalized |
|:---------------------------|---------------:|-------------:|
| lxml.html                  |      0.09 s    |      4x      |
| Parsel                     |      0.09 s    |      4x      |
| BeautifulSoup[html.parser] |      1.27 s    |     51x      |
| BeautifulSoup[html5lib]    |      2.47 s    |     98x      |
| BeautifulSoup[lxml]        |      0.92 s    |     37x      |
| Selectolax[modest]         |      0.03 s    |      1x      |
| Selectolax[lexbor]         |      0.02 s    |      1x      |

Selectolax is the winner here, both engines performed about 4x faster than lxml.html.
Parsel, as expected, was about the same speed as lxml.html since it is a thin wrapper around it.
BeautifulSoup was much slower, even when using lxml as the parser, it was about 10x slower than lxml.html alone. `html5lib` was about 20x slower than lxml.html, and nearly 100x slower than Selectolax.

#### Aside: Smaller Pages

In an earlier draft of the benchmarks, I used a smaller page to test the parsers.  The results were similar, but not as dramatic:

![](/img/graph2-load_dom-html5test.png)

Taking a look at a graph with just html5test, it is clear the relative speeds are about the same between the different test pages.

Parsing this page is so much faster than the larger more complex pages used for the rest of the tests that it basically disappeared on all graphs.

### #2 - Extracting Links

This benchmark uses each library to find all `<a>` tags with an `href` attribute.  This is a common task for scrapers and given the number of links on the two test pages, should be a good test of the libraries capabilities. The libraries have different ways of doing this, so I used the most natural way for each library based on their documentation.

#### Code

=== "lxml.html"

    ```python
    # in lxml, XPath is the native way to do this
    links = root.xpath('//a[@href]')
    ```
=== "BeautifulSoup"

    ```python
    # in BeautifulSoup, you'd typically use find_all
    links = root.find_all('a', href=True)
    ```
=== "Selectolax"

    ```python
    # Selectolax is essentially a CSS Selector implementation
    links = root.css('a[href]')
    ```
=== "Parsel"

    ```python
    # Parsel is a wrapper around lxml, so we'll use xpath
    links = root.xpath('//a[@href]')
    ```

#### Results

![links_natural](/img/links_natural.png)

| implementation             |   average_time |   normalized |
|:---------------------------|---------------:|-------------:|
| lxml.html                  |     0.0241     |     11x      |
| Parsel                     |     0.0469     |     21x      |
| BeautifulSoup[html.parser] |     0.0999     |     44x      |
| BeautifulSoup[html5lib]    |     0.0998     |     45x      |
| BeautifulSoup[lxml]        |     0.101      |     44x      |
| Selectolax[modest]         |     0.00228    |      1x      |
| Selectolax[lexbor]         |     0.00236    |      1x      |

Once again, Selectolax is in the lead. `lxml` and `parsel` are close, with `parsel`'s overhead adding a bit of time. `BeautifulSoup` is again very slow, it looks to be essentially the same speed regardless of parser. This suggests that once the DOM is parsed, BeautifulSoup is using its native methods for finding nodes, making it slower than a wrapper like `parsel` that takes advantage of `lxml`'s underlying speed.

Furthermore, the three BeautifulSoup implementations are virtually identical in speed. This was interesting, it looks like BeautifulSoup is likely using its own implementation of `find_all` instead of taking advantage of lxml's faster alternatives.

(It was verified that all implementations gave the same count of links.)

### #3 - Extracting Links (CSS)

I wanted to take a look at another way of getting the same data, in part to see if it'd level the playing field at all. Not all of the libraries support the same features, but all do support CSS selectors. We'll be querying for the same data as before, but this time with CSS selectors.

!!! tip
    For lxml to support this feature, it needs the [cssselect](https://pypi.org/project/cssselect/) library installed.

#### Code

=== "lxml.html"

    ```python
    links = root.cssselect('a[href]')
    ```
=== "BeautifulSoup"

    ```python
    links = root.select('a[href]')
    ```
=== "Selectolax" 

    ```python
    links = root.css('a[href]')
    ```
=== "Parsel"

    ```python
    links = root.css('a[href]')
    ```

#### Results

![links_css](/img/links_css.png)

| implementation             |   average_time |   normalized |
|:---------------------------|---------------:|-------------:|
| lxml.html                  |     0.0176     |      8x  |
| Parsel                     |     0.0397     |     19x  |
| BeautifulSoup[html.parser] |     0.181      |     86x  |
| BeautifulSoup[html5lib]    |     0.207      |     99x  |
| BeautifulSoup[lxml]        |     0.183      |     88x  |
| Selectolax[modest]         |     0.00210    |      1x  |
| Selectolax[lexbor]         |     0.00233    |      1x  |

These results didn't change much, the main difference is that `BeautifulSoup` got about twice as slow.

This did show that CSS Selectors are just as fast in lxml as XPath which is good news if you prefer using them.

(It was verified that all implementations gave the same count of links.)

### #4 - Counting Elements

For this benchmark we'll walk the DOM tree and count the number of elements.  DOM Traversal is just about the worst way to get data out of HTML, but sometimes it is necessary.

!!! tip
    `parsel` doesn't support direct DOM traversal.  It is possible to get child elements using XPath or CSS selectors, but it is drastically slower
    and didn't feel like a fair comparison since it isn't an intended use case.

    It is also possible to use `parsel` to get the underlying `lxml` object and use that to traverse the DOM. If you are using `parsel` 
    and need to do DOM traversal, this is the recommended approach.

#### Code 

=== "lxml.html"

    ```python
    all_elements = [e for e in root.iter()]
    ```
=== "BeautifulSoup"

    ```python
    # BeautifulSoup includes text nodes, which need to be excluded
    all_elements = [e for e in root.recursiveChildGenerator() if isinstance(e, Tag)]
    ```
=== "Selectolax"

    ```python
    all_elements = [e for e in root.iter()]
    ```

=== "Parsel"

    ```python
    # Parsel doesn't support DOM traversal, but here's an 
    # example of how to get the underlying lxml object
    all_elements = [e for e in root.root.iter()]
    ```

#### Results

![](/img/count_elements.png)

| implementation             |   average_time |   normalized |
|:---------------------------|---------------:|-------------:|
| lxml.html                  |      0.0281    |      1.3x   |
| BeautifulSoup[html.parser] |      0.0229    |      1.1x   |
| BeautifulSoup[html5lib]    |      0.0248    |      1.2x   |
| BeautifulSoup[lxml]        |      0.0221    |      1.04x  |
| Selectolax[modest]         |      0.0212    |      1.0x   |
| Selectolax[lexbor]         |      0.0239    |      1.1x   |

The variance here is the lowest of any of the benchmarks.  All implementations need to do roughly the same work, traversing an already-built tree of HTML nodes in Python. `lxml.html` is actually the slowest here, but it seems unlikely node-traversal will be a bottleneck in any case.

### #5 - Extracting Text

For this benchmark, we'll use each parser's built in text extraction function to extract the text from the pages.
These functions extract all of the text from a node and it's descendants and are useful for things like extracting large blocks of plain text with some markup.

!!! tip
    `parsel` does not have an equivalent function, favoring a different approach to text extraction.

These methods are used to extract all of the text from a block of HTML. This is useful for things like extracting large blocks of plain text with some markup.

For this benchmark in particular, we'll extract text from each of the `<ul>` tags on the page.

#### Code

=== "lxml.html"

    ```python
    uls = root.xpath('//ul')
    text = "".join([ul.text_content() for ul in uls])
    ```
=== "BeautifulSoup"

    ```python
    uls = root.find_all('ul')
    text = "".join([ul.get_text() for ul in uls])
    ```

=== "Selectolax"

    ```python
    uls = root.css('ul')
    text = "".join([ul.text() for ul in uls])
    ```

#### Results

![](/img/extract_text.png)

| implementation             |   average_time |   normalized |
|:---------------------------|---------------:|-------------:|
| lxml.html                  |     0.00938    |      1x      |
| BeautifulSoup[html.parser] |     0.0508     |      5x  |
| BeautifulSoup[html5lib]    |     0.0536     |      6x |
| BeautifulSoup[lxml]        |     0.0506     |      5x |
| Selectolax[modest]         |     0.0250     |      3x |
| Selectolax[lexbor]         |     0.0237     |      2x |

Here `lxml` is the clear winner.  With fewer `<ul>` elements on the page, `selectolax` keeps up, but with the pyindex example the difference becomes more clear.

Additionally, BeautifulSoup[html.parser] and BeautifulSoup[lxml] get different results than the rest:

| Libraries | Size of result for 'asha_bhosle' | Size of result for 'pyindex' |
|:----------|---------------------------------:|-----------------------------:|
| lxml.html, html5lib, and selectolax | 2,282 | 740,069 |
| BeautifulSoup[html.parser] and BeautifulSoup[lxml] | 2,270 | 565,339 |

This is a surprising result, and I'm not sure what's going on here yet.

I'd expected different parse trees, but `html5lib`
For the pyindex example it is notable that html5lib and lxml.html are finding about 200,000 more characters than the other parsers.
It's also quite strange that BeautifulSoup's lxml parser is finding the same number of characters as the html.parser, and not `lxml.html`.

I expect the next section where we look at flexibility will shed some light on this.

### #6 - "Real World"

So far we've been looking at very simple benchmarks of common methods. It seems clear that lxml.html is the fastest, but how much would that speed matter in a real world scenario?

To simulate a real world scrape, we'll compose a scrape from the pieces we've already done:

1) Parse the [Python documentation index](https://docs.python.org/3/genindex-all.html) as a start page.
2) For each link on the page, parse the page the link points to.  (Note: The index contains many links to the same page, we'll parse each page each time it is encountered to simulate having many more actual pages.)
3) On each of those pages, we'll perform 3 tasks:
  a) Extract the text from the root element.
  b) Count the number of elements on the page by walking the DOM.
  c) Count the spans on the page using CSS selectors.

This is a fair simulacrum of the work that a real scrape would do. All in all our mock scrape hits 11,824 pages, a moderately sized scrape.

And of course, as before, all of this will be done using local files so no actual network requests will be made. An initial run will warm an in-memory cache, so disk I/O will not be a factor either.

The results were interesting, after a sample run to warm the cache, the results looked like:

| Parser                      | Time (s) | Pages/s |
| --------------------------- | -------- | --------|
| lxml                        | 114  | 104 |
| BeautifulSoup\[html.parser] | 824  | 14 |
| BeautifulSoup\[html5lib]    | 1,728 | 7 |
| BeautifulSoup\[lxml]        | 623  | 19 |

For a moderate-sized scrape like this one, lxml.html is about 7x faster than BeautifulSoup's html.parser.

That said, notice that in each case, the number of pages per second is higher than 1.  A common wait time between requests is 1 second. This means that in each case, we'd be spending more time waiting for requests than actually parsing pages.

So does this mean the speed of a parser doesn't matter? Not at all.

What if you were able to make 20 requests per second?  At that point, only lxml.html could keep up.

Let's take a look at how this plays out as we increase the number of requests per second:

![](/img/rps_vs_time.png)

So, as we increase the number of requests per second, lxml.html is the only parser that can keep up with our hypothetical scrape.

## Memory Comparison

Finally, let's take a look at how much memory each parser uses while handling the following files:

| Example | Bytes | Tags | 
| ------- | ----- | ---- |
| asha_bhosle | 1,132,673 | ~38,450 |
| pyindex | 1,683,137 | ~34,950 |
| html5test | 18,992 | 218 |

This is somewhat difficult to measure, as the memory usage of an object is not easily accessible from Python.  I used [memray](https://github.com/bloomberg/memray) to measure a sample piece of code that loaded each parser and parsed the sample pages.  To compare the memory usage between complex pages and simple pages, the sample code also loaded the html5test page 100 times.

![](/img/memory_usage.png)

One thing to note is that the memory usage seems to be correlated to complexity (i.e. number of tags), which makes sense.

Again, lxml.html is the clear winner here, using less than half the memory of the other parsers.

## Conclusion

One one hand, performance isn't going to make or break your scrape.  If you're scraping a small number of pages, or are dealing with a slow site or rate limit, the difference between the fastest and slowest parsers is going to be negligible.

In practice, the real payoffs of using a faster parser are going to be felt the most during development of larger scrapers. If you're using a local cache while scraping (and I hope you are), your requests per second are nearly limitless.  This means that the speed of your parser is going to be the limiting factor in how fast you can iterate on your scrape.

In a 1,000 page scrape from cache of pages similar to our final benchmark, a full trial run would take less than 15 seconds while a full trial run with `html5lib.parser` would take nearly 3 minutes.  At 10,000 pages the difference between the shortest and longest is almost half an hour.

Memory usage might also matter to you, if you are running your scraper on a small VPS or have unusually complex pages, memory usage could be a factor and that's another place where `lxml.html` shines.

Next time, we'll take a look at how flexible each parser is, and how that affects your scrape.

## Notes

All benchmarks were evaluated on a 2021 MacBook Pro with an Apple M1 Pro.

| Component | Version |
| --------- | ------- |
| Python | 3.10.7 (installed via pyenv) |
| BeautifulSoup | 4.11.1 |
| cchardet  |  2.1.7 | 
| cssselect |  1.2.0 |
| html5lib | 1.1 |
| lxml | 4.9.1 |
| selectolax | 0.3.11| 

According to the [Beautiful Soup docs](https://beautiful-soup-4.readthedocs.io/en/latest/#improving-performance) installing `cchardet` is recommended for performance. These tests were run with `cchardet` installed to ensure a fair comparison, though it did not make a noticable difference in performance.

The sample pages referenced in the benchmarks are:

* [Python Documentation Full Index](https://docs.python.org/3/genindex-all.html) - A fairly large page with lots of links.
* [List of 2021-22 NBA Transactions](https://en.wikipedia.org/wiki/List_of_2021%E2%80%9322_NBA_season_transactions) - A very large Wikipedia page with a huge table.
* [List of Hindi songs recorded by Asha Bhosle](https://en.wikipedia.org/wiki/List_of_Hindi_songs_recorded_by_Asha_Bhosle) - At the time of writing, the largest Wikipedia page.
* [HTML5 Test Page](https://html5test.com/index.html) - A moderately sized page with lots of HTML5 features.

All source code for these experiments is in [scraping-experiments](https://github.com/jamesturk/scraping-experiments/).