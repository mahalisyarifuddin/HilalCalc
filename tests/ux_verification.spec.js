const { test, expect } = require('@playwright/test');
const path = require('path');

test.describe('HijriCalc UX Improvements', () => {
    test.beforeEach(async ({ page }) => {
        const filePath = path.resolve(__dirname, '../HijriCalc.html');
        await page.goto(`file://${filePath}`);
    });

    test('Enter key on Hijri Year input should update calendar', async ({ page }) => {
        await page.waitForSelector('#monthDisplay');

        await page.fill('#hDayInput', '1');
        await page.selectOption('#hMonthInput', '8');
        await page.fill('#hYearInput', '1450');

        await page.press('#hYearInput', 'Enter');

        const monthText = await page.textContent('#monthDisplay');
        expect(monthText).toContain('2029');
    });

    test('Changing Gregorian date input should update calendar', async ({ page }) => {
        await page.waitForSelector('#monthDisplay');

        await page.fill('#gDateInput', '2030-01-01');
        await page.evaluate(() => document.getElementById('gDateInput').blur());

        const monthText = await page.textContent('#monthDisplay');
        expect(monthText).toContain('2030');
    });

    test('Location button should show spinner', async ({ page }) => {
        await page.context().grantPermissions(['geolocation']);

        // Open Settings Dialog
        await page.click('#prefBtn');
        await page.waitForSelector('#prefDialog', { state: 'visible' });

        // Click the button
        await page.click('#myLocBtn');

        // Check for spinner immediately
        const spinnerExists = await page.locator('.spinner').count();
        expect(spinnerExists).toBeGreaterThan(0);
    });
});
