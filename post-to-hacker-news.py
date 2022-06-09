#! /usr/bin/env python3

"""
Post an article to news.ycombinator.com ("hacker news")
"""

# Standard library
import argparse
import os

# Local
from posters import post_to_hacker_news


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

# Submit post
# ===
post_url = post_to_hacker_news(
    args["title"], args["link"], args["username"], args["password"]
)

print(f"Successfully submitted: {post_url}\n")
