import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


base_url = "https://www.premiumbeautynews.com/"


def parse_url(url):
    response = requests.get(url)
    content = response.content
    parsed_response = BeautifulSoup(content, "lxml")
    return parsed_response


def extract_post_data(post_url):
    soup_post = parse_url(post_url)

    title = soup_post.find("h1", {"class": "article-title"}).text
    datetime = soup_post.find(
        "header", {"class": "row sub-header"}).find("span")["datetime"]
    abstract = soup_post.find("h2", {"class": "article-intro"}).text
    content = soup_post.find("div", {"class": "article-text"}).text

    data = {
        "title": title,
        "datetime": datetime,
        "abstract": abstract,
        "content": content,
        "url": post_url
    }

    return data


url = "https://www.premiumbeautynews.com/fr/marches-tendances/"
next_button = ""
posts_data = []
count = 1

while next_button is not None:
    print(f"page number : {count}")

    soup = parse_url(url)
    section = soup.find("section", {"class": "content"})
    posts = section.findAll("div", {"class": "post-style1 col-md-6"})

    for post in tqdm(posts, leave=False):
        uri = post.find("h4").find("a")["href"]
        post_url = base_url + uri
        data = extract_post_data(post_url)
        posts_data.append(data)

    next_button = soup.find("p", {"class": "pagination"}).find(
        "span", {"class": "next"})
    if next_button is not None:
        url = base_url + next_button.find("a")["href"]
        count += 1
