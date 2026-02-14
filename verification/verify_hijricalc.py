from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("file:///app/HijriCalc.html")

    # Open Preferences
    page.click("#prefBtn")
    # Verify formulaMode is NOT present
    try:
        page.wait_for_selector("#formulaMode", timeout=2000)
        print("FAIL: formulaMode selector found!")
    except:
        print("PASS: formulaMode selector not found.")

    # Screenshot Preferences
    page.screenshot(path="verification/preferences.png")

    # Close Preferences
    page.click("#closePref")

    # Open Formula Details
    # The summary is "Heuristic Formula".
    # We need to click the summary or set open=true
    page.evaluate("document.querySelector('details').open = true")

    # Verify text
    formula_desc = page.inner_text("#formulaDesc")
    print(f"Formula Desc: {formula_desc}")
    if "(Unified)" in formula_desc:
        print("PASS: Formula description updated.")
    else:
        print("FAIL: Formula description not updated.")

    page.screenshot(path="verification/formula.png")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
