const Astronomy = require('./node_modules/astronomy-engine/astronomy.js');
const { performance } = require('perf_hooks');

const width = 1200;
const height = 500;
const bounds = {
    minLat: -60,
    maxLat: 60,
    minLon: -180,
    maxLon: 180
};
const date = Astronomy.MakeTime(new Date('2023-01-01T12:00:00Z'));
const PPD = width / (bounds.maxLon - bounds.minLon);

const minAlt = 0;
const minElong = 6.4;
const isGIC = false;

const observer = new Astronomy.Observer(0, 0, 0);

function checkVisibilityBaseline(observer, sunsetUT, minAlt, minElong, isGIC, baseDateUT) {
    if (isGIC && sunsetUT >= (baseDateUT + 0.5)) return false;

    const moonEq = Astronomy.Equator(Astronomy.Body.Moon, sunsetUT, observer, true, true);
    const moonHor = Astronomy.Horizon(sunsetUT, observer, moonEq.ra, moonEq.dec, 'normal');
    if (moonHor.altitude < minAlt) return false;

    const elong = Astronomy.AngleFromSun(Astronomy.Body.Moon, sunsetUT);
    return (elong >= minElong);
}

function runBaseline() {
    let currentY = -1;
    let sunsetBase = null;
    const subset = 2000; // Rows
    const start = performance.now();

    // Process a few rows fully
    for (let y = 0; y < 20; y++) {
        const lat = bounds.maxLat - (y / PPD);
        observer.latitude = lat;
        observer.longitude = 0;
        const sunset = Astronomy.SearchRiseSet(Astronomy.Body.Sun, observer, 1, date.ut, 1);
        sunsetBase = sunset ? sunset.ut : null;

        if (sunsetBase !== null) {
            for (let x = 0; x < width; x++) {
                const lon = bounds.minLon + (x / PPD);
                observer.longitude = lon;
                const sunsetUT = sunsetBase - (lon / 360.0);
                checkVisibilityBaseline(observer, sunsetUT, minAlt, minElong, isGIC, date.ut);
            }
        }
    }
    return performance.now() - start;
}

function runInterpolated() {
    let currentY = -1;
    let sunsetBase = null;
    const start = performance.now();

    const INTERP_STEP = 10;

    for (let y = 0; y < 20; y++) {
        const lat = bounds.maxLat - (y / PPD);
        observer.latitude = lat;
        observer.longitude = 0;
        const sunset = Astronomy.SearchRiseSet(Astronomy.Body.Sun, observer, 1, date.ut, 1);
        sunsetBase = sunset ? sunset.ut : null;

        if (sunsetBase !== null) {

            // Pre-vars
            let nextRA, nextDec, nextUT, nextLon;
            let prevRA, prevDec, prevUT, prevLon;

            // We need to prime the interpolation
            // But doing it inside the loop is easier logic-wise if we handle boundaries

            for (let x = 0; x < width; x++) {
                const lon = bounds.minLon + (x / PPD);
                const sunsetUT = sunsetBase - (lon / 360.0);

                // Interpolation logic
                if (x % INTERP_STEP === 0) {
                     // Calculate exact
                     observer.longitude = lon;
                     const moonEq = Astronomy.Equator(Astronomy.Body.Moon, sunsetUT, observer, true, true);
                     prevRA = moonEq.ra;
                     prevDec = moonEq.dec;

                     // Calculate next target for interpolation
                     // We need the value at x + step
                     let nextX = x + INTERP_STEP;
                     if (nextX >= width) nextX = width - 1; // Clamp to end

                     // Optimization: if nextX == x (end of row), we don't need to interpolate
                     if (nextX > x) {
                         const nextLonVal = bounds.minLon + (nextX / PPD);
                         const nextSunsetUT = sunsetBase - (nextLonVal / 360.0);
                         observer.longitude = nextLonVal;
                         const nextMoonEq = Astronomy.Equator(Astronomy.Body.Moon, nextSunsetUT, observer, true, true);
                         nextRA = nextMoonEq.ra;
                         nextDec = nextMoonEq.dec;

                         // Handle RA wrap around 24h (360 degrees?)
                         // Astronomy Engine uses hours for RA? Check docs or return value.
                         // Docs say: ra is number. Usually hours [0, 24).
                         // Let's verify.
                         // If wrapping occurs, interpolation fails.
                         // Moon moves slowly, so wrap only happens once per day.
                         if (Math.abs(nextRA - prevRA) > 12) {
                             if (nextRA > prevRA) prevRA += 24;
                             else nextRA += 24;
                         }
                     }

                     // Use exact for this pixel
                     observer.longitude = lon;
                     const moonHor = Astronomy.Horizon(sunsetUT, observer, moonEq.ra, moonEq.dec, 'normal');
                     if (moonHor.altitude >= minAlt) {
                         Astronomy.AngleFromSun(Astronomy.Body.Moon, sunsetUT); // calculate elong
                     }

                } else {
                    // Interpolate
                    const fraction = (x % INTERP_STEP) / INTERP_STEP; // This is approximate if step is not uniform but here it is
                    // Actually we need to interpolate between prev and next
                    // Since x goes x...nextX
                    // Wait, logic above calculated next at x+step.
                    // So for current x (which is x_start + k), fraction is k/step.

                    let currRA = prevRA + (nextRA - prevRA) * fraction;
                    let currDec = prevDec + (nextDec - prevDec) * fraction;

                    if (currRA >= 24) currRA -= 24; // unwrap

                    observer.longitude = lon;
                    const moonHor = Astronomy.Horizon(sunsetUT, observer, currRA, currDec, 'normal');
                     if (moonHor.altitude >= minAlt) {
                         Astronomy.AngleFromSun(Astronomy.Body.Moon, sunsetUT);
                     }
                }
            }
        }
    }
    return performance.now() - start;
}

console.log("Warming up...");
runBaseline();
runInterpolated();

console.log("Running Baseline...");
const t1 = runBaseline();
console.log("Baseline:", t1.toFixed(2), "ms");

console.log("Running Interpolated...");
const t2 = runInterpolated();
console.log("Interpolated:", t2.toFixed(2), "ms");

console.log("Speedup:", (t1/t2).toFixed(2) + "x");
