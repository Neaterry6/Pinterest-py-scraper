

import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import random

def get_pinterest_images(query, count):
    url = "https://www.pinterest.com/"
    user_agent = UserAgent()
    user_agents = [user_agent.random for _ in range(10)]
    proxies = [
        'http://209.50.52.162:9050',
        'http://51.15.154.144:8080',
        'http://138.197.104.72:8080',
        # Add more proxies here
    ]
    image_urls = []
    for _ in range(count):
        proxy = random.choice(proxies)
        user_agent = random.choice(user_agents)
        headers = {
            "User-Agent": user_agent
        }
        params = {
            "q": query
        }
        response = requests.get(url, headers=headers, params=params, proxies={'http': proxy, 'https': proxy})
        soup = BeautifulSoup(response.content, "html.parser")
        for pin in soup.find_all("img"):
            image_url = pin.get("src")
            if image_url:
                image_urls.append(image_url)
    return image_urls

def send_images(image_urls):
    print("Image URLs:")
    for url in image_urls:
        print(url)

def main():
    query = "cat"
    count = 5
    image_urls = get_pinterest_images(query, count)
    send_images(image_urls)

if __name__ == "__main__":
    main()
