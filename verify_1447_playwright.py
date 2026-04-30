import asyncio
from playwright.async_api import async_playwright
import os

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))

        path = "file://" + os.path.abspath("HilalSync.html")
        await page.goto(path)

        ref_1447 = [
            (1, "Thursday, 26 June 2025"),
            (2, "Saturday, 26 July 2025"),
            (3, "Sunday, 24 August 2025"),
            (4, "Tuesday, 23 September 2025"),
            (5, "Thursday, 23 October 2025"),
            (6, "Friday, 21 November 2025"),
            (7, "Sunday, 21 December 2025"),
            (8, "Tuesday, 20 January 2026"),
            (9, "Wednesday, 18 February 2026"),
            (10, "Friday, 20 March 2026"),
            (11, "Saturday, 18 April 2026"),
            (12, "Tuesday, 19 May 2026"),
        ]

        print("Verifying 1447 AH GIC dates...")
        matches = 0
        for m, gic_exp in ref_1447:
            await page.fill("#hYearInput", "1447")
            await page.select_option("#hMonthInput", str(m))
            await page.click("#goBtn")

            # Use longer timeout for the global grid search
            await page.wait_for_timeout(3000)

            gic_got = await page.inner_text("#dateGic")
            if gic_got == gic_exp:
                print(f"Month {m} OK: {gic_got}")
                matches += 1
            else:
                print(f"Month {m} FAIL: Got '{gic_got}' | Exp '{gic_exp}'")

        print(f"\nTotal GIC matches: {matches}/12")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
