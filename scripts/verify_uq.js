const Astronomy = require('astronomy-engine');

const locations = [
    { name: 'Dakar', lat: 14.7167, lon: -17.4677 },
    { name: 'Mecca', lat: 21.4225, lon: 39.8262 },
    { name: 'Aceh', lat: 5.5483, lon: 95.3238 }
];

const monthsToCheck = [9, 10, 12]; // Ramadan, Shawwal, Dhu al-Hijjah
const startYear = 1000;
const endYear = 2000;

// Tabular Logic
function calculateTabularDate(hYear, hMonth, C) {
    const epoch = 1948439.5;

    const year = hYear - 1;
    const cycle = Math.floor(year / 30);
    const yearInCycle = year % 30;
    const dayInCycle = yearInCycle * 354 + Math.floor((11 * yearInCycle + C) / 30);
    const dayInYear = Math.ceil(29.5 * (hMonth - 1));

    const hDay = 1;
    const jd = epoch + cycle * 10631 + dayInCycle + dayInYear + hDay - 1;

    return Math.floor(jd + 0.5);
}

// UQ Criteria Logic
function checkUmmAlQura(jdOfConjunction, lat, lon) {
    const ut = jdOfConjunction - 2451545.0;
    const date = new Date("2000-01-01T12:00:00Z");
    date.setTime(date.getTime() + ut * 86400000);

    // Local Time of Conj
    const tz = lon / 15.0;
    const localDate = new Date(date.getTime() + tz * 3600 * 1000);

    // Normalize to Noon of that civil day
    const checkDate = new Date(localDate);
    checkDate.setUTCHours(12, 0, 0, 0);
    checkDate.setUTCMinutes(0);

    const observer = new Astronomy.Observer(lat, lon, 0);

    for (let i = 0; i < 3; i++) {
        // Calculate Sunset
        const searchTime = Astronomy.MakeTime(checkDate).ut;
        const sunset = Astronomy.SearchRiseSet(Astronomy.Body.Sun, observer, -1, searchTime, 1);

        if (!sunset) { checkDate.setDate(checkDate.getDate()+1); continue; }

        const sunsetUt = sunset.ut;
        const sunsetJd = sunsetUt + 2451545.0;

        // Check 1: Conjunction < Sunset
        if (jdOfConjunction > sunsetJd) {
            checkDate.setDate(checkDate.getDate() + 1);
            continue;
        }

        // Check 2: Moonset > Sunset
        // Check Altitude of Moon at Sunset.
        const moonEq = Astronomy.Equator(Astronomy.Body.Moon, sunsetUt, observer, true, true);
        const moonHor = Astronomy.Horizon(sunsetUt, observer, moonEq.ra, moonEq.dec, 'normal');

        if (moonHor.altitude > 0) {
            // Month starts NEXT day.
            const resultDate = new Date(checkDate);
            resultDate.setDate(resultDate.getDate() + 1);
            // Return JD of Result Date (Noon)
            const resTime = Astronomy.MakeTime(resultDate);
            return Math.floor(resTime.ut + 2451545.0);
        } else {
             checkDate.setDate(checkDate.getDate() + 1);
        }
    }
    return 0;
}

function getHijriMonthStartUQ(hYear, hMonth, lat, lon) {
    // Use Tabular date (C=0) as initial guess.
    const guessJD = calculateTabularDate(hYear, hMonth, 0);
    const guessUT = guessJD - 2451545.0;

    // Start search 5 days before guessJD.
    const searchStartUT = guessUT - 5;
    const conjunction = Astronomy.SearchMoonPhase(0, searchStartUT, 10);

    if (!conjunction) {
         console.error(`Conjunction not found for ${hYear}-${hMonth}`);
         return 0;
    }

    const jdConj = conjunction.ut + 2451545.0;

    if (jdConj > guessJD + 3) {
        const earlier = Astronomy.SearchMoonPhase(0, guessUT - 20, 15);
         if (earlier) {
             const jdEarlier = earlier.ut + 2451545.0;
             return checkUmmAlQura(jdEarlier, lat, lon);
         }
    }

    return checkUmmAlQura(jdConj, lat, lon);
}


// Main Execution
async function run() {
    console.log('Running Umm Al-Qura Verification...');

    const stats = {};
    locations.forEach(loc => {
        stats[loc.name] = { total: 0 };
        for(let c = -15; c <= 25; c++) {
            stats[loc.name][c] = 0;
        }
    });

    for (let year = startYear; year <= endYear; year++) {
        for (let month of monthsToCheck) {
            for (let loc of locations) {
                const trueJD = getHijriMonthStartUQ(year, month, loc.lat, loc.lon);

                // Track Best C
                for (let c = -15; c <= 25; c++) {
                    const tabJD = calculateTabularDate(year, month, c);
                    const diff = tabJD - trueJD;

                    if (diff === 0) {
                        stats[loc.name][c]++;
                    }
                }
            }
        }
        if (year % 100 === 0) console.log(`Processed ${year}...`);
    }

    console.log('\n--- Results ---');
    console.log('Location, Best C (Max Matches), Accuracy %, Current Formula Accuracy %, Proposed Formula Accuracy %');

    const totalEvents = (endYear - startYear + 1) * monthsToCheck.length;

    locations.forEach(loc => {
        let maxMatches = 0;
        let bestC = -999;

        for (let c = -15; c <= 25; c++) {
            if (stats[loc.name][c] > maxMatches) {
                maxMatches = stats[loc.name][c];
                bestC = c;
            }
        }

        const currentC = Math.round(loc.lon / 12.0 + 7.5);
        const currentMatches = stats[loc.name][currentC] || 0;

        const proposedC = Math.round(-0.12 * Math.abs(loc.lon - 39.8262));
        const proposedMatches = stats[loc.name][proposedC] || 0;

        console.log(`${loc.name}, Best:${bestC}, Acc:${(maxMatches/totalEvents*100).toFixed(2)}%, Current(C=${currentC}):${(currentMatches/totalEvents*100).toFixed(2)}%, Proposed(C=${proposedC}):${(proposedMatches/totalEvents*100).toFixed(2)}%`);
    });
}

run();
