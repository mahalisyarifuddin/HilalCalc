"""Assert a known conversion in all three HijriCalc modes."""
from playwright.sync_api import expect


def verify_modes(page, base_url):
    page.goto(f'{base_url}/HijriCalc.html')
    for mode, day in [('astronomic', '1'), ('linear', '2'), ('tabular', '1')]:
        page.click('#prefBtn')
        page.select_option('#calcMode', mode)
        page.click('#savePrefBtn')
        page.locator('#gDateInput').fill('2024-03-12')
        page.locator('#gDateInput').dispatch_event('change')
        expect(page.locator('#hYearInput')).to_have_value('1445')
        expect(page.locator('#hMonthInput')).to_have_value('9')
        expect(page.locator('#hDayInput')).to_have_value(day)


if __name__ == '__main__':
    from scripts.verify_browser import run

    run(verify_modes)
