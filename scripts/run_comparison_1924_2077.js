const fs = require('fs');
const runner = require('./tabular_experiment_runner');

// 1. Umm al-Qura Approximation Logic (requires ground truth file)
const UQ_DATA_FILE = 'data/uq_dates.json';
let uqGroundTruths = [];

if (fs.existsSync(UQ_DATA_FILE)) {
    uqGroundTruths = JSON.parse(fs.readFileSync(UQ_DATA_FILE, 'utf8'));
} else {
    console.error("UQ Data file not found!");
}

function calculateUQMetrics(cValue) {
    let matches = 0;
    let total = 0;
    let impossible = 0;

    // We use Mecca location for impossibility check
    const mecca = runner.LOCATIONS['Mecca'];

    // Tabular Logic (Duplicate from runner, but exposed)
    const hijriToGregorianTabular = (hYear, hMonth, hDay, C) => {
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
    };

    // Helper for moon altitude (uses runner's cached function logic? No, need to implement or import)
    // Actually runner doesn't export the helper. Let's rely on runner for visibility, but implement UQ check here.
    // For impossibility, we need moon altitude.

    // Wait, runner.js does not export `getMoonAltitudeAtSunsetOfEve`.
    // Let's modify runner to export it or just duplicate the simple check logic if needed.
    // Or, for simplicity in this script, we can skip impossibility for UQ metric if it's redundant with Mecca-C14 impossibility?
    // The previous UQ report included Impossibility.
    // Let's rely on the previous finding that Impossibility is high for C=1/C=-9.
    // Actually, let's just count matches for UQ.

    for (const item of uqGroundTruths) {
        // Filter range
        if (item.y < runner.START_YEAR_AH || item.y > runner.END_YEAR_AH) continue;

        const tabDate = hijriToGregorianTabular(item.y, item.m, 1, cValue);
        const tabStr = tabDate.toISOString().split('T')[0];

        if (tabStr === item.gt) matches++;
        total++;
    }

    return {
        accuracy: (matches / total) * 100,
        total: total
    };
}

async function runAll() {
    console.log(`\n======================================================================`);
    console.log(`COMPREHENSIVE TABULAR HIJRI COMPARISON (1343-1500 AH / 1924-2077 CE)`);
    console.log(`======================================================================\n`);

    const algorithms = [
        { name: 'Umm al-Qura Approx', C: 1 },
        { name: 'Kuwaiti (Standard)', C: 14 },
        { name: 'Mecca Visibility', C: 48 },
    ];

    const scenarios = [
        { loc: 'Dakar', name: 'Dakar Visibility' },
        { loc: 'Mecca', name: 'Mecca Visibility' },
        { loc: 'Kuala Belait', name: 'KB Visibility' }
    ];

    // 1. UQ Ground Truth Comparison
    console.log(`MATCHING OFFICIAL UMM AL-QURA CALENDAR (1343-1500 AH)`);
    console.log(`-----------------------------------------------------`);
    for (const algo of algorithms) {
        const res = calculateUQMetrics(algo.C);
        console.log(`${algo.name.padEnd(20)} (C=${algo.C}): Accuracy = ${res.accuracy.toFixed(2)}%`);
    }
    console.log(`\n`);

    // 2. Visibility Scenarios
    console.log(`MATCHING ASTRONOMICAL VISIBILITY (MABBIMS) - 1343-1500 AH`);
    console.log(`---------------------------------------------------------`);

    // Header
    console.log(`| Location       | Algorithm            | C  | Accuracy | Impossibility |`);
    console.log(`|----------------|----------------------|----|----------|---------------|`);

    for (const scenario of scenarios) {
        for (const algo of algorithms) {
            // Need to handle async properly if runner uses async (it currently does not use await internally but marked async)
            // wait, runner uses Astronomy engine which is synchronous.
            // But verify_uq.js used async?
            // runner.calculateMetrics is async? Not really, but I marked it async.

            // Wait, calculateMetrics in runner.js calls getHijriMonthStart which calls getMoonAltitude...
            // It's all synchronous in my implementation.

            const res = await runner.calculateMetrics(algo.C, scenario.loc, false); // All months

            console.log(`| ${scenario.name.padEnd(14)} | ${algo.name.padEnd(20)} | ${algo.C.toString().padStart(2)} | ${res.accuracy.toFixed(2)}%   | ${res.impossible.toFixed(2)}%        |`);
        }
        console.log(`|----------------|----------------------|----|----------|---------------|`);
    }

    console.log(`\nDone.`);
}

runAll();
