<script>
  const years = [2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035];
  // BAU trajectory (increasing)
  const bau = [100, 108, 116, 125, 135, 146, 158, 171, 185, 200, 218];
  // Optimised trajectory (declining)
  const opt = [100, 97, 93, 88, 83, 77, 71, 65, 60, 56, 52];

  const svgW = 480;
  const svgH = 200;
  const padL = 40;
  const padR = 20;
  const padT = 16;
  const padB = 32;

  const innerW = svgW - padL - padR;
  const innerH = svgH - padT - padB;

  function toX(i) {
    return padL + (i / (years.length - 1)) * innerW;
  }

  function toY(val, min, max) {
    return padT + innerH - ((val - min) / (max - min)) * innerH;
  }

  const allVals = [...bau, ...opt];
  const dataMin = Math.min(...allVals) - 5;
  const dataMax = Math.max(...allVals) + 5;

  function makePath(data) {
    return data
      .map((v, i) => `${i === 0 ? 'M' : 'L'} ${toX(i).toFixed(1)},${toY(v, dataMin, dataMax).toFixed(1)}`)
      .join(' ');
  }

  function makeArea(data, fillBottom) {
    const line = makePath(data);
    const lastX = toX(data.length - 1);
    return `${line} L ${lastX},${fillBottom} L ${padL},${fillBottom} Z`;
  }

  const bauPath = makePath(bau);
  const optPath = makePath(opt);
  const optArea = makeArea(opt, padT + innerH);

  const gridYVals = [50, 75, 100, 125, 150, 175, 200, 225];

  const metrics = [
    { label: 'CO₂ reduction', value: '−38%', sub: 'vs BAU by 2035', color: 'var(--green-2)' },
    { label: 'Cost avoidance', value: '€2.1M', sub: 'cumulative energy cost', color: 'var(--gold)' },
    { label: 'Compliance penalty risk', value: '−€4.8M', sub: 'avoided CSRD exposure', color: 'var(--blue)' },
  ];
</script>

<section id="forecast">
  <div class="inner w">
    <!-- Left copy -->
    <div class="copy">
      <div class="eyebrow">
        Forecast impact
      </div>

      <h2>See the difference optimised carbon strategy makes by 2035.</h2>

      <p class="body">
        Infrastructure teams that act on carbon signals early avoid both compliance penalties and energy cost escalations. Flaer quantifies the value of that lead time.
      </p>

      <div class="metrics">
        {#each metrics as m}
          <div class="metric-row">
            <div class="metric-val" style="color: {m.color};">{m.value}</div>
            <div class="metric-info">
              <div class="metric-label">{m.label}</div>
              <div class="metric-sub">{m.sub}</div>
            </div>
          </div>
        {/each}
      </div>
    </div>

    <!-- Right chart card -->
    <div class="chart-card">
      <div class="chart-header">
        <span class="chart-title">Carbon trajectory · 2025–2035</span>
        <div class="legend">
          <span class="leg-item leg-red">
            <span class="leg-line"></span> BAU trajectory
          </span>
          <span class="leg-item leg-green">
            <span class="leg-line"></span> Optimised
          </span>
        </div>
      </div>

      <div class="chart-wrap">
        <svg viewBox="0 0 {svgW} {svgH}" width="100%">
          <defs>
            <linearGradient id="opt-grad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#2cad84" stop-opacity="0.18"/>
              <stop offset="100%" stop-color="#2cad84" stop-opacity="0"/>
            </linearGradient>
          </defs>

          <!-- Grid lines -->
          {#each gridYVals as gv}
            {@const gy = toY(gv, dataMin, dataMax)}
            {#if gy >= padT && gy <= padT + innerH}
              <line
                x1={padL} y1={gy}
                x2={padL + innerW} y2={gy}
                stroke="rgba(255,255,255,0.07)"
                stroke-width="1"
              />
              <text x={padL - 6} y={gy + 4} text-anchor="end" fill="rgba(255,255,255,0.3)" font-size="9">{gv}</text>
            {/if}
          {/each}

          <!-- Year labels -->
          {#each years as yr, i}
            {#if i % 2 === 0}
              <text
                x={toX(i)}
                y={svgH - 6}
                text-anchor="middle"
                fill="rgba(255,255,255,0.3)"
                font-size="9"
              >{yr}</text>
            {/if}
          {/each}

          <!-- Optimised area -->
          <path d={optArea} fill="url(#opt-grad)"/>

          <!-- BAU line -->
          <path d={bauPath} fill="none" stroke="#d35d5c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="6 3"/>

          <!-- Optimised line -->
          <path d={optPath} fill="none" stroke="#2cad84" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>

          <!-- Start dot -->
          <circle cx={toX(0)} cy={toY(bau[0], dataMin, dataMax)} r="4" fill="#d35d5c"/>
          <circle cx={toX(0)} cy={toY(opt[0], dataMin, dataMax)} r="4" fill="#2cad84"/>
          <!-- End dots -->
          <circle cx={toX(10)} cy={toY(bau[10], dataMin, dataMax)} r="4" fill="#d35d5c"/>
          <circle cx={toX(10)} cy={toY(opt[10], dataMin, dataMax)} r="4" fill="#2cad84"/>
        </svg>
      </div>

      <div class="chart-footer">
        <span class="cf-stat green">−38% CO₂</span>
        <span class="cf-sep">·</span>
        <span class="cf-stat gold">€2.1M energy cost reduction</span>
        <span class="cf-sep">·</span>
        <span class="cf-stat">vs. BAU by 2035</span>
      </div>
    </div>
  </div>
</section>

<style>
  section {
    background: var(--paper);
    padding: 100px 0;
    border-top: 1px solid rgba(0,0,0,0.06);
  }

  .inner {
    display: grid;
    grid-template-columns: 1fr 1.2fr;
    gap: 64px;
    align-items: center;
  }

  .eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--green);
    margin-bottom: 16px;
  }

  h2 {
    font-size: clamp(24px, 2.8vw, 34px);
    font-weight: 800;
    line-height: 1.18;
    letter-spacing: -0.025em;
    color: var(--ink);
    margin-bottom: 16px;
  }

  .body {
    font-size: 15px;
    line-height: 1.65;
    color: var(--ink-soft);
    margin-bottom: 36px;
  }

  .metrics {
    display: flex;
    flex-direction: column;
    gap: 18px;
  }

  .metric-row {
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 16px 20px;
    background: #fff;
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: var(--radius-md);
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }

  .metric-val {
    font-size: 26px;
    font-weight: 900;
    letter-spacing: -0.03em;
    min-width: 80px;
  }

  .metric-label {
    font-size: 13px;
    font-weight: 700;
    color: var(--ink);
  }

  .metric-sub {
    font-size: 12px;
    color: var(--ink-muted);
    margin-top: 2px;
  }

  /* Chart card */
  .chart-card {
    background: #0a1c17;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: var(--radius-xl);
    overflow: hidden;
    box-shadow: 0 24px 60px rgba(0,0,0,0.2);
  }

  .chart-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 22px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
  }

  .chart-title {
    font-size: 12px;
    font-weight: 700;
    color: rgba(244,247,245,0.55);
    letter-spacing: 0.04em;
  }

  .legend {
    display: flex;
    gap: 14px;
  }

  .leg-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-weight: 600;
    color: rgba(244,247,245,0.5);
  }

  .leg-line {
    display: inline-block;
    width: 18px;
    height: 2px;
    border-radius: 2px;
  }

  .leg-red .leg-line  { background: #d35d5c; }
  .leg-green .leg-line { background: #2cad84; }

  .chart-wrap {
    padding: 10px 16px 0;
  }

  .chart-footer {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px 22px;
    border-top: 1px solid rgba(255,255,255,0.07);
    flex-wrap: wrap;
  }

  .cf-stat {
    font-size: 12px;
    font-weight: 700;
    color: rgba(244,247,245,0.5);
  }

  .cf-stat.green { color: var(--green-2); }
  .cf-stat.gold  { color: var(--gold); }

  .cf-sep {
    color: rgba(244,247,245,0.2);
    font-size: 14px;
  }

  @media (max-width: 860px) {
    .inner { grid-template-columns: 1fr; }
  }
</style>
