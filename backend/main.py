from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

BASE = "https://www.gsmarena.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


@app.get("/")
def root():
    return {"msg": "API OK"}


@app.get("/device")
def get_device(name: str):
    # 1. 검색
    search_url = f"{BASE}res.php3?sSearch={name.replace(' ', '+')}"
    res = requests.get(search_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    # 2. 첫 번째 결과
    link = soup.select_one(".makers li a")
    if not link:
        return {"error": "not found"}

    url = BASE + link.get("href")

    # 3. 상세 페이지
    res = requests.get(url, headers=HEADERS)
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

    # 스펙 테이블 파싱
    specs = {}
    for row in soup.select(".specs-table tr"):
        key = row.select_one("td.ttl")
        val = row.select_one("td.nfo")

        if key and val:
            specs[key.text.strip()] = val.text.strip()

    # 필요한 것만 추출
    data["chipset"] = specs.get("Chipset")
    data["display"] = specs.get("Size")
    data["battery"] = specs.get("Battery")
    data["memory"] = specs.get("Internal")

    return data
