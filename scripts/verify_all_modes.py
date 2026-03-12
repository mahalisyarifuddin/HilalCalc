import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Load the file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = "file://" + os.path.abspath(os.path.join(script_dir, "..", "HijriCalc.html"))
        await page.goto(file_path)

        modes = ["linear", "tabular"]

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
            await page.screenshot(path=os.path.join(script_dir, "..", f"mode_{mode}.png"))
            print(f"Verified mode: {mode}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
