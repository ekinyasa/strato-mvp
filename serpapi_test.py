# serpapi_test.py
from serpapi_fetcher import fetch_trends_with_serpapi

if __name__ == "__main__":
    keyword = input("Anahtar kelime girin: ")
    try:
        data = fetch_trends_with_serpapi(keyword)
        print("📊 Veri başarıyla çekildi:\n")
        for item in data:
            print(f"{item['date']}: {item['value']}")
    except Exception as e:
        print("❌ Hata:", e)