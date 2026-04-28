import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        def handle_console(msg):
            print(f"Browser Console: {msg.text}")
        page.on("console", handle_console)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = "file://" + os.path.abspath(os.path.join(script_dir, "..", "HilalSync.html"))
        print(f"Opening {file_path}")
        await page.goto(file_path)

        # Wait for initial calculation to finish
        await page.wait_for_selector("#calculationIndicator", state="hidden")

        months_1447 = [
            (1447, 1, "Thursday, 26 June 2025"),
            (1447, 2, "Saturday, 26 July 2025"),
            (1447, 3, "Sunday, 24 August 2025"),
            (1447, 4, "Tuesday, 23 September 2025"),
            (1447, 5, "Thursday, 23 October 2025"),
            (1447, 6, "Friday, 21 November 2025"),
            (1447, 7, "Sunday, 21 December 2025"),
            (1447, 8, "Tuesday, 20 January 2026"),
            (1447, 9, "Wednesday, 18 February 2026"),
            (1447, 10, "Friday, 20 March 2026"),
            (1447, 11, "Saturday, 18 April 2026"),
            (1447, 12, "Monday, 18 May 2026")
        ]

        print(f"{'Year-Month':10} | {'Expected':30} | {'Actual GIC':30} | {'Status'}")
        print("-" * 80)

        for year, month, expected in months_1447:
            await page.fill("#hijriYearInput", str(year))
            await page.select_option("#hijriMonthInput", str(month))

            await page.click("#goButton")

            # Wait for calculation indicator to appear then disappear
            await page.wait_for_selector("#calculationIndicator", state="visible")
            await page.wait_for_selector("#calculationIndicator", state="hidden", timeout=60000)

            gic_date = await page.inner_text("#dateGlobal")
            status = "MATCH" if gic_date == expected else "FAIL"
            print(f"{year}-{month:02}: {expected:30} | {gic_date:30} | {status}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
