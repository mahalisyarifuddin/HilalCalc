const { test, expect } = require('@playwright/test');
const path = require('path');

test('HijriCalc persists calculations to localStorage', async ({ page }) => {
  const filePath = path.resolve(__dirname, '../HijriCalc.html');
  await page.goto(`file://${filePath}`);

  // Wait for calendar to render (grid should be visible)
  await expect(page.locator('.calendar-grid')).toBeVisible();

  // Wait for the debounce timeout (1s) to pass so cache is saved
  await page.waitForTimeout(1500);

  // Check if cache exists in localStorage
  let cache = await page.evaluate(() => localStorage.getItem('hijriCalcCache'));
  expect(cache).not.toBeNull();

  let parsed = JSON.parse(cache);
  expect(parsed.version).toBe(1);
  expect(Object.keys(parsed.data).length).toBeGreaterThan(0);

  console.log('Cache size after first load:', Object.keys(parsed.data).length);

  // Store the cache content to compare later
  const initialCacheData = parsed.data;

  // Reload the page
  await page.reload();
  await expect(page.locator('.calendar-grid')).toBeVisible();

  // Check cache again immediately. It should be loaded from localStorage.
  // We can verify this by checking if it's still in localStorage (it should be)
  cache = await page.evaluate(() => localStorage.getItem('hijriCalcCache'));
  expect(cache).not.toBeNull();

  parsed = JSON.parse(cache);
  expect(parsed.version).toBe(1);

  // Verify data is preserved
  // Note: Depending on logic, reload might trigger re-save which might update timestamp or similar if we tracked it,
  // but the keys and values (gDate) should be identical.
  const reloadedCacheData = parsed.data;

  // Check if at least one key from initial cache exists in reloaded cache
  const firstKey = Object.keys(initialCacheData)[0];
  expect(reloadedCacheData[firstKey]).toBeDefined();
  expect(reloadedCacheData[firstKey].gDate).toBe(initialCacheData[firstKey].gDate);

  console.log('Cache verification successful.');
});
