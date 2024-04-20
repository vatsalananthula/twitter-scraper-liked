# X (Twitter) Liked Tweets Scrapper

## Disclaimer
- _The data I scrapped is strictly from my own account and is intended solely for my personal use_
- _It's crucial to address ethical concerns. Please be mindful of user privacy and obtain consent before utilizing any data. For research or analysis purposes, ensure proper user anonymization and clear communication about its usage_

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

## About the logic 
1. Scroll down by a specified amount.
2. Parse the current page.
3. Extract the data and append it to a list.
4. Repeat steps 1–3 until reaching the end of the page.
5. Create DataFrames from the list.
