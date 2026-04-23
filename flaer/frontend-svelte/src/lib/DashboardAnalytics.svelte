<script>
  const facilities = [
    { value: 'nv', label: 'Northern Virginia, USA', risk: 'High risk', ci: '412 gCO₂/kWh', cap: '240 MW capacity',
      pue: { val: '1.82', dashArr: '100 163', color: '#d35d5c', bar: 66 },
      wue: { val: '2.1', dashArr: '116 163', color: '#b67e3d', bar: 70 },
      cue: { val: '0.88', dashArr: '130 163', color: '#d35d5c', bar: 80 },
      renew: 22, fossil: 78, water: '504M L/yr', co2Total: '412,000 tCO₂',
      s1: '~5%', s2: '~90%', s3: '~5%', s1w: 5, s2w: 90, s3w: 5 },
    { value: 'sgp', label: 'Singapore', risk: 'High risk', ci: '408 gCO₂/kWh', cap: '180 MW capacity',
      pue: { val: '1.75', dashArr: '95 163', color: '#d35d5c', bar: 62 },
      wue: { val: '2.4', dashArr: '128 163', color: '#d35d5c', bar: 78 },
      cue: { val: '0.82', dashArr: '120 163', color: '#d35d5c', bar: 75 },
      renew: 18, fossil: 82, water: '432M L/yr', co2Total: '408,000 tCO₂',
      s1: '~4%', s2: '~92%', s3: '~4%', s1w: 4, s2w: 92, s3w: 4 },
    { value: 'fra', label: 'Frankfurt, Germany', risk: 'Medium risk', ci: '284 gCO₂/kWh', cap: '320 MW capacity',
      pue: { val: '1.52', dashArr: '75 163', color: '#b67e3d', bar: 50 },
      wue: { val: '1.6', dashArr: '88 163', color: '#2cad84', bar: 55 },
      cue: { val: '0.55', dashArr: '90 163', color: '#b67e3d', bar: 58 },
      renew: 45, fossil: 55, water: '320M L/yr', co2Total: '284,000 tCO₂',
      s1: '~6%', s2: '~86%', s3: '~8%', s1w: 6, s2w: 86, s3w: 8 },
    { value: 'war', label: 'Warsaw, Poland', risk: 'Low risk', ci: '234 gCO₂/kWh', cap: '120 MW capacity',
      pue: { val: '1.44', dashArr: '70 163', color: '#2cad84', bar: 46 },
      wue: { val: '1.4', dashArr: '77 163', color: '#2cad84', bar: 48 },
      cue: { val: '0.42', dashArr: '69 163', color: '#2cad84', bar: 44 },
      renew: 58, fossil: 42, water: '168M L/yr', co2Total: '234,000 tCO₂',
      s1: '~5%', s2: '~87%', s3: '~8%', s1w: 5, s2w: 87, s3w: 8 },
    { value: 'sto', label: 'Stockholm, Sweden', risk: 'Low risk', ci: '22 gCO₂/kWh', cap: '90 MW capacity',
      pue: { val: '1.18', dashArr: '40 163', color: '#2cad84', bar: 22 },
      wue: { val: '0.9', dashArr: '50 163', color: '#2cad84', bar: 30 },
      cue: { val: '0.04', dashArr: '7 163', color: '#2cad84', bar: 5 },
      renew: 92, fossil: 8, water: '81M L/yr', co2Total: '22,000 tCO₂',
      s1: '~3%', s2: '~84%', s3: '~13%', s1w: 3, s2w: 84, s3w: 13 },
  ];

  let selectedIdx = 0;
  $: dc = facilities[selectedIdx];
</script>

<div class="analytics-header">
  <select class="dc-select" bind:value={selectedIdx} on:change={e => selectedIdx = parseInt(e.target.value)}>
    {#each facilities as f, i}
      <option value={i}>{f.label}</option>
    {/each}
  </select>
  <div class="dc-tag">{dc.risk}</div>
  <div class="dc-tag">{dc.ci}</div>
  <div class="dc-tag">{dc.cap}</div>
</div>

<div class="metrics-row">
  <div class="metric-card">
    <h4>PUE — Power Usage Effectiveness</h4>
    <div class="gauge-wrap">
      <div class="gauge-arc">
        <svg viewBox="0 0 64 64">
          <circle cx="32" cy="32" r="26" fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="8"/>
          <circle cx="32" cy="32" r="26" fill="none" stroke={dc.pue.color} stroke-width="8"
            stroke-dasharray={dc.pue.dashArr} stroke-dashoffset="41" stroke-linecap="round"
            transform="rotate(-90 32 32)"/>
        </svg>
      </div>
      <div>
        <div class="gauge-label">{dc.pue.val}</div>
        <div class="gauge-sub">Industry avg: 1.5–2.0</div>
      </div>
    </div>
    <div class="gauge-target">Above target — aim for &lt;1.2</div>
    <div class="track"><div class="fill" style="width:{dc.pue.bar}%;background:{dc.pue.color};"></div></div>
  </div>

  <div class="metric-card">
    <h4>WUE — Water Usage Effectiveness</h4>
    <div class="gauge-wrap">
      <div class="gauge-arc">
        <svg viewBox="0 0 64 64">
          <circle cx="32" cy="32" r="26" fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="8"/>
          <circle cx="32" cy="32" r="26" fill="none" stroke={dc.wue.color} stroke-width="8"
            stroke-dasharray={dc.wue.dashArr} stroke-dashoffset="41" stroke-linecap="round"
            transform="rotate(-90 32 32)"/>
        </svg>
      </div>
      <div>
        <div class="gauge-label">{dc.wue.val}</div>
        <div class="gauge-sub">L/kWh · target &lt;1.8</div>
      </div>
    </div>
    <div class="gauge-target">Cooling review needed</div>
    <div class="track"><div class="fill" style="width:{dc.wue.bar}%;background:{dc.wue.color};"></div></div>
  </div>

  <div class="metric-card">
    <h4>CUE — Carbon Usage Effectiveness</h4>
    <div class="gauge-wrap">
      <div class="gauge-arc">
        <svg viewBox="0 0 64 64">
          <circle cx="32" cy="32" r="26" fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="8"/>
          <circle cx="32" cy="32" r="26" fill="none" stroke={dc.cue.color} stroke-width="8"
            stroke-dasharray={dc.cue.dashArr} stroke-dashoffset="41" stroke-linecap="round"
            transform="rotate(-90 32 32)"/>
        </svg>
      </div>
      <div>
        <div class="gauge-label">{dc.cue.val}</div>
        <div class="gauge-sub">kg CO₂/kWh · lower better</div>
      </div>
    </div>
    <div class="gauge-target">Grid intensity driving this</div>
    <div class="track"><div class="fill" style="width:{dc.cue.bar}%;background:{dc.cue.color};"></div></div>
  </div>
</div>

<div class="analytics-bottom">
  <div class="mix-card">
    <h4>Energy mix — {dc.label.split(',')[0]}</h4>
    <div class="mix-layout">
      <svg viewBox="0 0 120 120" width="108" height="108">
        <circle cx="60" cy="60" r="44" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="18"/>
        <circle cx="60" cy="60" r="44" fill="none" stroke="#2cad84" stroke-width="18"
          stroke-dasharray={`${Math.round(dc.renew/100*277)} 277`}
          stroke-dashoffset="0" transform="rotate(-90 60 60)"/>
        <circle cx="60" cy="60" r="44" fill="none" stroke="#d35d5c" stroke-width="18"
          stroke-dasharray={`${Math.round(dc.fossil/100*277)} 277`}
          stroke-dashoffset={-Math.round(dc.renew/100*277)}
          transform="rotate(-90 60 60)"/>
        <text x="60" y="56" text-anchor="middle" font-size="16" font-weight="900" fill="#f4f7f5" font-family="Inter,sans-serif">{dc.renew}%</text>
        <text x="60" y="70" text-anchor="middle" font-size="9" fill="rgba(244,247,245,0.5)" font-family="Inter,sans-serif">renewable</text>
      </svg>
      <div class="mix-rows">
        <div class="mix-row"><span>Renewable (solar/wind/hydro)</span><strong style="color:#2cad84">{dc.renew}%</strong></div>
        <div style="height:1px;background:rgba(255,255,255,0.07);margin:4px 0;"></div>
        <div class="mix-row"><span>Fossil fuels (coal/gas)</span><strong style="color:#d35d5c">{dc.fossil}%</strong></div>
        <div style="height:1px;background:rgba(255,255,255,0.07);margin:4px 0;"></div>
        <div class="mix-row"><span>Annual water use</span><strong>{dc.water}</strong></div>
        <div class="mix-row"><span>Annual CO₂ total</span><strong style="color:#d35d5c">{dc.co2Total}</strong></div>
      </div>
    </div>
  </div>

  <div class="scope-card">
    <h4>Scope 1 / 2 / 3 emissions breakdown</h4>
    <div class="scope-rows">
      <div class="scope-row">
        <div class="scope-label"><strong>Scope 1</strong><span>Direct — backup generators</span></div>
        <div class="scope-bar"><div class="scope-fill" style="width:{dc.s1w}%;background:#b67e3d;"></div></div>
        <div class="scope-pct" style="color:#b67e3d">{dc.s1}</div>
      </div>
      <div class="scope-row">
        <div class="scope-label"><strong>Scope 2</strong><span>Indirect — purchased electricity</span></div>
        <div class="scope-bar"><div class="scope-fill" style="width:{dc.s2w}%;background:#d35d5c;"></div></div>
        <div class="scope-pct" style="color:#d35d5c">{dc.s2}</div>
      </div>
      <div class="scope-row">
        <div class="scope-label"><strong>Scope 3</strong><span>Supply chain &amp; indirect</span></div>
        <div class="scope-bar"><div class="scope-fill" style="width:{dc.s3w}%;background:#2cad84;"></div></div>
        <div class="scope-pct" style="color:#2cad84">{dc.s3}</div>
      </div>
      <div class="co2-total-box">
        <div class="co2-label">Annual CO₂ total</div>
        <div class="co2-val">{dc.co2Total}</div>
      </div>
    </div>
  </div>
</div>

<style>
  .analytics-header { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; }

  .dc-select {
    padding: 9px 13px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.12);
    background: rgba(255,255,255,0.07);
    color: var(--text);
    font-size: 13px;
    font-weight: 700;
    font-family: inherit;
    min-width: 240px;
    cursor: pointer;
  }

  .dc-select option { background: #0b1714; color: #f4f7f5; }

  .dc-tag {
    padding: 7px 11px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
    border: 1px solid rgba(255,255,255,0.09);
    color: var(--ts);
  }

  .metrics-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 14px; }

  .metric-card { padding: 18px; border-radius: 22px; background: var(--panel); border: 1px solid var(--line); }

  .metric-card h4 {
    font-size: 10px;
    font-weight: 800;
    color: var(--tm);
    text-transform: uppercase;
    letter-spacing: 0.09em;
    margin-bottom: 10px;
  }

  .gauge-wrap { display: flex; align-items: center; gap: 14px; margin-bottom: 10px; }
  .gauge-arc { position: relative; width: 64px; height: 64px; flex-shrink: 0; }
  .gauge-arc svg { width: 100%; height: 100%; }
  .gauge-label { font-size: 20px; font-weight: 900; letter-spacing: -0.04em; color: var(--text); }
  .gauge-sub { font-size: 11px; color: var(--ts); margin-top: 3px; }
  .gauge-target { font-size: 11px; color: var(--tm); margin-bottom: 8px; }
  .track { height: 5px; border-radius: 999px; background: rgba(255,255,255,0.08); overflow: hidden; }
  .fill { height: 100%; border-radius: 999px; transition: width 0.4s ease; }

  .analytics-bottom { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }

  .mix-card, .scope-card { padding: 18px; border-radius: 22px; background: var(--panel); border: 1px solid var(--line); }
  .mix-card h4, .scope-card h4 { font-size: 13px; font-weight: 900; color: var(--text); margin-bottom: 14px; }

  .mix-layout { display: flex; align-items: center; gap: 18px; }
  .mix-rows { flex: 1; display: grid; gap: 9px; }
  .mix-row { display: flex; justify-content: space-between; align-items: center; font-size: 12px; }
  .mix-row span { color: var(--ts); }

  .scope-rows { display: grid; gap: 9px; }

  .scope-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 11px 13px;
    border-radius: 14px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
  }

  .scope-label { flex: 1; }
  .scope-label strong { display: block; font-size: 12px; font-weight: 800; color: var(--text); }
  .scope-label span { font-size: 11px; color: var(--tm); }
  .scope-pct { font-size: 18px; font-weight: 900; letter-spacing: -0.03em; }
  .scope-bar { flex: 1; height: 5px; border-radius: 999px; background: rgba(255,255,255,0.08); overflow: hidden; }
  .scope-fill { height: 100%; border-radius: 999px; }

  .co2-total-box {
    padding: 14px;
    border-radius: 14px;
    background: rgba(44,173,132,0.07);
    border: 1px solid rgba(44,173,132,0.16);
    margin-top: 4px;
  }

  .co2-label { font-size: 11px; color: var(--tm); margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.07em; }
  .co2-val { font-size: 24px; font-weight: 900; letter-spacing: -0.04em; color: var(--text); }
</style>
