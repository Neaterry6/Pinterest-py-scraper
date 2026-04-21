import requests
import random
import os
import json
from flask import Flask, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
]

def get_user_agent():
    return random.choice(user_agents)

def scrape_pinterest(keyword, num):
    try:
        headers = {'User-Agent': get_user_agent()}
        url = f"https://www.pinterest.com/search/pins/?q={keyword}"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Pinterest embeds JSON in a script tag with id="__PWS_DATA__"
        data_script = soup.find('script', id="__PWS_DATA__")
        if not data_script or not data_script.string:
            return []

        data_json = json.loads(data_script.string)

        # Navigate into the JSON to find pin images
        pins = data_json.get("props", {}).get("initialReduxState", {}).get("pins", {})
        results = []
        for pin in pins.values():
            if "images" in pin and "orig" in pin["images"]:
                results.append(pin["images"]["orig"]["url"])
            if len(results) >= num:
                break

        return results
    except Exception as e:
        return [f"Error: {str(e)}"]

@app.route('/pin/<keyword>/<int:num>', methods=['GET'])
def pin(keyword, num):
    image_urls = scrape_pinterest(keyword, num)
    return jsonify({'keyword': keyword, 'count': num, 'image_urls': image_urls})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
