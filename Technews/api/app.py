from flask import Flask, render_template, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Set your API keys here (or use environment variables for better security)
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "your_newsapi_key")  # Replace with your actual NewsAPI key
CURRENTAPI_KEY = os.getenv("CURRENTAPI_KEY", "your_currentapi_key")  # Replace with your actual CurrentAPI key

# Function to format the time
def format_time(timestamp):
    try:
        dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime("%d %b %Y, %I:%M %p")
    except:
        return timestamp

# Fetch tech news from NewsAPI
def fetch_from_newsapi():
    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"category=technology&language=en&pageSize=10&apiKey={NEWSAPI_KEY}"
    )
    res = requests.get(url)
    data = res.json()

    if data.get("status") != "ok":
        raise Exception("NewsAPI failed")

    articles = []
    for article in data["articles"]:
        articles.append({
            "title": article["title"],
            "description": article["description"],
            "url": article["url"],
            "source": article["source"]["name"],
            "publishedAt": format_time(article["publishedAt"]),
        })
    return articles

# Fetch tech news from CurrentAPI
def fetch_from_currentapi():
    url = (
        f"https://api.currentsapi.services/v1/latest-news?"
        f"language=en&category=technology&apiKey={CURRENTAPI_KEY}"
    )
    res = requests.get(url)
    data = res.json()

    if data.get("status") != "ok":
        raise Exception("CurrentAPI failed")

    articles = []
    for article in data["news"]:
        articles.append({
            "title": article["title"],
            "description": article["description"],
            "url": article["url"],
            "source": article.get("author", "CurrentAPI"),
            "publishedAt": format_time(article["published"]),
        })
    return articles

# Main function to fetch news from either API
def fetch_tech_news():
    try:
        return fetch_from_newsapi()
    except Exception as e:
        print(f"NewsAPI failed: {e}")
        try:
            return fetch_from_currentapi()
        except Exception as e:
            print(f"CurrentAPI failed: {e}")
            return []  # Return empty list if both APIs fail

@app.route("/")
def home():
    articles = fetch_tech_news()
    return render_template("main.html", articles=articles)

# Vercel compatibility (for serverless deployment)
def handler(request, context):
    return app(request.environ, start_response=context.start_response)

if __name__ == "__main__":
    app.run(debug=True)
