const Astronomy = require('astronomy-engine');

const locations = [
    { name: 'Dakar', lat: 14.7167, lon: -17.4677 },
    { name: 'Mecca', lat: 21.3891, lon: 39.8579 },
    { name: 'Banda Aceh', lat: 6.075, lon: 95.1125 }
];

const months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]; // All months
const startYear = 1000;
const endYear = 2000;

function calculateC(lon) {
    return Math.round(lon / 12.0 + 7.5);
}

function hijriToGregorianTabular(hYear, hMonth, hDay, C) {
    const epoch = 1948439.5; // Standard epoch (July 15, 622)
    const year = hYear - 1;
    const cycle = Math.floor(year / 30);
    const yearInCycle = year % 30;
    const dayInCycle = yearInCycle * 354 + Math.floor((11 * yearInCycle + C) / 30);
    const dayInYear = Math.ceil(29.5 * hMonth);
    const jd = epoch + cycle * 10631 + dayInCycle + dayInYear + hDay - 1;

    let z = Math.floor(jd + 0.5);
    let f = jd + 0.5 - z;
    let alpha = Math.floor((z - 1867216.25) / 36524.25);
    let a = z + 1 + alpha - Math.floor(alpha / 4);
    let b = a + 1524;
    let c = Math.floor((b - 122.1) / 365.25);
    let d = Math.floor(365.25 * c);
    let e = Math.floor((b - d) / 30.6001);
    let day = b - d - Math.floor(30.6001 * e) + f;
    let monthResult = e - 1;
    if (monthResult > 12) monthResult -= 12;
    let yearResult = c - 4715;
    if (e < 14) monthResult = e - 1; else monthResult = e - 13;
    if (monthResult > 2) yearResult = c - 4716; else yearResult = c - 4715;

    // Return a date object at noon to avoid boundary issues, though we care about the Date part.
    return new Date(Date.UTC(yearResult, monthResult - 1, Math.floor(day), 12, 0, 0));
}

function getTimezoneOffset(lon) {
    return Math.round(lon / 15);
}

function checkVisibility(dateObj, knownNewMoonUT, lat, lon) {
    const utcOffset = getTimezoneOffset(lon);
    // Construct baseUTC at 12:00 Local Time (approx sunset check time frame)
    // We want 12:00 Local, so we subtract offset from UTC.
    // If offset is +7, 12:00 Local is 05:00 UTC.
    // dateObj is expected to be a Date object representing the day (e.g. at 00:00 UTC or Local?).
    // In getHijriMonthStart, we construct checkDate from NewMoon shifted to local.

    // We can just use the dateObj (which is YMD) and set hours.
    const baseUTC = new Date(dateObj);
    baseUTC.setUTCHours(12 - utcOffset);

    const date = Astronomy.MakeTime(baseUTC);
    const observer = new Astronomy.Observer(lat, lon, 0);
    const sunset = Astronomy.SearchRiseSet(Astronomy.Body.Sun, observer, -1, date.ut, 1);
    if (!sunset) return false;
    const sunsetUT = sunset.ut;
    const moonEq = Astronomy.Equator(Astronomy.Body.Moon, sunsetUT, observer, true, true);
    const moonHor = Astronomy.Horizon(sunsetUT, observer, moonEq.ra, moonEq.dec, "normal");
    const sunEq = Astronomy.Equator(Astronomy.Body.Sun, sunsetUT, observer, true, true);
    const elongation = Astronomy.AngleBetween(sunEq.vec, moonEq.vec);

    let newMoonUT = knownNewMoonUT;
    if (newMoonUT === undefined || newMoonUT === null) {
        // Find New Moon near this date
        // Search center around the check time
        const bestNewMoon = Astronomy.SearchMoonPhase(0, date.ut, -35);
        if (!bestNewMoon) return false;
        newMoonUT = bestNewMoon.ut;
    }
    const age = sunsetUT - newMoonUT;
    if (age < 0) return false;
    const altitude = moonHor.altitude;
    return (altitude >= 3.0 && elongation >= 6.4);
}

// Helper to format date as YYYY-MM-DD
function formatDate(date) {
    return date.toISOString().split('T')[0];
}

function getHijriMonthStart(hYear, hMonth, lat, lon) {
    // 1. Approximate start
    // Using a fixed C=0 for approximation or just standard
    // Use the logic from HijriCalc to get close
    // anchor: 1445-01 approx 2023-07-19
    const daysSinceAnchor = ((hYear - 1445) * 354.367) + (hMonth * 29.53);
    const anchorDate = new Date("2023-07-19T12:00:00Z");
    const approxTime = anchorDate.getTime() + daysSinceAnchor * 86400000;
    const approxDate = new Date(approxTime);

    // 2. Find New Moon
    const searchStart = new Date(approxDate.getTime() - 5 * 86400000);
    const timeStart = Astronomy.MakeTime(searchStart);
    let bestNewMoon = Astronomy.SearchMoonPhase(0, timeStart.ut, 10);

    // If fail, fallback to approx (shouldn't happen in this range)
    if (!bestNewMoon) return formatDate(approxDate);

    const newMoonDate = bestNewMoon.date; // This is a Date object derived from UT
    const utcOffset = getTimezoneOffset(lon);

    // Shift to local time to determine "Day of New Moon"
    // We clone it to avoid mutating if it matters
    const localNM = new Date(newMoonDate.getTime() + utcOffset * 3600000);

    // checkDate is the day of New Moon in Local Time
    // We construct it as UTC YMD to avoid system timezone issues
    const checkDate = new Date(Date.UTC(localNM.getUTCFullYear(), localNM.getUTCMonth(), localNM.getUTCDate()));

    const isVisible = checkVisibility(checkDate, bestNewMoon.ut, lat, lon);

    const startDate = new Date(checkDate);
    startDate.setUTCDate(checkDate.getUTCDate() + (isVisible ? 1 : 2));

    return formatDate(startDate);
}

async function main() {
    console.log(`Analyzing years ${startYear}-${endYear} AH for months: ${months.join(', ')}`);
    console.log(`Locations: ${locations.map(l => l.name).join(', ')}`);
    console.log('---');

    for (const loc of locations) {
        console.log(`Processing ${loc.name} (${loc.lat}, ${loc.lon})...`);

        let groundTruths = [];

        // Calculate Ground Truths
        for (let y = startYear; y <= endYear; y++) {
            for (const m of months) {
                const gt = getHijriMonthStart(y, m, loc.lat, loc.lon);
                groundTruths.push({ y, m, gt });
            }
        }

        // Optimize C
        let bestC = -100;
        let bestAccuracy = -1;
        let results = [];

        for (let C = -15; C <= 30; C++) {
            let matches = 0;
            for (const item of groundTruths) {
                const tabDate = hijriToGregorianTabular(item.y, item.m, 1, C);
                const tabStr = formatDate(tabDate);
                if (tabStr === item.gt) {
                    matches++;
                }
            }
            const accuracy = (matches / groundTruths.length) * 100;
            results.push({ C, accuracy });

            if (accuracy > bestAccuracy) {
                bestAccuracy = accuracy;
                bestC = C;
            }
        }

        // Find all C with best accuracy
        const bestCs = results.filter(r => Math.abs(r.accuracy - bestAccuracy) < 0.001).map(r => r.C);
        // If multiple, pick the one closest to current formula prediction or median
        // Current formula: round(lon/12 + 7.5)
        const currentFormulaC = calculateC(loc.lon);

        console.log(`Best Accuracy: ${bestAccuracy.toFixed(2)}%`);
        console.log(`Best C values: ${bestCs.join(', ')}`);
        console.log(`Current Formula C: ${currentFormulaC}`);
        console.log('---');
    }
}

main();
