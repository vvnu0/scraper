'''
might not be possible
https://www.reddit.com/r/learnprogramming/comments/ozzvce/getting_html_code_of_instagram_profile/
insta caught onto me ig
'''

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape_instagram_profile(username):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the Instagram profile
        url = f"https://www.instagram.com/{username}/"
        page.goto(url)

        # Wait for the network to be idle to ensure all resources are loaded
        page.wait_for_load_state('networkidle')

        # Wait for the profile header to be visible
        page.wait_for_selector('header')

        # Extract the header content
        header_content = page.content()
        browser.close()

        # Parse the header content with BeautifulSoup
        soup = BeautifulSoup(header_content, 'html.parser')
        header = soup.find('header')
        if header:
            print(header.prettify())
        else:
            print("Header content not found")

# Replace 'username' with the actual Instagram username you want to scrape
username = 'vishnnunair'  # Example username
scrape_instagram_profile(username)
