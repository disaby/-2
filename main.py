from nturl2path import url2pathname
import requests
from bs4 import BeautifulSoup
import lxml
import json


def get_data():
    url = "https://www.securitymagazine.com/topics/2236-cyber-security-news"

    header = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"
    }

    r = requests.get(url=url, headers=header)
    soup = BeautifulSoup(r.text, "lxml")

    article_cards = soup.find_all("article", class_="article-summary")
    articles_dict = {}
    for article in article_cards:
        article_title = article.find(
            "h2", class_="article-summary__headline").find("a").text.strip()
        article_author = article.find(
            "span", class_="author-bylines__author-link-name").text.strip()
        article_date = article.find(
            "div", class_="article-summary__post-date").text.strip()
        article_abstract = article.find(
            "div",
            class_="abstract article-summary__teaser").find("p").text.strip()
        article_url = article.find(
            "h2", class_="article-summary__headline").find("a").get("href")
        article_id = article_url.split("/")[-1].split("-")[0]

        articles_dict[article_id] = {
            'article_title': article_title,
            'article_author': article_author,
            'article_date': article_date,
            'article_abstract': article_abstract,
            'article_url': article_url
        }
    print(articles_dict)

    with open("articles_dict.json", "w", encoding="utf-8") as file:
        json.dump(articles_dict, file, indent=4, ensure_ascii=False)


def check_update():
    articles_dict = {}
    fresh_news_dict = {}
    url = "https://www.securitymagazine.com/topics/2236-cyber-security-news"

    header = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"
    }

    with open("articles_dict.json") as file:
        articles_dict = json.load(file)

    r = requests.get(url=url, headers=header)
    soup = BeautifulSoup(r.text, "lxml")
    article_cards = soup.find_all("article", class_="article-summary")
    for article in article_cards:
        article_url = article.find(
            "h2", class_="article-summary__headline").find("a").get("href")
        article_id = article_url.split("/")[-1].split("-")[0]
        if article_id in articles_dict:
            continue
        else:
            article_title = article.find(
                "h2",
                class_="article-summary__headline").find("a").text.strip()
            article_author = article.find(
                "span",
                class_="author-bylines__author-link-name").text.strip()
            article_date = article.find(
                "div", class_="article-summary__post-date").text.strip()
            article_abstract = article.find(
                "div", class_="abstract article-summary__teaser").find(
                    "p").text.strip()

            articles_dict[article_id] = {
                'article_title': article_title,
                'article_author': article_author,
                'article_date': article_date,
                'article_abstract': article_abstract,
                'article_url': article_url
            }

            fresh_news_dict[article_id] = {
                'article_title': article_title,
                'article_author': article_author,
                'article_date': article_date,
                'article_abstract': article_abstract,
                'article_url': article_url
            }

    with open("articles_dict.json", "w", encoding="utf-8") as file:
        json.dump(articles_dict, file, indent=4, ensure_ascii=False)

    return fresh_news_dict


def main():
    # get_data()
    print("Something:\n")
    print(check_update())


if __name__ == '__main__':
    main()