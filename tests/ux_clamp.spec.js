const { test, expect } = require('@playwright/test');
const path = require('path');

test('Hijri Day input should auto-clamp when switching to shorter month', async ({ page }) => {
  const filePath = path.resolve(__dirname, '../HijriCalc.html');
  await page.goto(`file://${filePath}`);

  // Wait for hydration
  await page.waitForTimeout(500);

  const hDayInput = page.locator('#hDayInput');
  const hMonthSelect = page.locator('#hMonthInput');

  // Find a month with 30 days
  let month30 = -1;
  for (let i = 0; i < 12; i++) {
    await hMonthSelect.selectOption(String(i));
    const max = await hDayInput.getAttribute('max');
    if (max === '30') {
      month30 = i;
      break;
    }
  }

  expect(month30).not.toBe(-1); // Should find at least one 30-day month

  // Set Day to 30
  await hDayInput.fill('30');
  await expect(hDayInput).toHaveValue('30');

  // Find a month with 29 days
  let month29 = -1;
  for (let i = 0; i < 12; i++) {
    if (i === month30) continue;
    await hMonthSelect.selectOption(String(i));
    const max = await hDayInput.getAttribute('max');
    if (max === '29') {
      month29 = i;
      break;
    }
  }

  // If no 29-day month found in this year (unlikely but possible), try another year?
  // But usually there are both.
  expect(month29).not.toBe(-1);

  // Now perform the transition
  // 1. Select 30-day month
  await hMonthSelect.selectOption(String(month30));
  // 2. Set day to 30
  await hDayInput.fill('30');

  // 3. Select 29-day month
  await hMonthSelect.selectOption(String(month29));

  // 4. Check if max is 29
  await expect(hDayInput).toHaveAttribute('max', '29');

  // 5. Check if value is clamped to 29
  // If not clamped, it will be 30
  await expect(hDayInput).toHaveValue('29');
});
