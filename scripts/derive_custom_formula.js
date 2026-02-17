const fs = require('fs');

function loadGT(path) {
    const data = fs.readFileSync(path, 'utf8').trim().split('\n');
    const headers = data.shift();
    return data.map(line => {
        const [hYear, hMonth, gDate] = line.split(',');
        const date = new Date(gDate);
        return {
            y: parseInt(hYear),
            m: parseInt(hMonth),
            date: date,
            daysFromEpoch: Math.round((date - new Date("1979-11-21")) / 86400000) // Epoch: 1400-01-01
        };
    });
}

function deriveCustomFormula() {
    const gt = loadGT('verification/composite_1400_1500.csv');
    const totalMonths = gt.length;

    // Linear Search for K (Slope) and B (Intercept)
    // Formula: Days(m) = floor(K * m + B)
    // where m is 0-indexed month count from epoch

    // Theoretical mean synodic month is ~29.53059
    // Our analysis showed ~29.53014

    const minK = 29.5200;
    const maxK = 29.5400;
    const stepK = 0.0001;

    const minB = -10.0;
    const maxB = 10.0;
    const stepB = 0.1;

    let bestAcc = -1;
    let bestParams = { K: 0, B: 0 };

    console.log("Searching for optimal linear formula parameters...");

    for (let K = minK; K <= maxK; K += stepK) {
        for (let B = minB; B <= maxB; B += stepB) {
            let matches = 0;

            for (let i = 0; i < totalMonths; i++) {
                const item = gt[i];
                // m = months elapsed since 1400-01
                const m = (item.y - 1400) * 12 + (item.m - 1);

                const calcDays = Math.floor(K * m + B);

                if (calcDays === item.daysFromEpoch) {
                    matches++;
                }
            }

            const acc = (matches / totalMonths) * 100;

            if (acc > bestAcc) {
                bestAcc = acc;
                bestParams = { K, B };
                // Optimization: break early if perfect (unlikely)
                if (bestAcc > 99.9) break;
            }
        }
    }

    console.log(`\nOptimal Custom Formula Found:`);
    console.log(`DaysFromEpoch = floor(${bestParams.K.toFixed(5)} * m + ${bestParams.B.toFixed(2)})`);
    console.log(`Accuracy: ${bestAcc.toFixed(2)}%`);

    // Compare with Quadratic? Days(m) = floor(K*m + Q*m^2 + B)
    // Maybe unnecessary complexity but let's check a small Q range if linear is bad.
    if (bestAcc < 80) {
        console.log("\nTrying Quadratic Fit...");
        let bestQParams = { K: 0, Q: 0, B: 0 };
        let bestQAcc = -1;

        const centerK = bestParams.K;
        const centerB = bestParams.B;

        // Refine search around linear best
        for (let K = centerK - 0.005; K <= centerK + 0.005; K += 0.001) {
             for (let Q = -0.00005; Q <= 0.00005; Q += 0.000001) {
                 for (let B = centerB - 2; B <= centerB + 2; B += 0.2) {
                    let matches = 0;
                    for (let i = 0; i < totalMonths; i++) {
                        const item = gt[i];
                        const m = (item.y - 1400) * 12 + (item.m - 1);
                        const calcDays = Math.floor(K * m + Q * m * m + B);
                        if (calcDays === item.daysFromEpoch) matches++;
                    }
                    const acc = (matches / totalMonths) * 100;
                    if (acc > bestQAcc) {
                        bestQAcc = acc;
                        bestQParams = { K, Q, B };
                    }
                 }
             }
        }
        console.log(`Optimal Quadratic Formula Found:`);
        console.log(`DaysFromEpoch = floor(${bestQParams.K.toFixed(6)} * m + ${bestQParams.Q.toFixed(8)} * m^2 + ${bestQParams.B.toFixed(2)})`);
        console.log(`Accuracy: ${bestQAcc.toFixed(2)}%`);
    }
}

deriveCustomFormula();
