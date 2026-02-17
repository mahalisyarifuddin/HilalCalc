const Astronomy = require('astronomy-engine');

// --- Configuration ---
const START_YEAR_AH = 1343;
const END_YEAR_AH = 1500;
const LOCATIONS = {
    'Dakar': { lat: 14.740938, lon: -17.529938 },
    'Mecca': { lat: 21.354813, lon: 39.984063 },
    'Kuala Belait': { lat: 4.587063, lon: 114.075937 }
};
const MONTHS_ALL = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
const MONTHS_OBLIGATORY = [9, 10, 12];

const altCache = new Map();

// --- Tabular Hijri Logic ---
function hijriToGregorianTabular(hYear, hMonth, hDay, C) {
    const epoch = 1948439.5; // Standard epoch (July 15, 622)
    const year = hYear - 1;
    const cycle = Math.floor(year / 30);
    const yearInCycle = year % 30;
    const dayInCycle = yearInCycle * 354 + Math.floor((11 * yearInCycle + C) / 30);
    const dayInYear = Math.ceil(29.5 * (hMonth - 1));
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

    return new Date(Date.UTC(yearResult, monthResult - 1, Math.floor(day), 12, 0, 0));
}

// --- Astronomy Helpers ---
function getTimezoneOffset(lon) {
    return Math.round(lon / 15);
}

function checkVisibility(dateObj, knownNewMoonUT, lat, lon) {
    const utcOffset = getTimezoneOffset(lon);
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
        const bestNewMoon = Astronomy.SearchMoonPhase(0, date.ut, -35);
        if (!bestNewMoon) return false;
        newMoonUT = bestNewMoon.ut;
    }
    const age = sunsetUT - newMoonUT;
    if (age < 0) return false;
    const altitude = moonHor.altitude;

    // MABBIMS Criteria: Alt >= 3.0 and Elongation >= 6.4
    return (altitude >= 3.0 && elongation >= 6.4);
}

function getMoonAltitudeAtSunsetOfEve(dateObj, lat, lon) {
    const key = `${dateObj.toISOString().split('T')[0]}-${lat}-${lon}`;
    if (altCache.has(key)) return altCache.get(key);

    const utcOffset = getTimezoneOffset(lon);
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

function formatDate(date) {
    return date.toISOString().split('T')[0];
}

function getHijriMonthStart(hYear, hMonth, lat, lon) {
    const daysSinceAnchor = ((hYear - 1445) * 354.367) + ((hMonth - 1) * 29.53);
    const anchorDate = new Date("2023-07-19T12:00:00Z");
    const approxTime = anchorDate.getTime() + daysSinceAnchor * 86400000;
    const approxDate = new Date(approxTime);

    const searchStart = new Date(approxDate.getTime() - 5 * 86400000);
    const timeStart = Astronomy.MakeTime(searchStart);
    let bestNewMoon = Astronomy.SearchMoonPhase(0, timeStart.ut, 10);

    if (!bestNewMoon) return formatDate(approxDate);

    const newMoonDate = bestNewMoon.date;
    const utcOffset = getTimezoneOffset(lon);

    const localNM = new Date(newMoonDate.getTime() + utcOffset * 3600000);
    const checkDate = new Date(Date.UTC(localNM.getUTCFullYear(), localNM.getUTCMonth(), localNM.getUTCDate()));

    const isVisible = checkVisibility(checkDate, bestNewMoon.ut, lat, lon);

    const startDate = new Date(checkDate);
    startDate.setUTCDate(checkDate.getUTCDate() + (isVisible ? 1 : 2));

    return formatDate(startDate);
}

// --- Analysis Logic ---

async function calculateMetrics(cValue, locationName, useObligatoryOnly = false) {
    const loc = LOCATIONS[locationName];
    const months = useObligatoryOnly ? MONTHS_OBLIGATORY : MONTHS_ALL;
    let matches = 0;
    let total = 0;
    let impossible = 0;

    for (let y = START_YEAR_AH; y <= END_YEAR_AH; y++) {
        for (const m of months) {
            // Ground Truth: Astronomical Visibility (MABBIMS)
            const gt = getHijriMonthStart(y, m, loc.lat, loc.lon);

            // Prediction: Tabular Date
            const tabDate = hijriToGregorianTabular(y, m, 1, cValue);
            const tabStr = formatDate(tabDate);

            // Accuracy Check
            if (tabStr === gt) matches++;
            total++;

            // Impossibility Check (Moon below horizon at sunset of eve)
            const altitude = getMoonAltitudeAtSunsetOfEve(tabDate, loc.lat, loc.lon);
            if (altitude < 0) impossible++;
        }
    }

    return {
        accuracy: (matches / total) * 100,
        impossible: (impossible / total) * 100,
        total: total
    };
}

module.exports = {
    calculateMetrics,
    LOCATIONS,
    START_YEAR_AH,
    END_YEAR_AH
};
