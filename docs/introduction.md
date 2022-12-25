# Introduction

Web scraping can be somewhat polarizing among developers. A lot of people hate it, finding it frustrating and tedious. Many of us get a sense of satisfaction out of it, enjoying the challenges it presents and the end result of having machine-readable data where it didn't exist before.

For thirteen years (2009-2022), I led the [Open States project](https://openstates.org). Open States maintains a database of legislative data for all 50 states (and DC and PR) that updates regularly throughout the day. The project relies on around 200 custom scrapers, and then uses that data to power a variety of services including a public API and website. Millions of individuals have used Open States over the years to find their representatives & track legislation, and the data is widely used by researchers, journalists, and nonprofits.

A lot of web scrapers are built as one-offs, and as a result not a lot of thought is put into the design of the scraper. This makes sense, but creates a sort of feedback loop where most scraper code is fragile and hard to maintain, so people looking to write more reliable scrapers wind up learning from code that is fragile and hard to maintain. Over the years I onboarded dozens of new contributors, and often wished for better resources on web scraping that reflected best practices. My hope is that I can help to fill that gap.

Data Engineering has taken off as a field in recent years, and web scraping is a key part of many data engineering pipelines. Despite being absolutely essential, it'll typically be the most fragile, least maintainable part of the pipeline. We'll take a look at why that is, and how we can improve it.


## About

!!! note 

    This is a work in progress, the table of contents is aspirational.

    TODO: explain how to subscribe

One of the goals of this project is to provide a resource for people looking to write reliable scrapers. While code examples will be in Python, many of the concepts should be applicable regardless of language. **Part 1** in particular will focus on high-level concepts and design patterns, and be broadly applicable.

**Part 2** is explicitly focused on the Python scraping ecosystem.
Whatever language you use, picking the right tools is essential. For a lot of people 2-3 Python libraries seem like the end-all-be-all, but there are a lot of options out there, and I think it's worth exploring them.  We'll also take a look at some oft-neglected parts of the scraping stack, like data validation and logging.

Right now I'm also grouping more advanced topics into **Part 3**. That's the least certain part of the plan right now.

**Part 1: Understanding Web Scraping**

This section aims to cover broad topics in web scraping. This isn't particularly focused on Python, but rather on the general concepts of web scraping.

* **Chapter 1: Web Scraping 101** - An overview of the basics of web scraping.
* **Chapter 2: [Scraping Philosophy](philosophy.md)** - A discussion of the philosophy behind writing scrapers.
* **Chapter 3: Best Practices** - Writing resilient & sustainable scrapers.
* **Chapter 4: Ethical & Legal Guidelines** - A discussion of ethical & legal guidelines for scraping.

**Part 2: Python Scraping Ecosystem**

These chapters are focused on the Python scraping ecosystem.  Each chapter will compare a few libraries, and discuss the pros & cons of each.

* **Chapter 5: Making Requests** - Various libraries for making HTTP requests.
* **Chapter 6: [Parsing HTML](parsing/index.md) ** - Comparing various libraries for parsing HTML.
* **Chapter 7: Other Libraries** - Other libraries that are useful for scraping.
* **Chapter 8: Scrapy** - A discussion of Scrapy.

**Part 3: Advanced Concepts**

These chapters discuss more advanced topics in web scraping. Not every scraper will need to use these, but they're useful to know about as your scrapers grow more advanced.

* **Chapter 9: Data Validation** - A discussion of data validation.
* **Chapter 10: Deploying Scrapers** - A discussion of deploying scrapers.
* **Chapter 11: Browser Automation** - A discussion of browser automation.

**Appendix A: XPath & CSS Selectors**