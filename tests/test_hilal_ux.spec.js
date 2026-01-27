const { test, expect } = require('@playwright/test');
const path = require('path');

test.describe('HilalMap UX Improvements', () => {
    test.beforeEach(async ({ page }) => {
        const filePath = path.resolve(__dirname, '../HilalMap.html');
        await page.goto(`file://${filePath}`);
    });

    test('Use My Location button shows loading state', async ({ page }) => {
        // Switch to Detailed Calculations tab
        await page.click('#tabCalc');
        await expect(page.locator('#calcView')).toBeVisible();

        // Mock Geolocation with delay
        await page.evaluate(() => {
            if (!navigator.geolocation) {
                navigator.geolocation = {};
            }
            navigator.geolocation.getCurrentPosition = (success, error, options) => {
                setTimeout(() => {
                    const position = { coords: { latitude: 5.55, longitude: 95.32 } };
                    success(position);
                }, 1000);
            };
        });

        const btn = page.locator('#getLocation');

        // Click the button
        await btn.click();

        // Verify Loading State
        await expect(btn).toBeDisabled();
        // Check for spinner or text "Locating..." (case insensitive)
        // Since we haven't implemented it yet, this test is expected to fail initially or we write it to pass only after impl.
        // I will write it to expect the IMPROVED state.
        await expect(btn).toHaveText(/Locating/i);
        // We can also check for the spinner class if we want to be specific, but text is usually enough for UX.

        // Wait for completion
        await expect(btn).not.toBeDisabled({ timeout: 2000 });
        await expect(btn).toHaveText('📍 Use My Location');
    });

    test('Render Map button shows loading status', async ({ page }) => {
         // Switch to Map tab (default)
        await expect(page.locator('#mapView')).toBeVisible();

        const renderBtn = page.locator('#renderMap');
        const status = page.locator('#mapStatus');

        // We can't easily delay the Worker without modifying the worker code or mocking Worker.
        // But for "Render Map", the text updates to "Calculating (Worker)..." and button to "Cancel".
        // We want to verify that the status contains a spinner and "Calculating...".

        // Click Render
        await renderBtn.click();

        // Verify Status has "Calculating"
        await expect(status).toHaveText(/Calculating/i);

        // Verify Button is "Cancel"
        await expect(renderBtn).toHaveText('Cancel');

        // Verify Status has spinner
        await expect(status.locator('.spinner')).toBeVisible();
    });
});
