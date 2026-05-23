## 2024-05-15 - Date Input Timezone Fix in HilalMap.html
**Mode:** Medic
**Learning:** Setting `input.valueAsDate = new Date()` maps to UTC time, which causes off-by-one errors (showing yesterday or tomorrow) for users in timezones like Asia/Jakarta, depending on the time of day. This happens because `new Date()` is essentially a timestamp, and `valueAsDate` interprets the given date's UTC start of day.
**Action:** Always format `new Date()` manually to `YYYY-MM-DD` using local getters (`getFullYear()`, `getMonth()`, `getDate()`) and assign it to `input.value` to guarantee the input matches the user's local day.
