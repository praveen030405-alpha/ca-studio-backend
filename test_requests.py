import requests
from bs4 import BeautifulSoup

def test_icai():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get("https://www.icai.org/post/important-announcements", headers=headers)
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
