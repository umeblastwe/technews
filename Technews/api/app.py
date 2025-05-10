from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Route for frontend
@app.route('/')
def index():
    return render_template('main.html')

# Route for getting news data from NewsAPI
@app.route('/main')
def main():
    api_key = 'your_newsapi_key_here'  # Replace with your NewsAPI key
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    
    try:
        response = requests.get(url)
        data = response.json()
        return jsonify({"articles": data.get("articles", [])})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
