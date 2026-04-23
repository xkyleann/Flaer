<script>
  let activeFilter = 'all';
  let selectedDC = null;

  const dataCenters = [
    { id: 'nv', name: 'N. Virginia', region: 'US East', risk: 'high', cx: 215, cy: 100, co2: '412 gCO₂/kWh', cap: '240 MW', pue: '1.82', renew: '22%' },
    { id: 'ca', name: 'California', region: 'US West', risk: 'med', cx: 95, cy: 88, co2: '220 gCO₂/kWh', cap: '160 MW', pue: '1.65', renew: '48%' },
    { id: 'sto', name: 'Stockholm', region: 'Nordic', risk: 'low', cx: 490, cy: 61, co2: '22 gCO₂/kWh', cap: '90 MW', pue: '1.18', renew: '92%' },
    { id: 'fra', name: 'Frankfurt', region: 'EU West', risk: 'med', cx: 462, cy: 70, co2: '284 gCO₂/kWh', cap: '320 MW', pue: '1.52', renew: '45%' },
    { id: 'war', name: 'Warsaw', region: 'EU Central', risk: 'low', cx: 396, cy: 57, co2: '234 gCO₂/kWh', cap: '120 MW', pue: '1.44', renew: '58%' },
    { id: 'sgp', name: 'Singapore', region: 'APAC', risk: 'high', cx: 790, cy: 174, co2: '408 gCO₂/kWh', cap: '180 MW', pue: '1.75', renew: '18%' },
    { id: 'tky', name: 'Tokyo', region: 'APAC', risk: 'med', cx: 858, cy: 84, co2: '340 gCO₂/kWh', cap: '200 MW', pue: '1.60', renew: '32%' },
    { id: 'syd', name: 'Sydney', region: 'ANZ', risk: 'low', cx: 858, cy: 290, co2: '180 gCO₂/kWh', cap: '100 MW', pue: '1.38', renew: '65%' },
    { id: 'dxb', name: 'Dubai', region: 'ME', risk: 'med', cx: 645, cy: 172, co2: '310 gCO₂/kWh', cap: '140 MW', pue: '1.70', renew: '28%' },
    { id: 'bra', name: 'São Paulo', region: 'LATAM', risk: 'low', cx: 220, cy: 278, co2: '120 gCO₂/kWh', cap: '85 MW', pue: '1.42', renew: '74%' },
  ];

  function riskColor(r) {
    if (r === 'high') return '#d35d5c';
    if (r === 'med') return '#b67e3d';
    return '#2cad84';
  }

  function riskBg(r) {
    if (r === 'high') return 'rgba(211,93,92,0.12)';
    if (r === 'med') return 'rgba(182,126,61,0.12)';
    return 'rgba(44,173,132,0.16)';
  }

  $: filtered = dataCenters.filter(dc => {
    if (activeFilter === 'all') return true;
    if (activeFilter === 'high') return dc.risk === 'high';
    if (activeFilter === 'med') return dc.risk === 'med';
    if (activeFilter === 'low') return dc.risk === 'low';
    if (activeFilter === 'eu') return ['fra', 'war', 'sto'].includes(dc.id);
    return true;
  });
</script>

<div class="gmap-filters">
  {#each [['all','All facilities'],['high','High risk'],['med','Medium risk'],['low','Low risk'],['eu','EU regulated']] as [val, lbl]}
    <button class="gf-chip" class:on={activeFilter === val} on:click={() => activeFilter = val}>{lbl}</button>
  {/each}
</div>

<div class="gmap-layout">
  <div>
    <div class="gmap-wrap">
      <svg viewBox="0 0 1000 420" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="gland" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#1e332d"/>
            <stop offset="100%" stop-color="#162420"/>
          </linearGradient>
          <filter id="gcglow">
            <feGaussianBlur stdDeviation="6" result="b"/>
            <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
        </defs>
        <rect width="1000" height="420" fill="#0a1412"/>
        <path d="M60,55 L100,40 L160,37 L220,43 L260,50 L280,74 L275,104 L260,130 L240,152 L210,166 L185,174 L160,178 L140,168 L120,154 L100,144 L80,126 L65,100Z" fill="url(#gland)" stroke="#274039" stroke-width="1"/>
        <path d="M280,22 L330,16 L350,30 L340,50 L310,55 L285,44Z" fill="url(#gland)" stroke="#274039" stroke-width="1"/>
        <path d="M185,198 L240,193 L265,207 L275,240 L270,276 L255,304 L235,326 L210,334 L190,320 L175,292 L170,260 L175,228Z" fill="url(#gland)" stroke="#274039" stroke-width="1"/>
        <path d="M418,48 L450,43 L490,45 L520,53 L530,72 L520,95 L500,109 L475,113 L450,107 L425,97 L410,78Z" fill="url(#gland)" stroke="#274039" stroke-width="1"/>
        <path d="M392,50 L408,44 L415,57 L405,70 L390,64Z" fill="url(#gland)" stroke="#274039" stroke-width="1"/>
        <path d="M448,22 L490,17 L510,27 L505,47 L480,52 L455,44Z" fill="url(#gland)" stroke="#274039" stroke-width="1"/>
        <path d="M420,126 L495,121 L530,136 L545,168 L540,210 L525,246 L505,274 L475,287 L445,282 L420,263 L405,230 L400,192 L405,158Z" fill="url(#gland)" stroke="#274039" stroke-width="1"/>
        <path d="M530,98 L590,93 L620,107 L625,130 L600,142 L560,139 L535,124Z" fill="url(#gland)" stroke="#274039" stroke-width="1"/>
        <path d="M500,22 L700,15 L780,30 L790,56 L760,74 L700,79 L620,77 L540,72 L505,58Z" fill="url(#gland)" stroke="#274039" stroke-width="1"/>
        <path d="M700,56 L800,48 L840,60 L850,88 L835,116 L800,130 L760,132 L720,125 L695,106 L692,82Z" fill="url(#gland)" stroke="#274039" stroke-width="1"/>
        <path d="M750,140 L800,133 L820,148 L815,170 L790,177 L760,168 L745,153Z" fill="url(#gland)" stroke="#274039" stroke-width="1"/>
        <path d="M780,240 L870,230 L910,244 L920,282 L900,314 L860,325 L815,320 L780,300 L770,268Z" fill="url(#gland)" stroke="#274039" stroke-width="1"/>
        <path d="M620,136 L660,130 L685,144 L695,176 L685,204 L665,218 L645,213 L625,194 L610,166 L612,148Z" fill="url(#gland)" stroke="#274039" stroke-width="1"/>
        <g filter="url(#gcglow)">
          {#each filtered as dc}
            <circle cx={dc.cx} cy={dc.cy} r="16" fill={riskBg(dc.risk)}/>
            <circle cx={dc.cx} cy={dc.cy} r="7" fill={riskColor(dc.risk)}
              style="cursor:pointer"
              on:click={() => selectedDC = dc}/>
          {/each}
        </g>
      </svg>
      <div class="map-legend-abs">
        <div class="ml-item"><span class="ml-dot" style="background:#d35d5c"></span>High risk</div>
        <div class="ml-item"><span class="ml-dot" style="background:#b67e3d"></span>Medium</div>
        <div class="ml-item"><span class="ml-dot" style="background:#2cad84"></span>Low risk</div>
      </div>
    </div>
  </div>

  <div class="dc-panel">
    {#if selectedDC}
      <div class="dc-panel-header">
        <h3>{selectedDC.name}</h3>
        <span class="dc-risk-badge" style="background:{riskBg(selectedDC.risk)};color:{riskColor(selectedDC.risk)}">{selectedDC.risk} risk</span>
      </div>
      <div class="dc-panel-body">
        <div class="dc-stat-grid">
          <div class="dc-stat">
            <div class="sl">Carbon Intensity</div>
            <div class="sv">{selectedDC.co2}</div>
          </div>
          <div class="dc-stat">
            <div class="sl">Capacity</div>
            <div class="sv">{selectedDC.cap}</div>
          </div>
          <div class="dc-stat">
            <div class="sl">PUE</div>
            <div class="sv">{selectedDC.pue}</div>
          </div>
          <div class="dc-stat">
            <div class="sl">Renewable</div>
            <div class="sv">{selectedDC.renew}</div>
          </div>
        </div>
        <div class="dc-section-title">Region</div>
        <div class="dc-row"><span>Location</span><strong>{selectedDC.region}</strong></div>
      </div>
    {:else}
      <div class="dc-panel-placeholder">
        <svg width="40" height="40" viewBox="0 0 20 20" fill="none">
          <circle cx="10" cy="10" r="7" stroke="rgba(244,247,245,0.3)" stroke-width="1.5"/>
          <ellipse cx="10" cy="10" rx="3.5" ry="7" stroke="rgba(244,247,245,0.3)" stroke-width="1.2"/>
          <line x1="3" y1="10" x2="17" y2="10" stroke="rgba(244,247,245,0.3)" stroke-width="1.2"/>
        </svg>
        <p>Click a facility on the map to view details</p>
      </div>
    {/if}
  </div>
</div>

<style>
  .gmap-filters { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }

  .gf-chip {
    padding: 7px 13px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.09);
    background: rgba(255,255,255,0.05);
    color: rgba(244,247,245,0.7);
    font-size: 12px;
    font-weight: 800;
    cursor: pointer;
    transition: 0.14s;
    font-family: inherit;
  }

  .gf-chip.on { background: rgba(44,173,132,0.18); border-color: rgba(44,173,132,0.30); color: #b6ffe7; }

  .gmap-layout { display: grid; grid-template-columns: 1fr 340px; gap: 14px; align-items: start; }

  .gmap-wrap {
    position: relative;
    border-radius: 22px;
    overflow: hidden;
    background: linear-gradient(180deg, #091310, #060e0c);
    border: 1px solid rgba(255,255,255,0.08);
  }

  .gmap-wrap svg { width: 100%; display: block; }

  .map-legend-abs {
    position: absolute;
    right: 12px;
    bottom: 12px;
    display: flex;
    gap: 9px;
    padding: 8px 11px;
    border-radius: 999px;
    background: rgba(6,14,12,0.90);
    border: 1px solid rgba(255,255,255,0.07);
  }

  .ml-item { display: flex; align-items: center; gap: 5px; font-size: 10px; font-weight: 700; color: rgba(244,247,245,0.7); }
  .ml-dot { width: 7px; height: 7px; border-radius: 50%; }

  .dc-panel {
    border-radius: 24px;
    background: linear-gradient(180deg, rgba(255,255,255,0.07), rgba(255,255,255,0.04));
    border: 1px solid rgba(255,255,255,0.09);
    overflow: hidden;
    min-height: 400px;
  }

  .dc-panel-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: 32px;
    text-align: center;
    color: rgba(244,247,245,0.3);
    gap: 12px;
    min-height: 400px;
    font-size: 13px;
  }

  .dc-panel-header {
    padding: 16px 18px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .dc-panel-header h3 { font-size: 15px; font-weight: 900; color: #f4f7f5; margin-bottom: 4px; }
  
  .dc-status-badge {
    font-size: 11px;
    font-weight: 700;
    color: rgba(244,247,245,0.6);
    margin-top: 2px;
  }
  
  .dc-status-badge.planned {
    color: #7facff;
  }

  .dc-risk-badge {
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 10px;
    font-weight: 900;
    text-transform: capitalize;
  }

  .dc-panel-body { padding: 16px; }

  .dc-stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 14px; }

  .dc-stat {
    padding: 12px;
    border-radius: 16px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    transition: all 0.2s ease;
  }
  
  .dc-stat:hover {
    background: rgba(255,255,255,0.08);
    border-color: rgba(44,173,132,0.2);
  }

  .dc-stat .sl { font-size: 10px; color: rgba(244,247,245,0.46); font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 5px; }
  .dc-stat .sv { font-size: 20px; font-weight: 900; letter-spacing: -0.04em; color: #f4f7f5; transition: color 0.2s; }
  .dc-stat .sv.excellent { color: #2cad84; }

  .dc-section-title { font-size: 12px; font-weight: 800; color: rgba(244,247,245,0.54); text-transform: uppercase; letter-spacing: 0.09em; margin: 14px 0 8px; }

  .dc-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 13px; }
  .dc-row:last-child { border-bottom: none; }
  .dc-row span { color: rgba(244,247,245,0.56); }
  .dc-row strong { color: #f4f7f5; }
  
  .planning-recommendation {
    margin-top: 16px;
    padding: 14px;
    border-radius: 16px;
    background: rgba(44,173,132,0.08);
    border: 1px solid rgba(44,173,132,0.2);
  }
  
  .pr-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    font-size: 13px;
    font-weight: 800;
    color: #2cad84;
  }
  
  .planning-recommendation p {
    font-size: 12px;
    line-height: 1.6;
    color: rgba(244,247,245,0.7);
    margin: 0;
  }
  
  @media (max-width: 1200px) {
    .gmap-layout {
      grid-template-columns: 1fr;
    }
    
    .dc-panel {
      min-height: 300px;
    }
  }
</style>
