# Social poster

Scripts to post articles to social media sites.

I intend to roll these into a GitHub Action to happen when I commit to my website repository at some point.

## Install dependencies

To run any of these scripts, you'll need to have the project dependencies installed into the an active Python environment. I recommend creating a local one so you don't pollute your system dependencies:

``` bash
$ python3 -m venv env3
$ source env3/bin/activate
$ pip3 install -r requirements.txt
```

## Hacker news

I stole most of this code [from David Bieber](https://davidbieber.com/snippets/2020-05-02-hackernews-submit/).

It uploads a link and title to news.ycombinator.com, and gives you the link to the discussion page.

### Usage instructions

``` bash
$ ./post-to-hacker-news.py --help
usage: post-to-hacker-news.py [-h] -u USERNAME [-p PASSWORD] -t TITLE -l LINK

Post an article to hacker news

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Username for login
  -p PASSWORD, --password PASSWORD
                        Password for login. Or use HN_PASSWORD env var.
  -t TITLE, --title TITLE
                        The article title
  -l LINK, --link LINK  URL to the article
```

### Posting an article

``` bash
$ ./post-to-hacker-news.py -u nottrobin -p xxxxxxxxx -t "Freedom from the tyranny of metrics" -l "https://robinwinslow.uk/freedom-from-the-tyranny-of-metrics"
Successfully logged in as nottrobin

fnid successfully extracted:
qOrqgH4XTxq2TaqfeUR4o5

Successfully submitted: https://news.ycombinator.com/item?id=31638829
```

## Twitter

The hardest part in getting this to work is setting up an app with the right permissions on https://developer.twitter.com/. You have to go under "User authentication settings", turn on OAuth 1.0a with "Read & Write permission". It will ask for a callback URL. It doesn't actually matter what this is, so you can just put in https://twitter.com if you want.

Anyway, once you've enabled all that, you just need to have saved your API key, API key secret, access token and access token secret (you don't need the bearer token for this).

### Usage instructions

``` bash
$ ./post-to-twitter.py --help
usage: post-to-twitter.py [-h] -t TWEET [-k API_KEY] [-s API_KEY_SECRET] [-a ACCESS_TOKEN] [-z ACCESS_TOKEN_SECRET]

Post an article to twitter.com

optional arguments:
  -h, --help            show this help message and exit
  -t TWEET, --tweet TWEET
                        The text of the tweet to send
  -k API_KEY, --api-key API_KEY
                        The API key for the twitter application. Or use TWITTER_API_KEY env var.
  -s API_KEY_SECRET, --api-key-secret API_KEY_SECRET
                        The API key secret for the twitter application. Or use TWITTER_API_KEY_SECRET env var.
  -a ACCESS_TOKEN, --access-token ACCESS_TOKEN
                        The access token for the twitter application. Or use TWITTER_ACCESS_TOKEN env var.
  -z ACCESS_TOKEN_SECRET, --access-token-secret ACCESS_TOKEN_SECRET
                        The access token secret for the twitter application. Or use TWITTER_ACCESS_TOKEN_SECRET env var.
```

### Posting an article

``` bash
$ ./post-to-twitter.py --tweet "hello worldly"
Successfully submitted tweet https://twitter.com/nottrobin/status/1534172049517727746
```
