<script>
  let activeScenario = 0;
  let showAssumptions = false;
  let showSimulate = false;

  // Custom scenario sliders
  let renewablePct = 60;
  let pueTarget = 1.35;
  let workloadShift = 20;

  const scenarios = [
    {
      title: 'SSP5-8.5 — High warming',
      desc: 'Steeper demand growth, elevated cooling stress, grid intensity increases.',
      pill: 'SSP5-8.5',
      pillCls: 'red',
      reduction: -8,
      energySaved: -0.4,
      waterReduction: -5,
      reductionColor: '#d35d5c',
      reductionDisplay: '+8% increase',
      assumptions: [
        { label: 'Grid carbon intensity growth', value: '+1.8%/yr' },
        { label: 'Cooling degree days increase', value: '+12% by 2035' },
        { label: 'Demand growth rate', value: '+9%/yr' },
        { label: 'Grid renewable share', value: '22% by 2035' },
        { label: 'PUE trajectory (2025→2035)', value: '1.62 → 1.70' },
        { label: 'EU ETS carbon price', value: '$85/tCO₂e by 2030' },
        { label: 'Cooling stress events/yr', value: '18 days (up from 7)' },
      ],
    },
    {
      title: 'Balanced transition',
      desc: 'Moderate grid decarbonisation and incremental operational improvement.',
      pill: 'Balanced',
      pillCls: 'amber',
      reduction: 12,
      energySaved: 0.7,
      waterReduction: 8,
      reductionColor: '#b79563',
      reductionDisplay: '−12%',
      assumptions: [
        { label: 'Grid carbon intensity change', value: '−1.2%/yr' },
        { label: 'Grid renewable share', value: '45% by 2035' },
        { label: 'Demand growth rate', value: '+6%/yr' },
        { label: 'PUE trajectory (2025→2035)', value: '1.62 → 1.50' },
        { label: 'Cooling upgrades', value: 'Partial evaporative retrofit 2027' },
        { label: 'EU ETS carbon price', value: '$55/tCO₂e by 2030' },
        { label: 'Avoided carbon cost/yr', value: '$1.1M by 2030' },
      ],
    },
    {
      title: 'Optimised pathway',
      desc: 'Renewable procurement, cooling upgrades, and workload relocation combined.',
      pill: 'Optimised',
      pillCls: 'green',
      reduction: 38,
      energySaved: 2.1,
      waterReduction: 25,
      reductionColor: '#2cad84',
      reductionDisplay: '−38%',
      assumptions: [
        { label: 'PPA procurement', value: '80% renewable by 2027' },
        { label: 'Cooling upgrade', value: 'Free-air + adiabatic 2026' },
        { label: 'Workload shift to low-carbon', value: '25% by 2028' },
        { label: 'PUE trajectory (2025→2035)', value: '1.62 → 1.28' },
        { label: 'Grid decarbonisation (with PPAs)', value: '−3.5%/yr' },
        { label: 'Avoided carbon cost', value: '$4.2M/yr by 2030' },
        { label: 'Water intensity reduction', value: '−0.8 L/kWh by 2030' },
      ],
    },
    {
      title: 'Custom assumptions',
      desc: 'Apply your own renewable, capacity, and intensity assumptions.',
      pill: 'Custom',
      pillCls: 'blue',
    },
  ];

  function computeReduction() {
    const ren = (renewablePct / 100) * 18;
    const pue = Math.max(0, (1.62 - pueTarget) / 0.62) * 28;
    const shift = (workloadShift / 100) * 14;
    return Math.min(60, Math.round(ren + pue + shift));
  }

  $: customReduction = computeReduction();
  $: activeReduction = activeScenario === 3 ? customReduction : scenarios[activeScenario].reduction;
  $: activeColor = activeScenario === 3 ? '#7faeff' : scenarios[activeScenario].reductionColor;
  $: activeEnergySaved = activeScenario === 3
    ? +(customReduction * 0.055).toFixed(1)
    : scenarios[activeScenario].energySaved;
  $: activeWater = activeScenario === 3
    ? Math.min(35, Math.round(customReduction * 0.65))
    : scenarios[activeScenario].waterReduction;
  $: activeAssumptions = activeScenario === 3 ? [
    { label: 'Renewable procurement', value: `${renewablePct}%` },
    { label: 'PUE target', value: pueTarget.toFixed(2) },
    { label: 'Workload shift to low-carbon regions', value: `${workloadShift}%` },
    { label: 'Estimated CO₂ reduction by 2035', value: `−${customReduction}%` },
    { label: 'Estimated energy cost savings', value: `€${+(customReduction * 0.055).toFixed(1)}M/yr` },
    { label: 'Estimated water use reduction', value: `−${Math.min(35, Math.round(customReduction * 0.65))}%` },
  ] : scenarios[activeScenario].assumptions;

  // SVG optimized path — y axis: 0kt=270, 200kt=30 → scale=1.2px/kt
  // BaU 2025 = ~80kt → y=174; optimized 2035 based on reduction
  $: opt2035Y = Math.round(196 + (38 - Math.max(-8, Math.min(60, activeReduction))) * 1.55);
  $: optMid1Y = Math.round(230 + (38 - Math.max(-8, Math.min(60, activeReduction))) * 0.4);
  $: optMid2Y = Math.round(218 + (38 - Math.max(-8, Math.min(60, activeReduction))) * 0.9);
  $: optPts = `100,238 208,${optMid1Y} 352,${optMid2Y} 532,${Math.round((optMid2Y + opt2035Y)/2)} 712,${opt2035Y}`;
  $: fillPts = `100,238 ${optPts.split('100,238 ')[1]} 712,270 100,270`;
  $: optLabel = activeScenario === 3
    ? `Custom −${customReduction}%`
    : (scenarios[activeScenario].reductionDisplay ?? '');
</script>

<div class="forecast-layout">
  <div class="panel">
    <div class="panel-head">
      <div>
        <h3>2030 / 2035 emissions forecast — N. Virginia cluster</h3>
        <div class="sub">Business-as-usual vs. optimized path under selected scenario</div>
      </div>
      <div class="pill" class:red={activeScenario===0} class:amber={activeScenario===1} class:green={activeScenario===2} class:blue={activeScenario===3}>
        {scenarios[activeScenario].pill}
      </div>
    </div>
    <div class="panel-body">
      <svg viewBox="0 0 820 320" width="100%" style="overflow:visible">
        <defs>
          <clipPath id="fc"><rect x="64" y="10" width="720" height="260"/></clipPath>
        </defs>
        <!-- Grid lines -->
        <line x1="64" y1="270" x2="784" y2="270" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        <line x1="64" y1="210" x2="784" y2="210" stroke="rgba(255,255,255,0.07)" stroke-width="1" stroke-dasharray="4,5"/>
        <line x1="64" y1="150" x2="784" y2="150" stroke="rgba(255,255,255,0.07)" stroke-width="1" stroke-dasharray="4,5"/>
        <line x1="64" y1="90" x2="784" y2="90" stroke="rgba(255,255,255,0.07)" stroke-width="1" stroke-dasharray="4,5"/>
        <line x1="64" y1="30" x2="784" y2="30" stroke="rgba(255,255,255,0.07)" stroke-width="1" stroke-dasharray="4,5"/>
        <line x1="64" y1="270" x2="64" y2="10" stroke="rgba(255,255,255,0.07)" stroke-width="1"/>
        <!-- Y labels -->
        <text x="52" y="274" text-anchor="end" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">0</text>
        <text x="52" y="214" text-anchor="end" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">50k</text>
        <text x="52" y="154" text-anchor="end" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">100k</text>
        <text x="52" y="94" text-anchor="end" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">150k</text>
        <text x="52" y="34" text-anchor="end" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">200k</text>
        <!-- X labels -->
        <text x="100" y="290" text-anchor="middle" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">2025</text>
        <text x="208" y="290" text-anchor="middle" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">2027</text>
        <text x="352" y="290" text-anchor="middle" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">2030</text>
        <text x="532" y="290" text-anchor="middle" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">2033</text>
        <text x="712" y="290" text-anchor="middle" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">2035</text>
        <!-- EED threshold -->
        <line x1="64" y1="128" x2="784" y2="128" stroke="rgba(183,149,99,0.8)" stroke-width="1.2" stroke-dasharray="6,6"/>
        <text x="790" y="132" font-size="9" fill="rgba(255,224,180,0.75)" font-family="Inter,sans-serif">EED threshold</text>
        <!-- BaU fill + line -->
        <polygon points="100,238 208,218 352,184 532,136 712,76 712,270 100,270" fill="rgba(211,93,92,0.07)" clip-path="url(#fc)"/>
        <polyline points="100,238 208,218 352,184 532,136 712,76" stroke="#d35d5c" stroke-width="2.8" fill="none" stroke-linecap="round" stroke-linejoin="round" clip-path="url(#fc)"/>
        <!-- Optimized fill + line (reactive) -->
        <polygon points={fillPts} fill="rgba(44,173,132,0.09)" clip-path="url(#fc)"/>
        <polyline points={optPts} stroke={activeColor} stroke-width="2.8" fill="none" stroke-linecap="round" stroke-linejoin="round" clip-path="url(#fc)"/>
        <!-- 2030 milestone -->
        <circle cx="352" cy="184" r="5" fill="#d35d5c"/>
        <circle cx="352" cy={optMid2Y} r="5" fill={activeColor}/>
        <line x1="352" y1="184" x2="352" y2={optMid2Y} stroke="rgba(255,255,255,0.2)" stroke-width="1"/>
        <rect x="360" y="168" rx="10" ry="10" width="110" height="34" fill="rgba(8,16,15,0.92)" stroke="rgba(255,255,255,0.09)"/>
        <text x="372" y="182" font-size="9" fill="rgba(244,247,245,0.5)" font-family="Inter,sans-serif">Milestone 2030</text>
        <text x="372" y="196" font-size="10" fill="#f4f7f5" font-family="Inter,sans-serif" font-weight="700">Cooling upgrade</text>
        <!-- 2035 labels -->
        <circle cx="712" cy="76" r="5" fill="#d35d5c"/>
        <circle cx="712" cy={opt2035Y} r="5" fill={activeColor}/>
        <text x="668" y="68" font-size="10" fill="#d35d5c" font-family="Inter,sans-serif" font-weight="900">BAU</text>
        <text x="600" y={opt2035Y - 8} font-size="10" fill={activeColor} font-family="Inter,sans-serif" font-weight="900">{optLabel}</text>
      </svg>
    </div>
  </div>

  <div class="right-col">
    <div class="scenario-list">
      {#each scenarios as scenario, i}
        <div
          class="scenario"
          class:active={activeScenario === i}
          on:click={() => { activeScenario = i; showAssumptions = false; showSimulate = false; }}
        >
          <div class="scenario-selector">
            <h4>{scenario.title}</h4>
            <span class="scenario-dot"></span>
          </div>
          <p>{scenario.desc}</p>
        </div>
      {/each}
    </div>

    <div class="sc-actions">
      <button class="sc-btn" class:active={showAssumptions} on:click={() => { showAssumptions = !showAssumptions; showSimulate = false; }}>
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        View assumptions
      </button>
      <button class="sc-btn accent" class:active={showSimulate} on:click={() => { showSimulate = !showSimulate; showAssumptions = false; }}>
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
        Simulate impact
      </button>
    </div>
  </div>
</div>

<!-- Assumptions drawer -->
{#if showAssumptions}
  <div class="drawer">
    <div class="drawer-head">
      <span>Model assumptions — {scenarios[activeScenario].title}</span>
      <button class="drawer-close" on:click={() => showAssumptions = false} aria-label="Close assumptions">×</button>
    </div>
    <div class="assumptions-grid">
      {#each activeAssumptions as a}
        <div class="assum-row">
          <span class="assum-label">{a.label}</span>
          <span class="assum-val">{a.value}</span>
        </div>
      {/each}
    </div>
    <div class="drawer-note">
      Assumptions sourced from IEA 2024 World Energy Outlook, IPCC AR6, and internal operational baseline data.
      All figures are indicative estimates for planning purposes only.
    </div>
  </div>
{/if}

<!-- Simulate impact panel -->
{#if showSimulate}
  <div class="drawer">
    <div class="drawer-head">
      <span>Simulate impact — custom levers</span>
      <button class="drawer-close" on:click={() => showSimulate = false} aria-label="Close simulate">×</button>
    </div>
    <div class="sim-grid">
      <div class="sim-lever">
        <div class="sim-lever-head">
          <span class="sim-lever-label">Renewable procurement</span>
          <span class="sim-lever-val">{renewablePct}%</span>
        </div>
        <input type="range" min="0" max="100" step="5" bind:value={renewablePct} class="sim-range"/>
        <div class="sim-hints"><span>0% — grid only</span><span>100% — full PPA</span></div>
      </div>
      <div class="sim-lever">
        <div class="sim-lever-head">
          <span class="sim-lever-label">PUE target by 2030</span>
          <span class="sim-lever-val">{pueTarget.toFixed(2)}</span>
        </div>
        <input type="range" min="1.10" max="1.80" step="0.05" bind:value={pueTarget} class="sim-range"/>
        <div class="sim-hints"><span>1.10 — best in class</span><span>1.80 — BAU</span></div>
      </div>
      <div class="sim-lever">
        <div class="sim-lever-head">
          <span class="sim-lever-label">Workload shift to low-carbon regions</span>
          <span class="sim-lever-val">{workloadShift}%</span>
        </div>
        <input type="range" min="0" max="50" step="5" bind:value={workloadShift} class="sim-range"/>
        <div class="sim-hints"><span>0% — no shift</span><span>50% — max shift</span></div>
      </div>
    </div>
    <div class="sim-result">
      <div class="sim-res-row">
        <span>Estimated CO₂ reduction by 2035</span>
        <span class="sim-res-big" style="color:{customReduction >= 30 ? '#2cad84' : customReduction >= 15 ? '#b79563' : '#d35d5c'}">−{customReduction}%</span>
      </div>
      <div class="sim-res-row">
        <span>Estimated energy cost savings</span>
        <span class="sim-res-val">€{+(customReduction * 0.055).toFixed(1)}M/yr</span>
      </div>
      <div class="sim-res-row">
        <span>Water use reduction</span>
        <span class="sim-res-val">−{Math.min(35, Math.round(customReduction * 0.65))}%</span>
      </div>
      <button class="sim-apply" on:click={() => { activeScenario = 3; showSimulate = false; }}>
        Apply as custom scenario
      </button>
    </div>
  </div>
{/if}

<div class="impact-row">
  <div class="impact-cell">
    <div class="label">Projected CO₂ reduction</div>
    <div class="value" style="color:{activeColor}">{activeReduction >= 0 ? '−' : '+'}{Math.abs(activeReduction)}%</div>
    <div class="note">By 2035 under selected path</div>
  </div>
  <div class="impact-cell">
    <div class="label">Annual energy cost saved</div>
    <div class="value" style="color:{activeEnergySaved > 0 ? 'var(--text)' : '#d35d5c'}">{activeEnergySaved >= 0 ? '' : '−'}€{Math.abs(activeEnergySaved)}M</div>
    <div class="note">Modelled annualised savings</div>
  </div>
  <div class="impact-cell">
    <div class="label">Water use reduction</div>
    <div class="value" style="color:{activeWater > 0 ? 'var(--text)' : '#d35d5c'}">{activeWater >= 0 ? '−' : '+'}{Math.abs(activeWater)}%</div>
    <div class="note">Through cooling optimisation</div>
  </div>
</div>

<style>
  .forecast-layout {
    display: grid;
    grid-template-columns: 1fr 280px;
    gap: 14px;
    margin-bottom: 14px;
  }

  .right-col {
    display: flex;
    flex-direction: column;
    gap: 9px;
  }

  .panel {
    border-radius: 26px;
    overflow: hidden;
    background: linear-gradient(180deg, rgba(255,255,255,0.065), rgba(255,255,255,0.035));
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: var(--slg);
  }

  .panel-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    padding: 14px 18px;
    border-bottom: 1px solid var(--line);
  }

  .panel-head h3 { font-size: 14px; font-weight: 900; color: var(--text); }
  .panel-head .sub { font-size: 12px; color: var(--tm); margin-top: 2px; }
  .panel-body { padding: 16px; }

  .pill {
    padding: 5px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 900;
    border: 1px solid rgba(255,255,255,0.08);
    white-space: nowrap;
  }
  .pill.blue { background: var(--bs); color: #dce8ff; }
  .pill.green { background: rgba(44,173,132,0.15); color: #8ef0cc; }
  .pill.amber { background: rgba(183,149,99,0.15); color: #e8d5a0; }
  .pill.red { background: rgba(211,93,92,0.15); color: #f0a0a0; }

  .scenario-list { display: grid; gap: 9px; flex: 1; }

  .scenario {
    padding: 14px;
    border-radius: 18px;
    background: var(--panel);
    border: 1px solid var(--line);
    cursor: pointer;
    transition: 0.16s;
  }

  .scenario.active {
    background: rgba(255,255,255,0.09);
    border-color: rgba(127,174,255,0.28);
  }

  .scenario h4 { font-size: 13px; font-weight: 900; color: var(--text); margin-bottom: 5px; }
  .scenario p { font-size: 12px; color: var(--ts); }

  .scenario-selector {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .scenario-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    border: 2px solid rgba(255,255,255,0.2);
    flex-shrink: 0;
  }

  .scenario.active .scenario-dot {
    background: var(--blue);
    border-color: var(--blue);
  }

  .sc-actions {
    display: flex;
    gap: 8px;
  }

  .sc-btn {
    flex: 1;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 9px 10px;
    border-radius: 13px;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.045);
    color: var(--ts);
    font-size: 11.5px;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: 0.16s;
  }

  .sc-btn:hover, .sc-btn.active {
    background: rgba(255,255,255,0.09);
    color: var(--text);
    border-color: rgba(255,255,255,0.18);
  }

  .sc-btn.accent.active {
    background: rgba(44,173,132,0.15);
    border-color: rgba(44,173,132,0.3);
    color: #8ef0cc;
  }

  /* Drawer */
  .drawer {
    margin-bottom: 14px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.04);
    overflow: hidden;
  }

  .drawer-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    font-size: 12.5px;
    font-weight: 700;
    color: var(--text);
  }

  .drawer-close {
    background: none;
    border: none;
    color: var(--tm);
    font-size: 18px;
    cursor: pointer;
    padding: 0 4px;
    line-height: 1;
    font-family: inherit;
  }

  .drawer-close:hover { color: var(--text); }

  .assumptions-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    padding: 8px 0;
  }

  .assum-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 9px 16px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    gap: 12px;
  }

  .assum-label { font-size: 12px; color: var(--tm); }
  .assum-val { font-size: 12.5px; font-weight: 700; color: var(--text); white-space: nowrap; }

  .drawer-note {
    padding: 10px 16px;
    font-size: 11px;
    color: var(--ts);
    line-height: 1.5;
    border-top: 1px solid rgba(255,255,255,0.05);
  }

  /* Simulate panel */
  .sim-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1px;
    background: rgba(255,255,255,0.05);
    border-bottom: 1px solid rgba(255,255,255,0.07);
  }

  .sim-lever {
    padding: 14px 16px;
    background: rgba(255,255,255,0.02);
  }

  .sim-lever-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    gap: 8px;
  }

  .sim-lever-label { font-size: 11.5px; color: var(--tm); font-weight: 600; }
  .sim-lever-val { font-size: 13px; font-weight: 900; color: var(--text); white-space: nowrap; }

  .sim-range {
    width: 100%;
    accent-color: #2cad84;
    cursor: pointer;
    margin-bottom: 6px;
  }

  .sim-hints {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: var(--ts);
  }

  .sim-result {
    display: flex;
    align-items: center;
    gap: 24px;
    padding: 12px 16px;
    flex-wrap: wrap;
  }

  .sim-res-row {
    display: flex;
    flex-direction: column;
    gap: 3px;
  }

  .sim-res-row > span:first-child { font-size: 11px; color: var(--tm); }

  .sim-res-big { font-size: 22px; font-weight: 900; letter-spacing: -0.04em; }
  .sim-res-val { font-size: 16px; font-weight: 700; color: var(--text); }

  .sim-apply {
    margin-left: auto;
    padding: 8px 16px;
    border-radius: 11px;
    border: 1px solid rgba(44,173,132,0.3);
    background: rgba(44,173,132,0.12);
    color: #8ef0cc;
    font-size: 12px;
    font-weight: 700;
    font-family: inherit;
    cursor: pointer;
    transition: 0.16s;
  }

  .sim-apply:hover {
    background: rgba(44,173,132,0.22);
  }

  /* Impact row */
  .impact-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
  }

  .impact-cell {
    padding: 18px;
    border-radius: 22px;
    background: var(--panel);
    border: 1px solid var(--line);
    transition: 0.25s;
  }

  .impact-cell .label {
    color: var(--tm);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 8px;
  }

  .impact-cell .value {
    font-size: 28px;
    font-weight: 900;
    letter-spacing: -0.05em;
    color: var(--text);
    margin-bottom: 5px;
    transition: color 0.25s;
  }

  .impact-cell .note { color: var(--ts); font-size: 12px; }
</style>
