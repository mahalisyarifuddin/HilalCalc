const Astronomy = require('astronomy-engine');
const fs = require('fs');
const path = require('path');

const locations = {
    Mecca: { lat: 21.354813, lon: 39.984063 },
    KB: { lat: 4.587063, lon: 114.075937 }
};

const startAH = 1000;
const endAH = 6000;

function hijriToGregorianTabular(hYear, hMonth, hDay) {
    // Standard tabular arithmetic (Kuwaiti algorithm C=14 for approximation)
    const C = 14;
    const epoch = 1948439.5; // Standard epoch (July 16, 622 AD, Julian)
    const year = hYear - 1;
    const cycle = Math.floor(year / 30);
    const yearInCycle = year % 30;

    // Days elapsed before the current year in the cycle
    const daysInCycle = yearInCycle * 354 + Math.floor((11 * yearInCycle + C) / 30);

    // Days elapsed in the current year before the current month
    const daysInYear = Math.ceil(29.5 * (hMonth - 1));

    // Total days since epoch
    const daysSinceEpoch = (cycle * 10631) + daysInCycle + daysInYear + (hDay - 1);

    const jd = epoch + daysSinceEpoch;
    return Astronomy.MakeTime(jd - 2451545.0).date; // Returns Date object
}

function getAltitudeAtSunset(dateObj, lat, lon) {
    const observer = new Astronomy.Observer(lat, lon, 0);

    // Find sunset on this calendar day
    // We assume sunset is roughly 18:00 local time.
    const utcOffsetHours = lon / 15.0;
    const noonLocal = new Date(dateObj);
    noonLocal.setUTCHours(12 - utcOffsetHours);

    const searchDate = Astronomy.MakeTime(noonLocal);
    const sunset = Astronomy.SearchRiseSet(Astronomy.Body.Sun, observer, -1, searchDate.ut, 1);

    if (!sunset) return -999;

    const sunsetUT = sunset.ut;
    const moonEq = Astronomy.Equator(Astronomy.Body.Moon, sunsetUT, observer, true, true);
    const moonHor = Astronomy.Horizon(sunsetUT, observer, moonEq.ra, moonEq.dec, "normal");

    return moonHor.altitude;
}

function formatDate(date) {
    return date.toISOString().slice(0, 19).replace('T', ' ');
}

async function run() {
    console.log(`Starting simulation from ${startAH} to ${endAH} AH...`);

    // Output file
    const outFile = path.join(__dirname, '..', 'altitude_difference_1000_6000.csv');
    const stream = fs.createWriteStream(outFile);
    stream.write('HijriYear,Month,ConjunctionUTC,AltMecca,AltKB,Diff(Mecca-KB)\n');

    let count = 0;
    let sumDiff = 0;
    let minDiff = 999;
    let maxDiff = -999;
    let diffs = [];

    // Initialize search around 1000 AH
    const startApprox = hijriToGregorianTabular(startAH, 1, 1);
    // Go back a few days to be safe and search for New Moon
    let time = Astronomy.MakeTime(startApprox);
    let nm = Astronomy.SearchMoonPhase(0, time.ut - 10, 30);

    let currentHYear = startAH;
    let currentHMonth = 1; // 1 = Muharram

    while (currentHYear <= endAH) {
        if (!nm) break;

        const conjunctionDate = nm.date;
        const conjunctionStr = formatDate(conjunctionDate);

        // Calculate Altitude at Sunset on the Day of Conjunction
        const dayOfConjunction = new Date(conjunctionDate);
        dayOfConjunction.setUTCHours(12, 0, 0, 0); // Set to Noon UTC to represent the "Day"

        const altMecca = getAltitudeAtSunset(dayOfConjunction, locations.Mecca.lat, locations.Mecca.lon);
        const altKB = getAltitudeAtSunset(dayOfConjunction, locations.KB.lat, locations.KB.lon);

        const diff = altMecca - altKB;

        stream.write(`${currentHYear},${currentHMonth},${conjunctionStr},${altMecca.toFixed(4)},${altKB.toFixed(4)},${diff.toFixed(4)}\n`);

        sumDiff += diff;
        if (diff < minDiff) minDiff = diff;
        if (diff > maxDiff) maxDiff = diff;
        diffs.push(diff);

        count++;

        // Advance Month
        currentHMonth++;
        if (currentHMonth > 12) {
            currentHMonth = 1;
            currentHYear++;
        }

        // Find next New Moon
        // Search starting 25 days after current NM
        nm = Astronomy.SearchMoonPhase(0, nm.ut + 25, 10);
    }

    stream.end();

    // Stats
    const mean = sumDiff / count;
    diffs.sort((a, b) => a - b);
    const median = diffs[Math.floor(diffs.length / 2)];

    // 95% Confidence Interval
    const idx2_5 = Math.floor(diffs.length * 0.025);
    const idx97_5 = Math.floor(diffs.length * 0.975);
    const ciLower = diffs[idx2_5];
    const ciUpper = diffs[idx97_5];

    console.log(`Simulation Complete.`);
    console.log(`Total Months: ${count}`);
    console.log(`Altitude Difference (Mecca - KB) Stats:`);
    console.log(`  Mean:   ${mean.toFixed(4)} degrees`);
    console.log(`  Median: ${median.toFixed(4)} degrees`);
    console.log(`  Min:    ${minDiff.toFixed(4)} degrees`);
    console.log(`  Max:    ${maxDiff.toFixed(4)} degrees`);
    console.log(`  95% CI: [${ciLower.toFixed(4)}, ${ciUpper.toFixed(4)}] degrees`);
    console.log(`Data written to ${outFile}`);
}

run();
