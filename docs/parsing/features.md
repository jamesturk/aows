# Parsing: Developer Experience

When it comes to writing resilient scrapers, the developer experience is perhaps the most important dimension.
A nice, clean, and consistent API is an important factor in the cleanliness & readability of your scraper code.

We'll compare the experience by looking at a few aspects of the developer experience:

* Features
* Documentation
* Common Tasks Compared

| Library | Stars (Dec 2022) | 
| --- | --- |
| [lxml](https://lxml.de/) | [2.2k](https://github.com/lxml/lxml) |
| [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) | ✳ |
| [selectolax](https://github.com/rushter/selectolax) | ~850 |
| [parsel](https://github.com/scrapy/parsel) | ~700 |

✳ BeautifulSoup is developed [on Launchpad](https://code.launchpad.net/beautifulsoup) not GitHub.

All of the libraries are permissively licensed (either MIT or BSD).

## Feature Comparison

These libraries are all perfectly capable libraries, each provides HTML parsing as well as various selection mechanisms to extract content from the DOM.

The main differences among them are which methods they provide for selecting nodes, and how they handle text extraction:

| Library | XPath | CSS | DOM Traversal API | Text Extraction | 
| --- | --- | --- | --- | --- |
| `lxml` | ✅ | ✅ ✳ | ✅ | ✅ |
| `BeautifulSoup` | ❌ | ✅ | ✅ | ✅ |
| `selectolax` | ❌ | ✅ | ✅ | ✅ |
| `parsel` | ✅ | ✅ | ❌ | ❌ |

!!! tip

    ✳ `cssselect` must be installed separately but augments lxml.html

### Pluggable Parsers

`lxml` and `BeautifulSoup` both have parsers and Node APIs that are separate from one another.  It is technically possible to use `lxml.html`'s parser with BeautifulSoup's Node API, or vice versa.  Additionally, `selectolax` allows choosing between two different backend parsers.

This isn't going to factor into feature comparisons, since each supported parser is equally capable and we'll be looking at speed & flexibility in other sections.

Having pluggable parsers is a nice feature, but as we'll see in the rest of this comparison, it might not be as useful as it sounds.

### Selectors

`lxml` is an XML-first library, and as such supports XPath. It also supports the ElementTree API, which is a DOM traversal API. It also supports CSS selectors, but you must install `cssselect` separately.

`parsel`, mostly a wrapper around `lxml`, also supports XPath and CSS selectors treating both as equal. It does not expose a DOM traversal API of its own.

`BeautifulSoup` has a custom selector API, and also supports CSS selectors since 4.0.

`selectolax` is CSS-first, but also has methods for directly traversing the DOM.

### Attribute Access

A common feature among all libraries is dictionary-like attribute access on nodes.

TODO: example

### Text Extraction

[selectolax's text extraction](https://selectolax.readthedocs.io/en/latest/parser.html#selectolax.parser.HTMLParser.merge_text_nodes) seems the most sophisticated. It's [`text`](https://selectolax.readthedocs.io/en/latest/parser.html#selectolax.parser.HTMLParser.text) function has convinient parameters to strip text and opt between including text from child nodes or not.

On the other end of the spectrum, `parsel`'s text extraction is very limited. As noted in it's exclusion from the [Extracting Text Benchmark](parsing/performance/#5-extracting-text), it lacks a native function to do this work. Of course, you can access the underlying `lxml` object and use it's `text_content` method, but this is not a very clean solution and would break if `parsel` ever switched to a different underlying library, which has at least been discussed.

## Complexity

At their core, all of these APIs provide a method to parse a string of HTML, and then a node API. One measure of complexity is taking a look at what methods and properties are available on each library's node type.

| Library | Class Name | Methods | Public Properties |
| --- | --- | --- | --- |
| `BeautifulSoup` | `bs4.element.Tag` | 69 | 39 | 
| `lxml` | `lxml.html.HtmlElement` | 43 | 15 |
| `parsel` | `parsel.selector.Selector` | 11 | 6 |
| `selectolax` | `selectolax.parser.Node` | 11 | 21 |

This is a somewhat arbitrary measure, but illustrates that `parsel` and `selectolax` are concise APIs, perhaps at the cost of some functionality.

## Documentation

[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) has very comprehensive documentation. It has a nice [quick start guide](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#quick-start) and then detailed examples of its numerous features. One thing that becomes obvious when comparing it to the others is that it has a lot of features, it has a large API for modifying the tree, and dozens of methods for various types of navigation (e.g. `next_sibling`, `next_siblings`, `next_element`, `next_elements` all exist, with the same for `previous` and each being slightly different from its peers).

As the most widely-used there's also the advantage of a large community of users and a lot of examples online, but I'd temper that by noting that a large number of examples are old and use outdated APIs.

[lxml](https://lxml.de/) also has incredibly detailed documentation. The documentation site covers all of the features of `lxml`, which is a large library that contains many features unrelated to HTML parsing. It can be useful to limit your search to the [lxml.html](https://lxml.de/lxmlhtml.html) module, which is the module that contains the HTML parsing features.

Though you may need to look at other parts of the documentation to understand some of the concepts, the documentation for `lxml.html` is fairly concise and covers most of what you'd need to know.

[parsel](https://parsel.readthedocs.io/en/latest/) has a very concise API, and the documentation reflects that. Consisting primarily of a [Usage page](https://parsel.readthedocs.io/en/latest/usage.html) and an [API reference](https://parsel.readthedocs.io/en/latest/parsel.html).

The documentation would probably benefit from more examples, especially since parsel's small API might leave some users wondering where features they've come to rely upon in other libraries are. A few more examples of how to replicate common tasks in other libraries would be helpful.

[selectolax](https://selectolax.readthedocs.io/en/latest/) is another very small API. Like `parsel` it mainly concerns itself with a small set of methods and properties available on a node type. The documentation is purely-module based and does not include any kind of tutorial or usage guide.

## Conclusions

Each library has it's advantages and disadvantages.

### `BeautifulSoup`

As the most widely used library, it is easy to find examples and documentation online.  Very feature-rich, including features like DOM modification outside the scope of this comparison.

The API is large and can be confusing to new users, with the often favored node-search based approach being very specific to BeautifulSoup as opposed to things like XPath & CSS selectors that are more broadly used in scrapers.

In many ways `BeautifulSoup` feels like a victim of its own success. It has a lot of legacy code and features that are no longer as relevant, but I'd imagine the sheer number of users makes it difficult to make breaking changes even if the author's wanted to.

### `lxml`

A powerful & underrated library, `lxml.html` wins major points for being the only one to support XPath and CSS selectors natively. It has a DOM traversal API that can be used similarly to `BeautifulSoup`'s node-search based approach if desired.

Like `BeautifulSoup`, it has a somewhat sprawling API that contains dozens of methods most people will never need. Many of these are part of the `ElementTree` API, which is a DOM traversal API that is not specific to HTML parsing.

The most commonly-cited downside is that it relies upon C libraries, which can make installation and deployment more difficult on some platforms. I find with modern package managers this is less of an issue than it used to be, but it's still a valid concern.

### `parsel`

`parsel` is a nice idea, a thin wrapper around `lxml` that focuses on providing a simple API for XPath and CSS selectors. It's a good idea, but using it leaves something to be desired. Its API is very small, perhaps going too far in the other direction.

As a wrapper around `lxml` it has the same advantages and disadvantages. If installing C libraries is a concern, it's a concern here too.

### `selectolax`

I was completely unfamiliar with `selectolax` before starting this comparison and came away impressed. The API is small and easy to learn, but with a few convenience functions that I found nice to have compared to `parsel`'s approach.

The main downside I see is that it does not have native XPath support. While CSS selectors are more widely-used, XPath is very powerful and it is nice to have the option to use it when using `lxml.html` or `parsel`.

`selectolax` of course also depends upon C libraries, leaving `BeautifulSoup` the only option if pure Python is a requirement.

## Example Scraper

TODO: write example in each library