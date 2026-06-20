## 2024-05-15 - Date Input Timezone Fix in HilalMap.html
**Mode:** Medic
**Learning:** Setting `input.valueAsDate = new Date()` maps to UTC time, which causes off-by-one errors (showing yesterday or tomorrow) for users in timezones like Asia/Jakarta, depending on the time of day. This happens because `new Date()` is essentially a timestamp, and `valueAsDate` interprets the given date's UTC start of day.
**Action:** Always format `new Date()` manually to `YYYY-MM-DD` using local getters (`getFullYear()`, `getMonth()`, `getDate()`) and assign it to `input.value` to guarantee the input matches the user's local day.

## 2024-05-18 - Memoize Independent Astronautical Checks
**Mode:** Bolt
**Learning:** When using web workers to render map pixels (like `HilalMap.html`), repeatedly executing independent astronomical calculations (like determining `fajrNZ_ut` for the GIC criteria) across every pixel grid iteration causes severe bottlenecks. The target date and observer (Wellington NZ) are completely constant during a map render.
**Action:** Always memoize date-dependent but location-independent constants/thresholds (like a global Fajr deadline) before entering the per-coordinate loop to save thousands of redundant operations and drastically reduce execution time.
