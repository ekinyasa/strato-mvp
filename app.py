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
@app.route("/trends", methods=["GET"])
def trends():
    keyword = request.args.get("q", "")
    if not keyword:
        return jsonify({"error": "Kelime girilmedi."}), 400

    try:
        pytrends = TrendReq(hl='tr-TR', tz=180)

        time.sleep(1.5)  # 🔒 Google'a aşırı istek atmamak için bekletme

        pytrends.build_payload([keyword], cat=0, timeframe='today 3-m', geo='TR', gprop='')
        df = pytrends.interest_over_time()

        if df.empty:
            return jsonify([])

        data = [
            {"date": str(index.date()), "value": int(row[keyword])}
            for index, row in df.iterrows()
            if not row['isPartial']
        ]

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 Uygulama başlat
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
