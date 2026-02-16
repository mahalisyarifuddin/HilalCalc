const Astronomy = require('astronomy-engine');

const locations = {
    mecca: { name: 'Mecca', lat: 21.354813, lon: 39.984063 },
    kb: { name: 'Kuala Belait', lat: 4.587063, lon: 114.075937 }
};

const months = [9, 10, 12]; // Obligatory months: Ramadan, Shawwal, Dhu al-Hijjah
const startYear = 1000;
const endYear = 6000;

const altCache = new Map();

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

// ============================================================================
// PARETO FRONTIER ANALYSIS FOR MECCA/KUALA BELAIT
// ============================================================================

function findParetoFrontier(candidates) {
    // Sort by Mecca Accuracy (Descending)
    const sorted = [...candidates].sort((a, b) => b.meccaAcc - a.meccaAcc);
    let frontier = [];
    let minImp = Infinity;

    for (const candidate of sorted) {
        // We want to MINIMIZE KB Impossibility
        if (candidate.kbImp < minImp) {
            frontier.push(candidate);
            minImp = candidate.kbImp;
        } else if (candidate.kbImp === minImp && frontier.length > 0) {
            // Handle ties: keep if strictly better accuracy (which is guaranteed by sort order for equal Impossible)
             if (candidate.meccaAcc > frontier[frontier.length - 1].meccaAcc) {
                frontier[frontier.length - 1] = candidate;
            }
        }
    }
    return frontier;
}

function distanceToIdeal(candidate) {
    // Ideal: Mecca Acc = 100%, KB Imp = 0%
    const accGap = 100 - candidate.meccaAcc;
    const impGap = candidate.kbImp - 0;
    return Math.sqrt(accGap ** 2 + impGap ** 2);
}

function findKneePoint(frontier) {
    if (frontier.length <= 2) return frontier[0];

    // Normalize to [0,1]
    const maxAcc = Math.max(...frontier.map(f => f.meccaAcc));
    const minAcc = Math.min(...frontier.map(f => f.meccaAcc));
    const maxImp = Math.max(...frontier.map(f => f.kbImp));
    const minImp = Math.min(...frontier.map(f => f.kbImp));

    const normalize = (f) => ({
        acc: maxAcc === minAcc ? 0.5 : (f.meccaAcc - minAcc) / (maxAcc - minAcc),
        imp: maxImp === minImp ? 0.5 : (f.kbImp - minImp) / (maxImp - minImp)
    });

    let maxCurvature = -Infinity;
    let kneeIndex = 0;

    for (let i = 1; i < frontier.length - 1; i++) {
        const prev = normalize(frontier[i - 1]);
        const curr = normalize(frontier[i]);
        const next = normalize(frontier[i + 1]);

        const a = Math.sqrt((curr.acc - prev.acc) ** 2 + (curr.imp - prev.imp) ** 2);
        const b = Math.sqrt((next.acc - curr.acc) ** 2 + (next.imp - curr.imp) ** 2);
        const c = Math.sqrt((next.acc - prev.acc) ** 2 + (next.imp - prev.imp) ** 2);

        const s = (a + b + c) / 2;
        const area = Math.sqrt(Math.max(0, s * (s - a) * (s - b) * (s - c)));
        const curvature = (a * b * c > 0) ? (4 * area) / (a * b * c) : 0;

        if (curvature > maxCurvature) {
            maxCurvature = curvature;
            kneeIndex = i;
        }
    }

    if (maxCurvature === 0 || !isFinite(maxCurvature)) {
        kneeIndex = frontier.reduce((bestIdx, curr, idx, arr) =>
            distanceToIdeal(curr) < distanceToIdeal(arr[bestIdx]) ? idx : bestIdx, 0);
    }
    return frontier[kneeIndex];
}

async function main() {
    console.log(`\n${'='.repeat(70)}`);
    console.log(`MECCA VISIBILITY vs KUALA BELAIT IMPOSSIBILITY EXPERIMENT (OBLIGATORY MONTHS)`);
    console.log(`Analyzing years ${startYear}-${endYear} AH`);
    console.log(`${'='.repeat(70)}\n`);

    const mecca = locations.mecca;
    const kb = locations.kb;

    console.log(`Calculating ground truths for Mecca...`);
    let meccaGT = [];
    for (let y = startYear; y <= endYear; y++) {
        for (const m of months) {
            meccaGT.push({ y, m, gt: getHijriMonthStart(y, m, mecca.lat, mecca.lon) });
        }
    }

    // We don't need KB GT for Impossibility check, we just check moon altitude.

    let results = [];

    console.log(`Evaluating C from -100 to 100...`);
    for (let C = -100; C <= 100; C++) {
        // Mecca Accuracy
        let meccaMatches = 0;
        let total = 0;
        for (const item of meccaGT) {
            const tabDate = hijriToGregorianTabular(item.y, item.m, 1, C);
            const tabStr = formatDate(tabDate);
            if (tabStr === item.gt) meccaMatches++;
            total++;
        }
        const meccaAcc = (meccaMatches / total) * 100;

        // KB Impossibility
        let kbImpossibleCount = 0;
        let kbTotal = 0;
        // We iterate through all months for KB as well (same set of tabular dates effectively)
        for (let y = startYear; y <= endYear; y++) {
            for (const m of months) {
                const tabDate = hijriToGregorianTabular(y, m, 1, C);
                const altitude = getMoonAltitudeAtSunsetOfEve(tabDate, kb.lat, kb.lon);
                if (altitude < 0) kbImpossibleCount++;
                kbTotal++;
            }
        }
        const kbImp = (kbImpossibleCount / kbTotal) * 100;

        results.push({ C, meccaAcc, kbImp });
    }

    // Find Pareto Frontier
    const frontier = findParetoFrontier(results);
    const kneePoint = findKneePoint(frontier);
    const idealPoint = results.reduce((best, curr) =>
        distanceToIdeal(curr) < distanceToIdeal(best) ? curr : best, results[0]);

    console.log(`\n${'='.repeat(70)}`);
    console.log(`RESULTS TABLE (C, Mecca Acc, KB Imp)`);
    console.log(`${'='.repeat(70)}`);
    console.log(` C | Mecca Acc | KB Imp   | Notes`);
    console.log(`---|-----------|----------|------`);

    results.forEach(r => {
        let notes = [];
        if (frontier.some(f => f.C === r.C)) notes.push('Pareto Frontier');
        if (kneePoint.C === r.C) notes.push('KNEE POINT');
        if (idealPoint.C === r.C) notes.push('IDEAL DIST');

        console.log(`${r.C.toString().padStart(3)}| ${r.meccaAcc.toFixed(2)}%    | ${r.kbImp.toFixed(2)}%    | ${notes.join(', ')}`);
    });

    console.log(`\n${'='.repeat(70)}`);
    console.log(`OPTIMAL RECOMMENDATIONS`);
    console.log(`${'='.repeat(70)}`);

    console.log(`1. Knee Point (Best Trade-off):    C=${kneePoint.C} (Mecca Acc=${kneePoint.meccaAcc.toFixed(2)}%, KB Imp=${kneePoint.kbImp.toFixed(2)}%)`);
    console.log(`2. Ideal Distance (Closest to 100%/0%): C=${idealPoint.C} (Mecca Acc=${idealPoint.meccaAcc.toFixed(2)}%, KB Imp=${idealPoint.kbImp.toFixed(2)}%)`);

    // Additional suggestion: Min KB Imp < 1% with Max Mecca Acc
    const feasible = results.filter(r => r.kbImp < 1.0).sort((a,b) => b.meccaAcc - a.meccaAcc);
    if (feasible.length > 0) {
        console.log(`3. Low Impossibility (<1%):        C=${feasible[0].C} (Mecca Acc=${feasible[0].meccaAcc.toFixed(2)}%, KB Imp=${feasible[0].kbImp.toFixed(2)}%)`);
    }

    console.log(`\n${'='.repeat(70)}`);
}

main();
