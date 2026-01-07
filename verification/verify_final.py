import os
from playwright.sync_api import sync_playwright

def verify(page):
    # Load the local file
    cwd = os.getcwd()
    file_path = f"file://{cwd}/index.html"
    print(f"Navigating to {file_path}")
    page.goto(file_path)

    # 1. Verify Apportionment View (Default)
    print("Checking Apportionment View...")
    page.wait_for_selector("#apportionment")
    page.screenshot(path="verification/apportionment.png")

    # 2. Switch to Visibility Map
    print("Switching to Visibility Map...")
    page.click("text=Visibility Map")

    # 3. Verify Map View
    print("Checking Map View...")
    page.wait_for_selector("#visibility")
    page.wait_for_selector("#mapCanvas")

    # 4. Render Map (Optional, might be slow but let's try clicking render)
    # The button text is "Render Map" or "Render Peta" depending on language (default English)
    print("Clicking Render...")
    page.click("#renderMap")

    # Wait a bit for rendering to start/finish (it uses requestAnimationFrame)
    page.wait_for_timeout(2000)

    page.screenshot(path="verification/visibility_map.png")
    print("Done.")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    try:
        verify(page)
    except Exception as e:
        print(f"Error: {e}")
        page.screenshot(path="verification/error.png")
    finally:
        browser.close()
