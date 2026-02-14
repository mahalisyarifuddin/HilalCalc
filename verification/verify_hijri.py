
import time
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("file:///app/HijriCalc.html")

    # 1. Open Preferences
    page.click("#prefBtn")
    time.sleep(0.5)

    # 2. Check if "Balanced" option is gone
    options = page.eval_on_selector_all("#formulaMode option", "options => options.map(o => o.value)")
    print("Formula Options:", options)
    assert "phase3" not in options, "Phase 3 option should be removed"

    # 3. Set Location to Makkah (Mecca) AND SAVE
    page.select_option("#locPreset", "mecca")
    time.sleep(0.5)
    page.click("#savePrefBtn") # Save and close
    time.sleep(0.5)

    # 4. Expand Formula Details
    page.evaluate("document.querySelector('details').open = true")
    time.sleep(0.5)

    # 5. Check Formula C value (Default Phase 1 for Mecca should be 14)
    formula_note = page.text_content("#formulaNote")
    print("Formula Note (Phase 1):", formula_note)
    if "C=14" not in formula_note:
        print("FAIL: Expected C=14 for Mecca Phase 1")
    else:
        print("PASS: C=14 for Mecca Phase 1")

    # 6. Switch to Phase 2
    page.click("#prefBtn")
    time.sleep(0.5)
    page.select_option("#formulaMode", "phase2")
    time.sleep(0.5)
    page.click("#savePrefBtn") # Save and close
    time.sleep(0.5)

    # 7. Check Formula C value (Phase 2 for Mecca should be 15)
    formula_note_2 = page.text_content("#formulaNote")
    print("Formula Note (Phase 2):", formula_note_2)
    if "C=15" not in formula_note_2:
        print("FAIL: Expected C=15 for Mecca Phase 2")
    else:
        print("PASS: C=15 for Mecca Phase 2")

    page.screenshot(path="verification/verification.png")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
