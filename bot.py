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
                        f"🚨 New post from {fb_page} 🚨\n" + \
                        post['text'] + \
                        f"\nhttps://www.facebook.com/{fb_page}/")
                    break

def check_loop():
    while True:
        print("Checking")
        #It fails sometimes randomly so this is just a way to protect against that
        try:
            check_fb_posts()
        except:
            check_fb_posts() 
        print("Sleeping")
        sleep(5 * 60)

def main():
    asyncio.run(check_loop())


if __name__ == "__main__":
    main()
