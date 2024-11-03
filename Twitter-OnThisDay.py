"""
This script finds tweets that were tweeted the same day in previous years, ala Facebook's memories.
Required for this to work are the files tweets.js and account.js, both of which are included in Twitter's downloadable data.
Before proceeding, make sure to edit the abovementioned files and remove "window.YTD.account.part0" to make the JSON valid.
"""

import json
from datetime import datetime
import pytz
import os
import webbrowser

def format_date(tweet):
    date_raw = tweet['tweet']['created_at']

    # String to datetime object
    date_obj = datetime.strptime(date_raw, "%a %b %d %H:%M:%S %z %Y")

    # Convert from UTC to Manila time
    date_obj_PHT = date_obj.astimezone(pytz.timezone('Asia/Manila'))

    # Datetime to string
    date_created_string = date_obj_PHT.strftime("%d %B %Y, %A | %I:%M:%S %p")

    return date_created_string, date_obj


def date_only(date_obj):
    # Datetime to string showing only date without year
    date_string = date_obj.strftime("%m-%d")  # 07-22 formatting for example
    return date_string


def print_tweets(tweet, username):
    if tweet['years_ago'] == 1:
        print(f"{tweet['years_ago']} year ago")
    else:
        print(f"{tweet['years_ago']} years ago")

    print(tweet['date_string'])
    print(f"\n{tweet['tweet_content']}\n")
    print(f"Likes: {tweet['likes']}")
    print(f"Retweets: {tweet['retweets']}")
    print(f"URL: https://x.com/{username}/status/{tweet['tweet_id']}")
    print("___________________________\n")

def load_tweets (tweet, username):
    url = f"https://x.com/{username}/status/{tweet['tweet_id']}"
    webbrowser.open(url, new=1, autoraise=True)

# Open and read account.js
with open(f'{os.getcwd()}/account.js', 'r', encoding='utf-8') as account_json:
    account_data = json.load(account_json)
# Extract username, to be used in the URL
username = account_data[0]['account']['username']

# Open and read tweets.js
with open(f'{os.getcwd()}/tweets.js', 'r', encoding='utf-8') as tweet_json:
    tweet_data = json.load(tweet_json)

on_this_day = []  # Empty list that will contain tweet IDs of today's tweets

print ("ON THIS DAY ON TWITTER")
while True:
    option = input("\n1 - See today's tweets\n2 - Enter custom date\n0 - Exit\n")
    if option == "1":
        selected_date = datetime.now()
        break
    elif option == "2":
        while True:
            selected_date = input("Input a date (MM-DD): ")
            try:
                selected_date = datetime.strptime(selected_date, "%m-%d")
                break
            except Exception as e:
                print("Please enter a valid date in the correct format!")
        break
    elif option == "0":
        exit()
    else:
        print("Input a valid value!")


# Extract same-day tweets and transfer to list
for tweet in tweet_data:
    date_string, date_obj = format_date(tweet)
    if date_only(date_obj.date()) == date_only(selected_date):
        years_ago = datetime.today().year - date_obj.year
        tweet_content = tweet['tweet']['full_text']
        likes = int(tweet['tweet']['favorite_count'])
        retweets = int(tweet['tweet']['retweet_count'])
        tweet_id = int(tweet['tweet']['id'])
        on_this_day.append({'date_string': date_string, 'date_obj': date_obj, 'years_ago': years_ago, 'tweet_content': tweet_content, 'likes': likes, 'retweets': retweets, 'tweet_id': tweet_id})

# Arrange tweets by dates in ascending order
sorted_on_this_day = sorted(on_this_day, key=lambda tweet: tweet['date_obj'])

# Print tweets
print("\nYou have reached the end!\n")
for tweet in sorted_on_this_day:
    print_tweets(tweet, username)

print(f"Number of tweets this day: {len(sorted_on_this_day)}\n")

while True:
    load = input("\n1 - Load tweets on a web browser\n0 - Exit\n")
    if load == '1':
        for tweet in sorted_on_this_day:
            load_tweets (tweet, username)
        break
    elif load == "0":
        break
    else:
        print("Input a valid value!")

print("Goodbye")