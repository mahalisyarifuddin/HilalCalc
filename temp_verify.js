
    const Astronomy = require('astronomy-engine');
    const state = { lang: "en", year: 1447, month: 12, AE_OFFSET: 2451545.0, BA_LAT: 5.54829, BA_LON: 95.32375 };
    function jdToDate(jd) { return new Date((jd - 2440587.5) * 86400000); }
    function utToDate(ut) { return jdToDate(ut + state.AE_OFFSET); }
    (jd) { return new Date((jd - 2440587.5) * 86400000); }
        function utToDate(ut) { return jdToDate(ut + state.AE_OFFSET); }
        function updateLang() {
            state.lang = elements.language.value; const strings = text[state.lang];
            elements.statsTitle.textContent = strings.statsTitle; elements.statsContent.innerHTML = strings.statsContent;
            elements.methodology.innerHTML = strings.methodology; elements.appTitle.textContent = strings.appTitle;
            elements.todayBtn.textContent = strings.today; elements.mabTitle.textContent = strings.mabTitle; elements.gicTitle.textContent = strings.gicTitle;
            for (let i = 0; i < 12; i++) elements.hMonthInput.options[i].textContent = strings.monthNames[i];
            calculate();
        }
        function formatDate(jd) {
            const date = jdToDate(jd);
            return date.toLocaleDateString(state.lang === 'id' ? 'id-ID' : 'en-GB', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' });
        }
        function updateTheme() { const val = elements.theme.value; document.documentElement.className = val === 'auto' ? '' : val; }
        function getGeocentricAltitude(time, observer, moonGeoVec) {
            const obsVec = Astronomy.ObserverVector(time, observer, true);
            const dist = Astronomy.AngleBetween(obsVec, moonGeoVec);
            return 90.0 - dist;
        }
        function getStartJD(year, month) {
            const totalMonths = (year - 1) * 12 + (month - 1);
            const approxJD = 1948440 + totalMonths * 29.53059;
            const startTime = Astronomy.MakeTime(jdToDate(approxJD - 15));
            const conj = Astronomy.SearchMoonPhase(0, startTime, 40);
            const day29StartJD = Math.floor(conj.ut + state.AE_OFFSET + 0.5) - 0.5;

            // MABBIMS Banda Aceh search
            let jdMab, detailMab, foundMab = false;
            const obsAceh = new Astronomy.Observer(state.BA_LAT, state.BA_LON, 0);
            for (let d = 0; d < 2; d++) {
                const sJD = day29StartJD + d;
                const ss = Astronomy.SearchRiseSet(Astronomy.Body.Sun, obsAceh, -1, Astronomy.MakeTime(jdToDate(sJD + 0.5 - state.BA_LON/360.0)), 1.0);
                if (ss && ss.ut >= conj.ut - 0.0001) {
                    const t = Astronomy.MakeTime(utToDate(ss.ut));
                    const mVec = Astronomy.GeoVector(Astronomy.Body.Moon, t, true), sVec = Astronomy.GeoVector(Astronomy.Body.Sun, t, true);
                    const elong = Astronomy.AngleBetween(mVec, sVec), eqMT = Astronomy.Equator(Astronomy.Body.Moon, t, obsAceh, true, true);
                    const ht = Astronomy.Horizon(t, obsAceh, eqMT.ra, eqMT.dec, "normal").altitude;
                    if (ht >= 3.0 && elong >= 6.4) { jdMab = sJD + 1.0; detailMab = { ut: ss.ut, alt: ht, elong: elong }; foundMab = true; break; }
                }
            }
            if (!foundMab) { jdMab = day29StartJD + 2.0; detailMab = { ut: conj.ut, alt: -1, elong: -1 }; }

            // GIC Global search
            let jdGic, detailGic, foundGic = false;
            const fNZ = Astronomy.SearchAltitude(Astronomy.Body.Sun, new Astronomy.Observer(-41.28, 174.77, 0), 1, Astronomy.MakeTime(jdToDate(day29StartJD + 0.5)), 1.0, -18.0);

            for (let d = 0; d < 2; d++) {
                const sJD = day29StartJD + d;
                const midnightUTC = sJD + 1.0 - state.AE_OFFSET;
                for (let lon = 180; lon >= -180; lon -= 2) {
                    for (let lat = -60; lat <= 60; lat += 2) {
                        const obs = new Astronomy.Observer(lat, lon, 0);
                        const ss = Astronomy.SearchRiseSet(Astronomy.Body.Sun, obs, -1, Astronomy.MakeTime(jdToDate(sJD + 0.5 - lon/360.0)), 1.0);
                        if (ss && ss.ut >= conj.ut - 0.0001) {
                            const t = Astronomy.MakeTime(utToDate(ss.ut));
                            const mVec = Astronomy.GeoVector(Astronomy.Body.Moon, t, true), sVec = Astronomy.GeoVector(Astronomy.Body.Sun, t, true);
                            const elong = Astronomy.AngleBetween(mVec, sVec), alt = getGeocentricAltitude(t, obs, mVec);
                            if (alt >= 5.0 && elong >= 8.0) {
                                let valid = false;
                                if (ss.ut <= midnightUTC + 0.0001) valid = true;
                                else if (fNZ && conj.ut < fNZ.ut && lon <= -20) valid = true;

                                if (valid) {
                                    jdGic = sJD + 1.0; detailGic = { ut: ss.ut, alt, elong };
                                    foundGic = true; break;
                                }
                            }
                        }
                    }
                    if (foundGic) break;
                }
                if (foundGic) break;
            }
            if (!foundGic) { jdGic = day29StartJD + 2.0; detailGic = { ut: conj.ut, alt: -1, elong: -1 }; }
            return { jdAceh: jdMab, jdGic, detailAceh: detailMab, detailGic };
        }
        function calculate() {
            state.year = parseInt(elements.hYearInput.value) || 1; state.month = parseInt(elements.hMonthInput.value);
            let res = getStartJD(state.year, state.month); const strings = text[state.lang];
            elements.dateAceh.textContent = formatDate(res.jdAceh); elements.dateGic.textContent = formatDate(res.jdGic);
            const fmtInfo = (info, prefix) => prefix + (info.alt > -180 ? (utToDate(info.ut).toISOString().substring(11, 19) + " UTC<br>" + strings.alt + ": " + info.alt.toFixed(2) + "°, " + strings.elong + ": " + info.elong.toFixed(2) + "°") : "N/A");
            elements.infoAceh.innerHTML = fmtInfo(res.detailAceh, strings.acehInfo); elements.infoGic.innerHTML = fmtInfo(res.detailGic, strings.gicInfo);
            const sim = Math.abs(res.jdAceh - res.jdGic) < 0.1;
            elements.verdict.textContent = strings[sim ? 'simultaneous' : 'divergent'];
            elements.verdict.className = "verdict-box verdict-" + (sim ? "simultaneous" : "divergent");
        }
        elements.language.onchange = updateLang; elements.theme.onchange = updateTheme;
        elements.prevBtn.onclick = () => { state.month--; if (state.month < 1) { state.month = 12; state.year--; } elements.hYearInput.value = state.year; elements.hMonthInput.value = state.month; calculate(); };
        elements.nextBtn.onclick = () => { state.month++; if (state.month > 12) { state.month = 1; state.year++; } elements.hYearInput.value = state.year; elements.hMonthInput.value = state.month; calculate(); };
        elements.goBtn.onclick = calculate;
        elements.todayBtn.onclick = () => {
            const index = Math.floor((Date.now() / 86400000 + 2440587.5 - 1948440 - 0.236624) / 29.530573265);
            state.year = Math.floor(index / 12) + 1; state.month = (index % 12) + 1;
            elements.hYearInput.value = state.year; elements.hMonthInput.value = state.month; calculate();
        };
        elements.hYearInput.value = state.year; elements.hMonthInput.value = state.month;
        elements.language.value = navigator.language?.startsWith('id') ? 'id' : 'en';
        updateLang(); updateTheme();

    console.log(JSON.stringify(getStartJD(1447, 12)));
