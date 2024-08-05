import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import logging
import time

logging.basicConfig(level=logging.INFO)

async def scrape_linkedin_profile(page):
    await page.wait_for_timeout(2000)  # Wait for page to load

    if 'authwall' in page.url:
        await page.screenshot(path='auth.png')
        return -1
    
    # Close popup if present
    try:
        await page.locator('button[aria-label="Dismiss"]').click()
    except:
        pass  # No popup present

    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')

    try:
        name = soup.select_one('div[class*="top-card__profile-image"] img')['alt']
        profile_picture = soup.select_one('div[class*="top-card__profile-image"] img')['src']

        # Check for default profile picture
        if profile_picture == 'https://static.licdn.com/aero-v1/sc/h/9c8pery4andzj6ohjkjp54ma2':
            profile_picture = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRTHp7HDUzfrraXrobnp_eKUtNeFiq9E8NklA&s'
        
        university = None
        # Search for university information
        education_section = soup.find('div', {'data-section': 'educationsDetails'})
        if education_section:
            university = education_section.find('span', {'class': 'top-card-link__description'}).get_text(strip=True)

        return {
            'name': name,
            'profile_picture': profile_picture,
            'university': university,
        }
    except Exception as e:
        await page.screenshot(path='error_screenshot.png')
        logging.error(f"Error scraping profile: {e}")
        return -1

async def main(query, links=None):
    if links is None:
        links = set()
    
    search_url = f'https://www.google.com/search?q={query}'

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.goto(search_url)
        await page.wait_for_timeout(2000)  # Wait for results to load
        await page.screenshot(path='google-search.png')
        
        if not links:  # Extract top 5 unique links
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
        
            for link in soup.select('a[href^="https://www.linkedin.com/in/"]')[:5]:
                links.add(link["href"])

        logging.info(f"Found links: {links}")
        results = []

        # Extract data from each LinkedIn profile
        while links:
            link = list(links)[0]
            await page.goto(link)
            profile_data = await scrape_linkedin_profile(page)
            
            if profile_data == -1:
                return results, links
            
            links.remove(link)

            if profile_data['university'] != 'Cornell University':
                logging.info(f"Skipped: {profile_data['name']} is not from Cornell University.")
                continue

            results.append({
                'name': profile_data['name'],
                'profile_picture': profile_data['profile_picture'],
                'university': profile_data['university'],
                'link': link
            })
            
            logging.info(f"Scraped: {profile_data['name']}")

        await browser.close()

    return results, links

def runSearch(query):
    try_again = 0
    res = []
    links = set()

    while try_again < 3:
        logging.info("Trying again from the start")
        time.sleep(1)  # Adding useful sleep intervals
        results, links = asyncio.run(main(query, links))
        res.extend(results)
        if not links:
            break
        try_again += 1

    logging.info(f"Final results: {res}")
    if links:
        logging.info(f"Couldn't check the rest, is it one of these? {links}")

    return res, links

# query = '"Victoria" "Cornell University" site:linkedin.com/in'
# res, links = runSearch(query)