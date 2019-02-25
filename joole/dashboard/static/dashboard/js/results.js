const MONTH_NAMES = [
    'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août',
    'Septembre', 'Octobre', 'Novembre', 'Décembre'
];

function plotYearlyCost(container, years, monthlyCons) {
    let traces = [];
    for (let iy in years) {
        traces.push({
            type: 'bar',
            x: [years[iy]],
            y: [monthlyCons[iy].reduce((a, b) => a + b)],
        });
    }

    Plotly.plot(container, traces, {
        title: 'Dépenses annuelles',
        showlegend: false,
        xaxis: { tickvals: years },
        yaxis: { ticksuffix: ' €' },
    });
}

function plotMonthlyCost(container, years, monthlyCons) {
    let traces = [];
    for (let iy in years) {
        traces.push({
            type: 'bar',
            x: MONTH_NAMES,
            y: monthlyCons[iy],
            name: years[iy],
        });
    }

    Plotly.plot(container, traces, {
        title: 'Dépenses mensuelles',
        yaxis: { ticksuffix: ' €' },
    });
}

plotYearlyCost(document.getElementById('yearly-cost-plot'), data.years, data.consEuro);
plotMonthlyCost(document.getElementById('monthly-cost-plot'), data.years, data.consEuro);
