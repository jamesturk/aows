# Introduction

I've written a lot of web scrapers. 

For the better part of thirteen years, I led the [Open States project](https://openstates.org), which maintains a database of legislative data for all 50 states. We scraped data from state websites, and then used that data to power a variety of services, including a public API, a website, and a mobile app.

When we started the project in 2009, the state-of-the-art in Python was `urllib2` (this was Python 2 of course), and `BeautifulSoup` for HTML.

Shortly after the project started, we switched to `lxml` for HTML parsing, and eventually built our own library `scrapelib` to add caching and retry features to `urllib2`.  Eventually `requests` came along and we ported `scrapelib` to use that instead of `urllib2`, but still benefited from `scrapelib`'s caching and retry features.

Many web scrapers are written to be run once and thrown away.
Our goal was to be able to run our scrapers continuously, to create an ongoing stream of legislative data updating our database.

Ultimately our core requirements shaped a lot of this philosophy:
* We needed to be able to run our scrapers continuously, to create an ongoing stream of legislative data updating our database.
* Our scrapers were necessarily fragile, we were scraping specific legislative metadata, not just collecting full text.
* As an open source project dependent upon volunteers, we needed to be able to easily onboard new contributors.
* We were scraping government websites, many of which had spotty uptime and were often slow to respond.

We built a lot of tools to help us with these goals, and over the years we built up a lot of knowledge about how to build reliable scrapers.

The goal of this series is to start trying to put some of that knowledge into one place, and exploring the Python scraping ecosystem.

## Table of Contents

Here's what I'm planning to write about:

* Parsing Library Comparison (lxml, html5lib, beautifulsoup4, selectolax)
    * Performance - Speed & Memory Usage
    * Handling Bad HTML
    * Ease of Use / Features
    * Other Considerations
* Fetching Library Comparison (urllib.request, requests, urllib3, httpx)
* Helpful Fetching Features
    * Caching
    * Retries
    * Rate Limiting
    * Proxies
    * User Agents
    * Cookies
    * Other Considerations
* Scraping Rules
* Object Validation (maybe?)
* ORM / Etc (maybe?)
* Git Scraping?

I figured I'd share this because if people are particularly interested in any of these topics, I might prioritize writing about them.

### Why not Scrapy?

Inevitably this question comes up. One answer is that it didn't exist when we started the project, at least not as a public project.
As far as why we never switched, scrapy is a heavyweight system, filled with opinionated choices.  By the time it became a popular library, we had already built our own system, so we stuck with what we had.

So would I use it today? Probably not.

`scrapy` borrows ideas and its core philosophy from Django. It is an opinionated framework, not particularly suited to being used in part.
Sometimes that's exactly what you want, but it isn't what we wanted.  We wanted to be able to swap out parts of the system as needed, and `scrapy` is not designed for that.

If you like `scrapy`, by all means, use it!

If you, like me, prefer to use lightweight library for scraping, you might be more interested in the libraries I aim to compare here. These libraries give you more control over the full process and are easier to integrate into existing systems.  Scrapy is a great library, but it's not a great fit for every project.

I prefer to use a lightweight library for scraping, and then build my own system on top of that.  I like to have control over the entire process, and I like to be able to easily switch out parts of the system as needed.  Scrapy is a great library, but it's not a great fit for every project.