# Scraping Philosophy

## Scrapers Are Ugly

A lot of the ugliest code you'll ever write is web scraping code.

I always told new contributors, often less experienced developers coming in with an academic understanding of what clean code is, that they should understand that web scraping code can't be more elegant than the site it is scraping. If the HTML page you are dealing with is full of weird edge cases, your code will necessarily be full of weird edge cases too.

Also, many web scrapers are written to be run once and thrown away, in which case, who cares if it's ugly?

For Open States, we knew that our goal was to be able to run our scrapers continuously, to create an ongoing stream of legislative data updating our database.

But I've found scrapers are rarely as ephemeral as their authors intend. I've seen many scrapers someone wrote years ago to grab some data for a one-off project wound up being a core part of someone's data pipeline long after the original author departed the team. The thought may horrify the original author, who assumed the code would be thrown away. With good enough tools, and the right philosophy, you can make this prospect slightly less terrifying.

Ultimately our core requirements shaped a lot of this philosophy:

* We needed to be able to run our scrapers continuously, to create an ongoing stream of legislative data updating our database.
* Our scrapers were necessarily fragile, we were scraping specific legislative metadata, not just collecting full text. We couldn't afford to be imprecise.
* As an open source project dependent upon volunteers, we needed to be able to easily onboard new contributors.
* We were scraping government websites, many of which had spotty uptime and were often slow to respond.

We built a lot of tools to help us with these goals, and over the years we built up a lot of knowledge about how to build reliable scrapers.

## Scrapers Are Fragile

## Scrapers Are Tied to the Page Structure

## Scrapers Stick Around

## Scrapers Are Living Things

## Complementarity

You may be familiar with Heisenberg's uncertainty principle, which states that the more precisely you measure the position of a particle, the less precisely you can measure its momentum, and vice versa. This is an example of a concept called complementarity.

In the context of scrapers, we can think of precision and robustness as being complementary. When selecting data from a page, you can either be precise and fragile, or you can be robust and imprecise. You can't be both.

An example can make this more clear:

Let's say there is a deeply nested set of `<div>` tags on a page, something like this:

```python
<div class="container">
    <div class="section1">
        <div class="user">
            <h2>Sally Smith</h2>
            <div>123 Main St</div>
            <div>Boise</div>
            <div>ID</div>
            <div>12345</div>
        </div>
    </div>
</div>
```

You could assume that `<div class="user">` contains the address, and select it like this:

```python
address = " ".join(page.xpath('//div[@class="user"]/div/text()'))
```

Which would obtain `"123 Main St Boise ID 12345"`.

Now imagine that you encounter another user where there is a 5th div, and you realize that they add the phone number if available:.

```python
<div class="container">
    <div class="section1">
        <div class="user">
            <h2>Sally Smith</h2>
            <div>123 Main St</div>
            <div>Boise</div>
            <div>ID</div>
            <div>12345</div>
            <div>555-555-5555</div>
        </div>
    </div>
</div>
```

Your code will now break, because it will select the phone number.
