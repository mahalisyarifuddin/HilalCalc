const locations = [
    { name: 'Mecca', lat: 21.354813, lon: 39.984063 }
];

// Standard Kuwaiti Leap Years (1-based)
const standardLeaps = [2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29];

function getLeapYears(C) {
    let leaps = [];
    for (let y = 1; y <= 30; y++) {
        const startY = (y-1) * 354 + Math.floor((11 * (y-1) + C) / 30);
        const startNextY = (y) * 354 + Math.floor((11 * y + C) / 30);
        const daysInY = startNextY - startY;
        if (daysInY === 355) leaps.push(y);
    }
    return leaps;
}

const leaps14 = getLeapYears(14);
const leaps15 = getLeapYears(15);

console.log("Standard Kuwaiti Leaps:", standardLeaps.join(', '));
console.log("C=14 Leaps:          ", leaps14.join(', '));
console.log("C=15 Leaps:          ", leaps15.join(', '));

const is14Standard = JSON.stringify(leaps14) === JSON.stringify(standardLeaps);
const is15Standard = JSON.stringify(leaps15) === JSON.stringify(standardLeaps);

console.log(`Is C=14 Vanilla? ${is14Standard}`);
console.log(`Is C=15 Vanilla? ${is15Standard}`);

console.log("\n--- Comparison ---");
console.log("C=14 (Vanilla): Higher Raw Accuracy (64.94%), Higher Impossible Rate (2.19%)");
console.log("C=15 (Modified): Lower Raw Accuracy (64.17%), Lower Impossible Rate (1.77%)");

if (is14Standard && !is15Standard) {
    console.log("\nConclusion: C=15 changes the leap year pattern. C=14 is the only Vanilla option.");
} else if (is14Standard && is15Standard) {
    console.log("\nConclusion: Both produce Vanilla leap years (unlikely).");
} else {
    console.log("\nConclusion: Neither or both differ.");
}
