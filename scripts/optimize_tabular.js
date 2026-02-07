const Astronomy = require('astronomy-engine');

const locations = [
    { name: 'Dakar', lat: 14.7167, lon: -17.4677 },
    { name: 'Mecca', lat: 21.3891, lon: 39.8579 },
    { name: 'Banda Aceh', lat: 6.075, lon: 95.1125 }
];

const months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]; // All months
const obligMonths = [9, 10, 12];
const startYear = 1000;
const endYear = 2000;

const altCache = new Map();

function calculateC(lon) {
    return Math.round(lon / 12.4848 + 7.8628);
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
        const bestNewMoon = Astronomy.SearchMoonPhase(0, date.ut, -35);
        if (!bestNewMoon) return false;
        newMoonUT = bestNewMoon.ut;
    }
    const age = sunsetUT - newMoonUT;
    if (age < 0) return false;
    const altitude = moonHor.altitude;
    return (altitude >= 3.0 && elongation >= 6.4);
}

// Get Moon Altitude at sunset for the eve of the given date (date - 1 day)
function getMoonAltitudeAtSunsetOfEve(dateObj, lat, lon) {
    const key = `${dateObj.toISOString().split('T')[0]}-${lat}-${lon}`;
    if (altCache.has(key)) return altCache.get(key);

    const utcOffset = getTimezoneOffset(lon);
    // Observation is on the evening BEFORE the Tabular Date (which starts at Maghrib)
    // Wait, let's be precise.
    // If Tabular Date is "March 23", it starts at sunset on March 22.
    // So we check sunset on March 22.
    // dateObj represents "March 23" at noon UTC.
    // So dateObj - 1 day is "March 22".

    const obsDate = new Date(dateObj.getTime() - 86400000);
    const baseUTC = new Date(obsDate);
    baseUTC.setUTCHours(12 - utcOffset);

    const date = Astronomy.MakeTime(baseUTC);
    const observer = new Astronomy.Observer(lat, lon, 0);
    const sunset = Astronomy.SearchRiseSet(Astronomy.Body.Sun, observer, -1, date.ut, 1);

    let altitude = -999;
    if (sunset) {
        const sunsetUT = sunset.ut;
        const moonEq = Astronomy.Equator(Astronomy.Body.Moon, sunsetUT, observer, true, true);
        const moonHor = Astronomy.Horizon(sunsetUT, observer, moonEq.ra, moonEq.dec, "normal");
        altitude = moonHor.altitude;
    }

    altCache.set(key, altitude);
    return altitude;
}

// Helper to format date as YYYY-MM-DD
function formatDate(date) {
    return date.toISOString().split('T')[0];
}

function getHijriMonthStart(hYear, hMonth, lat, lon) {
    // 1. Approximate start
    // anchor: 1445-01 approx 2023-07-19
    const daysSinceAnchor = ((hYear - 1445) * 354.367) + (hMonth * 29.53);
    const anchorDate = new Date("2023-07-19T12:00:00Z");
    const approxTime = anchorDate.getTime() + daysSinceAnchor * 86400000;
    const approxDate = new Date(approxTime);

    // 2. Find New Moon
    const searchStart = new Date(approxDate.getTime() - 5 * 86400000);
    const timeStart = Astronomy.MakeTime(searchStart);
    let bestNewMoon = Astronomy.SearchMoonPhase(0, timeStart.ut, 10);

    if (!bestNewMoon) return formatDate(approxDate);

    const newMoonDate = bestNewMoon.date; // This is a Date object derived from UT
    const utcOffset = getTimezoneOffset(lon);

    // Shift to local time to determine "Day of New Moon"
    const localNM = new Date(newMoonDate.getTime() + utcOffset * 3600000);

    // checkDate is the day of New Moon in Local Time
    const checkDate = new Date(Date.UTC(localNM.getUTCFullYear(), localNM.getUTCMonth(), localNM.getUTCDate()));

    const isVisible = checkVisibility(checkDate, bestNewMoon.ut, lat, lon);

    const startDate = new Date(checkDate);
    startDate.setUTCDate(checkDate.getUTCDate() + (isVisible ? 1 : 2));

    return formatDate(startDate);
}

async function main() {
    console.log(`Analyzing years ${startYear}-${endYear} AH`);
    console.log('Calculating dual accuracy rates: All Months vs Obligatory Months (9, 10, 12)');
    console.log('---');

    for (const loc of locations) {
        console.log(`Processing ${loc.name} (${loc.lat}, ${loc.lon})...`);

        let groundTruths = [];

        // Calculate Ground Truths for ALL months
        for (let y = startYear; y <= endYear; y++) {
            for (const m of months) {
                const gt = getHijriMonthStart(y, m, loc.lat, loc.lon);
                groundTruths.push({ y, m, gt });
            }
        }

        let bestCAll = -100;
        let maxAccAll = -1;
        let bestCOblig = -100;
        let maxAccOblig = -1;

        // Track the "Impossible" rate for the BEST C
        // We will store all stats to retrieve later
        let stats = [];

        for (let C = -15; C <= 30; C++) {
            let matchesAll = 0;
            let totalAll = 0;
            let matchesOblig = 0;
            let totalOblig = 0;

            let impossibleAll = 0;
            let impossibleOblig = 0;

            for (const item of groundTruths) {
                const tabDate = hijriToGregorianTabular(item.y, item.m, 1, C);
                const tabStr = formatDate(tabDate);

                // Check if Moon was below horizon on the eve of tabDate
                const altitude = getMoonAltitudeAtSunsetOfEve(tabDate, loc.lat, loc.lon);
                const isImpossible = (altitude < 0);

                totalAll++;
                if (tabStr === item.gt) matchesAll++;
                if (isImpossible) impossibleAll++;

                if (obligMonths.includes(item.m)) {
                    totalOblig++;
                    if (tabStr === item.gt) matchesOblig++;
                    if (isImpossible) impossibleOblig++;
                }
            }
            const accAll = (matchesAll / totalAll) * 100;
            const accOblig = (matchesOblig / totalOblig) * 100;
            const impAll = (impossibleAll / totalAll) * 100;
            const impOblig = (impossibleOblig / totalOblig) * 100;

            stats.push({ C, accAll, accOblig, impAll, impOblig });

            if (accAll > maxAccAll) { maxAccAll = accAll; bestCAll = C; }
            if (accOblig > maxAccOblig) { maxAccOblig = accOblig; bestCOblig = C; }
        }

        // Find stats for best All
        const bestAllStats = stats.find(s => s.C === bestCAll);
        // Find stats for best Oblig
        const bestObligStats = stats.find(s => s.C === bestCOblig);

        console.log(`Best C (All Months): ${bestCAll} (Acc: ${bestAllStats.accAll.toFixed(2)}%, Impossible: ${bestAllStats.impAll.toFixed(2)}%)`);
        console.log(`Best C (Obligatory): ${bestCOblig} (Acc: ${bestObligStats.accAll.toFixed(2)}%, Impossible: ${bestObligStats.impAll.toFixed(2)}%)`); // Use impAll or impOblig? Usually we care about impossible rate for the specific months we optimized for, or overall? Let's report both contexts.
        // Actually, if optimizing for Obligatory, we care about impossible rate for Obligatory months mainly.
        // But let's stick to the column format: "Best C | Oblig Acc | All Acc | Impossible (relevant scope)"
        // If Phase 1 (Oblig), "Impossible" should be for Obligatory months?
        // Let's print extensive info.

        console.log(`Phase 1 (Obligatory Months) C=${bestCOblig}:`);
        console.log(`  - Obligatory Accuracy: ${bestObligStats.accOblig.toFixed(2)}%`);
        console.log(`  - All Months Accuracy: ${bestObligStats.accAll.toFixed(2)}%`);
        console.log(`  - Obligatory Impossible: ${bestObligStats.impOblig.toFixed(2)}%`);
        console.log(`  - All Months Impossible: ${bestObligStats.impAll.toFixed(2)}%`);

        console.log(`Phase 2 (All Months) C=${bestCAll}:`);
        console.log(`  - Obligatory Accuracy: ${bestAllStats.accOblig.toFixed(2)}%`);
        console.log(`  - All Months Accuracy: ${bestAllStats.accAll.toFixed(2)}%`);
        console.log(`  - Obligatory Impossible: ${bestAllStats.impOblig.toFixed(2)}%`);
        console.log(`  - All Months Impossible: ${bestAllStats.impAll.toFixed(2)}%`);
        console.log('---');
    }
}

main();
