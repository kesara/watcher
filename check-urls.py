from csv import reader as csv_reader, writer as csv_writer
from datetime import date
from os import listdir, path
from re import compile as re_compile
from sys import exit
from urllib.request import urlopen


CSV_DIRECTORY = "csv"


def get_latest_urls_file(directory):
    file_pattern = re_compile(r"urls_\d{4}-\d{2}-\d{2}\.csv")
    files = listdir(directory)
    matching_files = [f for f in files if file_pattern.match(f)]
    if not matching_files:
        exit("No URL CSV files.")
    sorted_files = sorted(matching_files, reverse=True)
    return path.join(directory, sorted_files[0])


def get_status(url):
    try:
        response = urlopen(url)
        return response.getcode()
    except Exception as e:
        return f"Connection error: {str(e)}"


def watch_status(url_list_filename, status_filename):
    with open(status_filename, "w", newline="") as status_csv_file:
        writer = csv_writer(status_csv_file)
        writer.writerow(["filename", "url", "status/error"])

        with open(url_list_filename, "r") as csv_file:
            reader = csv_reader(csv_file)
            next(reader)  # discard header row
            for row in reader:
                filename, url = row
                status = get_status(url)
                writer.writerow([filename, url, status])


current_date = date.today().strftime("%Y-%m-%d")

latest_url_file = get_latest_urls_file(CSV_DIRECTORY)
status_filename = f"{CSV_DIRECTORY}/url_status_{current_date}.csv"
watch_status(latest_url_file, status_filename)
