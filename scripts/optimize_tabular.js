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

// Simple Pareto Dominance Check
// A solution S1 dominates S2 if:
// S1.Accuracy >= S2.Accuracy AND S1.Impossible <= S2.Impossible AND (S1.Accuracy > S2.Accuracy OR S1.Impossible < S2.Impossible)
function findParetoFrontier(candidates) {
    // Candidates structure: { C, accuracy, impossible }
    // Sort by Impossible ASC (primary) then Accuracy DESC (secondary)
    // Actually, for Pareto, sorting helps.
    // Let's iterate and keep only non-dominated solutions.

    let frontier = [];

    for (const candidate of candidates) {
        let isDominated = false;
        for (const other of candidates) {
            if (candidate === other) continue;
            // Does 'other' dominate 'candidate'?
            // Higher Accuracy is better, Lower Impossible is better.
            if (other.accuracy >= candidate.accuracy && other.impossible <= candidate.impossible) {
                if (other.accuracy > candidate.accuracy || other.impossible < candidate.impossible) {
                    isDominated = true;
                    break;
                }
            }
        }
        if (!isDominated) {
            frontier.push(candidate);
        }
    }

    // Sort frontier for readability: High Accuracy first
    return frontier.sort((a, b) => b.accuracy - a.accuracy);
}

// Or select the best "knee point" or weighted sum.
// Let's define "Best" as maximizing: Accuracy - 2 * Impossible
// This puts a heavy penalty on impossible sightings.
function findWeightedBest(candidates) {
    return candidates.reduce((best, current) => {
        const score = current.accuracy - (2 * current.impossible);
        const bestScore = best ? best.accuracy - (2 * best.impossible) : -Infinity;
        return score > bestScore ? current : best;
    }, null);
}


async function main() {
    console.log(`Analyzing years ${startYear}-${endYear} AH`);
    console.log('Finding Pareto-optimal C values (Accuracy vs Impossible Rate)');
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

        let candidatesAll = [];
        let candidatesOblig = [];

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

            candidatesAll.push({ C, accuracy: accAll, impossible: impAll, context: 'All' });
            candidatesOblig.push({ C, accuracy: accOblig, impossible: impOblig, context: 'Oblig' });
        }

        const frontierAll = findParetoFrontier(candidatesAll);
        const frontierOblig = findParetoFrontier(candidatesOblig);

        const bestAll = findWeightedBest(candidatesAll);
        const bestOblig = findWeightedBest(candidatesOblig);

        console.log("Pareto Frontier (All Months):");
        frontierAll.forEach(c => console.log(`  C=${c.C}: Acc=${c.accuracy.toFixed(2)}%, Imp=${c.impossible.toFixed(2)}%`));
        console.log(`Selected Best (All): C=${bestAll.C} (Acc=${bestAll.accuracy.toFixed(2)}%, Imp=${bestAll.impossible.toFixed(2)}%)`);

        console.log("Pareto Frontier (Obligatory):");
        frontierOblig.forEach(c => console.log(`  C=${c.C}: Acc=${c.accuracy.toFixed(2)}%, Imp=${c.impossible.toFixed(2)}%`));
        console.log(`Selected Best (Oblig): C=${bestOblig.C} (Acc=${bestOblig.accuracy.toFixed(2)}%, Imp=${bestOblig.impossible.toFixed(2)}%)`);

        // Let's also output the full stats for the selected bests to match previous report format
        // Find the full candidate object from the original list (though findWeightedBest returns it)
        // Wait, we need cross-stats for the report table (Oblig stats for All-Optimized C, etc)

        // Helper to find stats
        const getStats = (cVal) => {
            const all = candidatesAll.find(x => x.C === cVal);
            const oblig = candidatesOblig.find(x => x.C === cVal);
            return {
                C: cVal,
                accAll: all.accuracy,
                impAll: all.impossible,
                accOblig: oblig.accuracy,
                impOblig: oblig.impossible
            };
        }

        const statsAll = getStats(bestAll.C);
        const statsOblig = getStats(bestOblig.C);

        console.log(`Report Data for ${loc.name}:`);
        console.log(`Phase 1 (Oblig Best C=${statsOblig.C}): AccOblig=${statsOblig.accOblig.toFixed(2)}%, AccAll=${statsOblig.accAll.toFixed(2)}%, ImpOblig=${statsOblig.impOblig.toFixed(2)}%, ImpAll=${statsOblig.impAll.toFixed(2)}%`);
        console.log(`Phase 2 (All Best C=${statsAll.C}): AccOblig=${statsAll.accOblig.toFixed(2)}%, AccAll=${statsAll.accAll.toFixed(2)}%, ImpOblig=${statsAll.impOblig.toFixed(2)}%, ImpAll=${statsAll.impAll.toFixed(2)}%`);

        console.log('---');
    }
}

main();
