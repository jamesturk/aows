# Comparing Parsing Libraries

When people talk about Python libraries for writing
web scrapers, [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) often comes up first.

It's popular enough people were often surprised to find out that Open States didn't use it. We used [lxml](http://lxml.de/) instead, switching around the time of the somewhat fraught BeautifulSoup 4 transition.

The conventional wisdom is that Beautiful Soup is the most flexible, while lxml is much faster, but the most popular Stack Overflow answers on the topic are from about a decade ago.

Furthermore, as of BS4, Beautiful Soup works as a wrapper around a number of different parsers. It's [documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser) explains how to pick a parser and offers some conventional wisdom about which you should pick. The default parser is [html.parser](https://docs.python.org/3/library/html.parser.html), which is part of the Python standard library. You can also use [lxml](http://lxml.de/) or html5lib.

There's also a much newer kid in town, while Beautiful Soup & lxml have been around for over a decade (as their websites might remind you), [Selectolax](https://github.com/rushter/selectolax) popped up in the last few years.

So in part, this experiment is to get a better sense for how these three libraries stack up against one another.

* How does the developer experience compare?
* With Beautiful Soup offering a wrapper around lxml, is there any reason to use lxml directly if you're using Beautiful Soup?
* Have Python speed improvements negated much of lxml's performance advantage?
* How does Selectolax fit into all this?
* How much does the flexibility of the parsers differ in 2023? Is it worth the performance hit to use html5lib?

To explore these questions, we'll take a look at these libraries among a couple of dimensions:

* [Performance](./performance.md)
* [Parser Flexibility](./bad_html.md)
* [Ease of Use & Features](./features.md)