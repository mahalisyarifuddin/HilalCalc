"""HilalSync regression scenarios, served from a local HTTP origin."""
import json
from pathlib import Path

from playwright.sync_api import expect

FIXTURES = Path(__file__).resolve().parent / "tests"


def verify_sync(page, base_url):
    page.goto(f'{base_url}/HilalSync.html')
    page.wait_for_function('Boolean(landGeojson) && Boolean(document.querySelector("#verdict").textContent)')
    assert page.evaluate('''() => [0, 99, 100].map(year => {
        const date = new Date('2000-12-31T23:59:59Z');
        date.setUTCFullYear(year);
        return utcMidnight(date, 1).toISOString();
    })''') == ['0001-01-01T00:00:00.000Z', '0100-01-01T00:00:00.000Z', '0101-01-01T00:00:00.000Z']
    cases = json.loads((FIXTURES / 'month_start_cases.json').read_text())
    for case in cases:
        if 'land_fixture' in case:
            continue
        actual = page.evaluate('''([year, month]) => {
            const {jdAceh, jdGic} = getStartJD(year, month);
            return [jdAceh, jdGic];
        }''', [case['year'], case['month']])
        assert actual == case['browser_jd'], (case['note'], actual)
    page.locator('#hYearInput').fill('1445')
    page.select_option('#hMonthInput', '12')
    page.click('#nextBtn')
    expect(page.locator('#hYearInput')).to_have_value('1446')
    expect(page.locator('#hMonthInput')).to_have_value('1')
    page.click('#prevBtn')
    expect(page.locator('#hYearInput')).to_have_value('1445')
    expect(page.locator('#hMonthInput')).to_have_value('12')

    for case in cases:
        if 'land_fixture' not in case:
            continue
        land = FIXTURES / case['land_fixture']
        page.route('**/ne_110m_land.geojson', lambda route: route.fulfill(path=land))
        page.reload()
        page.wait_for_function('Boolean(landGeojson)')
        actual = page.evaluate('''([year, month]) => {
            const {jdAceh, jdGic, detailAceh} = getStartJD(year, month);
            return [jdAceh, jdGic, detailAceh];
        }''', [case['year'], case['month']])
        assert actual == [*case['browser_jd'], None], (case['note'], actual)
        page.unroute('**/ne_110m_land.geojson')

    for response in ({'status': 503}, {'json': {'type': 'FeatureCollection', 'features': [
            {'geometry': {'type': 'Polygon', 'coordinates': []}}
    ]}}):
        page.route('**/ne_110m_land.geojson', lambda route: route.fulfill(**response))
        page.reload()
        expect(page.locator('#dateGic')).to_have_text('—')
        expect(page.locator('#verdict')).to_contain_text('Land data unavailable')
        assert page.evaluate('isLandGeoJSON(26, -70)') is False
        page.unroute('**/ne_110m_land.geojson')


if __name__ == '__main__':
    from scripts.verify_browser import run

    run(verify_sync)
