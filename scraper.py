# scraper.py - 개선 버전
import requests
from bs4 import BeautifulSoup
import time

BASE = "https://www.gsmarena.com/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def search_device(name: str):
    """제품 검색 후 상세 페이지 URL 반환"""
    if not name:
        return None
    url = f"{BASE}res.php3?sSearch={name.replace(' ', '+')}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        link = soup.select_one(".makers a")
        if link and link.get("href"):
            return BASE + link.get("href")
    except:
        pass
    return None

def parse_device(url: str):
    """상세 페이지에서 스펙 파싱"""
    if not url:
        return {}
    try:
        res = requests.get(url, headers=HEADERS, timeout=12)
        soup = BeautifulSoup(res.text, "html.parser")

        data = {}

        # 이름
        title = soup.select_one(".specs-phone-name-title")
        if title:
            data["name"] = title.text.strip()

        # 이미지
        img = soup.select_one(".specs-photo-main img")
        if img and img.get("src"):
            data["image"] = img.get("src") if img.get("src").startswith("http") else "https:" + img.get("src")

        # 스펙 테이블 파싱 (더 많은 키를 안정적으로 가져옴)
        for table in soup.select("#specs-list table"):
            cat = table.find("th").text.strip() if table.find("th") else ""
            for tr in table.find_all("tr"):
                ttl = tr.find("td", class_="ttl")
                nfo = tr.find("td", class_="nfo")
                if ttl and nfo:
                    key = f"{cat}::{ttl.text.strip()}"
                    data[key] = nfo.text.strip()

        # chipset 키 통합
        if "Platform::Chipset" not in data and "chipset" not in data:
            chipset = soup.find("td", string=lambda t: t and "Chipset" in t)
            if chipset and chipset.find_next("td"):
                data["Platform::Chipset"] = chipset.find_next("td").text.strip()

        return data
    except:
        return {}

def get_device(name: str):
    """메인 함수 - 캐싱 없이도 조금 더 안정적으로"""
    url = search_device(name)
    if not url:
        return {"name": name, "error": "not found"}
    return parse_device(url)
