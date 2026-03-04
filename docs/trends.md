# Trend Analysis

## 📈 $TRUMP 30-Day Interactive Dashboard

<div style="margin-bottom: 10px; display: flex; gap: 8px; align-items: center;">
  <strong>View:</strong>
  <button id="btn-daily" style="padding: 6px 12px; border: 1px solid #888; border-radius: 6px; cursor: pointer;">Daily (default)</button>
  <button id="btn-raw" style="padding: 6px 12px; border: 1px solid #888; border-radius: 6px; cursor: pointer;">Raw snapshots</button>
</div>

<div id="trend-highlights" style="margin: 10px 0 14px 0; padding: 10px 12px; border: 1px solid #ddd; border-radius: 8px;"></div>
<div id="trend-chart" style="width: 100%; height: 520px;"></div>
<div id="trend-status" style="margin-top: 12px; opacity: 0.8;"></div>

<script src="../assets/js/echarts.min.js"></script>
<script>
(async function () {
  const statusEl = document.getElementById('trend-status');
  const container = document.getElementById('trend-chart');
  const btnDaily = document.getElementById('btn-daily');
  const btnRaw = document.getElementById('btn-raw');
  const highlightsEl = document.getElementById('trend-highlights');

  if (!container || !window.echarts) {
    if (statusEl) statusEl.textContent = 'Chart init failed: local ECharts not loaded.';
    return;
  }

  const chart = echarts.init(container);

  function fmtNum(v, digits = 2) {
    return (v === null || v === undefined) ? 'N/A' : Number(v).toFixed(digits);
  }

  function pctChange(start, end) {
    if (start === null || end === null || start === undefined || end === undefined || Number(start) === 0) return null;
    return ((Number(end) - Number(start)) / Number(start)) * 100;
  }

  function renderHighlights(raw, daily) {
    if (!highlightsEl) return;
    const src = daily.length ? daily : raw;
    if (!src.length) {
      highlightsEl.textContent = 'No highlights available yet.';
      return;
    }

    const latest = src[src.length - 1] || {};
    const weekBack = src[Math.max(0, src.length - 8)] || src[0] || {};

    const priceChange7d = pctChange(weekBack.price_usd, latest.price_usd);
    const bullChange7d = pctChange(weekBack.bull_probability_pct, latest.bull_probability_pct);

    const allPrices = src.map(p => p.price_usd).filter(v => v !== null && v !== undefined);
    const allBull = src.map(p => p.bull_probability_pct).filter(v => v !== null && v !== undefined);

    const minPrice = allPrices.length ? Math.min(...allPrices) : null;
    const maxPrice = allPrices.length ? Math.max(...allPrices) : null;
    const minBull = allBull.length ? Math.min(...allBull) : null;
    const maxBull = allBull.length ? Math.max(...allBull) : null;

    highlightsEl.innerHTML = `
      <strong>Trend Highlights</strong><br/>
      • 7D Price Change: <b>${priceChange7d === null ? 'N/A' : fmtNum(priceChange7d) + '%'}</b> &nbsp; | &nbsp;
      7D Bull Probability Change: <b>${bullChange7d === null ? 'N/A' : fmtNum(bullChange7d) + '%'}</b><br/>
      • Price Range (window): <b>$${fmtNum(minPrice)} → $${fmtNum(maxPrice)}</b><br/>
      • Bull Probability Range (window): <b>${fmtNum(minBull)}% → ${fmtNum(maxBull)}%</b>
    `;
  }

  function render(seriesName, points, isDaily) {
    const labels = points.map(p => isDaily ? p.day : new Date(p.ts).toLocaleString('en-GB', {
      month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', timeZone: 'Asia/Shanghai'
    }));

    const price = points.map(p => p.price_usd ?? null);
    const bull = points.map(p => p.bull_probability_pct ?? null);
    const holder = points.map(p => p.top10_holder_pct ?? null);

    chart.setOption({
      title: {
        text: '$TRUMP Multi-Metric Trend (Price vs Bull Probability vs Top10 Holder %)',
        left: 'center'
      },
      tooltip: { trigger: 'axis' },
      legend: {
        top: 28,
        data: ['Price (USD)', 'Bull Probability (%)', 'Top10 Holder (%)']
      },
      grid: { left: 50, right: 60, top: 80, bottom: 70 },
      xAxis: {
        type: 'category',
        data: labels,
        axisLabel: { rotate: 35 }
      },
      yAxis: [
        { type: 'value', name: 'Price (USD)', position: 'left' },
        { type: 'value', name: 'Percent (%)', position: 'right', min: 0, max: 100, axisLabel: { formatter: '{value}%' } }
      ],
      dataZoom: [{ type: 'inside', start: 0, end: 100 }, { start: 0, end: 100 }],
      series: [
        { name: 'Price (USD)', type: 'line', yAxisIndex: 0, smooth: true, showSymbol: false, lineStyle: { width: 3 }, data: price },
        { name: 'Bull Probability (%)', type: 'line', yAxisIndex: 1, smooth: true, showSymbol: false, lineStyle: { width: 2 }, data: bull },
        { name: 'Top10 Holder (%)', type: 'line', yAxisIndex: 1, smooth: true, showSymbol: false, lineStyle: { width: 2, type: 'dashed' }, data: holder }
      ]
    }, true);

    const latest = points[points.length - 1] || {};
    const latestTs = isDaily ? latest.day : latest.ts;
    statusEl.textContent = `${seriesName} | Updated ${latestTs || 'N/A'} | Points: ${points.length} | Latest: $${fmtNum(latest.price_usd)} / Bull ${fmtNum(latest.bull_probability_pct)}% / Holder ${fmtNum(latest.top10_holder_pct)}%`;
  }

  function setActive(mode) {
    const activeBg = '#c62828';
    const activeColor = '#fff';
    const normalBg = '#fff';
    const normalColor = '#111';

    if (mode === 'daily') {
      btnDaily.style.background = activeBg;
      btnDaily.style.color = activeColor;
      btnRaw.style.background = normalBg;
      btnRaw.style.color = normalColor;
    } else {
      btnRaw.style.background = activeBg;
      btnRaw.style.color = activeColor;
      btnDaily.style.background = normalBg;
      btnDaily.style.color = normalColor;
    }
  }

  try {
    const res = await fetch('../assets/data/trends.json', { cache: 'no-cache' });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const payload = await res.json();

    const daily = Array.isArray(payload.points_daily) ? payload.points_daily : [];
    const raw = Array.isArray(payload.points_raw) ? payload.points_raw : [];

    if (!daily.length && !raw.length) {
      statusEl.textContent = 'No trend data available yet.';
      return;
    }

    renderHighlights(raw, daily);

    // default: daily
    const initial = daily.length ? daily : raw;
    const initialMode = daily.length ? 'daily' : 'raw';
    render(initialMode === 'daily' ? 'Daily view' : 'Raw snapshot view', initial, initialMode === 'daily');
    setActive(initialMode);

    btnDaily.addEventListener('click', () => {
      if (!daily.length) return;
      render('Daily view', daily, true);
      setActive('daily');
    });

    btnRaw.addEventListener('click', () => {
      if (!raw.length) return;
      render('Raw snapshot view', raw, false);
      setActive('raw');
    });

    window.addEventListener('resize', () => chart.resize());
  } catch (err) {
    statusEl.textContent = 'Failed to load trend data: ' + err.message;
  }
})();
</script>

---

## Notes

- Data source: `data/timeseries.jsonl`
- Build step converts raw snapshots into `assets/data/trends.json`
- Default view is **Daily** for readability; **Raw** view remains available for detailed inspection
- Time labels use Asia/Shanghai timezone in Raw view

Fight. Fight. Fight.
