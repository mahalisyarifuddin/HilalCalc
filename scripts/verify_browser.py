"""Deterministic local HTTP browser regressions. Run from repo root with -m."""
import os
import re

from playwright.sync_api import expect, sync_playwright

from scripts.verify_export_png import ROOT, start_server


def verify_map(page, base_url):
    page.goto(f'{base_url}/HilalMap.html')
    expect(page.locator('#landStatus')).to_have_text(re.compile('Land mask ready|Mask daratan siap'))
    page.select_option('#mapRegion', 'indonesia')
    page.locator('#mapDate').fill('2024-04-10')
    page.locator('#landOnlyToggle').evaluate('e => e.click()')
    page.click('#renderMap')
    expect(page.locator('#mapStatus')).to_have_text(re.compile('Done|Selesai'), timeout=30000)
    with page.expect_download() as masked_result:
        page.locator('#exportCsvBtn').evaluate('e => e.click()')
    masked = masked_result.value.path().read_text().splitlines()[1:]
    page.locator('#landOnlyToggle').evaluate('e => e.click()')
    page.select_option('#mapRegion', 'world')
    page.locator('#renderMap').evaluate('e => { e.click(); e.click(); }')
    with page.expect_download() as result:
        page.locator('#exportCsvBtn').evaluate('e => e.click()')
    download = result.value
    assert download.suggested_filename.startswith('hilalmap-indonesia-')
    assert download.suggested_filename.endswith('-2024-04-10.csv')
    rows = download.path().read_text().splitlines()[1:]
    assert rows and all(95 <= float(row.split(',')[1]) <= 141 for row in rows)
    assert len(masked) == len(rows)
    assert sum(row.split(',')[2] == '1' for row in masked) < sum(row.split(',')[2] == '1' for row in rows)


def verify_map_worker_error(page, base_url):
    page.add_init_script('''window.Worker = class extends Worker {
        constructor() {
            const url = URL.createObjectURL(new Blob(["importScripts('/missing-worker-dependency.js')"], {type: 'application/javascript'}));
            super(url);
            URL.revokeObjectURL(url);
        }
    };''')
    page.goto(f'{base_url}/HilalMap.html')
    button = page.locator('#renderMap')
    initial = button.text_content()
    button.click()
    expect(page.locator('#mapStatus')).to_have_text(re.compile('^Error:'))
    expect(button).to_be_enabled()
    expect(button).to_have_text(initial)


def verify_map_invalid_calculator_inputs(page, base_url):
    page.goto(f'{base_url}/HilalMap.html')
    page.locator('#calcLat').fill('91')
    page.locator('#calcLon').fill('0')
    page.locator('#calcDate').fill('2024-04-10')
    page.on('dialog', lambda dialog: dialog.accept())
    page.locator('#calculateBtn').click()
    expect(page.locator('#results')).to_be_empty()
    page.locator('#calcLat').fill('0')
    page.locator('#calcLon').fill('181')
    page.locator('#calculateBtn').click()
    expect(page.locator('#results')).to_be_empty()
    page.locator('#calcLon').fill('0')
    page.locator('#calcDate').fill('2024-02-31')
    page.locator('#calculateBtn').click()
    expect(page.locator('#results')).to_be_empty()


def run(*scenarios):
    server = start_server(ROOT, cors=False)
    try:
        url = f'http://127.0.0.1:{server.server_address[1]}'
        with sync_playwright() as p:
            options = {'executable_path': os.environ['CHROMIUM_PATH']} if 'CHROMIUM_PATH' in os.environ else {}
            browser = p.chromium.launch(**options)
            for scenario in scenarios:
                page = browser.new_page(timezone_id='UTC', locale='en-US', accept_downloads=True)
                page.route('https://**/*', lambda route: route.abort())
                errors = []
                page.on('pageerror', lambda error: errors.append(str(error)))
                scenario(page, url)
                assert not errors, errors
                page.close()
                print(f'PASS: {scenario.__name__}')
            browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    from scripts.verify_all_modes import verify_modes
    from verify_hilalsync import verify_sync

    run(verify_modes, verify_sync, verify_map, verify_map_worker_error, verify_map_invalid_calculator_inputs)
