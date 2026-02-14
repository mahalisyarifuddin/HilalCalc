const Astronomy = require('astronomy-engine');

const locations = [
    { name: 'Dakar', lat: 14.7167, lon: -17.4677 },
    { name: 'Mecca', lat: 21.3891, lon: 39.8579 },
    { name: 'Banda Aceh', lat: 6.075, lon: 95.1125 }
];

const months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]; // All months
const startYear = 1000;
const endYear = 2000;

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

    // MABBIMS Criteria: Alt >= 3.0 and Elongation >= 6.4
    // Note: Some definitions include Age >= 8 hours, but standard MABBIMS focuses on Alt/Elong.
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
    const daysSinceAnchor = ((hYear - 1445) * 354.367) + ((hMonth - 1) * 29.53);
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

// ============================================================================
// ENHANCED PARETO FRONTIER ANALYSIS
// ============================================================================

/**
 * Find Pareto frontier using efficient algorithm
 * A solution dominates another if it's better in at least one objective
 * and not worse in any objective.
 * 
 * Objectives: Maximize Accuracy, Minimize Impossible Rate
 * 
 * @param {Array} candidates - Array of {C, accuracy, impossible}
 * @returns {Array} Pareto frontier solutions
 */
function findParetoFrontier(candidates) {
    // More efficient O(n log n) algorithm: sort by one objective first
    const sorted = [...candidates].sort((a, b) => b.accuracy - a.accuracy);
    let frontier = [];
    let minImpossible = Infinity;

    for (const candidate of sorted) {
        // Since sorted by accuracy (descending), we only need to check if impossible is lower
        if (candidate.impossible < minImpossible) {
            frontier.push(candidate);
            minImpossible = candidate.impossible;
        } else if (candidate.impossible === minImpossible && frontier.length > 0) {
            // Handle ties - keep both if same impossible rate but different accuracy
            if (candidate.accuracy > frontier[frontier.length - 1].accuracy) {
                frontier[frontier.length - 1] = candidate;
            }
        }
    }

    return frontier;
}

/**
 * Calculate Euclidean distance to ideal point (100% accuracy, 0% impossible)
 */
function distanceToIdeal(candidate) {
    const accuracyGap = 100 - candidate.accuracy;
    const impossibleGap = candidate.impossible - 0;
    return Math.sqrt(accuracyGap ** 2 + impossibleGap ** 2);
}

/**
 * Find knee point using maximum curvature method
 * The knee represents the best trade-off where we get diminishing returns
 * 
 * Uses Menger curvature to find the point with maximum bend in the Pareto curve
 */
function findKneePoint(frontier) {
    if (frontier.length <= 2) return frontier[0];

    // Normalize to [0,1] range for fair comparison
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

    // Calculate curvature for each point (except endpoints)
    for (let i = 1; i < frontier.length - 1; i++) {
        const prev = normalize(frontier[i - 1]);
        const curr = normalize(frontier[i]);
        const next = normalize(frontier[i + 1]);

        // Menger curvature: curvature of circle through 3 points
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

    // If no clear knee found (flat frontier), use distance to ideal
    if (maxCurvature === 0 || !isFinite(maxCurvature)) {
        kneeIndex = frontier.reduce((bestIdx, curr, idx, arr) => 
            distanceToIdeal(curr) < distanceToIdeal(arr[bestIdx]) ? idx : bestIdx, 0);
    }

    return frontier[kneeIndex];
}

/**
 * Provide multiple selection strategies for choosing the best C value
 */
function selectBestSolutions(candidates) {
    const frontier = findParetoFrontier(candidates);
    
    return {
        frontier: frontier,
        
        // Strategy 1: Knee point (best trade-off based on curvature)
        kneePoint: findKneePoint(frontier),
        
        // Strategy 2: Closest to ideal point (100% acc, 0% imp)
        idealDistance: frontier.reduce((best, curr) => 
            distanceToIdeal(curr) < distanceToIdeal(best) ? curr : best, frontier[0]),
        
        // Strategy 3: Weighted sum (configurable weights)
        weighted: (accWeight = 1, impWeight = 2) => 
            candidates.reduce((best, curr) => {
                const score = accWeight * curr.accuracy - impWeight * curr.impossible;
                const bestScore = best ? accWeight * best.accuracy - impWeight * best.impossible : -Infinity;
                return score > bestScore ? curr : best;
            }, null),
        
        // Strategy 4: Lexicographic (prioritize impossible < threshold, then max accuracy)
        lexicographic: (maxImpossible = 5) => {
            const feasible = candidates.filter(c => c.impossible <= maxImpossible);
            if (feasible.length === 0) {
                // If no solution meets threshold, pick lowest impossible rate
                return candidates.reduce((a, b) => a.impossible < b.impossible ? a : b);
            }
            // Among feasible, pick highest accuracy
            return feasible.reduce((a, b) => a.accuracy > b.accuracy ? a : b);
        },
        
        // Strategy 5: Minimum impossible rate (most conservative)
        minImpossible: candidates.reduce((a, b) => a.impossible < b.impossible ? a : b)
    };
}

/**
 * Calculate detailed trade-off metrics for the Pareto frontier
 */
function analyzeFrontier(frontier) {
    const metrics = {
        count: frontier.length,
        accuracyRange: [
            Math.min(...frontier.map(f => f.accuracy)),
            Math.max(...frontier.map(f => f.accuracy))
        ],
        impossibleRange: [
            Math.min(...frontier.map(f => f.impossible)),
            Math.max(...frontier.map(f => f.impossible))
        ],
        tradeoffs: []
    };

    // Calculate marginal trade-off rates between adjacent points
    for (let i = 0; i < frontier.length - 1; i++) {
        const curr = frontier[i];
        const next = frontier[i + 1];
        const accChange = next.accuracy - curr.accuracy;
        const impChange = next.impossible - curr.impossible;
        
        if (Math.abs(impChange) > 0.001) {
            const tradeoffRate = accChange / impChange;
            metrics.tradeoffs.push({
                fromC: curr.C,
                toC: next.C,
                accuracyChange: accChange.toFixed(2),
                impossibleChange: impChange.toFixed(2),
                rate: tradeoffRate.toFixed(2) // % accuracy gained per % impossible added
            });
        }
    }

    return metrics;
}

/**
 * Enhanced output with multiple recommendation strategies
 */
function displayResults(locationName, candidates, unifiedC) {
    const solutions = selectBestSolutions(candidates);
    const metrics = analyzeFrontier(solutions.frontier);
    
    console.log(`\n${'='.repeat(70)}`);
    console.log(`LOCATION: ${locationName}`);
    console.log(`${'='.repeat(70)}\n`);
    
    // Pareto Frontier
    console.log(`📊 PARETO FRONTIER (${metrics.count} non-dominated solutions):`);
    console.log(`   Accuracy Range: ${metrics.accuracyRange[0].toFixed(2)}% - ${metrics.accuracyRange[1].toFixed(2)}%`);
    console.log(`   Impossible Range: ${metrics.impossibleRange[0].toFixed(2)}% - ${metrics.impossibleRange[1].toFixed(2)}%\n`);
    
    solutions.frontier.forEach((c, idx) => {
        const marker = c.C === solutions.kneePoint.C ? ' ← KNEE POINT' : 
                       c.C === solutions.idealDistance.C ? ' ← IDEAL DIST' : '';
        console.log(`   [${idx + 1}] C=${c.C.toString().padStart(3)}: Acc=${c.accuracy.toFixed(2)}%, Imp=${c.impossible.toFixed(2)}%${marker}`);
    });
    
    // Trade-off Analysis
    if (metrics.tradeoffs.length > 0) {
        console.log(`\n📈 TRADE-OFF ANALYSIS:`);
        console.log(`   (Moving along Pareto frontier)`);
        metrics.tradeoffs.forEach(t => {
            console.log(`   C ${t.fromC} → ${t.toC}: Acc ${t.accuracyChange}%, Imp ${t.impossibleChange}% (ratio: ${t.rate})`);
        });
    }
    
    // Recommendations
    console.log(`\n🎯 RECOMMENDED C VALUES (by strategy):`);
    console.log(`   1. Knee Point (best trade-off):    C=${solutions.kneePoint.C} (Acc=${solutions.kneePoint.accuracy.toFixed(2)}%, Imp=${solutions.kneePoint.impossible.toFixed(2)}%)`);
    console.log(`   2. Ideal Distance (closest to 100%/0%): C=${solutions.idealDistance.C} (Acc=${solutions.idealDistance.accuracy.toFixed(2)}%, Imp=${solutions.idealDistance.impossible.toFixed(2)}%)`);
    
    const weighted = solutions.weighted(1, 2);
    console.log(`   3. Weighted (1:2 ratio):           C=${weighted.C} (Acc=${weighted.accuracy.toFixed(2)}%, Imp=${weighted.impossible.toFixed(2)}%)`);
    
    const lex = solutions.lexicographic(5);
    console.log(`   4. Lexicographic (Imp≤5%, max Acc): C=${lex.C} (Acc=${lex.accuracy.toFixed(2)}%, Imp=${lex.impossible.toFixed(2)}%)`);
    
    const minImp = solutions.minImpossible;
    console.log(`   5. Min Impossible (conservative):  C=${minImp.C} (Acc=${minImp.accuracy.toFixed(2)}%, Imp=${minImp.impossible.toFixed(2)}%)`);
    
    // Unified Formula Comparison
    const unifiedStats = candidates.find(x => x.C === unifiedC);
    const onFrontier = solutions.frontier.some(f => f.C === unifiedC);
    console.log(`\n🔍 UNIFIED FORMULA COMPARISON:`);
    console.log(`   Predicted C=${unifiedC}: Acc=${unifiedStats.accuracy.toFixed(2)}%, Imp=${unifiedStats.impossible.toFixed(2)}%`);
    console.log(`   Status: ${onFrontier ? '✓ ON Pareto frontier (optimal!)' : '✗ NOT on Pareto frontier (dominated)'}`);
    
    if (!onFrontier) {
        // Find dominating solutions
        const dominators = solutions.frontier.filter(f => 
            f.accuracy >= unifiedStats.accuracy && f.impossible <= unifiedStats.impossible &&
            (f.accuracy > unifiedStats.accuracy || f.impossible < unifiedStats.impossible)
        );
        if (dominators.length > 0) {
            console.log(`   Dominated by: ${dominators.map(d => `C=${d.C}`).join(', ')}`);
        }
    }
}


async function main() {
    console.log(`\n${'='.repeat(70)}`);
    console.log(`TABULAR HIJRI CALENDAR OPTIMIZATION`);
    console.log(`Analyzing years ${startYear}-${endYear} AH (${endYear - startYear + 1} years, ${(endYear - startYear + 1) * 12} months)`);
    console.log(`Enhanced Pareto Frontier Analysis with Multiple Selection Strategies`);
    console.log(`${'='.repeat(70)}`);

    for (const loc of locations) {
        console.log(`\n⏳ Processing ${loc.name} (${loc.lat}°, ${loc.lon}°)...`);

        let groundTruths = [];

        // Calculate Ground Truths for ALL months
        for (let y = startYear; y <= endYear; y++) {
            for (const m of months) {
                const gt = getHijriMonthStart(y, m, loc.lat, loc.lon);
                groundTruths.push({ y, m, gt });
            }
        }

        let candidates = [];

        for (let C = -15; C <= 30; C++) {
            let matches = 0;
            let total = 0;
            let impossible = 0;

            for (const item of groundTruths) {
                const tabDate = hijriToGregorianTabular(item.y, item.m, 1, C);
                const tabStr = formatDate(tabDate);

                // Check if Moon was below horizon on the eve of tabDate
                const altitude = getMoonAltitudeAtSunsetOfEve(tabDate, loc.lat, loc.lon);
                // Impossible if Altitude < 0 degrees
                const isImpossible = (altitude < 0);

                total++;
                if (tabStr === item.gt) matches++;
                if (isImpossible) impossible++;
            }
            
            const acc = (matches / total) * 100;
            const imp = (impossible / total) * 100;

            candidates.push({ C, accuracy: acc, impossible: imp });
        }

        // Calculate unified C prediction
        const unifiedC = Math.round(loc.lon / 14.0 + 11.2);
        
        // Display comprehensive results
        displayResults(loc.name, candidates, unifiedC);
    }
    
    console.log(`\n${'='.repeat(70)}`);
    console.log(`ANALYSIS COMPLETE`);
    console.log(`${'='.repeat(70)}\n`);
}

main();
