from contextlib import redirect_stderr
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.verify_gt_consistency import main, verify_rows


class GroundTruthTest(unittest.TestCase):
    good = [['0', '1948085'], ['1', '1948114']]

    def verify(self, rows, **kwargs):
        verify_rows(iter(rows), lambda jd: jd + 29, 2, **kwargs)

    def test_valid(self):
        self.verify(self.good)

    def test_truncated(self):
        with self.assertRaisesRegex(ValueError, 'Truncated'):
            self.verify(self.good[:1])

    def test_corrupt(self):
        for row in (['2', '1948114'], ['1', '1948115']):
            with self.subTest(row=row), self.assertRaisesRegex(ValueError, 'Expected index 1'):
                self.verify([self.good[0], row])

    def test_extra_rows_only_allowed_in_prefix_mode(self):
        rows = self.good + [['2', '1948143']]
        self.verify(rows, prefix=True)
        with self.assertRaisesRegex(ValueError, 'more than'):
            self.verify(rows)

    def test_cli_exits_nonzero_on_truncated_data(self):
        with tempfile.TemporaryDirectory() as temp:
            csv_path = Path(temp) / 'partial.csv'
            csv_path.write_text('Index,JD\n0,1948085\n')
            for quick in (False, True):
                with (self.subTest(quick=quick),
                      patch('sys.argv', ['verify', str(csv_path)]),
                      patch('scripts.verify_gt_consistency.mecca_next_jd', return_value=lambda jd: jd + 29),
                      redirect_stderr(io.StringIO()) as errors,
                      self.assertRaises(SystemExit) as exited):
                    main(quick=quick)
                self.assertEqual(exited.exception.code, 1)
                self.assertIn('Truncated CSV', errors.getvalue())
