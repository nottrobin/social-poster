#! /usr/bin/env python3

"""
Post an article to news.ycombinator.com ("hacker news")

Copied and modified from David Bieber:
https://davidbieber.com/snippets/2020-05-02-hackernews-submit/
"""

# Standard library
import argparse
import os

# Packages
import tweepy


# Parse arguments
# ===
parser = argparse.ArgumentParser(description="Post an article to twitter.com")
parser.add_argument(
    "-t", "--tweet", help="The text of the tweet to send", required=True
)
parser.add_argument(
    "-k",
    "--api-key",
    help=(
        "The API key for the twitter application. "
        "Or use TWITTER_API_KEY env var."
    ),
    default=os.getenv("TWITTER_API_KEY"),
)
parser.add_argument(
    "-s",
    "--api-key-secret",
    help=(
        "The API key secret for the twitter application. "
        "Or use TWITTER_API_KEY_SECRET env var."
    ),
    default=os.getenv("TWITTER_API_KEY_SECRET"),
)
parser.add_argument(
    "-a",
    "--access-token",
    help=(
        "The access token for the twitter application. "
        "Or use TWITTER_ACCESS_TOKEN env var."
    ),
    default=os.getenv("TWITTER_ACCESS_TOKEN"),
)
parser.add_argument(
    "-z",
    "--access-token-secret",
    help=(
        "The access token secret for the twitter application. "
        "Or use TWITTER_ACCESS_TOKEN_SECRET env var."
    ),
    default=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
)

args = vars(parser.parse_args())

if not args.get("api_key"):
    breakpoint()
    print("No API key provided\n")
    exit(parser.print_help())


if not args.get("api_key_secret"):
    print("No API key secret provided\n")
    exit(parser.print_help())

if not args.get("access_token"):
    print("No access token provided\n")
    exit(parser.print_help())

if not args.get("access_token_secret"):
    print("No access token secret provided\n")
    exit(parser.print_help())


# Auth
# ===

api = tweepy.API(
    tweepy.OAuth1UserHandler(
        args["api_key"],
        args["api_key_secret"],
        args["access_token"],
        args["access_token_secret"],
    )
)

# Send the tweet
# ===

response = api.update_status(args["tweet"])

print(
    "Successfully submitted tweet "
    f"https://twitter.com/{response.user.screen_name}/status/{response.id}"
)
