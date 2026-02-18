const getLinearMonthStartJD = (index) => Math.floor(29.5306828885 * index + 2444199);

let globalMinUpper = Infinity;
let globalMaxLower = -Infinity;

for (let index = 0; index < 6000; index++) {
    const startJD = getLinearMonthStartJD(index);
    const nextStartJD = getLinearMonthStartJD(index + 1);

    // For every JD in this month:
    for (let jd = startJD; jd < nextStartJD; jd++) {
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
    console.log(`Found valid K! Example: ${(globalMaxLower + globalMinUpper) / 2}`);
} else {
    console.log("No single K works for all months.");
}
