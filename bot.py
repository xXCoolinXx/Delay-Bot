import datetime
import requests
from facebook_scraper import get_posts
from requests.cookies import RequestsCookieJar
from datetime import timedelta
from datetime import datetime
import http
import os
from time import sleep
from dotenv import load_dotenv
import asyncio

load_dotenv() 
TOKEN = os.getenv('BOT_ID')
fb_page = os.getenv('FB_PAGE')
keyword_list = ["closed", "open", "late", "delay"]
url = f"https://api.groupme.com/v3/bots/post?bot_id={TOKEN}&text="

def groupme_post(text):
    requests.post(url + text)

def check_fb_posts():
    for post in get_posts(fb_page, pages=1, cookies="cookies.json"):
        time_diff = datetime.now() - post['time']
        print(post['time'])
        if time_diff <= timedelta(minutes=5.10):
            for kw in keyword_list:
                if kw.lower() in post['text'].lower():
                    print(post['text'][:50])
                    groupme_post(\
                        "🚨 New post from SCS 🚨\n" + \
                        post['text'] + \
                        "\nhttps://www.facebook.com/SumnerSchools/")
                    break

def check_failsafe():
    #It fails sometimes :/
    try:
        check_fb_posts()
    except:
        check_fb_posts() 


def main():
    #Every five minutes, checking if a new post has been made in
    #the last 5.1 minutes that contains one of the keywords.
    #This is run in a separate thread to prevent from blocking and missing some posts
    #There is a small chance that a post will be sent twice, but this should be rare
    while True:
        print("Checking")
        asyncio.run(check_failsafe())
        print("Sleeping")
        sleep(5 * 60)

    


if __name__ == "__main__":
    main()