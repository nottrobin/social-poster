#! /usr/bin/env python3

"""
Post an article to news.ycombinator.com ("hacker news")
"""

# Standard library
import argparse
import os

# Local
from posters import email_to_mailchimp_list, MAILCHIMP_MAILING_LIST_ID


# Parse arguments
# ===
parser = argparse.ArgumentParser(description="Post an article to hacker news")
parser.add_argument("-t", "--title", help="The article title", required=True)
parser.add_argument(
    "-d", "--description", help="A description of the article", required=True
)
parser.add_argument("-u", "--url", help="URL to the article", required=True)
parser.add_argument(
    "-m",
    "--mailing-list-id",
    help="The ID for the Mailchimp mailing list to send to",
    default=MAILCHIMP_MAILING_LIST_ID,
)
parser.add_argument(
    "-k",
    "--api-key",
    help="The mailchimp API key",
    default=os.getenv("MAILCHIMP_API_KEY"),
)
args = vars(parser.parse_args())
if not args.get("api_key"):
    print("No API key provided\n")
    exit(parser.print_help())

# Submit post
# ===
campaign = email_to_mailchimp_list(
    args["title"], args["url"], args["mailing_list_id"], args["api_key"]
)

print(f"Successfully send campaign {campaign['id']}\n")
