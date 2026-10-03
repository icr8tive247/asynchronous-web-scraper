import asyncio
import csv
import json
import logging
from datetime import datetime
from playwright.async_api import async_playwright
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

class DynamicDataExtractor:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.extracted_data = []
        self.browser_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    async def extract_page_data(self):
        logging.info(f"Initializing headless browser instance for: {self.base_url}")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(extra_http_headers=self.browser_headers)
            page = await context.new_page()
            try:
                await page.goto(self.base_url, wait_until="networkidle", timeout=60000)
                logging.info("Network idle state reached. Parsing DOM elements...")
                elements = await page.locator(".submission").all()
                if not elements:
                    elements = await page.locator("tr.athing").all()

                for index, element in enumerate(elements[:25]):
                    try:
                        title_element = element.locator("td.title > span.titleline > a")
                        if await title_element.count() > 0:
                            raw_title = await title_element.first.inner_text()
                            raw_url = await title_element.first.get_attribute("href")
                        else:
                            continue

                        clean_title = raw_title.strip().replace("\n", "").replace("\r", "")
                        record = {
                            "id": index + 1,
                            "timestamp": datetime.utcnow().isoformat(),
                            "source_domain": self.base_url,
                            "extracted_title": clean_title,
                            "extracted_url": raw_url if raw_url.startswith("http") else f"{self.base_url}{raw_url}"
                        }
                        self.extracted_data.append(record)
                    except Exception as e:
                        logging.warning(f"Failed parsing node entry index {index}: {str(e)}")
                        continue
                logging.info(f"Data pipeline complete. Successfully extracted {len(self.extracted_data)} records.")
            except Exception as e:
                logging.error(f"Critical execution error during browser workflow: {str(e)}")
            finally:
                await context.close()
                await browser.close()

    def export_datasets(self, base_filename: str):
        if not self.extracted_data:
            logging.error("No valid dataset memory footprint available for serialization.")
            return
        json_file = f"{base_filename}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(self.extracted_data, f, indent=4, ensure_ascii=False)
        csv_file = f"{base_filename}.csv"
        df = pd.DataFrame(self.extracted_data)
        df.to_csv(csv_file, index=False, encoding="utf-8")

if __name__ == "__main__":
    TARGET_ENDPOINT = "https://ycombinator.com"
    OUTPUT_NAME = "normalized_web_extraction"
    extractor = DynamicDataExtractor(base_url=TARGET_ENDPOINT)
    asyncio.run(extractor.extract_page_data())
    extractor.export_datasets(base_filename=OUTPUT_NAME)
