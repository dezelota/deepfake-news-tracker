# deepfake-news-tracker

A command-line tool that collects recent news articles about deepfakes from multiple RSS feeds, stores them in a local SQLite database with automatic deduplication, and uses a local LLM (Ollama) to summarize and classify each article.

## How it works

1. **Fetch** — pulls articles from 3 RSS feeds (Ars Technica, Hacker News, NYT Technology), filters for deepfake-related content, and scrapes the full article text
2. **Summarize** — sends each article to a local Llama 3.2 model via Ollama and generates a 2-3 sentence summary
3. **Tag** — classifies each article into one of 6 fixed categories: `technology`, `crime & scams`, `politics & policy`, `privacy & consent`, `education`, or `entertainment`

All data is stored in a local SQLite database (`deepfake.db`). Deduplication is handled automatically — re-running the fetcher will never create duplicate entries.

## Requirements

- [Ollama](https://ollama.com) with `llama3.2` installed

## Setup

1. Clone the repo
```bash
git clone https://github.com/yourusername/deepfake-news-tracker.git
cd deepfake-news-tracker
```

2. Create and activate the conda environment
```bash
conda env create -f environment.yml
conda activate deepfake-tracker
```

3. Install Ollama and pull the model
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
```

## Usage

Run all steps at once:
```bash
./newsfetch --all
```

Or run each step individually:
```bash
./newsfetch --fetch        # collect and scrape articles
./newsfetch --summarize    # summarize with Ollama
./newsfetch --tag          # classify into categories
```

If you run with no arguments it will print the help menu:
```bash
./newsfetch
```

## Sources

- [Ars Technica](https://feeds.arstechnica.com/arstechnica/technology-lab)
- [Hacker News](https://hnrss.org/newest?q=deepfake)
- [NYT Technology](https://rss.nytimes.com/services/xml/rss/nyt/Technology.rss)

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