import requests
from bs4 import BeautifulSoup

BASE = "https://www.gsmarena.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def search_device(name):
    url = f"{BASE}res.php3?sSearch={name.replace(' ', '+')}"
    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    link = soup.select_one(".makers a")
    if not link:
        return None

    return BASE + link.get("href")

def parse_device(url):
    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    data = {}

    # 이름
    title = soup.select_one(".specs-phone-name-title")
    if title:
        data["name"] = title.text.strip()

    # 이미지
    img = soup.select_one(".specs-photo-main img")
    if img:
        data["image"] = img.get("src")

    # 스펙
    for table in soup.select("#specs-list table"):
        cat = table.find("th").text.strip()

        for tr in table.find_all("tr"):
            ttl = tr.find("td", class_="ttl")
            nfo = tr.find("td", class_="nfo")

            if ttl and nfo:
                key = f"{cat}::{ttl.text.strip()}"
                data[key] = nfo.text.strip()

    return data

def get_device(name):
    url = search_device(name)
    if not url:
        return {}
    return parse_device(url)
