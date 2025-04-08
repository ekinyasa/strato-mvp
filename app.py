from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  # Tüm kaynaklara CORS izni verir

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
