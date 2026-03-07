import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Load the file
        file_path = "file://" + os.path.abspath("../HijriCalc.html")
        await page.goto(file_path)

        modes = ["linear", "tabular", "tabular_fixed"]

        for mode in modes:
            # Open settings
            await page.click("#prefBtn")
            await page.wait_for_selector("#prefDialog", state="visible")

            # Select mode
            await page.select_option("#calcMode", mode)

            # Save
            await page.click("#savePrefBtn")
            await page.wait_for_timeout(500)

            # Open formula details
            await page.evaluate("document.querySelector('details').open = true")
            await page.wait_for_timeout(500)

            # Take screenshot
            await page.screenshot(path=f"../mode_{mode}.png")
            print(f"Verified mode: {mode}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
