import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def fetch_device(name):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        result = {}

        try:
            search_url = f"https://www.gsmarena.com/res.php3?sSearch={name.replace(' ', '+')}"
            await page.goto(search_url)

            link = page.locator(".makers a").first
            if await link.count() == 0:
                return {}

            href = await link.get_attribute("href")
            url = "https://www.gsmarena.com/" + href

            await page.goto(url)
            await page.wait_for_selector("#specs-list")

            soup = BeautifulSoup(await page.content(), "html.parser")

            # 이미지
            img = soup.select_one(".specs-photo-main img")
            result["image"] = img["src"] if img else ""

            # 이름
            name_tag = soup.select_one(".specs-phone-name-title")
            result["name"] = name_tag.text.strip() if name_tag else name

            # 스펙 파싱
            for table in soup.select("#specs-list table"):
                cat = table.find("th").text.strip()

                for row in table.find_all("tr"):
                    ttl = row.find("td", class_="ttl")
                    nfo = row.find("td", class_="nfo")

                    if ttl and nfo:
                        key = f"{cat}::{ttl.text.strip()}"
                        result[key] = nfo.text.strip()

        except Exception as e:
            print(e)

        await browser.close()
        return result


def get_device(name):
    return asyncio.run(fetch_device(name))
