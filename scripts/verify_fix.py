import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = "file://" + os.path.abspath(os.path.join(script_dir, "..", "HilalSync.html"))
        await page.goto(file_path)

        # Dhu al-Hijjah 1447 (1447-12)
        await page.fill("#hYearInput", "1447")
        await page.select_option("#hMonthInput", "12")
        await page.click("#goBtn")
        await page.wait_for_timeout(3000)

        verdict = await page.inner_text("#verdict")
        date_aceh = await page.inner_text("#dateAceh")
        date_gic = await page.inner_text("#dateGic")

        print(f"1447-12 Verdict: {verdict}")
        print(f"  MABBIMS: {date_aceh}")
        print(f"  GIC:     {date_gic}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
