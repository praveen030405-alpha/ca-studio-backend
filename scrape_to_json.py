import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import datetime

def fetch_and_save():
    updates = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            print("Navigating to ICAI portal...")
            page.goto("https://www.icai.org/post/important-announcements", timeout=60000, wait_until="domcontentloaded")
            
            page.wait_for_timeout(2000)
            
            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            container = soup.find(class_="page-content")
            if container:
                list_items = container.find_all("li")
                for li in list_items[:10]:
                    link = li.find("a")
                    if link:
                        text = link.get_text(strip=True)
                        href = link.get("href", "")
                        
                        if href and not href.startswith("http"):
                            href = "https://www.icai.org" + href
                        
                        date_str = datetime.datetime.now().strftime("%b %d, %Y")
                        date_span = li.find(class_="date")
                        if date_span:
                            date_str = date_span.get_text(strip=True)
                            
                        if text and len(text) > 10:
                            updates.append({
                                "title": text,
                                "date": date_str,
                                "url": href
                            })
            
            browser.close()
            
            if updates:
                with open("updates.json", "w") as f:
                    json.dump(updates, f, indent=4)
                print(f"Successfully scraped and saved {len(updates)} updates.")
            else:
                print("No updates found.")

    except Exception as e:
        print(f"Error scraping: {e}")

if __name__ == "__main__":
    fetch_and_save()
