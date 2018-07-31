from bs4 import BeautifulSoup
import urllib3
import json
import bcolors as bc
import argparse as ap

http = urllib3.PoolManager()


def crawl(url):
    soup = get_url_data(url)
    values = get_page_data(soup)
    surf(soup, url)


def surf(data, url):
    for link in data.find_all("a"):
        link = link.get("href")

        if link.startswith("/"):
            link = url + link
            soup = get_url_data(link)
            values = get_page_data(soup)
            json_update(values[0], values[1], values[2], link)
        elif link.startswith("./"):
            link = link.replace(".", url)
            soup = get_url_data(link)
            values = get_page_data(soup)
            json_update(values[0], values[1], values[2], link)
        else:
            soup = get_url_data(link)
            values = get_page_data(soup)
            json_update(values[0], values[1], values[2], link)


def get_page_data(data):
    desc = ""
    content = ""

    for meta in data.find_all("meta", {"name": "description"}):
        if meta:
            desc = meta["content"]
    for meta in data.find_all("meta", {"name": "keywords"}):
        if meta:
            content = meta["content"]
    title = data.title.string
    return [desc, content, title]


def get_url_data(url):
    response = http.request("GET", url)
    html = response.data
    soup = BeautifulSoup(html, "html.parser")
    return soup


def json_update(title, description, keywords, url):
    if title == "":
        title = description
        if description == "":
            title = keywords
    jsonData = {"Title": title, "Description": description, "Keywords": keywords, "URL": url}

    with open("data.json", "r") as file:
        data = json.load(file)
        file.close()
    strData = str(data)

    if not strData.find(str(jsonData)) >= 0:
        data.append(jsonData)

        with open("data.json", "w") as file:
            json.dump(data, file, indent=4, separators=(',', ':'))
            file.close()


def main():
    print(bc.bcolors.BOLD + "Spiedie, Spiedie does whatever a Spiedie wants to do!")
    parser = ap.ArgumentParser()
    parser.add_argument("link", help="Link to the site you want to crawl")
    args = parser.parse_args()
    crawl(args.link)
    print(bc.bcolors.OKBLUE + "Crawled site " + bc.bcolors.BOLD + str(
        args.link) + bc.bcolors.OKBLUE + " data will be sent to data.json")


if __name__ == '__main__':
    main()