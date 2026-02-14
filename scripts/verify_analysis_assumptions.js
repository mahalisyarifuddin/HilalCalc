const Astronomy = require('astronomy-engine');

// --- Part 1: Verify Kuwaiti Leap Year Pattern ---
function verifyKuwaitiPattern() {
    console.log("Verifying Kuwaiti Leap Year Pattern...");
    const standardLeapYears = [2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29]; // 1-based

    // Formula: dayInCycle = yearInCycle * 354 + Math.floor((11 * yearInCycle + C) / 30);
    // yearInCycle is 0..29 (corresponding to years 1..30)
    // Leap year y (1-based) is when dayInCycle(y) - dayInCycle(y-1) == 355
    // which means Math.floor((11*y + C)/30) - Math.floor((11*(y-1) + C)/30) == 1

    let bestC = -999;

    for (let C = 0; C < 30; C++) {
        let currentLeaps = [];
        for (let y = 1; y <= 30; y++) {
            const yearInCycle = y - 1; // 0-based for calculation of start of year y?
            // Wait, dayInCycle calculation in optimize_tabular.js:
            // const dayInCycle = yearInCycle * 354 + Math.floor((11 * yearInCycle + C) / 30);
            // This calculates days *before* the start of yearInCycle.
            // So for year y (1-based), yearInCycle = y-1.
            // Days in year y = dayInCycle(y) - dayInCycle(y-1)
            // Wait. dayInCycle(y) is start of year y+1 (0-based index y).
            // Let's use the function from optimize_tabular logic.

            // Days *in* year y (1-based index):
            // Start of year y: yearInCycle = y-1.
            // Start of year y+1: yearInCycle = y.

            const startY = (y-1) * 354 + Math.floor((11 * (y-1) + C) / 30);
            const startNextY = (y) * 354 + Math.floor((11 * y + C) / 30);
            const daysInY = startNextY - startY;

            if (daysInY === 355) {
                currentLeaps.push(y);
            }
        }

        // Compare with standard
        const isMatch = JSON.stringify(currentLeaps) === JSON.stringify(standardLeapYears);
        if (isMatch) {
            console.log(`Found Match! C = ${C} produces the standard Kuwaiti leap years.`);
            console.log(`Leap Years: ${currentLeaps.join(', ')}`);
            bestC = C;
        }
    }

    if (bestC === -999) {
        console.log("No C value found that matches standard Kuwaiti leap years exactly.");
        // Let's print what C=14 (Standard Kuwaiti usually implies 14) produces
        const C = 14;
        let currentLeaps = [];
        for (let y = 1; y <= 30; y++) {
            const startY = (y-1) * 354 + Math.floor((11 * (y-1) + C) / 30);
            const startNextY = (y) * 354 + Math.floor((11 * y + C) / 30);
            const daysInY = startNextY - startY;
            if (daysInY === 355) currentLeaps.push(y);
        }
        console.log(`For C=${C}, Leap Years: ${currentLeaps.join(', ')}`);
    }
}

// --- Part 2: Verify Ground Truth Logic ---

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

    // MABBIMS Criteria: Alt >= 3 AND Elongation >= 6.4
    return (altitude >= 3.0 && elongation >= 6.4);
}

function getHijriMonthStart(hYear, hMonth, lat, lon) {
    // 1. Approximate start
    const daysSinceAnchor = ((hYear - 1445) * 354.367) + ((hMonth - 1) * 29.53);
    const anchorDate = new Date("2023-07-19T12:00:00Z");
    const approxTime = anchorDate.getTime() + daysSinceAnchor * 86400000;
    const approxDate = new Date(approxTime);

    // 2. Find New Moon
    const searchStart = new Date(approxDate.getTime() - 5 * 86400000);
    const timeStart = Astronomy.MakeTime(searchStart);
    let bestNewMoon = Astronomy.SearchMoonPhase(0, timeStart.ut, 10);

    if (!bestNewMoon) return "Error";

    const newMoonDate = bestNewMoon.date;
    const utcOffset = getTimezoneOffset(lon);
    const localNM = new Date(newMoonDate.getTime() + utcOffset * 3600000);
    const checkDate = new Date(Date.UTC(localNM.getUTCFullYear(), localNM.getUTCMonth(), localNM.getUTCDate()));

    const isVisible = checkVisibility(checkDate, bestNewMoon.ut, lat, lon);

    const startDate = new Date(checkDate);
    startDate.setUTCDate(checkDate.getUTCDate() + (isVisible ? 1 : 2));

    return startDate.toISOString().split('T')[0];
}

async function verifyGroundTruth() {
    console.log("\nVerifying Ground Truth Logic...");
    // Check known dates.
    // Example: Ramadan 1445.
    // Start of Ramadan 1445 in Mecca.
    // New Moon for Ramadan (end of Shaban) was March 10, 2024.
    // Conjunction: March 10, 2024 at 09:00 UTC (12:00 Mecca).
    // Sunset Mecca: ~18:29.
    // Age: ~6.5 hours.
    // Altitude: Low?
    // Official Saudi Arabia: Monday March 11, 2024. (So visible on 10th?)
    // Actually, Saudi Arabia often uses Umm Al-Qura (Moonset > Sunset && Conjunction < Sunset).
    // But here we are using MABBIMS (3 deg alt, 6.4 elong).
    // Let's see what our logic says for Mecca, Ramadan 1445.

    const hYear = 1445;
    const hMonth = 9;
    const mecca = { lat: 21.3891, lon: 39.8579 };

    const calcDate = getHijriMonthStart(hYear, hMonth, mecca.lat, mecca.lon);
    console.log(`Calculated Start of Ramadan 1445 (Mecca, MABBIMS): ${calcDate}`);

    // Check Banda Aceh
    const aceh = { lat: 6.075, lon: 95.1125 };
    const calcDateAceh = getHijriMonthStart(hYear, hMonth, aceh.lat, aceh.lon);
    console.log(`Calculated Start of Ramadan 1445 (Banda Aceh, MABBIMS): ${calcDateAceh}`);

    // According to MABBIMS criteria for 1445 (March 2024):
    // Conjunction March 10.
    // In SE Asia (Aceh), sunset is earlier. Age is smaller.
    // Likely not visible on March 10. Start March 12.
    // Let's verify.
}

verifyKuwaitiPattern();
verifyGroundTruth();
