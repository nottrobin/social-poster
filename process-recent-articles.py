#! /usr/bin/env python3

"""
This script is intended to be run automatically in CI for every commit
to a blog repository.

Look in the most recent commit for all articles that have been touched,
check if they have been shared to social media and email and if not,
share them and update their frontmatter accordingly
"""

# Packages
import git
import frontmatter
import requests
from bs4 import BeautifulSoup, element
from requests.adapters import HTTPAdapter, Retry

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
files = repo.head.object.stats.files
article_paths = []

for file in files:
    if file.startswith("_articles/") and not file.startswith("_articles/_"):
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
    additions = []

    # First, wait until article is definitely published
    article_html = get_article_html(article_url)

    if "dev_to_url" not in article_markdown:
        article_markdown["dev_to_url"] = post_to_dev_to(article_markdown, article_url)
        print(f"- Posted to dev.to: {article_markdown['dev_to_url']}")
        additions.append("dev_to_url")

    if "hn_url" not in article_markdown:
        article_markdown["hn_url"] = post_to_hacker_news(title, article_url, "nottrobin")
        print(f"- Posted to HN: {article_markdown['hn_url']}")
        additions.append("hn_url")

    if "tweet_url" not in article_markdown:
        article_markdown["tweet_url"] = post_to_twitter(article_html)
        print(f"- Posted to Twitter: {article_markdown['tweet_url']}")
        additions.append("tweet_url")

    if "email_campaign_id" not in article_markdown:
        campaign = email_to_mailchimp_list(title, description, article_url)
        article_markdown["email_campaign_id"] = campaign["id"]
        print(f"- Email campaign sent: {campaign['id']}\n")
        additions.append("email_campaign_id")

    if additions:
        frontmatter.dump(article_markdown, path)
        print(f"- Updated metadata")
    else:
        print(f"- No updates necessary")
