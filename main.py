from fastapi import FastAPI
from pydantic import BaseModel
from scraper import fetch_icai_updates
import threading
import time

app = FastAPI(title="CA Studio ICAI Updates API")

class UpdateItem(BaseModel):
    title: str
    date: str
    url: str

# In-memory cache
cache = {
    "updates": [],
    "last_fetched": 0
}

CACHE_TTL = 3600 # 1 hour

def refresh_cache():
    print("Scraping fresh updates...")
    data = fetch_icai_updates()
    if data:
        cache["updates"] = data
        cache["last_fetched"] = time.time()
        print(f"Cache refreshed with {len(data)} updates.")

@app.on_event("startup")
def startup_event():
    # Initial fetch in background
    thread = threading.Thread(target=refresh_cache)
    thread.daemon = True
    thread.start()

@app.get("/api/v1/updates", response_model=list[UpdateItem])
def get_updates():
    # Check if cache is expired
    if time.time() - cache["last_fetched"] > CACHE_TTL:
        # Trigger background refresh, but return stale data immediately for fast UX
        thread = threading.Thread(target=refresh_cache)
        thread.daemon = True
        thread.start()
        
    return cache.get("updates", [])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
