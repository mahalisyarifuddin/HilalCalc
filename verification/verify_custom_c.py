from playwright.sync_api import sync_playwright
import os

def test_custom_c():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the file
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/HijriCalc.html")

        # Open Preferences
        page.click("#prefBtn")

        # Check Custom C
        page.check("#useCustomC")

        # Enter Custom C value
        page.fill("#cValueInput", "50")

        # Save and Close
        page.click("#savePrefBtn")

        # Open Details to see formula
        # Set open=true via evaluate because clicking summary can be tricky
        page.evaluate("document.querySelector('details').open = true")

        # Verify Formula Text
        formula_note = page.text_content("#formulaNote")
        print(f"Formula Note: {formula_note}")

        if "C=50" in formula_note and "Custom Tabular Constant" in formula_note:
            print("SUCCESS: Custom C value is displayed.")
        else:
            print("FAILURE: Custom C value is NOT displayed correctly.")

        # Scroll to bottom
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        # Screenshot
        page.screenshot(path="verification/custom_c_verification.png", full_page=True)

        browser.close()

if __name__ == "__main__":
    test_custom_c()
