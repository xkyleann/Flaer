<script>
  import { dataCenters } from './data.js';

  // Enrich data centers with derived metrics
  const facilities = dataCenters.map((dc, i) => ({
    ...dc,
    pue:       +(1.2 + (dc.intensity / 1000) * 1.8 + (i % 5) * 0.08).toFixed(2),
    wue:       +(0.4 + (dc.intensity / 800) * 2.0 + (i % 4) * 0.15).toFixed(2),
    cue:       +(dc.intensity / 400).toFixed(2),
    renewable: Math.max(5, Math.min(98, Math.round(100 - dc.intensity / 6 + (i % 7) * 3))),
    scope1:    Math.round(150 + i * 45),
    scope2:    Math.round(dc.intensity * 8760 * 0.45 / 1000),
    scope3:    Math.round(800 + i * 120),
    powerMW:   Math.round(parseFloat(dc.capacity) * 1000 * 0.42),
  }));

  let selected = ['us-west-2', 'eu-central-1', 'ca-central'];
  let metric    = 'intensity';
  let timeframe = 'Q2 2026';
  let generating = false;
  let exported   = false;
  let sortCol    = null;
  let sortDir    = 1;

  const metrics = [
    { id: 'intensity',  label: 'Carbon Intensity',  unit: 'gCO₂/kWh', lower: true,  color: '#d35d5c' },
    { id: 'pue',        label: 'PUE',               unit: '',          lower: true,  color: '#7faeff' },
    { id: 'wue',        label: 'WUE',               unit: 'L/kWh',    lower: true,  color: '#7faeff' },
    { id: 'cue',        label: 'CUE',               unit: '',          lower: true,  color: '#b79563' },
    { id: 'renewable',  label: 'Renewable %',        unit: '%',         lower: false, color: '#2cad84' },
  ];

  const allMetrics = [
    { id: 'intensity', label: 'Carbon Intensity',      unit: 'gCO₂/kWh', lower: true  },
    { id: 'pue',       label: 'PUE',                   unit: '',          lower: true  },
    { id: 'wue',       label: 'WUE (L/kWh)',           unit: 'L/kWh',    lower: true  },
    { id: 'cue',       label: 'CUE',                   unit: '',          lower: true  },
    { id: 'renewable', label: 'Renewable %',            unit: '%',         lower: false },
    { id: 'scope1',    label: 'Scope 1 (tCO₂e)',       unit: 'tCO₂e',    lower: true  },
    { id: 'scope2',    label: 'Scope 2 (tCO₂e)',       unit: 'tCO₂e',    lower: true  },
    { id: 'scope3',    label: 'Scope 3 (tCO₂e)',       unit: 'tCO₂e',    lower: true  },
    { id: 'powerMW',   label: 'IT Load (MW)',           unit: 'MW',        lower: false },
    { id: 'forecast2035', label: '2035 Forecast',      unit: 'gCO₂/kWh', lower: true  },
  ];

  $: compared = facilities.filter(f => selected.includes(f.id));

  function toggle(id) {
    if (selected.includes(id)) {
      if (selected.length > 2) selected = selected.filter(x => x !== id);
    } else {
      if (selected.length < 4) selected = [...selected, id];
    }
  }

  function bestFor(metId) {
    if (!compared.length) return null;
    const m = allMetrics.find(m => m.id === metId);
    return compared.reduce((best, dc) =>
      m.lower ? (dc[metId] < best[metId] ? dc : best)
              : (dc[metId] > best[metId] ? dc : best)
    );
  }

  function rankFacilities() {
    return [...compared].map(dc => {
      let score = 0;
      allMetrics.forEach(m => {
        const vals = compared.map(d => d[m.id]);
        const best = m.lower ? Math.min(...vals) : Math.max(...vals);
        if (dc[m.id] === best) score += 1;
      });
      return { ...dc, score };
    }).sort((a, b) => b.score - a.score);
  }

  $: ranked = rankFacilities();

  function barWidth(dc, metId) {
    const vals = compared.map(d => d[metId]);
    const max  = Math.max(...vals);
    const min  = Math.min(...vals);
    const m    = allMetrics.find(m => m.id === metId);
    if (max === min) return 60;
    if (m.lower) return (1 - (dc[metId] - min) / (max - min)) * 70 + 30;
    return ((dc[metId] - min) / (max - min)) * 70 + 30;
  }

  function isBest(dc, metId) {
    const b = bestFor(metId);
    return b && b.id === dc.id;
  }

  function riskColor(risk) {
    return risk === 'green' ? '#2cad84' : risk === 'amber' ? '#b79563' : '#d35d5c';
  }

  function doExport() {
    generating = true;
    setTimeout(() => { generating = false; exported = true; }, 1800);
  }

  const facilityColors = ['#2cad84', '#7faeff', '#b79563', '#d35d5c'];
  $: colorMap = Object.fromEntries(compared.map((dc, i) => [dc.id, facilityColors[i]]));

  $: activeMetricDef = metrics.find(m => m.id === metric) || metrics[0];
  $: maxVal = Math.max(...compared.map(dc => dc[metric]));
</script>

<div class="cr-wrap">
  <!-- Left: facility picker + controls -->
  <aside class="cr-sidebar">
    <div class="cr-panel">
      <div class="cr-panel-title">
        <svg width="14" height="14" viewBox="0 0 20 20" fill="none">
          <rect x="2" y="2" width="7" height="7" rx="1.5" stroke="#2cad84" stroke-width="1.6"/>
          <rect x="11" y="2" width="7" height="7" rx="1.5" stroke="#7faeff" stroke-width="1.6"/>
          <rect x="2" y="11" width="7" height="7" rx="1.5" stroke="#b79563" stroke-width="1.6"/>
          <rect x="11" y="11" width="7" height="7" rx="1.5" stroke="#d35d5c" stroke-width="1.6"/>
        </svg>
        Select Facilities
      </div>
      <p class="cr-hint">Pick 2–4 to compare</p>

      <div class="facility-list">
        {#each facilities as dc}
          {@const active = selected.includes(dc.id)}
          {@const idx = selected.indexOf(dc.id)}
          <button
            class="fac-row"
            class:fac-active={active}
            class:fac-disabled={!active && selected.length >= 4}
            on:click={() => toggle(dc.id)}
            style={active ? `--fc:${facilityColors[idx]}` : ''}
          >
            <span class="fac-dot" style="background:{active ? facilityColors[idx] : 'rgba(255,255,255,0.15)'}"></span>
            <span class="fac-name">{dc.name}</span>
            <span class="fac-region">{dc.region}</span>
            <span class="fac-risk" style="color:{riskColor(dc.risk)}">●</span>
          </button>
        {/each}
      </div>
    </div>

    <div class="cr-panel">
      <div class="cr-panel-title">
        <svg width="14" height="14" viewBox="0 0 20 20" fill="none">
          <polyline points="2,15 6,8 11,11 18,3" stroke="#7faeff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Highlight Metric
      </div>
      <div class="metric-pills">
        {#each metrics as m}
          <button
            class="metric-pill"
            class:active={metric === m.id}
            style={metric === m.id ? `border-color:${m.color};color:${m.color};background:${m.color}18` : ''}
            on:click={() => metric = m.id}
          >{m.label}</button>
        {/each}
      </div>
    </div>

    <div class="cr-panel">
      <div class="cr-panel-title">
        <svg width="14" height="14" viewBox="0 0 20 20" fill="none">
          <rect x="2" y="3" width="16" height="14" rx="2" stroke="#b79563" stroke-width="1.5"/>
          <line x1="2" y1="7" x2="18" y2="7" stroke="#b79563" stroke-width="1.2"/>
        </svg>
        Timeframe
      </div>
      <div class="tf-group">
        {#each ['Q2 2026','Q1 2026','Q4 2025','Annual 2025'] as t}
          <button class="tf-btn" class:active={timeframe === t} on:click={() => timeframe = t}>{t}</button>
        {/each}
      </div>
    </div>

    <button class="export-btn" on:click={doExport} disabled={generating}>
      {#if generating}
        <span class="spin"></span> Generating…
      {:else if exported}
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><polyline points="20 6 9 17 4 12" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>
        Report ready
      {:else}
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke="currentColor" stroke-width="2"/><polyline points="7 10 12 15 17 10" stroke="currentColor" stroke-width="2"/><line x1="12" y1="15" x2="12" y2="3" stroke="currentColor" stroke-width="2"/></svg>
        Export PDF Report
      {/if}
    </button>
  </aside>

  <!-- Right: comparison content -->
  <div class="cr-main">

    <!-- Header banner -->
    <div class="cr-header">
      <div class="cr-header-left">
        <div class="cr-badge">COMPARISON REPORT</div>
        <h2>Facility vs. Facility Analysis</h2>
        <p>{compared.length} facilities · {timeframe} · {allMetrics.length} metrics evaluated</p>
      </div>
      <div class="cr-header-chips">
        {#each compared as dc, i}
          <div class="chip" style="border-color:{facilityColors[i]};color:{facilityColors[i]}">
            <span class="chip-dot" style="background:{facilityColors[i]}"></span>
            {dc.name}
          </div>
        {/each}
      </div>
    </div>

    <!-- Winner podium -->
    {#if ranked.length >= 2}
      <div class="podium-row">
        {#each ranked as dc, i}
          <div class="podium-card" class:podium-first={i === 0} style="--pc:{colorMap[dc.id]}">
            <div class="podium-rank">#{i + 1}</div>
            <div class="podium-name">{dc.name}</div>
            <div class="podium-region">{dc.region}</div>
            <div class="podium-score">
              <span class="score-num">{dc.score}</span>
              <span class="score-of">/{allMetrics.length} wins</span>
            </div>
            {#if i === 0}
              <div class="podium-crown">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M2 17L5 7L10 13L12 6L14 13L19 7L22 17H2Z" fill="currentColor" opacity="0.9"/>
                </svg>
                Best overall
              </div>
            {/if}
          </div>
        {/each}
      </div>
    {/if}

    <!-- Highlighted metric bar chart -->
    <div class="section-card">
      <div class="section-head">
        <div class="section-title">
          <svg width="14" height="14" viewBox="0 0 20 20" fill="none">
            <rect x="2" y="4" width="4" height="12" rx="1" fill="{activeMetricDef.color}" opacity="0.5"/>
            <rect x="8" y="8" width="4" height="8" rx="1" fill="{activeMetricDef.color}" opacity="0.75"/>
            <rect x="14" y="2" width="4" height="14" rx="1" fill="{activeMetricDef.color}"/>
          </svg>
          {activeMetricDef.label} — side-by-side
        </div>
        <span class="section-meta">{activeMetricDef.lower ? 'Lower is better' : 'Higher is better'}</span>
      </div>
      <div class="bar-chart">
        {#each compared as dc, i}
          {@const pct = maxVal > 0 ? (dc[metric] / maxVal) * 100 : 50}
          {@const best = isBest(dc, metric)}
          <div class="bar-row">
            <div class="bar-label">
              <span class="bar-dot" style="background:{colorMap[dc.id]}"></span>
              <span class="bar-name">{dc.name}</span>
              {#if best}<span class="best-tag" style="background:{activeMetricDef.color}18;color:{activeMetricDef.color}">Best</span>{/if}
            </div>
            <div class="bar-track">
              <div
                class="bar-fill"
                style="width:{pct}%;background:linear-gradient(90deg,{colorMap[dc.id]},{colorMap[dc.id]}88)"
                class:bar-winner={best}
              ></div>
            </div>
            <div class="bar-value" style="color:{best ? activeMetricDef.color : 'var(--text)'}">
              {dc[metric]}{activeMetricDef.unit}
            </div>
          </div>
        {/each}
      </div>
    </div>

    <!-- Full metrics table -->
    <div class="section-card">
      <div class="section-head">
        <div class="section-title">
          <svg width="14" height="14" viewBox="0 0 20 20" fill="none">
            <rect x="2" y="3" width="16" height="14" rx="2" stroke="rgba(244,247,245,0.5)" stroke-width="1.4"/>
            <line x1="2" y1="8" x2="18" y2="8" stroke="rgba(244,247,245,0.5)" stroke-width="1.2"/>
            <line x1="8" y1="3" x2="8" y2="17" stroke="rgba(244,247,245,0.5)" stroke-width="1.2"/>
          </svg>
          Full metrics table
        </div>
        <span class="section-meta">{timeframe}</span>
      </div>

      <div class="table-wrap">
        <table class="cmp-table">
          <thead>
            <tr>
              <th class="th-metric">Metric</th>
              {#each compared as dc, i}
                <th class="th-dc" style="color:{facilityColors[i]}">
                  <span class="th-dot" style="background:{facilityColors[i]}"></span>
                  {dc.name}
                </th>
              {/each}
            </tr>
          </thead>
          <tbody>
            {#each allMetrics as m}
              <tr>
                <td class="td-metric">{m.label}</td>
                {#each compared as dc}
                  {@const best = isBest(dc, m.id)}
                  <td class="td-val" class:td-best={best}>
                    {#if best}<span class="win-star">★</span>{/if}
                    {dc[m.id]}{m.unit ? ' ' + m.unit : ''}
                  </td>
                {/each}
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Risk & compliance summary -->
    <div class="section-card">
      <div class="section-head">
        <div class="section-title">
          <svg width="14" height="14" viewBox="0 0 20 20" fill="none">
            <path d="M10 2L3 6V10C3 14.4 6.1 18.5 10 19.5C13.9 18.5 17 14.4 17 10V6L10 2Z" stroke="#b79563" stroke-width="1.5" fill="none"/>
          </svg>
          Risk &amp; CSRD exposure
        </div>
      </div>
      <div class="risk-grid">
        {#each compared as dc, i}
          <div class="risk-card" style="border-color:{colorMap[dc.id]}22">
            <div class="risk-header" style="border-bottom:1px solid {colorMap[dc.id]}22">
              <span class="risk-dot" style="background:{colorMap[dc.id]}"></span>
              <span class="risk-dcname">{dc.name}</span>
              <span class="risk-region">{dc.region}</span>
            </div>
            <div class="risk-body">
              <div class="risk-row">
                <span>Climate risk</span>
                <span class="risk-badge" style="color:{riskColor(dc.risk)};background:{riskColor(dc.risk)}18">
                  {dc.risk.charAt(0).toUpperCase() + dc.risk.slice(1)}
                </span>
              </div>
              <div class="risk-row">
                <span>CSRD exposure</span>
                <span class="risk-badge" style="
                  color:{dc.csrdExposure === 'None' ? '#2cad84' : dc.csrdExposure === 'Low' ? '#2cad84' : dc.csrdExposure === 'Medium' ? '#b79563' : '#d35d5c'};
                  background:{dc.csrdExposure === 'None' || dc.csrdExposure === 'Low' ? 'rgba(44,173,132,0.12)' : dc.csrdExposure === 'Medium' ? 'rgba(183,149,99,0.12)' : 'rgba(211,93,92,0.12)'}
                ">{dc.csrdExposure}</span>
              </div>
              <div class="risk-row">
                <span>Trend</span>
                <span class="risk-badge" style="color:{dc.trend.startsWith('-') ? '#2cad84' : '#d35d5c'};background:{dc.trend.startsWith('-') ? 'rgba(44,173,132,0.12)' : 'rgba(211,93,92,0.12)'}">
                  {dc.trend} YoY
                </span>
              </div>
              <div class="risk-row">
                <span>2035 forecast</span>
                <span style="color:var(--text);font-weight:600">{dc.forecast2035} gCO₂/kWh</span>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>

    <!-- Insight callouts -->
    <div class="insights-row">
      {#each [
        {
          icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 22C12 22 3 16 3 9C3 5.1 7.1 2 12 2C16.9 2 21 5.1 21 9C21 16 12 22 12 22Z" stroke="#2cad84" stroke-width="1.8" fill="none"/><circle cx="12" cy="9" r="2.5" fill="#2cad84"/></svg>`,
          label: 'Lowest carbon intensity',
          value: (() => { const b = bestFor('intensity'); return b ? b.name : '—'; })(),
          sub:   (() => { const b = bestFor('intensity'); return b ? b.intensity + ' gCO₂/kWh' : ''; })(),
          color: '#2cad84',
        },
        {
          icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="7" height="7" rx="1" stroke="#7faeff" stroke-width="1.8"/><rect x="14" y="3" width="7" height="7" rx="1" stroke="#7faeff" stroke-width="1.8"/><rect x="3" y="14" width="7" height="7" rx="1" stroke="#7faeff" stroke-width="1.8"/><rect x="14" y="14" width="7" height="7" rx="1" stroke="#7faeff" stroke-width="1.8"/></svg>`,
          label: 'Best PUE',
          value: (() => { const b = bestFor('pue'); return b ? b.name : '—'; })(),
          sub:   (() => { const b = bestFor('pue'); return b ? 'PUE ' + b.pue : ''; })(),
          color: '#7faeff',
        },
        {
          icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" fill="#b79563" opacity="0.9"/></svg>`,
          label: 'Most renewable energy',
          value: (() => { const b = bestFor('renewable'); return b ? b.name : '—'; })(),
          sub:   (() => { const b = bestFor('renewable'); return b ? b.renewable + '% renewable' : ''; })(),
          color: '#b79563',
        },
        {
          icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12" stroke="#2cad84" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
          label: 'Best 2035 forecast',
          value: (() => { const b = bestFor('forecast2035'); return b ? b.name : '—'; })(),
          sub:   (() => { const b = bestFor('forecast2035'); return b ? b.forecast2035 + ' gCO₂/kWh by 2035' : ''; })(),
          color: '#2cad84',
        },
      ] as ins}
        <div class="insight-card" style="border-color:{ins.color}22">
          <div class="ins-icon" style="background:{ins.color}15;color:{ins.color}">{@html ins.icon}</div>
          <div class="ins-body">
            <div class="ins-label">{ins.label}</div>
            <div class="ins-value" style="color:{ins.color}">{ins.value}</div>
            <div class="ins-sub">{ins.sub}</div>
          </div>
        </div>
      {/each}
    </div>

  </div>
</div>

<style>
  .cr-wrap {
    display: grid;
    grid-template-columns: 260px 1fr;
    gap: 20px;
    height: 100%;
  }

  /* Sidebar */
  .cr-sidebar {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }

  .cr-panel {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 16px;
  }

  .cr-panel-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--ts);
    margin-bottom: 6px;
  }

  .cr-hint {
    font-size: 11px;
    color: var(--tm);
    margin: 0 0 12px;
  }

  .facility-list {
    display: flex;
    flex-direction: column;
    gap: 3px;
    max-height: 320px;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: rgba(255,255,255,0.1) transparent;
  }

  .fac-row {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 7px 10px;
    border-radius: 9px;
    border: 1px solid transparent;
    background: transparent;
    color: var(--ts);
    font-size: 12px;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.15s ease;
    text-align: left;
    width: 100%;
  }

  .fac-row:hover:not(.fac-disabled) {
    background: rgba(255,255,255,0.05);
    color: var(--text);
  }

  .fac-active {
    background: rgba(255,255,255,0.05) !important;
    border-color: var(--fc, rgba(255,255,255,0.12)) !important;
    color: var(--text) !important;
  }

  .fac-disabled {
    opacity: 0.35;
    cursor: not-allowed;
  }

  .fac-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    flex-shrink: 0;
    transition: background 0.2s;
  }

  .fac-name {
    flex: 1;
    font-weight: 600;
    font-size: 12px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .fac-region {
    font-size: 10px;
    color: var(--tm);
    white-space: nowrap;
  }

  .fac-risk {
    font-size: 9px;
    flex-shrink: 0;
  }

  .metric-pills {
    display: flex;
    flex-direction: column;
    gap: 5px;
    margin-top: 8px;
  }

  .metric-pill {
    padding: 7px 12px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.1);
    background: transparent;
    color: var(--tm);
    font-size: 12px;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.15s ease;
    text-align: left;
  }

  .metric-pill.active {
    font-weight: 700;
  }

  .metric-pill:hover:not(.active) {
    background: rgba(255,255,255,0.05);
    color: var(--ts);
  }

  .tf-group {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5px;
    margin-top: 8px;
  }

  .tf-btn {
    padding: 7px 8px;
    border-radius: 7px;
    border: 1px solid rgba(255,255,255,0.08);
    background: transparent;
    color: var(--tm);
    font-size: 11px;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .tf-btn.active {
    background: rgba(44,173,132,0.15);
    border-color: rgba(44,173,132,0.4);
    color: #2cad84;
  }

  .tf-btn:hover:not(.active) {
    background: rgba(255,255,255,0.05);
    color: var(--ts);
  }

  .export-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px 16px;
    border-radius: 12px;
    border: none;
    background: linear-gradient(135deg, #d2e8dd, #f0dfbc);
    color: #07110f;
    font-size: 13px;
    font-weight: 700;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.25), 0 3px 8px rgba(44,173,132,0.15);
  }

  .export-btn:hover:not(:disabled) {
    filter: brightness(1.05);
    transform: translateY(-1px);
  }

  .export-btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .spin {
    width: 14px;
    height: 14px;
    border: 2px solid rgba(0,0,0,0.2);
    border-top-color: #07110f;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    flex-shrink: 0;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  /* Main content */
  .cr-main {
    display: flex;
    flex-direction: column;
    gap: 16px;
    overflow-y: auto;
  }

  /* Header banner */
  .cr-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    background: linear-gradient(135deg, rgba(44,173,132,0.08), rgba(127,174,255,0.05));
    border: 1px solid rgba(44,173,132,0.18);
    border-radius: 16px;
    padding: 20px 24px;
  }

  .cr-badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    background: rgba(44,173,132,0.15);
    border: 1px solid rgba(44,173,132,0.3);
    color: #2cad84;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.1em;
    margin-bottom: 8px;
  }

  .cr-header h2 {
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--text);
    margin: 0 0 4px;
  }

  .cr-header p {
    font-size: 12px;
    color: var(--tm);
    margin: 0;
  }

  .cr-header-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    flex-shrink: 0;
  }

  .chip {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 999px;
    border: 1px solid;
    font-size: 11px;
    font-weight: 700;
    background: rgba(255,255,255,0.04);
  }

  .chip-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
  }

  /* Podium */
  .podium-row {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 12px;
  }

  .podium-card {
    background: var(--panel);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 16px;
    position: relative;
    transition: border-color 0.2s;
    border-top: 3px solid var(--pc);
  }

  .podium-first {
    background: linear-gradient(135deg, rgba(44,173,132,0.08), rgba(255,255,255,0.03));
    border-color: rgba(44,173,132,0.25);
  }

  .podium-rank {
    font-size: 11px;
    font-weight: 800;
    color: var(--tm);
    letter-spacing: 0.05em;
    margin-bottom: 6px;
  }

  .podium-name {
    font-size: 15px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.02em;
    margin-bottom: 2px;
  }

  .podium-region {
    font-size: 10.5px;
    color: var(--tm);
    margin-bottom: 12px;
  }

  .podium-score {
    display: flex;
    align-items: baseline;
    gap: 3px;
  }

  .score-num {
    font-size: 26px;
    font-weight: 900;
    letter-spacing: -0.04em;
    color: var(--pc);
  }

  .score-of {
    font-size: 11px;
    color: var(--tm);
    font-weight: 500;
  }

  .podium-crown {
    display: flex;
    align-items: center;
    gap: 5px;
    margin-top: 10px;
    padding: 5px 10px;
    border-radius: 999px;
    background: rgba(44,173,132,0.12);
    color: #2cad84;
    font-size: 11px;
    font-weight: 700;
    width: fit-content;
  }

  /* Section cards */
  .section-card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 14px;
    overflow: hidden;
  }

  .section-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 18px;
    border-bottom: 1px solid var(--line);
  }

  .section-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    font-weight: 700;
    color: var(--text);
  }

  .section-meta {
    font-size: 11px;
    color: var(--tm);
  }

  /* Bar chart */
  .bar-chart {
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }

  .bar-row {
    display: grid;
    grid-template-columns: 200px 1fr 80px;
    align-items: center;
    gap: 12px;
  }

  .bar-label {
    display: flex;
    align-items: center;
    gap: 8px;
    min-width: 0;
  }

  .bar-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .bar-name {
    font-size: 13px;
    font-weight: 600;
    color: var(--ts);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .best-tag {
    padding: 2px 7px;
    border-radius: 999px;
    font-size: 10px;
    font-weight: 700;
    flex-shrink: 0;
  }

  .bar-track {
    height: 10px;
    background: rgba(255,255,255,0.06);
    border-radius: 999px;
    overflow: hidden;
  }

  .bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.6s cubic-bezier(0.4,0,0.2,1);
  }

  .bar-winner {
    box-shadow: 0 0 10px currentColor;
  }

  .bar-value {
    font-size: 13px;
    font-weight: 700;
    text-align: right;
    font-variant-numeric: tabular-nums;
  }

  /* Table */
  .table-wrap {
    overflow-x: auto;
  }

  .cmp-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12.5px;
  }

  .cmp-table th {
    padding: 10px 14px;
    text-align: left;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--tm);
    border-bottom: 1px solid var(--line);
    background: rgba(255,255,255,0.02);
    white-space: nowrap;
  }

  .th-dc {
    text-align: center !important;
  }

  .th-dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    margin-right: 6px;
    vertical-align: middle;
  }

  .cmp-table td {
    padding: 9px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    color: var(--ts);
  }

  .cmp-table tr:last-child td {
    border-bottom: none;
  }

  .cmp-table tr:hover td {
    background: rgba(255,255,255,0.025);
  }

  .td-metric {
    font-weight: 600;
    color: var(--ts);
    white-space: nowrap;
  }

  .td-val {
    text-align: center;
    font-variant-numeric: tabular-nums;
    font-weight: 500;
  }

  .td-best {
    color: #2cad84 !important;
    font-weight: 700 !important;
    background: rgba(44,173,132,0.06) !important;
  }

  .win-star {
    font-size: 10px;
    margin-right: 3px;
    opacity: 0.8;
  }

  /* Risk grid */
  .risk-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
    padding: 16px;
  }

  .risk-card {
    background: var(--bg2);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    overflow: hidden;
  }

  .risk-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 14px;
  }

  .risk-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .risk-dcname {
    font-size: 13px;
    font-weight: 700;
    color: var(--text);
    flex: 1;
  }

  .risk-region {
    font-size: 10px;
    color: var(--tm);
  }

  .risk-body {
    padding: 10px 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .risk-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: var(--tm);
  }

  .risk-badge {
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
  }

  /* Insights */
  .insights-row {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 12px;
  }

  .insight-card {
    background: var(--panel);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 16px;
    display: flex;
    gap: 12px;
    align-items: flex-start;
    transition: border-color 0.2s;
  }

  .ins-icon {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    display: grid;
    place-items: center;
    flex-shrink: 0;
  }

  .ins-body {
    min-width: 0;
  }

  .ins-label {
    font-size: 11px;
    color: var(--tm);
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 600;
  }

  .ins-value {
    font-size: 16px;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-bottom: 2px;
  }

  .ins-sub {
    font-size: 11px;
    color: var(--tm);
  }

  @media (max-width: 1100px) {
    .cr-wrap {
      grid-template-columns: 1fr;
    }
    .cr-sidebar {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    }
    .bar-row {
      grid-template-columns: 140px 1fr 60px;
    }
  }
</style>
