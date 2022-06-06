# Social poster

Scripts to post articles to social media sites.

I intend to roll these into a GitHub Action to happen when I commit to my website repository at some point.

## Hacker news

I stole most of this code [from David Bieber](https://davidbieber.com/snippets/2020-05-02-hackernews-submit/).

It uploads a link and title to news.ycombinator.com, and gives you the link to the discussion page.

``` bash
# Install dependencies
$ python3 -m venv env3
$ source env3/bin/activate
$ pip3 install -r requirements.txt

# Upload an article to hacker news
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

$ ./post-to-hacker-news.py -u nottrobin -p xxxxxxxxx -t "Freedom from the tyranny of metrics" -l "https://robinwinslow.uk/freedom-from-the-tyranny-of-metrics"
Successfully logged in as nottrobin

fnid successfully extracted:
qOrqgH4XTxq2TaqfeUR4o5

Successfully submitted: https://news.ycombinator.com/item?id=31638829
```
