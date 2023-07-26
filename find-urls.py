from csv import writer as csv_writer
from datetime import date
from lxml import etree
from os import listdir, path
from re import compile
from urllib.parse import urlparse


RFC_DIRECTORY = "rfc"
CSV_DIRECTORY = "csv"
URL_ATTRIBUTES = [
    "href",
    "target",
    "src",
    "cite",
]
URL_ELEMENTS = [
    "uri",
]
TEXT_RFC = [f"rfc{i}.txt" for i in range(1, 8650)]


url_re = compile(
    r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+[<>.\s]+"
)


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([len(result.scheme) > 0, result.netloc])
    except ValueError:
        return False


def find_urls(directory, csv_filename):
    with open(csv_filename, "w", newline="") as csv_file:
        writer = csv_writer(csv_file)
        writer.writerow(["filename", "url"])

        for filename in listdir(directory):
            if filename.endswith(".txt") and filename in TEXT_RFC:
                urls = []
                filepath = path.join(directory, filename)
                with open(filepath, "r", encoding="iso-8859-1") as file:
                    urls = url_re.findall(file.read())
                    for url in urls:
                        url = url.rstrip("<>),. \n\r")
                        if is_valid_url(url):
                            writer.writerow([filename, url])
            if filename.endswith(".xml"):
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
                            writer.writerow([filename, url])
                except etree.XMLSyntaxError:
                    print(f"Error parsing XML file: {filepath}")


current_date = date.today().strftime("%Y-%m-%d")

csv_filename = f"{CSV_DIRECTORY}/urls_{current_date}.csv"
find_urls(RFC_DIRECTORY, csv_filename)
