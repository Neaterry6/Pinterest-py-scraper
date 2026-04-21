import requests
import os
from flask import Flask, jsonify

app = Flask(__name__)

def get_unsplash_images(keyword, num):
    urls = []
    for _ in range(num):
        try:
            # Unsplash Source API returns a redirect to a random image
            url = f"https://source.unsplash.com/600x400/?{keyword}"
            response = requests.get(url, allow_redirects=True, timeout=10)
            urls.append(response.url)
        except Exception:
            # Fallback to Picsum if Unsplash fails
            urls.append("https://picsum.photos/600/400")
    return urls

@app.route('/pin/<keyword>/<int:num>', methods=['GET'])
def pin(keyword, num):
    image_urls = get_unsplash_images(keyword, num)
    return jsonify({'keyword': keyword, 'count': num, 'image_urls': image_urls})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
