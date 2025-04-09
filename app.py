from flask import Flask, request, jsonify
from flask_cors import CORS
from pytrends.request import TrendReq
import requests
import json
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔹 Autocomplete endpoint
@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    keyword = request.args.get("q", "")
    if not keyword:
        return jsonify([])

    url = "http://suggestqueries.google.com/complete/search"
    params = {
        "client": "firefox",
        "hl": "tr",
        "gl": "tr",
        "q": keyword
    }

    response = requests.get(url, params=params)
    suggestions = json.loads(response.text)[1]
    return jsonify(suggestions)

# 🔹 Google Trends endpoint
@app.route("/trends")
def get_trends():
    keyword = request.args.get("q", "")
    if not keyword:
        return jsonify({"error": "No keyword provided"}), 400

    try:
        pytrends = TrendReq(
            hl='tr-TR',
            tz=180,
            requests_args={
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
            }
        )

        time.sleep(3)  # 🧘 Daha yavaş sorgu → ban riskini azaltır

        pytrends.build_payload([keyword], cat=0, timeframe='today 3-m', geo='TR', gprop='')
        df = pytrends.interest_over_time()

        print("✅ Payload oluşturuldu:", keyword)
        print("📈 Veriler çekiliyor...")

        if df.empty:
            return jsonify([])

        data = [
            {"date": str(index.date()), "value": int(row[keyword])}
            for index, row in df.iterrows()
            if not row['isPartial']
        ]

        return jsonify(data)

    except Exception as e:
        print("Google Trends hatası:", str(e))
        if "429" in str(e):
            return jsonify({"error": "The request failed: Google returned a response with code 429"}), 200
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# 🔹 Uygulama başlat
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
