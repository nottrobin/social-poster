#! /usr/bin/env python3

"""
This script is intended to be run automatically in CI for every commit
to a blog repository.

Look in the most recent commit for all articles that have been touched,
check if they have been shared to social media and email and if not,
share them and update their frontmatter accordingly
"""

# Standard library
import os
import time

# Packages
import git
import frontmatter
import requests
from copy import copy
from bs4 import BeautifulSoup, element
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import RequestException

# Local
from apis import (
    get_article_html,
    post_to_dev_to,
    post_to_hacker_news,
    post_to_twitter,
    email_to_mailchimp_list,
)


# Setup git
repo = git.Repo(search_parent_directories=True)

# Get latest commit
head_hash = repo.head.object.hexsha

# Find articles in latest commit
files = repo.head.commit.stats.files
article_paths = []

for file in files:
    if (
        os.path.exists(file)
        and file.startswith("_articles/")
        and not file.startswith("_articles/_")
    ):
        article_paths.append(file)

print(f"Found {len(article_paths)} articles")

# Send tweet, add tweet ID
for path in article_paths:
    print(f"\nProcessing {path}")

    article_markdown = frontmatter.load(path)

    if not {"date", "title", "description"}.issubset(article_markdown.keys()):
        # Skip articles without date, title or description
        print(f"- Missing some metadata - skipping")
        continue

    url_path = path.removeprefix("_articles/").removesuffix(".md")
    article_url = f"https://robinwinslow.uk/{url_path}"
    title = article_markdown["title"]
    description = article_markdown.get("description", "")

    # First, wait until article is definitely published
    article_html = get_article_html(article_url)

    if "cross_posts" in article_markdown:
        cross_posts = article_markdown["cross_posts"]
    else:
        cross_posts = {}
        article_markdown["cross_posts"] = cross_posts

    if "DEV" not in cross_posts:
        print("- Posting to dev.to", flush=True)
        try:
            cross_posts["DEV"] = post_to_dev_to(article_markdown, article_url)
        except RequestException as request_error:
            response = request_error.response
            print(f"  > [ERROR]: {response.status_code} - {response.text}")
        else:
            print(f"  > Posted to DEV: {cross_posts['DEV']}")
            frontmatter.dump(article_markdown, path)
            print(f"  > Updated metadata")

    if "Hacker News" not in cross_posts:
        print("- Posting to Hacker News", flush=True)
        try:
            cross_posts["Hacker News"] = post_to_hacker_news(title, article_url)
        except RequestException as request_error:
            response = request_error.response
            print(f"  > [ERROR]: {response.status_code} - {response.text}", flush=True)
        else:
            print(f"  > Posted to HN: {cross_posts['Hacker News']}")
            frontmatter.dump(article_markdown, path)
            print(f"  > Updated metadata")

    if "Twitter" not in cross_posts:
        print("- Posting to Twitter", flush=True)
        cross_posts["Twitter"] = post_to_twitter(title, description, article_url, article_html)
        print(f"  > Posted to Twitter: {cross_posts['Twitter']}")
        frontmatter.dump(article_markdown, path)
        print(f"  > Updated metadata", flush=True)

    if "email_campaign_id" not in article_markdown:
        print("- Sending email", flush=True)
        campaign = email_to_mailchimp_list(title, description, article_url, article_html)
        article_markdown["email_campaign_id"] = campaign["id"]
        print(f"  > Email campaign sent: {campaign['id']}")
        frontmatter.dump(article_markdown, path)
        print(f"  > Updated metadata", flush=True)

    # If not last item, wait before the next item
    if path != article_paths[-1]:
        print(f"- Waiting 35 seconds to avoid rate limits", flush=True)
        time.sleep(35)
