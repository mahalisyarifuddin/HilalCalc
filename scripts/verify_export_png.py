"""Playwright check: PNG export of HilalMap.html must include the map (base) layer.

Scenarios (base map served from a second origin, like upload.wikimedia.org):
  1. base map sends Access-Control-Allow-Origin -> readable image path
  2. base map has NO CORS header                  -> must fall back to land-data base map

Pass/fail is decided from the downloaded PNG pixels: the ocean/land colours of the
base map must be present. The bug being guarded against exported only the overlay
on a white background (no map layer).

Usage:
  pip install playwright pillow
  playwright install chromium
  python scripts/verify_export_png.py

Optional environment variables:
  ASTRONOMY_ENGINE_JS  local path to astronomy.browser.min.js; if set, the jsDelivr
                       request is served from this file (useful offline).
  CHROMIUM_PATH        path to a Chromium binary to use instead of Playwright's.
"""
import collections
import functools
import http.server
import io
import json
import os
import socketserver
import sys
import tempfile
import threading

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OCEAN_RGB = (0xBC, 0xD9, 0xEA)  # fallback land-base ocean colour
LAND_RGB = (0xE3, 0xDC, 0xCB)   # fallback land-base land colour
TEST_OCEAN = (0xA6, 0xCE, 0xE3)  # colours of the test base SVG (CORS case)
TEST_LAND = (0xC9, 0xA8, 0x6A)


def build_test_base_svg():
    """Equirectangular 360x180 world base map built from the repo's land data."""
    with open(os.path.join(ROOT, 'ne_110m_land.geojson'), encoding='utf-8') as f:
        geo = json.load(f)
    paths = []
    for feat in geo['features']:
        g = feat['geometry']
        polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for poly in polys:
            d = ' '.join(
                'M' + ' L'.join(f'{lon + 180:.3f},{90 - lat:.3f}' for lon, lat in ring) + ' Z'
                for ring in poly)
            paths.append(f'<path d="{d}"/>')
    body = (f'<rect width="360" height="180" fill="#{TEST_OCEAN[0]:02x}{TEST_OCEAN[1]:02x}{TEST_OCEAN[2]:02x}"/>'
            f'<g fill="#{TEST_LAND[0]:02x}{TEST_LAND[1]:02x}{TEST_LAND[2]:02x}">' + ''.join(paths) + '</g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="500" '
            f'viewBox="0 0 360 180">{body}</svg>').encode('utf-8')


def start_server(directory, cors):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            if cors:
                self.send_header('Access-Control-Allow-Origin', '*')
            super().end_headers()

        def log_message(self, *args):
            pass

    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), functools.partial(Handler, directory=directory))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def count_colours(png_bytes):
    im = Image.open(io.BytesIO(png_bytes)).convert('RGB')
    total = im.size[0] * im.size[1]
    pixels = im.get_flattened_data() if hasattr(im, 'get_flattened_data') else im.getdata()
    counts = collections.Counter(pixels)
    return im.size, total, counts


def share(counts, total, rgb):
    return counts.get(rgb, 0) / total


def run_scenario(p, app_port, base_port, base_dir, cors, label):
    launch_kwargs = {'headless': True, 'args': ['--no-sandbox', '--disable-gpu']}
    if os.environ.get('CHROMIUM_PATH'):
        launch_kwargs['executable_path'] = os.environ['CHROMIUM_PATH']
    browser = p.chromium.launch(**launch_kwargs)
    try:
        ctx = browser.new_context(accept_downloads=True, viewport={'width': 1400, 'height': 900})
        js_path = os.environ.get('ASTRONOMY_ENGINE_JS')
        if js_path:
            ctx.route('https://cdn.jsdelivr.net/**', lambda r: r.fulfill(
                status=200, body=open(js_path, 'rb').read(),
                headers={'content-type': 'application/javascript', 'access-control-allow-origin': '*'}))
        pg = ctx.new_page()
        errors = []
        pg.on('pageerror', lambda e: errors.append(str(e)))
        pg.goto(f'http://127.0.0.1:{app_port}/HilalMap.html')
        # Serve the base map from another origin (cross-origin <img crossorigin="anonymous">)
        pg.evaluate("u => { document.getElementById('map-image').src = u; }",
                    f'http://127.0.0.1:{base_port}/basemap.svg')
        pg.wait_for_function("document.getElementById('map-image').complete", timeout=30000)
        pg.wait_for_timeout(300)
        pg.click('#renderMap')
        pg.wait_for_selector('#mapStatus .spinner', timeout=30000)
        pg.wait_for_selector('#mapStatus .spinner', state='detached', timeout=600000)
        pg.wait_for_timeout(300)
        with pg.expect_download(timeout=60000) as dl:
            pg.click('#exportPngBtn')
        png = open(dl.value.path(), 'rb').read()
        if errors:
            print(f'  [{label}] page errors: {errors[:3]}')
    finally:
        browser.close()
    size, total, counts = count_colours(png)
    ocean_share = share(counts, total, TEST_OCEAN if cors else OCEAN_RGB)
    land_share = share(counts, total, TEST_LAND if cors else LAND_RGB)
    print(f'  [{label}] size={size} ocean={ocean_share:.1%} land={land_share:.1%}')
    return ocean_share, land_share


def main():
    base_dir = tempfile.mkdtemp(prefix='hilal-base-')
    with open(os.path.join(base_dir, 'basemap.svg'), 'wb') as f:
        f.write(build_test_base_svg())
    app = start_server(ROOT, cors=False)
    base_cors = start_server(base_dir, cors=True)
    base_nocors = start_server(base_dir, cors=False)
    failures = []
    try:
        with sync_playwright() as p:
            scenarios = [
                ('base map with CORS', base_cors, True),
                ('base map without CORS (regression)', base_nocors, False),
            ]
            for label, base, cors in scenarios:
                ocean, land = run_scenario(p, app.server_address[1], base.server_address[1], base_dir, cors, label)
                # Map layer present = both base colours cover a substantial part of the image.
                if ocean < 0.3 or land < 0.05:
                    failures.append(f'{label}: map layer missing (ocean={ocean:.1%}, land={land:.1%})')
    finally:
        app.shutdown()
        base_cors.shutdown()
        base_nocors.shutdown()
    if failures:
        print('FAIL')
        for f in failures:
            print(' -', f)
        return 1
    print('PASS: PNG export includes the map layer in all scenarios')
    return 0


if __name__ == '__main__':
    sys.exit(main())
