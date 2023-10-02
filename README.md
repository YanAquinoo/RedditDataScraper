# Reddit Data Scraper

The Reddit Data Scraper is a Python script that allows you to collect data from multiple subreddits on Reddit.
It consists of two main components: `runner.py` and `scraper.py`. 
- `runner.py` coordinates the execution of the scraper, while
- `scraper.py` retrieves and processes data from Reddit.

## Directory Structure

~~~
├── files
│   ├── mined_subreddits.txt
│   └── subreddits.txt
├── logs
│   ├── reddit_scraper.log
│   └── reddit_scraper_runner.log
├── output
└── src
    ├── runner.py
    └── scraper.py
~~~

### Files

  - `mined_subreddits.txt`: This file stores the names of subreddits that have already been mined by the scraper to avoid redundant data collection.
  - `subreddits.txt`: You can specify the list of subreddits you want to scrape in this file.

#### Logs

  - `reddit_scraper.log`: This log file records the activity and any errors that occur during data scraping.
  - `reddit_scraper_runner.log`: The runner script logs its activities and any errors here.

#### Output

This directory is where the scraped data will be saved. Each subreddit's data is stored in a JSON file with a name in the format `subredditname_data.json`.

#### Source Code

  - `runner.py`: This script is responsible for running the scraper at specified intervals until all subreddits are mined.
  - `scraper.py`: The scraper script connects to the Reddit API, collects data from the specified subreddits, and saves it to JSON files.

## Prerequisites

- Python 3 or higher.
- Python Library PRAW (Python Reddit API Wrapper)
- Reddit API credentials, including a client ID, client secret, username, and password.

## Usage

1. Ensure you have the required Python package installed. You can typically install it using pip:

~~~bash
pip install praw
~~~

2. Set up your Reddit API credentials by replacing the placeholders in `scraper.py` with your actual credentials.

3. Create a list of subreddits to scrape and save them in `files/subreddits.txt`, with each subreddit name on a separate line.

### Option 1: Using Runner.py
4. Run `runner.py` to start the scraping process:

~~~bash  
python3 src/runner.py
~~~

  This will continuously call the scraper.py script, untill all given Subreddits are collected. 

### Option 2: Scraper.py
4. You can run this script directly, without the runner, using:
   
~~~bash
python3 src/scraper/py
~~~

Note that, if you opt for option 2, if an unexpected error occur during the scraping of one Subreddit, it will be skipped, and its data will not be collected.
