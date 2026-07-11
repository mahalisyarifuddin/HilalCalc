## 2024-05-15 - Date Input Timezone Fix in HilalMap.html
**Mode:** Medic
**Learning:** Setting `input.valueAsDate = new Date()` maps to UTC time, which causes off-by-one errors (showing yesterday or tomorrow) for users in timezones like Asia/Jakarta, depending on the time of day. This happens because `new Date()` is essentially a timestamp, and `valueAsDate` interprets the given date's UTC start of day.
**Action:** Always format `new Date()` manually to `YYYY-MM-DD` using local getters (`getFullYear()`, `getMonth()`, `getDate()`) and assign it to `input.value` to guarantee the input matches the user's local day.

## 2024-05-18 - Memoize Independent Astronautical Checks
**Mode:** Bolt
**Learning:** When using web workers to render map pixels (like `HilalMap.html`), repeatedly executing independent astronomical calculations (like determining `fajrNZ_ut` for the GIC criteria) across every pixel grid iteration causes severe bottlenecks. The target date and observer (Wellington NZ) are completely constant during a map render.
**Action:** Always memoize date-dependent but location-independent constants/thresholds (like a global Fajr deadline) before entering the per-coordinate loop to save thousands of redundant operations and drastically reduce execution time.

## 2024-06-27 - Astronomy.SearchAltitude Null Return Handling
**Mode:** Medic
**Learning:** In the `astronomy-engine` library, `Astronomy.SearchAltitude()` can return `null` if the celestial body does not reach the specified altitude within the search time window. For example, the sun might never reach -18° altitude during summer/winter in high latitudes. Accessing `.ut` directly on the result (e.g., `fajrNZ.ut`) without a null check will cause an `Uncaught TypeError: Cannot read properties of null`.
**Action:** Always implement a null check for the return value of `Astronomy.SearchAltitude` before accessing its properties (e.g., `isBeforeDeadline = fajrNZ ? sunsetUT < fajrNZ.ut : false;`).

## 2025-02-12 - Defer Dependent Calculations in Render Loop
**Mode:** Bolt
**Learning:** In the web worker rendering logic (`HilalMap.html`), calculating the sun's position before determining if the moon's altitude meets visibility criteria results in many redundant, expensive calculations for coordinates where the moon is already out of view.
**Action:** Always defer dependent calculations (e.g., calculating the sun's position to check elongation) until after prerequisite checks (like moon minimum altitude) pass, especially inside dense rendering loops.
