import asyncio
from playwright.async_api import async_playwright
import os

async def verify_1447():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Open HilalSync.html
        abs_path = os.path.abspath("HilalSync.html")
        await page.goto(f"file://{abs_path}")

        # Expected results for 1447 AH (MABBIMS)
        # 1. 27 June 2025
        # 2. 27 July 2025
        # 3. 26 August 2025
        # 4. 24 September 2025
        # 5. 24 October 2025
        # 6. 23 November 2025
        # 7. 22 December 2025
        # 8. 21 January 2026
        # 9. 19 February 2026
        # 10. 21 March 2026
        # 11. 19 April 2026
        # 12. 19 May 2026

        expected = [
            "Friday, 27 June 2025",
            "Sunday, 27 July 2025",
            "Tuesday, 26 August 2025",
            "Wednesday, 24 September 2025",
            "Friday, 24 October 2025",
            "Sunday, 23 November 2025",
            "Monday, 22 December 2025",
            "Wednesday, 21 January 2026",
            "Thursday, 19 February 2026",
            "Saturday, 21 March 2026",
            "Sunday, 19 April 2026",
            "Tuesday, 19 May 2026"
        ]

        # Expected GIC results
        expected_gic = [
            "Friday, 27 June 2025",
            "Sunday, 27 July 2025",
            "Monday, 25 August 2025",
            "Wednesday, 24 September 2025",
            "Friday, 24 October 2025",
            "Sunday, 23 November 2025",
            "Monday, 22 December 2025",
            "Wednesday, 21 January 2026",
            "Thursday, 19 February 2026",
            "Saturday, 21 March 2026",
            "Sunday, 19 April 2026",
            "Tuesday, 19 May 2026"
        ]

        print(f"{'Month':<15} | {'Expected M':<25} | {'Actual M':<25} | {'Status'}")
        print("-" * 80)

        for m in range(1, 13):
            await page.fill("#hijriYearInput", "1447")
            await page.select_option("#hijriMonthInput", str(m))
            await page.click("#analyzeButton")

            # Wait for "Analyzing..." to disappear (button re-enabled)
            await page.wait_for_function("document.getElementById('analyzeButton').disabled === false", timeout=10000)

            actual_m = (await page.inner_text("#dateMabbimsDisplay")).strip()
            actual_g = (await page.inner_text("#dateGicDisplay")).strip()

            status = "PASS" if actual_m == expected[m-1] and actual_g == expected_gic[m-1] else "FAIL"
            print(f"Month {m:<8} | {expected[m-1]:<25} | {actual_m:<25} | {status}")
            if status == "FAIL":
                print(f"      (GIC) | {expected_gic[m-1]:<25} | {actual_g:<25}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_1447())
