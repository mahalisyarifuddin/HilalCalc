// Verification script for Index Fix
const X = 29.5306828885;
const EPOCH = 2444199;

function getLinearMonthStartJD(index) {
    return Math.floor(X * index + EPOCH);
}

// Fixed logic: Index = (Year-1400)*12 + Month (0-based)
function getIndex(hYear, hMonth) {
    return (hYear - 1400) * 12 + hMonth;
}

// Current Buggy logic
function getIndexBuggy(hYear, hMonth) {
    return (hYear - 1400) * 12 + (hMonth - 1);
}

const hYear = 1400;
const hMonth = 0; // Muharram

console.log(`Checking Muharram 1400 (hMonth=0)...`);
const idxFixed = getIndex(hYear, hMonth);
const jdFixed = getLinearMonthStartJD(idxFixed);
console.log(`Fixed Index: ${idxFixed}, JD: ${jdFixed}`);

const idxBuggy = getIndexBuggy(hYear, hMonth);
const jdBuggy = getLinearMonthStartJD(idxBuggy);
console.log(`Buggy Index: ${idxBuggy}, JD: ${jdBuggy}`);

if (jdFixed === 2444199) {
    console.log("SUCCESS: Fixed logic returns Epoch 2444199.");
} else {
    console.log("FAILURE: Fixed logic is wrong.");
}
