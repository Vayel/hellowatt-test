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
            hoverinfo: 'y',
        });
    }

    Plotly.plot(container, traces, {
        title: 'Dépenses annuelles',
        showlegend: false,
        margin: { l: 50, r: 10, t: 30 },
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
            hoverinfo: 'y',
        });
    }

    Plotly.plot(container, traces, {
        title: 'Dépenses mensuelles',
        margin: { l: 50, r: 10, t: 30 },
        yaxis: { ticksuffix: ' €' },
    });
}

function plotPowerConsumption(container, years, monthlyCons) {
    let traces = [];
    for (let iy in years) {
        traces.push({
            x: MONTH_NAMES,
            y: monthlyCons[iy],
            name: years[iy],
            hoverinfo: 'y',
            visible: (iy == years.length - 1) ? true : 'legendonly',
        });
    }

    Plotly.plot(container, traces, {
        margin: { l: 50, r: 10, t: 30 },
        yaxis: { ticksuffix: ' W' },
    });
}

plotYearlyCost(document.getElementById('yearly-cost-plot'), data.years, data.consEuro);
plotMonthlyCost(document.getElementById('monthly-cost-plot'), data.years, data.consEuro);
plotPowerConsumption(document.getElementById('consumption-plot'), data.years, data.consWatt);
