import requests
from .implementations import Lxml, BSoup

_cache = {}


start_url = "https://docs.python.org/3/genindex-all.html"


def cached_get(url):
    """
    Use a two-layer cache.

    First, check if the url is in _cache, and return it if so.
    Second, check if the url is cached to disk, and return it if so.
    Finally, fetch the URL if needed.
    """
    # normalize URL & only fetch URLs that start with library
    url = url.split("#")[0]
    if url.startswith("library/"):
        url = f"https://docs.python.org/3/{url}"

    if url not in _cache:
        try:
            with open(f"cache/{url.replace('/', '_')}", "rb") as f:
                _cache[url] = f.read()
        except FileNotFoundError:
            pass
        response = requests.get(url)
        _cache[url] = response.content
        with open(f"cache/{url.replace('/', '_')}", "wb") as f:
            f.write(response.content)
    return _cache[url]


def time_decorator(func):
    import time

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        print(f"took {end - start} seconds")

    return wrapper


@time_decorator
def scrape(impl):
    nodes = 0
    text_count = 0
    subpages = 0
    spans = 0
    seen = set()

    html = cached_get(start_url)
    tree = impl.parse_dom(html)
    for link in impl.find_tags(tree, "a"):
        href = link.get("href").split("#")[0]
        # if href in seen:
        #     continue
        # seen.add(href)
        if href.startswith("library/"):
            subpage = impl.parse_dom(cached_get(href))
            subpages += 1
            nodes += len(impl.all_nodes(subpage))
            text_count += len(impl.all_text(subpage))
            spans += len(list(impl.find_tags(subpage, "span")))

    print(
        f"{impl} scraped {nodes} nodes, {spans} <span> tags, and {text_count} characters from {subpages} subpages"
    )


# prime cache
scrape(Lxml())

scrape(Lxml())
scrape(BSoup("html.parser"))
scrape(BSoup("lxml"))
scrape(BSoup("html5lib"))
