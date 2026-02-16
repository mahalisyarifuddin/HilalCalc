const locations = [
    { name: 'Dakar', lon: -17.529953, expected: 15 },
    { name: 'Mecca', lon: 39.984078, expected: 19 },
    { name: 'Kuala Belait', lon: 114.075937, expected: 24 }
];

function calculateC(lon) {
    return Math.round(lon / 14.0 + 15.9);
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
