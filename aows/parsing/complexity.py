from .implementations import Lxml, BSoup, Parsel, Selectolax, SelectoLexbor
from collections import defaultdict

lxml = Lxml()
bs4 = BSoup("html.parser")
parsel = Parsel()
selectolax = Selectolax()


def type_name(obj, attr):
    try:
        name = type(getattr(root, attr)).__name__
        if name == "builtin_function_or_method":
            return "method"
        else:
            return name
    except AttributeError:
        return "missing"


def show_attributes(obj):
    attributes = defaultdict(set)

    # build inverse index
    for name in dir(obj):
        if name.startswith("_"):
            continue
        attributes[type_name(obj, name)].add(name)

    for attr_type, attrs in attributes.items():
        print(f"  {attr_type}: {len(attrs)}: {', '.join(sorted(attrs))}")


for impl in [lxml, bs4, parsel, selectolax]:
    root = impl.load_dom("html5test")
    print("\n\n# ", impl)
    print("  ", type(root))
    show_attributes(root)

    link = impl.find_tags(root, "a")[0]
    print("  ", type(link))
    show_attributes(link)
