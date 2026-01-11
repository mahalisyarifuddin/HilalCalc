from playwright.sync_api import sync_playwright, expect
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the local HTML file
        cwd = os.getcwd()
        file_path = f"file://{cwd}/index.html"
        print(f"Loading {file_path}")
        page.goto(file_path)

        # Click "Detailed Calculations" tab
        print("Clicking Detailed Calculations tab")
        page.get_by_role("button", name="Detailed Calculations").click()

        # Verify UTC Offset input exists
        print("Verifying UTC Offset input")
        utc_input = page.locator("#calcUtcOffset")
        expect(utc_input).to_be_visible()

        # Fill in data
        # Lat/Lon for Jakarta
        print("Filling inputs")
        page.fill("#calcLat", "-6.2000")
        page.fill("#calcLon", "106.8166")
        page.fill("#calcDate", "2023-10-27")

        # Set UTC Offset to 7
        page.fill("#calcUtcOffset", "7")

        # Click Calculate
        print("Clicking Calculate")
        page.click("#calculateBtn")

        # Wait for results
        print("Waiting for results")
        results = page.locator("#results")
        expect(results).to_contain_text("Sunset Time")

        # Check if output contains UTC+7
        # We need to find the element with sunset time or similar
        # The result cards contain "Sunset Time" and then the value.
        # We can just check if the text "(UTC+7)" is present in the results.
        # Note: The output format is `... (UTC+7)`
        print("Checking for (UTC+7) in results")
        content = results.text_content()
        print(f"Results content: {content}")

        expect(results).to_contain_text("(UTC+7)")

        # Take screenshot
        print("Taking screenshot")
        page.screenshot(path="verification/utc_offset_test.png")
        print("Verification script finished successfully.")

        browser.close()

if __name__ == "__main__":
    run()
