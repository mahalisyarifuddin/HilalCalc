/**
 * This script finds the optimal constant K for the linear Hijri formula inverse function:
 * Index = floor((JD - K) / 29.5306828885)
 *
 * We need K such that this inverse function matches the forward function:
 * StartJD = floor(29.5306828885 * Index + 2444199)
 * for all indices in a wide range (including negative ones).
 */

const getLinearMonthStartJD = (index) => Math.floor(29.5306828885 * index + 2444199);

let globalMinUpper = Infinity;
let globalMaxLower = -Infinity;

const startIdx = -17000; // Approx Year 1 AH
const endIdx = 6000;     // Approx Year 1900 AH

console.log(`Searching for K in range indices ${startIdx} to ${endIdx}...`);

for (let index = startIdx; index < endIdx; index++) {
    const startJD = getLinearMonthStartJD(index);
    const nextStartJD = getLinearMonthStartJD(index + 1);

    // For every JD in this month:
    for (let jd = startJD; jd < nextStartJD; jd++) {
        // Condition: floor((JD - K) / 29.53) == Index
        // Index <= (JD - K) / 29.53 < Index + 1

        // Upper bound on K: K <= JD - Index * 29.53
        const upper = jd - index * 29.5306828885;
        if (upper < globalMinUpper) globalMinUpper = upper;

        // Lower bound on K: K > JD - (Index + 1) * 29.53
        const lower = jd - (index + 1) * 29.5306828885;
        if (lower > globalMaxLower) globalMaxLower = lower;
    }
}

console.log(`Valid K range: (${globalMaxLower}, ${globalMinUpper}]`);

if (globalMaxLower < globalMinUpper) {
    const bestK = (globalMaxLower + globalMinUpper) / 2;
    console.log(`Found valid K! Example: ${bestK}`);
    console.log(`Current used constant: 2444198.00004`);
} else {
    console.error("No single K works for all months in this range.");
}
