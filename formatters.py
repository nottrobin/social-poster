# Standard library
import typing

# Packages
from tweetsplitter import tweet_splitter
from bs4.element import Tag


def article_to_tweets(article_soup: Tag) -> typing.List[str]:
    """
    Given an article URL, get the contents of the article
    and split it into a number of tweets
    """

    article_text = article_soup.get_text().replace("\n", "\n\n").strip()

    article_links = []
    for anchor in article_soup.select("a[href]"):
        if anchor.attrs["href"].startswith("http"):
            article_links.append(anchor.attrs["href"])
        else:
            article_links.append("https://robinwinslow.uk/" + anchor.attrs["href"])

    tweets = tweet_splitter(article_text, 0)

    # Add references
    if article_links:
        tweets.append("References:\n\n1: " + article_links[0])
        for index, link in enumerate(article_links[1:]):
            tweets.append(f"{index + 2}: {link}")


    for index, tweet in enumerate(tweets):
        tweets[index] = tweet + f" [{index + 1}/{len(tweets)}]"

    return tweets
