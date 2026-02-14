const Astronomy = require('astronomy-engine');
const fs = require('fs');
const path = require('path');

const locations = {
    Mecca: { lat: 21.3891, lon: 39.8579 },
    Aceh: { lat: 6.075, lon: 95.1125 }
};

const startAH = 1000;
const endAH = 2000;

function hijriToGregorianTabular(hYear, hMonth, hDay) {
    // Standard tabular arithmetic (Kuwaiti algorithm or similar)
    // C=0 is fine for approximation
    const C = 0;
    const epoch = 1948439.5; // Standard epoch (July 15, 622)
    const year = hYear - 1;
    const cycle = Math.floor(year / 30);
    const yearInCycle = year % 30;
    const dayInCycle = yearInCycle * 354 + Math.floor((11 * yearInCycle + C) / 30);
    const dayInYear = Math.ceil(29.5 * (hMonth - 1)); // Month is 1-based, dayInYear adds days BEFORE current month
    // Wait, let's double check optimize_tabular.js:
    // dayInYear = Math.ceil(29.5 * hMonth); -> If hMonth is input, it seems to add full months?
    // In optimize_tabular.js:
    // const dayInYear = Math.ceil(29.5 * hMonth);
    // const jd = epoch + cycle * 10631 + dayInCycle + dayInYear + hDay - 1;
    // If hMonth=1, dayInYear=30? That seems wrong for the START of month 1.
    // optimize_tabular.js uses hMonth to calculate END of month?
    // Let's re-read carefully: "const dayInYear = Math.ceil(29.5 * hMonth);"
    // If hMonth=1, it adds 30 days.
    // Hijri month 1 (Muharram) starts at day 0 relative to year start.
    // So for hMonth=1, we want 0 days offset.
    // The previous code might have a bug or specific usage.
    // I will use a standard implementation:

    // Adjusted implementation for start of month M, day D
    const daysSinceEpoch = (cycle * 10631) +
                           (yearInCycle * 354 + Math.floor((11 * yearInCycle + 14) / 30)) + // using 14 as typical base
                           Math.ceil(29.5 * (hMonth - 1)) +
                           (hDay - 1);

    const jd = epoch + daysSinceEpoch;
    return Astronomy.MakeTime(jd - 2451545.0).date; // Returns Date object
}

function getAltitudeAtSunset(dateObj, lat, lon) {
    const observer = new Astronomy.Observer(lat, lon, 0);

    // Find sunset on this calendar day
    // Start search at noon to avoid finding yesterday's or tomorrow's if close to midnight
    // We assume sunset is roughly 18:00 local time.
    // dateObj is likely 00:00 UTC or Noon UTC.
    // Let's set search time to Noon Local Time.
    const utcOffsetHours = lon / 15.0;
    const noonLocal = new Date(dateObj);
    noonLocal.setUTCHours(12 - utcOffsetHours);

    const searchDate = Astronomy.MakeTime(noonLocal);
    const sunset = Astronomy.SearchRiseSet(Astronomy.Body.Sun, observer, -1, searchDate.ut, 1);

    if (!sunset) return -999; // Polar day/night? Unlikely at these latitudes.

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
    const outFile = path.join(__dirname, '..', 'altitude_difference_1000_2000.csv');
    const stream = fs.createWriteStream(outFile);
    stream.write('HijriYear,Month,ConjunctionUTC,AltMecca,AltAceh,Diff(Mecca-Aceh)\n');

    let count = 0;
    let sumDiff = 0;
    let minDiff = 999;
    let maxDiff = -999;
    let diffs = [];

    // Initialize search around 1000 AH
    // 1000 AH start approx:
    const startApprox = hijriToGregorianTabular(startAH, 1, 1);
    // Go back a few days to be safe and search for New Moon
    let time = Astronomy.MakeTime(startApprox);
    let nm = Astronomy.SearchMoonPhase(0, time.ut - 10, 30);

    // We need to track "Approx Hijri Month".
    // Since we are just simulating lunations, we can just count 12 per year.
    // We start at Month 1 of Year 1000.

    let currentHYear = startAH;
    let currentHMonth = 1; // 1 = Muharram

    while (currentHYear <= endAH) {
        if (!nm) break;

        // Loop condition is <= 2000. If we pass year 2000, stop.
        // Actually, we should just run until the end of year 2000.

        const conjunctionDate = nm.date;
        const conjunctionStr = formatDate(conjunctionDate);

        // Calculate Altitude at Sunset on the Day of Conjunction
        // "Day of Conjunction" is the Gregorian calendar day of the event (UTC based? or Local?)
        // Let's use UTC day as the standard "Day".
        const dayOfConjunction = new Date(conjunctionDate);
        dayOfConjunction.setUTCHours(12, 0, 0, 0); // Set to Noon UTC to represent the "Day"

        const altMecca = getAltitudeAtSunset(dayOfConjunction, locations.Mecca.lat, locations.Mecca.lon);
        const altAceh = getAltitudeAtSunset(dayOfConjunction, locations.Aceh.lat, locations.Aceh.lon);

        const diff = altMecca - altAceh;

        stream.write(`${currentHYear},${currentHMonth},${conjunctionStr},${altMecca.toFixed(4)},${altAceh.toFixed(4)},${diff.toFixed(4)}\n`);

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
    console.log(`Altitude Difference (Mecca - Aceh) Stats:`);
    console.log(`  Mean:   ${mean.toFixed(4)} degrees`);
    console.log(`  Median: ${median.toFixed(4)} degrees`);
    console.log(`  Min:    ${minDiff.toFixed(4)} degrees`);
    console.log(`  Max:    ${maxDiff.toFixed(4)} degrees`);
    console.log(`  95% CI: [${ciLower.toFixed(4)}, ${ciUpper.toFixed(4)}] degrees`);
    console.log(`Data written to ${outFile}`);
}

run();
