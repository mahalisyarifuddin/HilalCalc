import subprocess
import json
import datetime

def get_dates(year, month):
    # Prepare JS code from HilalSync.html
    with open('HilalSync.html') as f:
        html = f.read()
    js_code = html.split('<script>')[1].split('</script>')[0]

    # Wrap in node compatible format
    full_js = f"""
    const Astronomy = require('astronomy-engine');
    const state = {{ lang: "en", year: {year}, month: {month}, AE_OFFSET: 2451545.0, BA_LAT: 5.54829, BA_LON: 95.32375 }};
    function jdToDate(jd) {{ return new Date((jd - 2440587.5) * 86400000); }}
    function utToDate(ut) {{ return jdToDate(ut + state.AE_OFFSET); }}
    {js_code.split('function jdToDate')[1] if 'function jdToDate' in js_code else js_code}
    console.log(JSON.stringify(getStartJD({year}, {month})));
    """

    # Save to temp file to avoid shell escape issues
    with open('temp_verify.js', 'w') as f:
        f.write(full_js)

    try:
        out = subprocess.check_output("node temp_verify.js", shell=True, stderr=subprocess.STDOUT).decode()
        return json.loads(out)
    except Exception as e:
        print(f"Error for {month}: {e}")
        if hasattr(e, 'output'):
            print(e.output.decode())
        return None

ref_1447 = [
    (1, "Thursday, 26 June 2025"),
    (2, "Saturday, 26 July 2025"),
    (3, "Sunday, 24 August 2025"),
    (4, "Tuesday, 23 September 2025"),
    (5, "Thursday, 23 October 2025"),
    (6, "Friday, 21 November 2025"),
    (7, "Sunday, 21 December 2025"),
    (8, "Tuesday, 20 January 2026"),
    (9, "Wednesday, 18 February 2026"),
    (10, "Friday, 20 March 2026"),
    (11, "Saturday, 18 April 2026"),
    (12, "Tuesday, 19 May 2026"),
]

def jd_to_str(jd):
    dt = datetime.datetime(2000, 1, 1, 12) + datetime.timedelta(days=jd - 2451545.0)
    return dt.strftime("%A, %-d %B %Y")

print("Verifying 1447 AH GIC dates...")
matches = 0
for m, gic_exp in ref_1447:
    res = get_dates(1447, m)
    if not res: continue

    gic_got = jd_to_str(res['jdGic'])
    if gic_got == gic_exp:
        print(f"Month {m} OK: {gic_got}")
        matches += 1
    else:
        print(f"Month {m} FAIL: Got {gic_got} | Exp {gic_exp}")

print(f"\nTotal GIC matches: {matches}/12")
