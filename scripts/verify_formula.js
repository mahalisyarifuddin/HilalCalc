const locations = [
    { name: 'Dakar', lon: -17.529938, expected: 39 },
    { name: 'Mecca', lon: 39.984063, expected: 45 },
    { name: 'Kuala Belait', lon: 114.075937, expected: 54 }
];

function calculateC(lon) {
    // Derived from Obligatory Months Optimization (1000-6000 AH)
    // Formula: C = 0.12 * Lon + 40.6
    return Math.round(lon * 0.12 + 40.6);
}

let allPass = true;
locations.forEach(loc => {
    const c = calculateC(loc.lon);
    console.log(`${loc.name}: Lon ${loc.lon}, Expected ${loc.expected}, Got ${c}`);
    if (c !== loc.expected) {
        console.error(`FAILED: ${loc.name} Expected ${loc.expected}, Got ${c}`);
        allPass = false;
    }
});

if (allPass) {
    console.log('SUCCESS: All locations match expected C values.');
} else {
    process.exit(1);
}
