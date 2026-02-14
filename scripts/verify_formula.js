const locations = [
    { name: 'Dakar', lon: -17.4677, expected: 10 },
    { name: 'Mecca', lon: 39.8579, expected: 15 },
    { name: 'Banda Aceh', lon: 95.1125, expected: 18 }
];

function calculateC(lon) {
    return Math.round(lon / 14.1 + 11.7);
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
