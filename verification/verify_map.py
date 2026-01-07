from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Increase viewport height significantly to ensure everything is "visible"
        page = browser.new_page(viewport={"width": 1280, "height": 2000})

        # Load the index.html file
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Select Turkey criteria
        page.select_option("#criteria", "turkey")

        # Select World view
        page.select_option("#view", "world")

        # Set a specific date
        page.fill("#date", "2024-04-09")

        print("Evaluating JS click...")
        # Use JS click to absolutely force it if Playwright still thinks it is outside viewport
        page.evaluate("document.getElementById('render').click()")

        # Wait for "Done." in status
        print("Waiting for render to complete...")
        try:
            page.wait_for_function("document.getElementById('status').textContent === 'Done.'", timeout=120000)
            print("Render complete.")
        except Exception as e:
            print(f"Timeout waiting for render: {e}")
            # Get status text
            status = page.text_content("#status")
            print(f"Current status: {status}")

        # Take screenshot
        page.screenshot(path="verification/map_turkey_world.png")

        print("Screenshot taken.")
        browser.close()

if __name__ == "__main__":
    run()
