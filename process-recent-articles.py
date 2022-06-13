#! /usr/bin/env python3

"""
This script is intended to be run automatically in CI for every commit
to a blog repository.

Look in the most recent commit for all articles that have been touched,
check if they have been shared to social media and email and if not,
share them and update their frontmatter accordingly
"""

import git
import frontmatter
from posters import (
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

    article = frontmatter.load(path)

    if not {"date", "title", "description"}.issubset(article.keys()):
        # Skip articles without date, title or description
        print(f"- Missing some metadata - skipping")
        continue

    url_path = path.removeprefix("_articles/").removesuffix(".md")
    url = f"https://robinwinslow.uk/{url_path}"
    title = article["title"]
    description = article.get("description", "")
    additions = []

    if "hn_url" not in article:
        article["hn_url"] = post_to_hacker_news(title, url, "nottrobin")
        print(f"- Posted to HN: {article['hn_url']}")
        additions.append("hn_url")

    if "tweet_url" not in article:
        article["tweet_url"] = post_to_twitter(
            f"I wrote an article!\n\n{description}\n\n{url}"
        )
        print(f"- Posted to Twitter: {article['tweet_url']}")
        additions.append("tweet_url")

    if "email_campaign_id" not in article:
        campaign = email_to_mailchimp_list(title, description, url)
        article["email_campaign_id"] = campaign["id"]
        print(f"- Email sent\n")
        additions.append("email_campaign_id")

    if additions:
        frontmatter.dump(article, path)
        repo.index.add(path)
        repo.index.commit(f"Updated '{title}' with: {', '.join(additions)}")
        print(f"- Commited with updated metadata")
    else:
        print(f"- No updates necessary")
