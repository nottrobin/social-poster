#! /usr/bin/env python3

"""
Post an article to news.ycombinator.com ("hacker news")

Copied and modified from David Bieber:
https://davidbieber.com/snippets/2020-05-02-hackernews-submit/
"""

# Standard library
import argparse
import time
import os
from html.parser import HTMLParser

# Packages
import requests
from bs4 import BeautifulSoup


# Classes
# ===
class FNIDExtractor(HTMLParser):
    """
    Extract the fnid from the submit form
    """

    fnid = None

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "input" and ("name", "fnid") in attrs:
            self.fnid = dict(attrs)["value"]


# Parse arguments
# ===
parser = argparse.ArgumentParser(description="Post an article to hacker news")
parser.add_argument(
    "-u", "--username", help="Username for login", required=True
)
parser.add_argument(
    "-p",
    "--password",
    help="Password for login. Or use HN_PASSWORD env var.",
    default=os.getenv("HN_PASSWORD"),
)
parser.add_argument("-t", "--title", help="The article title", required=True)
parser.add_argument("-l", "--link", help="URL to the article", required=True)
args = vars(parser.parse_args())
if not args.get("password"):
    print("No password provided\n")
    exit(parser.print_help())


# Login
# ===
session = requests.Session()
login_response = session.post(
    "https://news.ycombinator.com/login",
    data={
        "acct": args["username"],
        "pw": args["password"],
    },
)
login_response.raise_for_status()
if "Bad login." in login_response.text:
    raise Exception("Bad login")
else:
    print(f'Successfully logged in as {args["username"]}\n')


# Get the CSRF token ("FNID")
# ===
time.sleep(1)
f = FNIDExtractor()
submit_response = session.get("https://news.ycombinator.com/submit")
submit_response.raise_for_status()
f.feed(submit_response.text)
if not f.fnid:
    raise Exception("Failed to extract fnid from submit form")
else:
    print(f"fnid successfully extracted: {f.fnid}\n")


# Submit the post
# ===
time.sleep(2)
post_response = session.post(
    "https://news.ycombinator.com/r",
    data={
        "title": args["title"],
        "url": args["link"],
        "fnid": f.fnid,
    },
)
post_response.raise_for_status()

soup = BeautifulSoup(post_response.text, "html.parser")
item_id = soup.select(
    "table.itemlist tr:nth-child(2) td.subtext a:-soup-contains('discuss')"
)[0].get("href")[8:]

print(
    f"Successfully submitted: https://news.ycombinator.com/item?id={item_id}\n"
)
