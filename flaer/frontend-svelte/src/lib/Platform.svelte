<script>
  import Icon from './Icon.svelte';

  const features = [
    {
      icon: 'zap',
      title: 'Carbon intensity signals',
      body: 'Real-time grid carbon data from 40+ operators. 5-minute resolution for every major cloud region.',
    },
    {
      icon: 'trending-up',
      title: 'Ten-year forecasting',
      body: 'ML models trained on 15 years of grid data project regional carbon trajectories through 2035.',
    },
    {
      icon: 'clipboard',
      title: 'CSRD reporting',
      body: 'Auto-generate audit-ready CSRD, GHG Protocol, and CDP reports directly from infrastructure telemetry.',
    },
  ];

  const metrics = [
    { location: 'Frankfurt', value: 284, trend: '+2.4%', risk: 'amber' },
    { location: 'Dublin',    value: 198, trend: '-0.8%', risk: 'green' },
    { location: 'Stockholm', value: 18,  trend: '-5.2%', risk: 'green' },
    { location: 'Warsaw',    value: 701, trend: '-1.1%', risk: 'red'   },
  ];

  // SVG sparkline data (24h carbon intensity, normalized 0-100)
  const chartPoints = [62,68,72,65,58,55,60,64,70,74,69,63,60,58,56,54,50,48,52,58,62,60,57,55];
  const w = 400;
  const h = 80;
  const pad = 6;

  function buildPath(pts) {
    const max = Math.max(...pts);
    const min = Math.min(...pts);
    const range = max - min || 1;
    const step = (w - pad * 2) / (pts.length - 1);
    return pts.map((v, i) => {
      const x = pad + i * step;
      const y = h - pad - ((v - min) / range) * (h - pad * 2);
      return `${i === 0 ? 'M' : 'L'} ${x.toFixed(1)},${y.toFixed(1)}`;
    }).join(' ');
  }

  function buildArea(pts) {
    const linePath = buildPath(pts);
    const max = Math.max(...pts);
    const min = Math.min(...pts);
    const range = max - min || 1;
    const step = (w - pad * 2) / (pts.length - 1);
    const lastX = pad + (pts.length - 1) * step;
    return `${linePath} L ${lastX.toFixed(1)},${h - pad} L ${pad},${h - pad} Z`;
  }

  const linePath = buildPath(chartPoints);
  const areaPath = buildArea(chartPoints);
</script>

<section id="platform">
  <div class="inner w">
    <!-- Left copy -->
    <div class="copy">
      <div class="eyebrow">
        <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><circle cx="6" cy="6" r="5" stroke="currentColor" stroke-width="1.5"/><path d="M6 3v3l2 1.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
        The platform
      </div>

      <h2>The carbon layer your infrastructure is missing.</h2>

      <p class="body">
        Most infrastructure teams are flying blind on carbon. Flaer adds a continuous intelligence layer — connecting grid operators, cloud APIs, and compliance frameworks into a single system of record.
      </p>

      <div class="features">
        {#each features as f}
          <div class="feature-row">
            <div class="feature-icon">
            <Icon name={f.icon} size={16} />
          </div>
            <div class="feature-text">
              <div class="feature-title">{f.title}</div>
              <div class="feature-body">{f.body}</div>
            </div>
          </div>
        {/each}
      </div>
    </div>

    <!-- Right metrics card -->
    <div class="metrics-card">
      <div class="mc-header">
        <span class="mc-title">EU region · Carbon intensity</span>
        <span class="mc-period">Last 24h</span>
      </div>

      <!-- Chart -->
      <div class="chart-area">
        <svg viewBox="0 0 {w} {h}" width="100%" preserveAspectRatio="none">
          <defs>
            <linearGradient id="area-grad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#2cad84" stop-opacity="0.25"/>
              <stop offset="100%" stop-color="#2cad84" stop-opacity="0"/>
            </linearGradient>
          </defs>
          <path d={areaPath} fill="url(#area-grad)"/>
          <path d={linePath} fill="none" stroke="#2cad84" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <div class="chart-labels">
          <span>00:00</span>
          <span>06:00</span>
          <span>12:00</span>
          <span>18:00</span>
          <span>Now</span>
        </div>
      </div>

      <!-- Metric tiles -->
      <div class="tiles">
        {#each metrics as m}
          <div class="tile">
            <div class="tile-location">{m.location}</div>
            <div class="tile-value">{m.value} <span>gCO₂</span></div>
            <div class="tile-trend {m.risk === 'green' ? 'trend-down' : m.risk === 'red' ? 'trend-up' : 'trend-warn'}">
              {m.trend}
            </div>
          </div>
        {/each}
      </div>
    </div>
  </div>
</section>

<style>
  section {
    background: #061310;
    background-image:
      radial-gradient(ellipse 700px 400px at 100% 50%, rgba(183,149,99,0.07), transparent),
      radial-gradient(ellipse 500px 300px at 0% 50%, rgba(44,173,132,0.06), transparent);
    padding: 100px 0;
    position: relative;
  }

  section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(44,173,132,0.3), transparent);
  }

  .inner {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 64px;
    align-items: start;
  }

  /* Copy */
  .eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--green-2);
    margin-bottom: 18px;
  }

  h2 {
    font-size: clamp(26px, 3vw, 38px);
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -0.025em;
    color: #f4f7f5;
    margin-bottom: 18px;
  }

  .body {
    font-size: 15px;
    line-height: 1.65;
    color: rgba(244,247,245,0.6);
    margin-bottom: 36px;
  }

  .features {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .feature-row {
    display: flex;
    align-items: flex-start;
    gap: 16px;
  }

  .feature-icon {
    width: 36px;
    height: 36px;
    border-radius: 9px;
    background: rgba(44,173,132,0.10);
    border: 1px solid rgba(44,173,132,0.16);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--green-2);
    flex-shrink: 0;
  }

  .feature-title {
    font-size: 14px;
    font-weight: 700;
    color: #f4f7f5;
    margin-bottom: 4px;
  }

  .feature-body {
    font-size: 13.5px;
    line-height: 1.6;
    color: rgba(244,247,245,0.55);
  }

  /* Metrics card */
  .metrics-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: var(--radius-xl);
    overflow: hidden;
    box-shadow: 0 24px 60px rgba(0,0,0,0.3);
  }

  .mc-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 22px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
  }

  .mc-title {
    font-size: 12px;
    font-weight: 700;
    color: rgba(244,247,245,0.6);
    letter-spacing: 0.04em;
  }

  .mc-period {
    font-size: 11px;
    color: rgba(244,247,245,0.35);
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 3px 10px;
    border-radius: 99px;
  }

  .chart-area {
    padding: 20px 22px 8px;
  }

  .chart-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 6px;
    padding: 0 2px;
  }

  .chart-labels span {
    font-size: 10px;
    color: rgba(244,247,245,0.3);
    font-variant-numeric: tabular-nums;
  }

  .tiles {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
  }

  .tile {
    padding: 16px 22px;
    border-top: 1px solid rgba(255,255,255,0.07);
  }

  .tile:nth-child(odd) {
    border-right: 1px solid rgba(255,255,255,0.07);
  }

  .tile-location {
    font-size: 11px;
    font-weight: 600;
    color: rgba(244,247,245,0.4);
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-bottom: 5px;
  }

  .tile-value {
    font-size: 20px;
    font-weight: 800;
    color: #f4f7f5;
    letter-spacing: -0.02em;
    margin-bottom: 3px;
  }

  .tile-value span {
    font-size: 11px;
    font-weight: 500;
    color: rgba(244,247,245,0.38);
  }

  .tile-trend {
    font-size: 12px;
    font-weight: 600;
  }

  .trend-down { color: var(--green-2); }
  .trend-up   { color: var(--red); }
  .trend-warn { color: var(--amber); }

  @media (max-width: 860px) {
    .inner { grid-template-columns: 1fr; }
  }
</style>
