from os import listdir, path
from lxml import etree
from urllib.parse import urlparse


RFC_DIRECTORY = "rfc"
URL_ATTRIBUTES = [
    "href",
    "target",
    "src",
    "cite",
]
URL_ELEMENTS = [
    "uri",
]


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def find_urls(directory):
    for filename in listdir(directory):
        if filename.endswith(".xml"):
            print(filename)
            urls = []
            filepath = path.join(directory, filename)
            try:
                tree = etree.parse(filepath)
                url_elements = tree.xpath(
                    "//@{} | //{}".format(
                        " | //@".join(URL_ATTRIBUTES),
                        " | //".join(URL_ELEMENTS),
                    )
                )
                urls.extend(url_elements)
                for url in urls:
                    if is_valid_url(url):
                        print(url)
            except etree.XMLSyntaxError:
                print(f"Error parsing XML file: {filepath}")


urls = find_urls(RFC_DIRECTORY)
