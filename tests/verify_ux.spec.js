const { test, expect } = require('@playwright/test');
const path = require('path');

test('Use My Location button shows loading state', async ({ page }) => {
  const filePath = path.resolve(__dirname, '../HijriCalc.html');
  await page.goto(`file://${filePath}`);

  // Open Settings Dialog
  await page.click('#prefBtn');
  await expect(page.locator('#prefDialog')).toBeVisible();

  // Mock Geolocation with delay
  await page.evaluate(() => {
    // We must ensure navigator.geolocation exists or is mocked if missing in headless
    if (!navigator.geolocation) {
        navigator.geolocation = {};
    }
    navigator.geolocation.getCurrentPosition = (success, error, options) => {
      // Simulate delay
      setTimeout(() => {
        // Mock success
        const position = { coords: { latitude: 5.55, longitude: 95.32 } };
        success(position);
      }, 1000);
    };
  });

  // Click "Use My Location"
  const btn = page.locator('#myLocBtn');
  await btn.click();

  // Verify Loading State
  // The button should be disabled and show "Locating..."
  await expect(btn).toBeDisabled({ timeout: 500 }); // Should happen almost immediately
  await expect(btn).toHaveText(/Locating/);

  // Wait for completion ( > 1000ms)
  // We can just wait for the button to be enabled again
  await expect(btn).toBeEnabled({ timeout: 2000 });
  await expect(btn).toHaveText('Use My Location');
});
