from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

# Initialize the WebDriver
driver = webdriver.Edge()
driver.get('https://twitter.com/i/flow/login')
wait = WebDriverWait(driver, 10)


# Login to your account first
username = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete=username]'))
)
username.send_keys("fill with ur username")

login_button = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '[role=button].r-13qz1uu'))
)
login_button.click()

password = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '[type=password]'))
)
password.send_keys("fill with ur password")

login_button = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid*=Login_Button]'))
)
login_button.click()

direct_message_link = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid=AppTabBar_DirectMessage_Link]'))
)

# Navigate to the user liked tweets page 
driver.get("https://twitter.com/(username target)/likes")

# There are two function to scroll down. This one is use to scroll to the end of page
# This function is use to get the url of the oldest liked tweet
def scroll_to_end():
    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        # break condition
        if new_height == last_height:
            break
        last_height = new_height
      
scroll_to_end()

# This second scroll down function is use to scrolls the page down by a specified amount. I use 1000 pixels.
def scroll_down(driver, scroll_amount=1000):
    driver.execute_script(f"window.scrollTo(0, window.scrollY + {scroll_amount})")

# Define a function to parse the tweets
def parse_tweets(driver):
    """Parses the current page content and returns a list of tweet elements."""
    response = BeautifulSoup(driver.page_source, 'html.parser')
    tweets = response.find_all('article')  
    return tweets

# Define a function to extract tweet data: username, tweet text, image URL, tweet URL, and profile type (indicating whether the user is personal or a base account) 
# Replace with the appropriate selector if needed
def get_tweet_data(tweet_element):
    data = {}

    username_element = tweet_element.find('div', class_='css-175oi2r', attrs={'data-testid': 'User-Name'})
    if username_element:
        data['Username'] = username_element.text.strip()
    else:
        data['Username'] = ''
    
    image_element = tweet_element.find('div', class_='css-175oi2r', attrs={'data-testid': 'tweetPhoto'})
    if image_element:
        for child in image_element.children:
            if child.name == 'img':
                data['Image'] = child['src']
    else:
        data['Image'] = ''

    tweet_text_element = tweet_element.find('div', class_='css-1rynq56', attrs={'data-testid': 'tweetText'})

    if tweet_text_element:
        # Initialize an empty list to store the content
        tweet_content = []
        for child in tweet_text_element.children:
            # Extract text and emoji alt text
            if child.name == 'span':
                tweet_content.append(child.text.strip())
            elif child.name == 'img':
                tweet_content.append(child['alt'])

        # Join the content into a single string
        data['Tweet'] = ' '.join(tweet_content)
    else:
        data['Tweet'] = ''

    url_element = tweet_element.find('a', class_='css-1rynq56')
    if url_element:
        data['Url'] = url_element.get('href')
    else:
        data['Url'] = ''
        
    profile_type_element = tweet_element.find('div', class_='css-1rynq56 r-dnmrzs r-1udh08x r-3s2u2q r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41')

    if profile_type_element:
        for child in profile_type_element.children:
            if child.name == 'span':
                data['Profile_type'] = child.text
    else:
        data['Profile_type'] = ""

    return data

# Define the main function
def get_dataframe_and_check_duplicates(driver, max_scrolls=10):
    """Scrolls the page, extracts tweet data, and checks for duplicates before adding to DataFrame."""
    tweet_data_list = []
    scroll_count = 0

    last_tweet_set = set()  # Store the set of tweet URLs to check for duplicates
    condition= True

    while condition:
        if scroll_count==0:
            tweets = parse_tweets(driver)
        
        else:       
            scroll_down(driver)
            time.sleep(2.5) 
            tweets = parse_tweets(driver)
         # Adjust sleep time as needed to allow page to load

        for tweet in tweets:
            tweet_data = get_tweet_data(tweet)
            tweet_url = tweet_data.get('Url', '')  # Get tweet URL if available
            if tweet_url not in last_tweet_set:  # Check if tweet URL is new
                tweet_data_list.append(tweet_data)
                last_tweet_set.add(tweet_url)  # Add URL to seen set
        
        if scroll_count==0:
            print(scroll_count, len(tweet_data_list))
        else:
            print(scroll_count, len(tweet_data_list), tweet_data_list[-1].get('Url'), tweet_data_list[-1].get('Profile_type'))
            
        scroll_count += 1
        if tweet_data_list[-1].get('Url')=='(url from the oldest liked post)': # you can get the url with the first scroll down function
            condition=False
            
    column_names = ['Username', 'Tweet', 'Image', 'Url', 'Profile_type']
    df = pd.DataFrame(tweet_data_list, columns=column_names)

    if len(df) < 1393:
        print(f"Reached end of scrollable content, collected {len(df)} tweets (less than target).")
    else:
        print(f"Collected {len(df)} tweets (target reached).")

    return df

df = get_dataframe_and_check_duplicates(driver)
# And you can save to CSV!
