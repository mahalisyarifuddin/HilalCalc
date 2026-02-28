const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('http://localhost:8000/HilalMap.html');
  const tabs = await page.$$('.tab');
  console.log("Tabs count:", tabs.length);
  await browser.close();
})();
