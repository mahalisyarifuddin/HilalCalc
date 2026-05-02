from playwright.sync_api import sync_playwright
import os

def run_cuj(page):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = "file://" + os.path.abspath(os.path.join(script_dir, "HilalSync.html"))
    page.goto(file_path)
    page.wait_for_timeout(500)

    # Click prevBtn
    page.click("#prevBtn")
    page.wait_for_timeout(500)

    # Click nextBtn
    page.click("#nextBtn")
    page.wait_for_timeout(500)

    # Change language
    page.select_option("#language", "id")
    page.wait_for_timeout(500)

    # Click todayBtn
    page.click("#todayBtn")
    page.wait_for_timeout(500)

    page.screenshot(path="/home/jules/verification/screenshots/verification.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    os.makedirs("/home/jules/verification/videos", exist_ok=True)
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(record_video_dir="/home/jules/verification/videos")
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
