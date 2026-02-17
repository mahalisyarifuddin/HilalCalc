const fs = require('fs');

function loadGT(path) {
    const data = fs.readFileSync(path, 'utf8').trim().split('\n');
    const headers = data.shift();
    return data.map(line => {
        const [hYear, hMonth, gDate] = line.split(',');
        return { y: parseInt(hYear), m: parseInt(hMonth), date: new Date(gDate) };
    });
}

function analyze() {
    const gt = loadGT('verification/composite_1400_1500.csv');
    let monthLengths = [];
    let yearLengths = [];

    // Sort by date
    gt.sort((a, b) => a.date - b.date);

    for (let i = 0; i < gt.length - 1; i++) {
        const curr = gt[i];
        const next = gt[i+1];

        // Month length
        const diff = Math.round((next.date - curr.date) / 86400000);
        monthLengths.push(diff);
    }

    // Aggregate by Year
    for (let i = 0; i < gt.length - 1; i++) {
        const item = gt[i];
        if (item.m === 1) { // Start of year
            // Find start of next year (item.y + 1, m=1)
            const nextYearStart = gt.find(x => x.y === item.y + 1 && x.m === 1);
            if (nextYearStart) {
                const yearLen = Math.round((nextYearStart.date - item.date) / 86400000);
                yearLengths.push({ y: item.y, len: yearLen });
            }
        }
    }

    const counts = {};
    monthLengths.forEach(l => counts[l] = (counts[l] || 0) + 1);

    const yearCounts = {};
    yearLengths.forEach(l => yearCounts[l.len] = (yearCounts[l.len] || 0) + 1);

    const totalDays = monthLengths.reduce((a, b) => a + b, 0);
    const totalMonths = monthLengths.length;
    const avgMonth = totalDays / totalMonths;

    const totalYearDays = yearLengths.reduce((a, b) => a + b.len, 0);
    const totalYears = yearLengths.length;
    const avgYear = totalYearDays / totalYears;

    console.log(`\nAnalysis of Composite GT (1400-1500 AH):`);
    console.log(`Month Lengths Distribution:`, counts);
    console.log(`Year Lengths Distribution:`, yearCounts);
    console.log(`Average Month Length: ${avgMonth.toFixed(5)} days`);
    console.log(`Average Year Length: ${avgYear.toFixed(5)} days`);

    // Check alternating pattern (30, 29, 30, 29...)
    let strictAltMatches = 0;
    for (let i = 0; i < monthLengths.length; i++) {
        // Standard Tabular assumes odd months are 30, even are 29 (except 12th in leap year)
        // But here index 0 is Month 1 (odd) -> Length 30.
        // Index 1 is Month 2 (even) -> Length 29.
        const m = (gt[i].m - 1); // 0-based month index (0=Muharram)
        const expected = (m % 2 === 0) ? 30 : 29;

        // Special case: 12th month (index 11) can be 30 in leap years.
        // But let's just check raw alternation 30, 29 first.
        if (monthLengths[i] === expected) strictAltMatches++;
    }
    console.log(`Strict Alternating Month Match Rate: ${(strictAltMatches / totalMonths * 100).toFixed(2)}%`);

    // Check actual leap years vs tabular cycle
    const leapYears = yearLengths.filter(x => x.len === 355).map(x => x.y);
    console.log(`Leap Years (Length=355): ${leapYears.length} years`);
    console.log(`Leap Years List: ${leapYears.join(', ')}`);

    // Standard tabular leap years (Typical Kuwaiti: 2,5,7,10,13,16,18,21,24,26,29)
    // Check how many match standard 11/30 pattern?
}

analyze();
