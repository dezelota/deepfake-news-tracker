# deepfake-news-tracker

A command-line tool that collects recent news articles about deepfakes from multiple RSS feeds, stores them in a local SQLite database with automatic deduplication, and uses Claude (Anthropic) to summarize and classify each article.

## How it works

1. **Fetch**: pulls articles from 5 RSS feeds (Hacker News, Ars Technica, NPR, Wired, Time), filters for deepfake and synthetic media related content, and scrapes the full article text
2. **Summarize**: sends each article to Claude and generates a 2-3 sentence summary
3. **Tag**: classifies each article into one of 6 fixed categories: `technology`, `crime & scams`, `politics & policy`, `privacy & consent`, `education`, or `entertainment`
4. **Export**: exports all articles to a CSV file

All data is stored in a local SQLite database (`deepfake.db`). Deduplication is handled automatically — re-running the fetcher will never create duplicate entries.

## Requirements

- An Anthropic API key — get one at [console.anthropic.com](https://console.anthropic.com)

## Setup

1. Clone the repo
```bash
git clone https://github.com/dezelota/deepfake-news-tracker.git
cd deepfake-news-tracker
```

2. Create and activate the conda environment
```bash
conda env create -f environment.yml
conda activate deepfake-tracker
```

3. Add your API key — copy the example env file and fill in your key:
```bash
cp .env.example .env
```
Then open `.env` and replace `your-key-here` with your actual Anthropic API key, which you can get at [console.anthropic.com](https://console.anthropic.com).

## Usage

Ensure it has permissions to run:
```bash
chmod +x newsfetch
```

Run all steps at once:
```bash
./newsfetch --all
```

Or run each step individually:
```bash
./newsfetch --fetch        # collect and scrape articles
./newsfetch --summarize    # summarize with Claude
./newsfetch --tag          # classify into categories
./newsfetch --export       # export to articles.csv
```

If you run with no arguments it will print the help menu:
```bash
./newsfetch
```

## Sources

- [Hacker News](https://hnrss.org/newest?q=deepfake)
- [Ars Technica](https://feeds.arstechnica.com/arstechnica/index)
- [NPR](https://feeds.npr.org/1019/rss.xml)
- [Wired](https://www.wired.com/feed/rss)
- [Time](https://time.com/feed/)

## Database schema

| column | type | description |
|---|---|---|
| id | INTEGER | primary key |
| url | TEXT | article URL (unique) |
| title | TEXT | article title |
| source | TEXT | RSS feed source |
| published | TEXT | publication date |
| content | TEXT | full article text |
| summary | TEXT | LLM-generated summary |
| tags | TEXT | LLM-assigned category |