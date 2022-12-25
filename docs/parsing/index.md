# Comparing Parsing Libraries

When people talk about Python libraries for writing web scrapers, they immediately think of [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/).  Nearly 20 years old, it is one of the most well-established Python libraries out there. 

It's popular enough that I find that people are often surprised to learn there are alternatives.  Personally, I switched to [lxml](http://lxml.de/) around the time of the somewhat fraught BeautifulSoup 4 transition and never really looked back. Part of my motivation for looking at these libraries is to see where they stack up in 2023.

If you look on sites like Stack Overflow, the conventional wisdom is that Beautiful Soup is the most flexible, while lxml is much faster. 
While I expect this is still true, I'm curious to see how much has changed in the last decade.

Furthermore, as of BS4, Beautiful Soup works as a wrapper around a number of different parsers. It's [documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser) explains how to pick a parser and offers some conventional wisdom about which you should pick. The default parser is [html.parser](https://docs.python.org/3/library/html.parser.html), which is part of the Python standard library. You can also use [lxml](http://lxml.de/) or html5lib.

There's also a much newer kid in town, [Selectolax](https://github.com/rushter/selectolax). It's a wrapper around a new open source HTML parsing library and claims to be faster than lxml.

In this section, we'll be taking a look at how these libraries stack up against one another.

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