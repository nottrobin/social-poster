# Social poster

Scripts to post articles to social media sites.

I intend to roll these into a GitHub Action to happen when I commit to my website repository at some point.

## Hacker news

I stole most of this code [from David Bieber](https://davidbieber.com/snippets/2020-05-02-hackernews-submit/).

It uploads a link and title to news.ycombinator.com, and gives you the link to the discussion page.

``` bash
# Install dependencies
python3 -m venv env3
source env3/bin/activate
pip3 install -r requirements.txt

# Upload an article to hacker news
./post-to-hacker-news.py -u nottrobin -p xxxxxxxxx -t "Freedom from the tyranny of metrics" -l "https://robinwinslow.uk/freedom-from-the-tyranny-of-metrics"
```
