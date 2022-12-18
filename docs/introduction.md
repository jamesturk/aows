# Introduction

I figured it'd make sense to explain who I am & why I'm interested in this.  Feel free to skip this bit.

For the better part of thirteen years, I led the [Open States project](https://openstates.org). Open States maintains a database of legislative data for all 50 states (and DC and PR) that updates regularly throughout the day. The project relies on around 200 custom scrapers, and then uses that data to power a variety of services including a public API and website. Millions of individuals have used Open States over the years to find their representatives & track legislation, and the data is widely used by researchers, journalists, and nonprofits.

Building & maintaining this project taught me a lot about web scrapers. Over the years I onboarded dozens of new contributors, and often wished for better resources on web scraping that go beyond the basics. I also want to take a look at the Python scraping ecosystem, because I think for a lot of people 2-3 libraries seem like the end-all-be-all, but there are a lot of options out there, and I think it's worth exploring them.


## A Bit of History

When we started the project in 2009, the state-of-the-art in Python was `urllib2` (this was Python 2 of course), and `BeautifulSoup` for HTML.

Shortly after the project started, we switched to `lxml` for HTML parsing, and eventually built our own library `scrapelib` to add caching and retry features to `urllib2`.  Eventually `requests` came along and we ported `scrapelib` to use that instead of `urllib2`, but still benefited from `scrapelib`'s caching and retry features.

A few years later, `scrapy` came along. It wasn't mature enough for us to adopt when we first evaluated it, and ultimately the project was too opinionated for our needs.

The goal of this series is to start trying to put some of that knowledge into one place, and exploring the Python scraping ecosystem.

## How to Use This Book

This book is a work in progress, the table of contents is aspirational.

The book is structured into three major parts:

**Part 1: Understanding Web Scraping**

This section of the book aims to cover broad topics in web scraping. This isn't particularly focused on Python, but rather on the general concepts of web scraping.

* **Chapter 1: Web Scraping 101** - A quick overview of the basics of web scraping.
* **Chapter 2: [Scraping Philosophy](philosophy.md)** - A discussion of the philosophy behind writing scrapers.
* **Chapter 4: Best Practices** - Writing resilient & sustainable scrapers.
* **Chapter 5: Ethical & Legal Guidelines** - A discussion of ethical & legal guidelines for scraping.

**Part 2: Python Scraping Ecosystem**

These chapters are focused on the Python scraping ecosystem.  Each chapter will compare a few libraries, and discuss the pros & cons of each.

* **Chapter 6: [Making Requests](requests/libraries.md)** - Various libraries for making HTTP requests.
* **Chapter 7: [Parsing HTML](parsing/intro.md) ** - Comparing various libraries for parsing HTML.
* **Chapter 8: Other Libraries** - Other libraries that are useful for scraping.
* **Chapter 9: Scrapy** - A discussion of Scrapy.

**Part 3: Advanced Concepts**

These chapters discuss more advanced topics in web scraping. Not every scraper will need to use these, but they're useful to know about as your scrapers grow more advanced.

* **Chapter 10: Data Validation** - A discussion of data validation.
* **Chapter 11: Deploying Scrapers** - A discussion of deploying scrapers.
* **Chapter 12: Browser Automation** - A discussion of browser automation.

**Appendix A: XPath & CSS Selectors**
