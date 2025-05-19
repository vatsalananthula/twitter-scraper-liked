# X (Twitter) Liked Tweets Scrapper

## Disclaimer
- _Please be mindful of user privacy and obtain consent before utilizing any data. For research or analysis purposes, ensure proper user anonymization and clear communication about its usage_

## Overview
This Python script allows you to scrape user liked tweets from Twitter using Selenium WebDriver and BeautifulSoup.

The liked tweets data can potentially be leveraged. For instance:
- Understanding User Preferences: Analyzing the types of tweets a user likes provides valuable insights into their interests, preferences, and behaviors.
- Enhancing Marketing Strategies: Leveraging this data can optimize advertising efforts by targeting users with relevant content aligned with their interests, thereby maximizing engagement on social media platforms.
- Furthermore, this data forms the foundation of personalization, enabling platforms to tailor timelines, suggestions, or notifications based on users' liked tweets.

## Requirements
- Python 3.x
- Selenium WebDriver
- BeautifulSoup
- Pandas
- Web browser (Edge, Chrome, or Firefox)

## Installation
```bash
pip install -r requirements.txt
```

## Download WebDriver into local directory
Download the appropriate WebDriver for your browser:
Edge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
Chrome: https://chromedriver.chromium.org/downloads
Firefox: https://github.com/mozilla/geckodriver/releases

## Usage
Run the script from the command line:

```bash
python liked_tweets_scraper.py --username YOUR_USERNAME --password YOUR_PASSWORD --target TARGET_USERNAME
```

### Command Line Arguments:
- `--username` or `-u`: Your Twitter login username (required)
- `--password` or `-p`: Your Twitter login password (required)
- `--target` or `-t`: Username whose liked tweets to scrape (required)
- `--browser` or `-b`: Browser to use (choices: edge, chrome, firefox, default: edge)
- `--output` or `-o`: Output CSV file path (optional)
- `--max-tweets` or `-m`: Maximum number of tweets to scrape (optional)
- `--oldest-url`: URL of oldest tweet to scrape to (optional)

## Features
- Object-oriented design for better code organization
- Multi-browser support (Edge, Chrome, Firefox)
- Command-line interface for easy usage
- Detailed logging for troubleshooting
- Timestamp capture when available
- Proper URL formatting (adds base URL when needed)
- Error handling and graceful shutdown
- Automatic detection of end of scrollable content
- CSV output with configurable filename

## About the logic 
1. Login to Twitter
2. Navigate to the target user's liked tweets page
3. Either scroll to end or set a maximum number of tweets to collect
4. For each scroll iteration:
   - Parse the current page
   - Extract tweet data
   - Skip duplicates based on URLs
   - Check for stopping conditions (max tweets, oldest tweet, or end of content)
5. Save the collected data to CSV
