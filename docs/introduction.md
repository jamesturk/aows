# Introduction

I figured it'd make sense to explain who I am & why I'm interested in this.  Feel free to skip this bit.

For the better part of thirteen years, I led the [Open States project](https://openstates.org). Open States maintains a database of legislative data for all 50 states (and DC and PR) that updates regularly throughout the day. The project relies on around 200 custom scrapers, and then uses that data to power a variety of services including a public API and website. Millions of individuals have used Open States over the years to find their representatives & track legislation, and the data is widely used by researchers, journalists, and nonprofits.

Building & maintaining this project taught me a lot about web scrapers. Over the years I onboarded dozens of new contributors, and often wished for better resources on web scraping that go beyond the basics. I also want to take a look at the Python scraping ecosystem, because I think for a lot of people 2-3 libraries seem like the end-all-be-all, but there are a lot of options out there, and I think it's worth exploring them.


## A Bit of History

When we started the project in 2009, the state-of-the-art in Python was `urllib2` (this was Python 2 of course), and `BeautifulSoup` for HTML.

Shortly after the project started, we switched to `lxml` for HTML parsing, and eventually built our own library `scrapelib` to add caching and retry features to `urllib2`.  Eventually `requests` came along and we ported `scrapelib` to use that instead of `urllib2`, but still benefited from `scrapelib`'s caching and retry features.

A few years later, `scrapy` came along. It wasn't mature enough for us to adopt when we first evaluated it, and ultimately the project was too opinionated for our needs.

The goal of this series is to start trying to put some of that knowledge into one place, and exploring the Python scraping ecosystem.

### Why not Scrapy?

Inevitably this question comes up. One answer is that it didn't exist when we started the project, at least not as a public project.
As far as why we never switched, scrapy is a heavyweight system, filled with opinionated choices.  By the time it became a popular library, we had already built our own system, so we stuck with what we had.

So would I use it today? Probably not.

`scrapy` borrows ideas and its core philosophy from Django. It is an opinionated framework, not particularly suited to being used in part.
Sometimes that's exactly what you want, but it isn't what we wanted.  We wanted to be able to swap out parts of the system as needed, and `scrapy` is not designed for that.

If you like `scrapy`, by all means, use it!

If you, like me, prefer to use lightweight library for scraping, you might be more interested in the libraries I aim to compare here. These libraries give you more control over the full process and are easier to integrate into existing systems.  Scrapy is a great library, but it's not a great fit for every project.

I prefer to use a lightweight library for scraping, and then build my own system on top of that.  I like to have control over the entire process, and I like to be able to easily switch out parts of the system as needed.  Scrapy is a great library, but it's not a great fit for every project.