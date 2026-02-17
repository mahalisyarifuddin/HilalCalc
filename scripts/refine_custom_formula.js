const fs = require('fs');

function loadGT(path) {
    const data = fs.readFileSync(path, 'utf8').trim().split('\n');
    const headers = data.shift();
    // Epoch: 1979-11-21 (1400-01-01)
    const epoch = new Date("1979-11-21");
    return data.map(line => {
        const [hYear, hMonth, gDate] = line.split(',');
        const date = new Date(gDate);
        return {
            y: parseInt(hYear),
            m: parseInt(hMonth),
            daysFromEpoch: Math.round((date - epoch) / 86400000)
        };
    });
}

function refine() {
    const gt = loadGT('verification/composite_1400_1500.csv');
    const totalMonths = gt.length;

    // Refined Search
    const minK = 29.53040;
    const maxK = 29.53060;
    const stepK = 0.00001;

    const minB = 0.0;
    const maxB = 1.0;
    const stepB = 0.01;

    let bestAcc = -1;
    let bestParams = { K: 0, B: 0 };

    console.log("Refining linear formula...");

    for (let K = minK; K <= maxK; K += stepK) {
        for (let B = minB; B <= maxB; B += stepB) {
            let matches = 0;
            for (let i = 0; i < totalMonths; i++) {
                const item = gt[i];
                const m = (item.y - 1400) * 12 + (item.m - 1);
                const calcDays = Math.floor(K * m + B);
                if (calcDays === item.daysFromEpoch) matches++;
            }
            const acc = (matches / totalMonths) * 100;
            if (acc > bestAcc) {
                bestAcc = acc;
                bestParams = { K, B };
            }
        }
    }

    console.log(`Refined Optimal Formula:`);
    console.log(`Days = floor(${bestParams.K.toFixed(5)} * m + ${bestParams.B.toFixed(2)})`);
    console.log(`Accuracy: ${bestAcc.toFixed(2)}%`);

    // Verify error distribution
    let errors = { '-2': 0, '-1': 0, '0': 0, '1': 0, '2': 0 };
    for (let i = 0; i < totalMonths; i++) {
        const item = gt[i];
        const m = (item.y - 1400) * 12 + (item.m - 1);
        const calcDays = Math.floor(bestParams.K * m + bestParams.B);
        const diff = calcDays - item.daysFromEpoch;
        if (errors[diff] !== undefined) errors[diff]++;
        else errors['other'] = (errors['other'] || 0) + 1;
    }
    console.log("Error Distribution (Calc - GT):", errors);
}

refine();
