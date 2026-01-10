importScripts('https://cdn.jsdelivr.net/npm/astronomy-engine@2.1.19/astronomy.browser.min.js');

const RESOLUTION_FACTOR = 0.25; // 1/4th resolution = 16x faster
const INTERP_STEP = 10; // Interpolate every 10 *calculated* pixels

self.onmessage = function(e) {
    const {
        bounds,
        widthDeg,
        heightDeg,
        mapSizeX,
        criteria,
        dateTimestamp,
        minAlt: criteriaMinAlt,
        minElong: criteriaMinElong
    } = e.data;

    try {
        const date = Astronomy.MakeTime(new Date(dateTimestamp));

        let minAlt = 0, minElong = 0, isGIC = false;
        if (criteria === 'mabbims') { minAlt = 3; minElong = 6.4; }
        else if (criteria === 'gic') { minAlt = 5; minElong = 8; isGIC = true; }
        else if (criteria === 'alt0') { minAlt = 0; minElong = -100; }
        else if (criteria === 'custom') {
            minAlt = criteriaMinAlt;
            minElong = criteriaMinElong;
        }

        // Calculate PPD based on screen resolution and zoom, applied with RESOLUTION_FACTOR
        const PPD = (mapSizeX / widthDeg) * RESOLUTION_FACTOR;

        const width = Math.ceil(widthDeg * PPD);
        const height = Math.ceil(heightDeg * PPD);

        // Prepare buffer
        // RGBA = 4 bytes
        const buffer = new Uint8ClampedArray(width * height * 4);

        const totalPixels = width * height;
        const observer = new Astronomy.Observer(0, 0, 0);
        let currentY = -1;
        let sunsetBase = null;

        let prevRA, prevDec, prevElong, prevAlt;
        let nextRA, nextDec, nextElong, nextAlt;
        let cachedNextRA, cachedNextDec, cachedNextElong, cachedNextAlt;

        // Progress reporting interval
        const progressInterval = Math.floor(totalPixels / 20);
        let lastReported = 0;

        for (let pixelIndex = 0; pixelIndex < totalPixels; pixelIndex++) {
            // Report progress occasionally
            if (pixelIndex - lastReported > progressInterval) {
                self.postMessage({ status: 'progress', percent: Math.round(pixelIndex / totalPixels * 100) });
                lastReported = pixelIndex;
            }

            const x = pixelIndex % width;
            const y = Math.floor(pixelIndex / width);

            // Map pixel back to lat/lon
            const lat = bounds.maxLat - (y / PPD);
            const lon = bounds.minLon + (x / PPD);

            if (y !== currentY) {
                currentY = y;
                observer.latitude = lat;
                observer.longitude = 0;
                const sunset = Astronomy.SearchRiseSet(Astronomy.Body.Sun, observer, 1, date.ut, 1);
                sunsetBase = sunset ? sunset.ut : null;
                // Reset interpolation state on new row
                prevRA = undefined;
                cachedNextRA = undefined;
            }

            if (sunsetBase !== null) {
                observer.latitude = lat;
                observer.longitude = lon;

                const sunsetUT = sunsetBase - (lon / 360.0);
                let moonRA, moonDec, moonElong;
                let moonAlt;

                const xMod = x % INTERP_STEP;

                if (xMod === 0 || prevRA === undefined) {
                    if (x > 0 && prevRA !== undefined && cachedNextRA !== undefined) {
                        prevRA = cachedNextRA;
                        prevDec = cachedNextDec;
                        prevElong = cachedNextElong;
                        prevAlt = cachedNextAlt;
                    } else {
                        const moonEq = Astronomy.Equator(Astronomy.Body.Moon, sunsetUT, observer, true, true);
                        prevRA = moonEq.ra;
                        prevDec = moonEq.dec;
                        prevElong = Astronomy.AngleFromSun(Astronomy.Body.Moon, sunsetUT);
                        const moonHor = Astronomy.Horizon(sunsetUT, observer, prevRA, prevDec, 'normal');
                        prevAlt = moonHor.altitude;
                    }

                    // Calculate next keyframe
                    let nextX = x + INTERP_STEP;
                    if (nextX >= width) nextX = width - 1;

                    if (nextX > x) {
                        const nextLon = bounds.minLon + (nextX / PPD);
                        const nextSunsetUT = sunsetBase - (nextLon / 360.0);
                        observer.longitude = nextLon;

                        const nextMoonEq = Astronomy.Equator(Astronomy.Body.Moon, nextSunsetUT, observer, true, true);
                        cachedNextRA = nextMoonEq.ra;
                        cachedNextDec = nextMoonEq.dec;
                        cachedNextElong = Astronomy.AngleFromSun(Astronomy.Body.Moon, nextSunsetUT);
                        const nextMoonHor = Astronomy.Horizon(nextSunsetUT, observer, nextMoonEq.ra, nextMoonEq.dec, 'normal');
                        cachedNextAlt = nextMoonHor.altitude;

                        nextRA = cachedNextRA;
                        nextDec = cachedNextDec;
                        nextElong = cachedNextElong;
                        nextAlt = cachedNextAlt;

                        if (Math.abs(nextRA - prevRA) > 12) {
                            if (nextRA > prevRA) prevRA += 24;
                            else nextRA += 24;
                        }
                        observer.longitude = lon;
                    } else {
                        nextRA = prevRA;
                        nextDec = prevDec;
                        nextElong = prevElong;
                        nextAlt = prevAlt;
                        cachedNextRA = undefined;
                    }

                    moonRA = prevRA;
                    moonDec = prevDec;
                    moonElong = prevElong;
                    moonAlt = prevAlt;
                } else {
                    const fraction = xMod / INTERP_STEP;
                    moonRA = prevRA + (nextRA - prevRA) * fraction;
                    moonDec = prevDec + (nextDec - prevDec) * fraction;
                    moonElong = prevElong + (nextElong - prevElong) * fraction;
                    moonAlt = prevAlt + (nextAlt - prevAlt) * fraction;

                    if (moonRA >= 24) moonRA -= 24;
                }

                // Check visibility
                // Logic copied from index.html checkVisibility
                let visible = false;

                // --- checkVisibility logic inlined ---
                let isVisibleGIC = true;
                if (isGIC) {
                    if (sunsetUT >= (date.ut + 0.5)) isVisibleGIC = false;
                }

                if (isVisibleGIC) {
                    // We already have moonAlt calculated/interpolated
                    if (moonAlt >= minAlt) {
                         const elong = moonElong; // Already have it
                         if (elong >= minElong) {
                             visible = true;
                         }
                    }
                }
                // -------------------------------------

                if (visible) {
                    const idx = pixelIndex * 4;
                    buffer[idx] = 0;     // R
                    buffer[idx+1] = 255; // G
                    buffer[idx+2] = 0;   // B
                    buffer[idx+3] = 128; // A
                }
            }
        }

        self.postMessage({
            status: 'complete',
            buffer: buffer,
            width: width,
            height: height
        }, [buffer.buffer]);

    } catch (e) {
        self.postMessage({ status: 'error', message: e.message });
    }
};
