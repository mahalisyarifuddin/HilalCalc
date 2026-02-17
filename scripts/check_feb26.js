// Formula logic
const X = 29.5306828885;
const EPOCH = 2444199;

function getStartJD(index) {
    return Math.floor(X * index + EPOCH);
}

function getIndexFromJD(jd) {
    let index = Math.round((jd - EPOCH) / X);
    let jdStart = Math.floor(X * index + EPOCH);
    if (jd < jdStart) index--;
    return index;
}

function jdToGregorian(jd) {
    let z = Math.floor(jd + 0.5);
    let alpha = Math.floor((z - 1867216.25) / 36524.25);
    let a = z + 1 + alpha - Math.floor(alpha / 4);
    let b = a + 1524;
    let c = Math.floor((b - 122.1) / 365.25);
    let d = Math.floor(365.25 * c);
    let e = Math.floor((b - d) / 30.6001);
    let day = b - d - Math.floor(30.6001 * e) + (jd + 0.5 - z);
    let month = e - 1;
    if (month > 12) month -= 12;
    let year = c - 4715;
    if (e < 14) month = e - 1; else month = e - 13;
    if (month > 2) year = c - 4716; else year = c - 4715;
    return new Date(Date.UTC(year, month - 1, Math.floor(day)));
}

function gregorianToJD(year, month, day) {
    let m = month + 1;
    let y = year;
    if (m < 3) { y -= 1; m += 12; }
    let a = Math.floor(y / 100);
    let b = 2 - a + Math.floor(a / 4);
    if (y < 1583) b = 0;
    return Math.floor(365.25 * (y + 4716)) + Math.floor(30.6001 * (m + 1)) + day + b - 1524;
}

const months = ["Muharram", "Safar", "Rabi' I", "Rabi' II", "Jumada I", "Jumada II", "Rajab", "Sha'ban", "Ramadan", "Shawwal", "Dhu al-Q", "Dhu al-H"];

console.log("Checking Feb 2026...");
const startFeb = gregorianToJD(2026, 1, 1); // Feb 1
const endFeb = gregorianToJD(2026, 1, 28); // Feb 28

const idxStart = getIndexFromJD(startFeb);
const idxEnd = getIndexFromJD(endFeb);

function printHijri(jd) {
    const idx = getIndexFromJD(jd);
    const hYear = Math.floor(idx / 12) + 1400;
    const hMonth = idx % 12;
    const start = getStartJD(idx);
    const day = jd - start + 1;
    console.log(`JD ${jd}: ${day} ${months[hMonth]} ${hYear}`);
}

printHijri(startFeb);
printHijri(endFeb);

// Check Ramadan 1447 Start
const idxRamadan1447 = (1447 - 1400) * 12 + 8; // 8 = Ramadan (0-based)
const startRamadanJD = getStartJD(idxRamadan1447);
const startRamadanG = jdToGregorian(startRamadanJD);
console.log(`Ramadan 1447 starts on: ${startRamadanG.toISOString().split('T')[0]}`);
