import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def fetch_device(name):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        data = {}

        try:
            search_url = f"https://www.gsmarena.com/res.php3?sSearch={name.replace(' ', '+')}"
            await page.goto(search_url)
            await page.wait_for_selector(".makers")

            links = await page.locator(".makers a").all()

            if not links:
                return {}

            href = await links[0].get_attribute("href")
            url = "https://www.gsmarena.com/" + href

            await page.goto(url)
            await page.wait_for_selector("#specs-list")

            soup = BeautifulSoup(await page.content(), "html.parser")

            # 이미지
            img = soup.select_one(".specs-photo-main img")
            if img:
                data["image"] = img.get("src") or img.get("data-src")

            # 이름
            title = soup.select_one(".specs-phone-name-title")
            if title:
                data["name"] = title.text.strip()

            # 스펙
            for table in soup.select("#specs-list table"):
                cat = table.find("th").text.strip()

                for tr in table.find_all("tr"):
                    ttl = tr.find("td", class_="ttl")
                    nfo = tr.find("td", class_="nfo")

                    if ttl and nfo:
                        key = f"{cat}::{ttl.text.strip()}"
                        data[key] = nfo.text.strip()

        except Exception as e:
            print(e)

        await browser.close()
        return data


def get_device(name):
    return asyncio.run(fetch_device(name))
