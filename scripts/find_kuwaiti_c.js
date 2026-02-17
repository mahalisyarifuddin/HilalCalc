// Kuwaiti Algorithm Leap Year Pattern (Type II)
// Source: Microsoft HijriCalendar
// Leap years in 30-year cycle: 2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29

const typeII_leaps = [2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29];

// Type III (Standard): 2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29 ? Wait.
// Standard (I) often: 2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29
// Type II is Microsoft/Kuwaiti: 2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29.
// Type III (Mecca 1?): 2, 5, 8, 10, 13, 16, 19, 21, 24, 27, 29.
// Type IV (Mecca 2?): 2, 5, 8, 11, 13, 16, 19, 21, 24, 27, 30.

// Let's check common patterns.
const leaps = {
    "Type I (Standard)": [2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29],
    "Type II (Kuwaiti)": [2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29], // Wait, Type I and II are identical?
    "Type III (Fatimid)": [2, 5, 8, 10, 13, 16, 19, 21, 24, 27, 29],
    "Type IV (Habash)": [2, 5, 8, 11, 13, 16, 19, 21, 24, 27, 30]
};
// Actually, I'll search for C values that produce these leap years.

function getLeapYears(C) {
    let cycleLeaps = [];
    for (let year = 1; year <= 30; year++) {
        // yearInCycle (0-based) for calculation: year-1
        // days = floor((11 * (year-1) + C) / 30)
        // Leap if days(year) > days(year-1) + 354
        // Formula used in my code: dayInCycle = yearInCycle * 354 + floor((11 * yearInCycle + C) / 30)

        let yCurrent = year - 1;
        let daysCurrent = Math.floor((11 * yCurrent + C) / 30);

        let yNext = year; // actually next year start
        // Leap year adds 1 day to the year length.
        // Length of year Y = dayInCycle(Y+1) - dayInCycle(Y)
        // Length = 354 + floor((11*Y + C)/30) - floor((11*(Y-1) + C)/30)
        // If length == 355, it's a leap year.

        let len = 354 + Math.floor((11 * year + C) / 30) - Math.floor((11 * (year - 1) + C) / 30);
        if (len === 355) {
            cycleLeaps.push(year);
        }
    }
    return cycleLeaps;
}

function arraysEqual(a, b) {
    if (a.length !== b.length) return false;
    for (let i = 0; i < a.length; i++) {
        if (a[i] !== b[i]) return false;
    }
    return true;
}

console.log("Analyzing Tabular C values (-100 to 100) for Leap Year Patterns...\n");

for (let C = -100; C <= 100; C++) {
    const pattern = getLeapYears(C);

    // Check against known types
    for (const [name, target] of Object.entries(leaps)) {
        if (arraysEqual(pattern, target)) {
            console.log(`C = ${C}: Matches ${name}`);
        }
    }
}
