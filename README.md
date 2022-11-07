# scraping-experiments

Planning to do some side-by-side comparisons of various libraries within Python's scraping ecosystem.

## Parsers Compared

lxml
html5lib
beautifulsoup4

- Speed
  - Parse DOM
  - Traverse Tree
  - XPath
  - CSS Select
  - prettify
  - extract text
- API
- Reliability
- Other Considerations

## What's Next?

Explore libraries for fetching HTML.


## Scraping Stack Defined

Recommended Pieces of a web scraping stack:

* URL Retrieval
  * urllib.request
  * requests
  * urllib3
  * httpx
* DOM Parsing / Extraction
  * lxml
  * beautifulsoup4
  * html5lib
  * Python's builtin html parser
* Object Validation
  * pydantic
  * dataclasses
  * marshmallow
  * attrs
  * jsonschema, et al.
* Standalone ORM
  * 
