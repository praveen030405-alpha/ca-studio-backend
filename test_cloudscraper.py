import cloudscraper
from bs4 import BeautifulSoup

def test_icai():
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
    try:
        response = scraper.get("https://www.icai.org/post/important-announcements")
        print("Status code:", response.status_code)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select('.item a')
        
        for link in links[:3]:
            title = link.text.strip()
            print(f"Title: {title}")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_icai()
