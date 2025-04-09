import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()  # .env dosyasındaki API_KEY'i çekmek için

def fetch_trends_with_serpapi(keyword):
    params = {
        "engine": "google_trends",
        "q": keyword,
        "geo": "TR",
        "api_key": os.getenv("SERPAPI_API_KEY")
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    if "interest_over_time" in results:
        return [
            {"date": point["date"], "value": point["value"]}
            for point in results["interest_over_time"]
        ]
    else:
        raise Exception("Trends verisi bulunamadı.")
