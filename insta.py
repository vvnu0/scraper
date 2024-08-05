import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def get_instagram_profile_info(username):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        url = f"https://www.instagram.com/{username}/"

        # Go to the Instagram profile page
        page.goto(url)
        
        # Wait for the media (profile picture) to load
        page.wait_for_load_state('networkidle')

        # Extract the page content after loading
        content = page.content()
        browser.close()

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')

        # Extract profile picture link
        profile_pic_tag = soup.find('meta', property='og:image')
        profile_pic = profile_pic_tag['content'] if profile_pic_tag else None

        # Extract name - can't get the name for some reason (maybe insta caught onto to me but image retrival still works)
        # so there's an insta ban thing where if you send too many requests - insta ip bans u for a bit & name can't be access
        # keep this in an if condition - if this is the profile they choose - use the name to find linkedin profile
        # a way to get thu this are proxies but we can ignore that for now
        name_tag = soup.find('span', class_='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj')
        name = name_tag.text if name_tag else None

        return {
            "profile_picture": profile_pic,
            "name": name,
            "username": username,
            "profile_link": url
        }

# Example usage
# username = "adypatnaik"
# profile_info = get_instagram_profile_info(username)
# print(profile_info) # dictionary

'''
https://www.reddit.com/r/webscraping/comments/wzobpy/what_are_my_options_for_proxies_for_webscraping/
https://www.reddit.com/r/webscraping/comments/xvyisf/advice_on_scraping_instagram/
robots.txt - https://www.reddit.com/r/webscraping/comments/q4u7p7/help_in_scraping_instagram/

https://instaloader.github.io/ - but will be taken down if u use this
'''