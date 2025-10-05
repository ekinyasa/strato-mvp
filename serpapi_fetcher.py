import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

def fetch_trends_with_serpapi(keyword):
    api_key = os.getenv("SERPAPI_API_KEY")  # <-- dikkat: key adı da düzeltildi!

    if not api_key:
        raise Exception("API anahtarı .env dosyasından alınamadı.")

    params = {
        "engine": "google_trends",
        "q": keyword,
        "geo": "TR",
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    timeline = results.get("interest_over_time", {}).get("timeline_data", [])

    if not timeline:
        raise Exception("Trends verisi bulunamadı.")

    return [
        {
            "date": point["date"],
            "value": point["values"][0]["extracted_value"]  # değer buradan geliyor
        }
        for point in timeline
    ]