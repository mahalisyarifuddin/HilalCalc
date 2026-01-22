# CodeCraft Journal

## 2023-10-27 - [Initial Setup]
**Mode:** System
**Learning:** Codebase consists of standalone HTML files using CDN dependencies.
**Action:** When verifying, I need to be careful about network requests or potential lack of internet access in the sandbox, though the sandbox usually has internet. `astronomy-engine` is used for calculations.

## 2025-02-18 - Flexbox Alignment vs Hacks
**Mode:** Palette
**Learning:** The codebase used empty `<label>` elements for alignment in flex containers, which is brittle. `align-items: flex-end` is the robust solution here.
**Action:** Inspect form layouts for similar hacks before attempting other UI changes.
