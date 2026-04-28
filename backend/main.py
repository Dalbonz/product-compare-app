from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

BASE = "https://www.gsmarena.com/"

@app.get("/device")
def get_device(name: str):
    search_url = f"{BASE}res.php3?sSearch={name.replace(' ', '+')}"
    res = requests.get(search_url)
    soup = BeautifulSoup(res.text, "html.parser")

    link = soup.select_one(".makers a")
    if not link:
        return {"error": "not found"}

    url = BASE + link.get("href")

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    data = {}

    title = soup.select_one(".specs-phone-name-title")
    if title:
        data["name"] = title.text.strip()

    img = soup.select_one(".specs-photo-main img")
    if img:
        data["image"] = img.get("src")

    chipset = soup.find("td", string="Chipset")
    if chipset:
        data["chipset"] = chipset.find_next("td").text

    return data
