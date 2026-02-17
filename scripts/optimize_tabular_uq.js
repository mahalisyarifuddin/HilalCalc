const fs = require('fs');
const Astronomy = require('astronomy-engine');

const UQ_DATA_FILE = 'data/uq_dates.json';
const MECCA = { name: 'Mecca', lat: 21.354813, lon: 39.984063 };

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

    // Return a date object at noon to avoid boundary issues
    return new Date(Date.UTC(yearResult, monthResult - 1, Math.floor(day), 12, 0, 0));
}

function getTimezoneOffset(lon) {
    return Math.round(lon / 15);
}

function getMoonAltitudeAtSunsetOfEve(dateObj, lat, lon) {
    const key = `${dateObj.toISOString().split('T')[0]}-${lat}-${lon}`;
    if (altCache.has(key)) return altCache.get(key);

    const utcOffset = getTimezoneOffset(lon);
    // Observation is on the evening BEFORE the Tabular Date (which starts at Maghrib)
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

function formatDate(date) {
    return date.toISOString().split('T')[0];
}

// ============================================================================
// PARETO FRONTIER ANALYSIS
// ============================================================================

function findParetoFrontier(candidates) {
    // Sort by Accuracy (Descending)
    const sorted = [...candidates].sort((a, b) => b.accuracy - a.accuracy);
    let frontier = [];
    let minImpossible = Infinity;

    for (const candidate of sorted) {
        // Since sorted by accuracy (descending), we only need to check if impossible is lower
        if (candidate.impossible < minImpossible) {
            frontier.push(candidate);
            minImpossible = candidate.impossible;
        } else if (candidate.impossible === minImpossible && frontier.length > 0) {
            if (candidate.accuracy > frontier[frontier.length - 1].accuracy) {
                frontier[frontier.length - 1] = candidate;
            }
        }
    }

    return frontier;
}

function distanceToIdeal(candidate) {
    const accuracyGap = 100 - candidate.accuracy;
    const impossibleGap = candidate.impossible - 0;
    return Math.sqrt(accuracyGap ** 2 + impossibleGap ** 2);
}

function findKneePoint(frontier) {
    if (frontier.length <= 2) return frontier[0];

    const maxAcc = Math.max(...frontier.map(f => f.accuracy));
    const minAcc = Math.min(...frontier.map(f => f.accuracy));
    const maxImp = Math.max(...frontier.map(f => f.impossible));
    const minImp = Math.min(...frontier.map(f => f.impossible));

    const normalize = (f) => ({
        acc: maxAcc === minAcc ? 0.5 : (f.accuracy - minAcc) / (maxAcc - minAcc),
        imp: maxImp === minImp ? 0.5 : (f.impossible - minImp) / (maxImp - minImp)
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

function selectBestSolutions(candidates) {
    const frontier = findParetoFrontier(candidates);
    return {
        frontier: frontier,
        kneePoint: findKneePoint(frontier),
        idealDistance: frontier.reduce((best, curr) =>
            distanceToIdeal(curr) < distanceToIdeal(best) ? curr : best, frontier[0]),
        lexicographic: (maxImpossible = 5) => {
            const feasible = candidates.filter(c => c.impossible <= maxImpossible);
            if (feasible.length === 0) return candidates.reduce((a, b) => a.impossible < b.impossible ? a : b);
            return feasible.reduce((a, b) => a.accuracy > b.accuracy ? a : b);
        }
    };
}

async function main() {
    console.log(`\n${'='.repeat(70)}`);
    console.log(`OPTIMIZE TABULAR C FOR UMM AL-QURA (1343-1500 AH)`);
    console.log(`Comparing against official Umm al-Qura dates (from hijridate)`);
    console.log(`${'='.repeat(70)}\n`);

    if (!fs.existsSync(UQ_DATA_FILE)) {
        console.error(`Error: ${UQ_DATA_FILE} not found. Run generate_uq_data.py first.`);
        process.exit(1);
    }

    const groundTruths = JSON.parse(fs.readFileSync(UQ_DATA_FILE, 'utf8'));
    console.log(`Loaded ${groundTruths.length} Umm al-Qura month start dates.`);

    const candidates = [];

    console.log(`Evaluating C from -100 to 100...`);

    // Pre-calculate moon altitudes for all dates is expensive? No, we do it per C.
    // Actually, dates will be reused often across C?
    // Tabular dates shift by 1 day as C changes by ~30.
    // The cache handles re-requests for same date.

    for (let C = -100; C <= 100; C++) {
        let matches = 0;
        let total = 0;
        let impossible = 0;

        for (const item of groundTruths) {
            const tabDate = hijriToGregorianTabular(item.y, item.m, 1, C);
            const tabStr = formatDate(tabDate);

            // Accuracy Check
            if (tabStr === item.gt) matches++;
            total++;

            // Impossibility Check (Moon below horizon at sunset of eve)
            // Location: Mecca
            const altitude = getMoonAltitudeAtSunsetOfEve(tabDate, MECCA.lat, MECCA.lon);
            if (altitude < 0) impossible++;
        }

        const accuracy = (matches / total) * 100;
        const imp = (impossible / total) * 100;
        candidates.push({ C, accuracy, impossible: imp });
    }

    const solutions = selectBestSolutions(candidates);

    console.log(`\n${'='.repeat(70)}`);
    console.log(`RESULTS`);
    console.log(`${'='.repeat(70)}`);

    console.log(`Best Accuracy found: ${Math.max(...candidates.map(c => c.accuracy)).toFixed(2)}%`);
    console.log(`Lowest Impossible rate found: ${Math.min(...candidates.map(c => c.impossible)).toFixed(2)}%`);

    console.log(`\nPARETO FRONTIER:`);
    solutions.frontier.forEach(c => {
        let marker = '';
        if (c.C === solutions.kneePoint.C) marker += ' [KNEE POINT]';
        if (c.C === solutions.idealDistance.C) marker += ' [IDEAL DIST]';
        console.log(`C=${c.C.toString().padStart(3)}: Acc=${c.accuracy.toFixed(2)}%, Imp=${c.impossible.toFixed(2)}%${marker}`);
    });

    console.log(`\nRECOMMENDATIONS:`);
    console.log(`1. Knee Point: C=${solutions.kneePoint.C}`);
    console.log(`2. Ideal Distance: C=${solutions.idealDistance.C}`);

    const lex = solutions.lexicographic(1.0); // Allow 1% impossibility
    console.log(`3. Lexicographic (Imp<=1%, Max Acc): C=${lex.C} (Acc=${lex.accuracy.toFixed(2)}%, Imp=${lex.impossible.toFixed(2)}%)`);

    // Top 5 by Accuracy
    console.log(`\nTop 5 by Accuracy:`);
    candidates.sort((a, b) => b.accuracy - a.accuracy).slice(0, 5).forEach(c => {
        console.log(`C=${c.C}: Acc=${c.accuracy.toFixed(2)}%, Imp=${c.impossible.toFixed(2)}%`);
    });

    // Check C=48 (Mecca Knee Point from previous analysis)
    const c48 = candidates.find(c => c.C === 48);
    if (c48) {
        console.log(`\nCheck C=48 (Mecca Opt): Acc=${c48.accuracy.toFixed(2)}%, Imp=${c48.impossible.toFixed(2)}%`);
    }
}

main();
