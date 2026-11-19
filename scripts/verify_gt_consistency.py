"""Validate the legacy Mecca CSV; import Astronomy Engine only for real verification."""
import argparse
import csv
from pathlib import Path

DEFAULT_CSV = Path(__file__).resolve().parents[1] / 'gt_1_20000.csv'
TOTAL_ROWS = (20000 + 1) * 12
INITIAL_JD = 1948085


def verify_rows(rows, next_jd, expected_rows, *, prefix=False):
    current_jd = INITIAL_JD
    for index in range(expected_rows):
        row = next(rows, None)
        if row is None:
            raise ValueError(f'Truncated CSV: missing month index {index}')
        if index:
            current_jd = next_jd(current_jd)
        if len(row) < 2 or int(row[0]) != index or int(row[1]) != current_jd:
            raise ValueError(f'Expected index {index}, JD {current_jd}; got {row}')
    if not prefix and next(rows, None) is not None:
        raise ValueError(f'CSV has more than {expected_rows} month rows')


def mecca_next_jd():
    import astronomy as ae

    observer = ae.Observer(21.354813, 39.984063, 0)

    def calculate(jd):
        sunset = ae.SearchRiseSet(ae.Body.Sun, observer, ae.Direction.Set,
                                 ae.Time(jd + 28 - 2451545.0), 1.0)
        if sunset is None:
            raise ValueError(f'Could not find sunset for month beginning JD {jd}')
        moon = ae.Equator(ae.Body.Moon, sunset, observer, True, True)
        sun = ae.Equator(ae.Body.Sun, sunset, observer, True, True)
        altitude = ae.Horizon(sunset, observer, moon.ra, moon.dec, ae.Refraction.Normal).altitude
        return jd + (29 if altitude >= 0 and ae.AngleBetween(moon.vec, sun.vec) >= 0 else 30)

    return calculate


def main(*, quick=False):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', type=Path, nargs='?', default=DEFAULT_CSV)
    args = parser.parse_args()
    count = 101 if quick else TOTAL_ROWS
    try:
        with args.csv.open(newline='') as stream:
            rows = csv.reader(stream)
            if next(rows, None) is None:
                raise ValueError('Missing CSV header')
            verify_rows(rows, mecca_next_jd(), count, prefix=quick)
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f'Verification failed: {error}\n')
    print(f'Verified {count} month starts against Mecca 0°/0°')


if __name__ == '__main__':
    main()
