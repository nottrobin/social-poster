# Standard library
import time
import os
import copy
import json
from html.parser import HTMLParser

# Packages
import tweepy
import requests
import mailchimp_marketing
import frontmatter
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup
from bs4.element import Tag

# Local
from tweetsplitter import tweet_splitter
from formatters import article_to_tweets


# Functions
# ===
def get_article_html(article_url: str):
    """
    Given a URL, retry for a couple of minutes to
    get the article (in case it's not published yet),
    and then extract the HTML body from the article
    """

    session = requests.Session()
    retries = Retry(total=10, backoff_factor=1, status_forcelist=[ 404 ])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    response = session.get(article_url)
    response.raise_for_status()

    page_soup = BeautifulSoup(response.text, 'html.parser')

    article = page_soup.select_one("article")

    return article


def post_to_dev_to(article_markdown: frontmatter.Post, url: str):
    """
    Publish article to dev.to.
    """

    prelude = (
        f'_Originally published [on my blog]({url})._\n\n'
    )

    response = requests.post(
        "https://dev.to/api/articles",
        headers={
            "Content-Type": "application/json",
            "api-key": os.environ["DEV_TO_API_KEY"],
        },
        data=json.dumps(
            {
                "article": {
                    "title": article_markdown["title"],
                    "tags": article_markdown.get("tags", []),
                    "published": True,
                    "canonical_url": url,
                    "body_markdown": prelude + str(article_markdown)
                }
            }
        )
    )

    response.raise_for_status()

    return response.json()["url"]


def post_to_twitter(
    title: str,
    description: str,
    url: str,
    article_html: Tag
) -> str:
    """
    Post an article as a thread of tweets on Twitter
    
    Use the API & access credentials provided to about the new
    article at {url}, described in with {description}
    """

    api_key = os.environ["TWITTER_API_KEY"]
    api_key_secret = os.environ["TWITTER_API_KEY_SECRET"]
    access_token = os.environ["TWITTER_ACCESS_TOKEN"]
    access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

    api = tweepy.API(
        tweepy.OAuth1UserHandler(
            api_key,
            api_key_secret,
            access_token,
            access_token_secret,
        )
    )

    first_tweet = f"New article: {title}\n\n({description})\n\n{url}\n\n👇"

    previous_response = api.update_status(first_tweet)

    first_tweet_id = previous_response.id
    username = previous_response.user.screen_name

    for tweet in article_to_tweets(article_html):
        previous_response = api.update_status(
            status=tweet,
            in_reply_to_status_id=previous_response.id,
            auto_populate_reply_metadata=True
        )

    return (
        f"https://twitter.com/{username}/status/{first_tweet_id}"
    )


def post_to_hacker_news(
    title: str,
    url: str,
) -> str:
    """
    Post an article to Hacker News

    Copied and modified from David Bieber:
    https://davidbieber.com/snippets/2020-05-02-hackernews-submit/
    """

    username = os.environ["HN_USERNAME"]
    password = os.environ["HN_PASSWORD"]

    # Helper class for extracting the FNID from the submit form
    # ===
    class _FNIDExtractor(HTMLParser):
        """
        Extract the fnid from the submit form
        """

        fnid = None

        def handle_starttag(self, tag, attrs):
            if tag.lower() == "input" and ("name", "fnid") in attrs:
                self.fnid = dict(attrs)["value"]

    # Login
    # ===
    session = requests.Session()
    login_response = session.post(
        "https://news.ycombinator.com/login",
        data={
            "acct": username,
            "pw": password,
        },
    )
    login_response.raise_for_status()
    if "Bad login." in login_response.text:
        raise Exception("Bad login")

    # Get the CSRF token ("FNID")
    # ===
    time.sleep(1)
    extractor = _FNIDExtractor()
    submit_response = session.get("https://news.ycombinator.com/submit")
    submit_response.raise_for_status()
    extractor.feed(submit_response.text)
    if not extractor.fnid:
        raise Exception("Failed to extract fnid from submit form")

    # Submit the post
    # ===
    time.sleep(2)
    post_response = session.post(
        "https://news.ycombinator.com/r",
        data={
            "title": title,
            "url": url,
            "fnid": extractor.fnid,
        },
    )
    post_response.raise_for_status()

    soup = BeautifulSoup(post_response.text, "html.parser")
    item_id = soup.select(
        "table table tr:nth-child(2) td.subtext a:-soup-contains('discuss')"
    )[0].get("href")[8:]

    return f"https://news.ycombinator.com/item?id={item_id}"


def email_to_mailchimp_list(
    title: str,
    description: str,
    url: str,
    article_html: Tag,
) -> dict:
    """
    Send an email about the new post to the mailing list
    using Mailchimp's API.
    """

    client = mailchimp_marketing.Client()
    client.set_config({"api_key": os.environ["MAILCHIMP_API_KEY"]})

    template = client.templates.create(
        {
            "name": "Today's template",
            "html": (
                f'<p>New post <a href="{ url }">{ url.removeprefix("https://") }</a>:</p>'
                "<hr/>"
                '<article style="max-width: 48em; padding: 0 2em; border-left: 1px solid #ccc; margin: 2em 0;">'
                f"<h1>{ title }</h1>"
                f"{ article_html.decode_contents() }"
                "</article>"
                "<hr/>"
                '<p>Read all my posts at <a href="https://robinwinslow.uk">robinwinslow.uk</a>.'
            ),
        }
    )

    campaign = client.campaigns.create(
        {
            "type": "regular",
            "recipients": {
                "list_id": "8853044bbe",
            },
            "settings": {
                "subject_line": title,
                "preview_text": description,
                "title": title,
                "from_name": "Robin Winslow",
                "reply_to": "blog@robinwinslow.uk",
                "auto_footer": False,
                "template_id": template["id"],
            },
        }
    )

    client.campaigns.send(campaign["id"])

    return campaign
