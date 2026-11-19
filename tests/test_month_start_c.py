"""Check the historical C criteria against shared browser/C conjunction fixtures."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

FIXTURES = Path(__file__).resolve().parent
ROOT = FIXTURES.parent
RUNNER = ROOT / 'scripts' / 'astronomy_c_global_10k'


class HistoricalMonthStartTest(unittest.TestCase):
    def test_known_conjunctions(self):
        cases = json.loads((FIXTURES / 'month_start_cases.json').read_text())
        with tempfile.TemporaryDirectory() as temp:
            for case in cases:
                with self.subTest(case=case['note']):
                    land = ROOT / 'land_polygons.bin'
                    if 'land_fixture' in case:
                        land = Path(temp) / 'land.bin'
                        subprocess.run([sys.executable, ROOT / 'scripts' / 'prepare_land_binary.py',
                                        FIXTURES / case['land_fixture'], land], check=True, capture_output=True)
                    output = subprocess.check_output([RUNNER, '--conjunction-ut', str(case['conjunction_ut']), land], text=True)
                    self.assertEqual(list(map(float, output.strip().split(','))), case['historical_c_jd'])
