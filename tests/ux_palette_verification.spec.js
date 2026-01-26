const { test, expect } = require('@playwright/test');

test('HijriCalc Palette Changes Verification', async ({ page }) => {
  // Load the page relative to the test file
  await page.goto('file://' + process.cwd() + '/HijriCalc.html');

  // 1. Verify Border Color
  const button = page.locator('.secondary').first();
  const borderColor = await button.evaluate((el) => {
    return getComputedStyle(el).borderColor;
  });
  // #8D93A1 is rgb(141, 147, 161)
  expect(borderColor).toBe('rgb(141, 147, 161)');

  // 2. Verify aria-live
  const monthDisplay = page.locator('#monthDisplay');
  await expect(monthDisplay).toHaveAttribute('aria-live', 'polite');

  // 3. Verify Reactive Inputs
  // We need to change the Hijri Year and see if the calendar updates without pressing Enter or Go

  // First, get the current month display
  const initialMonthText = await monthDisplay.innerText();

  // Fill the Hijri Year input with a new value
  // Note: We use .fill() which triggers input/change events usually, but strictly we want to ensure 'change' does it.
  // We can blur the input to ensure 'change' event fires.
  await page.fill('#hYearInput', '1450');
  await page.locator('#hYearInput').blur(); // Trigger change

  // Wait for the update (debounced or immediate)
  // The code has no debounce on the event handler itself, it calls handleGoH immediately.
  // handleGoH calls render().

  // The calendar header should change.
  // 1450 Hijri corresponds to a different Gregorian year.
  await expect(monthDisplay).not.toHaveText(initialMonthText);
});
