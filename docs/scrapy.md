
### Why not Scrapy?

Inevitably this question comes up. One answer is that it didn't exist when we started the project, at least not as a public project.
As far as why we never switched, scrapy is a heavyweight system, filled with opinionated choices.  By the time it became a popular library, we had already built our own system, so we stuck with what we had.

So would I use it today? Probably not.

`scrapy` borrows ideas and its core philosophy from Django. It is an opinionated framework, not particularly suited to being used in part.
Sometimes that's exactly what you want, but it isn't what we wanted.  We wanted to be able to swap out parts of the system as needed, and `scrapy` is not designed for that.

If you like `scrapy`, by all means, use it!

If you, like me, prefer to use lightweight library for scraping, you might be more interested in the libraries I aim to compare here. These libraries give you more control over the full process and are easier to integrate into existing systems.  Scrapy is a great library, but it's not a great fit for every project.

I prefer to use a lightweight library for scraping, and then build my own system on top of that.  I like to have control over the entire process, and I like to be able to easily switch out parts of the system as needed.  Scrapy is a great library, but it's not a great fit for every project.

### Issues
- scrapy shell sets variables like response instead of letting you write real python 
- r =  fetch("") sshould work, it doesn't
- parsel
	- output of response (screenshot taken)
	- get() method that returns raw HTML vs. something useful