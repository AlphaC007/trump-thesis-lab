# Trend Analysis

## 📈 $TRUMP 30-Day Interactive Dashboard

<div id="trend-chart" style="width: 100%; height: 520px;"></div>

<div id="trend-status" style="margin-top: 12px; opacity: 0.8;"></div>

<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<script>
(async function () {
  const statusEl = document.getElementById('trend-status');
  const container = document.getElementById('trend-chart');

  if (!container || !window.echarts) {
    if (statusEl) statusEl.textContent = 'Chart init failed: ECharts not loaded.';
    return;
  }

  const chart = echarts.init(container);

  try {
    const res = await fetch('./assets/data/trends.json', { cache: 'no-cache' });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const payload = await res.json();
    const points = Array.isArray(payload.points) ? payload.points : [];

    if (!points.length) {
      if (statusEl) statusEl.textContent = 'No trend data available yet.';
      return;
    }

    const labels = points.map(p => new Date(p.ts).toLocaleString('en-GB', {
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
        {
          type: 'value',
          name: 'Price (USD)',
          position: 'left',
          axisLabel: { formatter: '{value}' }
        },
        {
          type: 'value',
          name: 'Percent (%)',
          position: 'right',
          min: 0,
          max: 100,
          axisLabel: { formatter: '{value}%' }
        }
      ],
      dataZoom: [
        { type: 'inside', start: 0, end: 100 },
        { start: 0, end: 100 }
      ],
      series: [
        {
          name: 'Price (USD)',
          type: 'line',
          yAxisIndex: 0,
          smooth: true,
          showSymbol: false,
          lineStyle: { width: 3 },
          data: price
        },
        {
          name: 'Bull Probability (%)',
          type: 'line',
          yAxisIndex: 1,
          smooth: true,
          showSymbol: false,
          lineStyle: { width: 2 },
          data: bull
        },
        {
          name: 'Top10 Holder (%)',
          type: 'line',
          yAxisIndex: 1,
          smooth: true,
          showSymbol: false,
          lineStyle: { width: 2, type: 'dashed' },
          data: holder
        }
      ]
    });

    const latest = points[points.length - 1];
    if (statusEl) {
      statusEl.textContent = `Updated ${new Date(payload.generated_at_utc).toLocaleString('en-GB')} UTC | Points: ${payload.count} | Latest: $${latest.price_usd} / Bull ${latest.bull_probability_pct}% / Holder ${latest.top10_holder_pct}%`;
    }

    window.addEventListener('resize', () => chart.resize());
  } catch (err) {
    if (statusEl) statusEl.textContent = 'Failed to load trend data: ' + err.message;
  }
})();
</script>

---

## Notes

- Data source: `data/timeseries.jsonl`
- Build step converts raw snapshots into `assets/data/trends.json`
- Time labels are displayed in Asia/Shanghai timezone

Fight. Fight. Fight.
