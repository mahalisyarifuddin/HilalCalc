const Astronomy = require('astronomy-engine');
const fs = require('fs');
const path = require('path');

const mecca = { lat: 21.354813, lon: 39.984063 };
const kb = { lat: 4.587063, lon: 114.075937 };

const startYear = 1400;
const endYear = 1500;

function getTimezoneOffset(lon) {
    return Math.round(lon / 15);
}

function checkVisibilityComposite(dateObj, newMoonUT) {
    // Check Mecca
    const meccaOffset = getTimezoneOffset(mecca.lon);
    const meccaBaseUTC = new Date(dateObj);
    meccaBaseUTC.setUTCHours(12 - meccaOffset);
    const meccaDate = Astronomy.MakeTime(meccaBaseUTC);
    const meccaObs = new Astronomy.Observer(mecca.lat, mecca.lon, 0);
    const meccaSunset = Astronomy.SearchRiseSet(Astronomy.Body.Sun, meccaObs, -1, meccaDate.ut, 1);

    if (!meccaSunset) return false;

    // Check KB
    const kbOffset = getTimezoneOffset(kb.lon);
    const kbBaseUTC = new Date(dateObj);
    kbBaseUTC.setUTCHours(12 - kbOffset);
    const kbDate = Astronomy.MakeTime(kbBaseUTC);
    const kbObs = new Astronomy.Observer(kb.lat, kb.lon, 0);
    const kbSunset = Astronomy.SearchRiseSet(Astronomy.Body.Sun, kbObs, -1, kbDate.ut, 1);

    if (!kbSunset) return false;

    // Check conditions
    // Mecca
    const mSunsetUT = meccaSunset.ut;
    const mMoonEq = Astronomy.Equator(Astronomy.Body.Moon, mSunsetUT, meccaObs, true, true);
    const mMoonHor = Astronomy.Horizon(mSunsetUT, meccaObs, mMoonEq.ra, mMoonEq.dec, "normal");
    const mSunEq = Astronomy.Equator(Astronomy.Body.Sun, mSunsetUT, meccaObs, true, true);
    const mElong = Astronomy.AngleBetween(mSunEq.vec, mMoonEq.vec);

    // KB
    const kSunsetUT = kbSunset.ut;
    const kMoonEq = Astronomy.Equator(Astronomy.Body.Moon, kSunsetUT, kbObs, true, true);
    const kMoonHor = Astronomy.Horizon(kSunsetUT, kbObs, kMoonEq.ra, kMoonEq.dec, "normal");

    const meccaOk = (mMoonHor.altitude >= 3.0 && mElong >= 6.4);
    const kbOk = (kMoonHor.altitude >= 0.0);

    const age = mSunsetUT - newMoonUT; // Age at Mecca sunset
    if (age < 0) return false; // Conjunction after sunset

    return meccaOk && kbOk;
}

function getCompositeMonthStart(hYear, hMonth) {
     // 1. Approximate start
    // anchor: 1445-01 approx 2023-07-19
    const daysSinceAnchor = ((hYear - 1445) * 354.367) + ((hMonth - 1) * 29.53);
    const anchorDate = new Date("2023-07-19T12:00:00Z");
    const approxTime = anchorDate.getTime() + daysSinceAnchor * 86400000;
    const approxDate = new Date(approxTime);

    // 2. Find New Moon
    const searchStart = new Date(approxDate.getTime() - 5 * 86400000);
    const timeStart = Astronomy.MakeTime(searchStart);
    let bestNewMoon = Astronomy.SearchMoonPhase(0, timeStart.ut, 10);

    if (!bestNewMoon) return approxDate.toISOString().split('T')[0];

    const newMoonDate = bestNewMoon.date; // Date derived from UT
    const utcOffset = getTimezoneOffset(mecca.lon); // Use Mecca as reference for "Day"

    // Shift to local time to determine "Day of New Moon"
    const localNM = new Date(newMoonDate.getTime() + utcOffset * 3600000);

    // checkDate is the day of New Moon in Local Time (at 00:00 UTC for that day)
    const checkDate = new Date(Date.UTC(localNM.getUTCFullYear(), localNM.getUTCMonth(), localNM.getUTCDate()));

    const isVisible = checkVisibilityComposite(checkDate, bestNewMoon.ut);

    const startDate = new Date(checkDate);
    startDate.setUTCDate(checkDate.getUTCDate() + (isVisible ? 1 : 2));

    return startDate.toISOString().split('T')[0];
}

function hijriToGregorianTabular(hYear, hMonth, hDay, C) {
    const epoch = 1948439.5;
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

async function main() {
    console.log("Generating Composite GT for 1400-1500 AH...");
    const gt = [];
    const csvRows = ["Hijri Year,Hijri Month,Gregorian Date"];

    for (let y = startYear; y <= endYear; y++) {
        for (let m = 1; m <= 12; m++) {
            const date = getCompositeMonthStart(y, m);
            gt.push({ y, m, date });
            csvRows.push(`${y},${m},${date}`);
        }
    }

    fs.writeFileSync('verification/composite_1400_1500.csv', csvRows.join('\n'));
    console.log("GT Generated. Optimizing C...");

    let bestC = -999;
    let bestAcc = -1;
    let candidates = [];

    for (let C = -100; C <= 100; C++) {
        let matches = 0;
        for (const item of gt) {
            const tabDate = hijriToGregorianTabular(item.y, item.m, 1, C);
            const tabStr = tabDate.toISOString().split('T')[0];
            if (tabStr === item.date) matches++;
        }
        const acc = (matches / gt.length) * 100;
        candidates.push({ C, acc });
        if (acc > bestAcc) {
            bestAcc = acc;
            bestC = C;
        }
    }

    // Sort by accuracy descending
    candidates.sort((a, b) => b.acc - a.acc);

    console.log(`Optimization Complete.`);
    console.log(`Best C: ${bestC} with Accuracy: ${bestAcc.toFixed(2)}%`);
    console.log(`Top 5 Candidates:`);
    candidates.slice(0, 5).forEach(c => console.log(`C=${c.C}, Acc=${c.acc.toFixed(2)}%`));
}

main();
