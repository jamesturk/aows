# Comparing Parsing Libraries

When people talk about Python libraries for writing
web scrapers, they immediately think of [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/).

Nearly 20 years old, Beautiful Soup is one of the most well-established Python libraries out there. It's popular enough people were often surprised to find out that Open States didn't use it. We used [lxml](http://lxml.de/) instead, switching around the time of the somewhat fraught BeautifulSoup 4 transition. Over the years I developed my own opinions about the libraries, but for the purposes of this book wanted to check my own assumptions as well as the conventional wisdom about these libraries.

If you look on sites like Stack Overflow, the conventional wisdom is that Beautiful Soup is the most flexible, while lxml is much faster. Many of these answers are from about a decade ago though.

Furthermore, as of BS4, Beautiful Soup works as a wrapper around a number of different parsers. It's [documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser) explains how to pick a parser and offers some conventional wisdom about which you should pick. The default parser is [html.parser](https://docs.python.org/3/library/html.parser.html), which is part of the Python standard library. You can also use [lxml](http://lxml.de/) or html5lib.

There's also a much newer kid in town, [Selectolax](https://github.com/rushter/selectolax).

I wanted to take a look at these three libraries and their various parsing engines to see how they stack up against one another.

We'll try to answer questions like:

* Which library offers the nicest developer experience?
* With Beautiful Soup offering a wrapper around lxml, is there any reason to use lxml directly if you're using Beautiful Soup?
* Have Python speed improvements negated much of lxml's performance advantage?
* How does Selectolax stack up against the more established libraries?
* How much does the flexibility of the parsers differ in 2023? Is it worth the performance hit to use html5lib?

To explore these questions, we'll take a look at these libraries among a couple of dimensions:

* [Performance](./performance.md)
* [Parser Flexibility](./bad_html.md)
* [Ease of Use & Features](./features.md)