<script>
  let activeScenario = 0;

  const scenarios = [
    { title: 'SSP5-8.5 — High warming', desc: 'Steeper demand growth, elevated cooling stress, grid intensity increases.' },
    { title: 'Balanced transition', desc: 'Moderate grid decarbonisation and incremental operational improvement.' },
    { title: 'Optimised pathway', desc: 'Renewable procurement, cooling upgrades, and workload relocation combined.' },
    { title: 'Custom assumptions', desc: 'Apply your own renewable, capacity, and intensity assumptions.' },
  ];
</script>

<div class="forecast-layout">
  <div class="panel">
    <div class="panel-head">
      <div>
        <h3>2030 / 2035 emissions forecast — N. Virginia cluster</h3>
        <div class="sub">Business-as-usual vs. optimized path under SSP5-8.5 climate scenario</div>
      </div>
      <div class="pill blue">SSP5-8.5</div>
    </div>
    <div class="panel-body">
      <svg viewBox="0 0 820 320" width="100%" style="overflow:visible">
        <defs>
          <clipPath id="fc"><rect x="64" y="10" width="720" height="260"/></clipPath>
        </defs>
        <line x1="64" y1="270" x2="784" y2="270" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        <line x1="64" y1="210" x2="784" y2="210" stroke="rgba(255,255,255,0.07)" stroke-width="1" stroke-dasharray="4,5"/>
        <line x1="64" y1="150" x2="784" y2="150" stroke="rgba(255,255,255,0.07)" stroke-width="1" stroke-dasharray="4,5"/>
        <line x1="64" y1="90" x2="784" y2="90" stroke="rgba(255,255,255,0.07)" stroke-width="1" stroke-dasharray="4,5"/>
        <line x1="64" y1="30" x2="784" y2="30" stroke="rgba(255,255,255,0.07)" stroke-width="1" stroke-dasharray="4,5"/>
        <line x1="64" y1="270" x2="64" y2="10" stroke="rgba(255,255,255,0.07)" stroke-width="1"/>
        <text x="52" y="274" text-anchor="end" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">0</text>
        <text x="52" y="214" text-anchor="end" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">50k</text>
        <text x="52" y="154" text-anchor="end" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">100k</text>
        <text x="52" y="94" text-anchor="end" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">150k</text>
        <text x="52" y="34" text-anchor="end" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">200k</text>
        <text x="100" y="290" text-anchor="middle" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">2025</text>
        <text x="208" y="290" text-anchor="middle" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">2027</text>
        <text x="352" y="290" text-anchor="middle" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">2030</text>
        <text x="532" y="290" text-anchor="middle" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">2033</text>
        <text x="712" y="290" text-anchor="middle" font-size="10" fill="rgba(244,247,245,0.4)" font-family="Inter,sans-serif">2035</text>
        <line x1="64" y1="128" x2="784" y2="128" stroke="rgba(183,149,99,0.8)" stroke-width="1.2" stroke-dasharray="6,6"/>
        <text x="790" y="132" font-size="9" fill="rgba(255,224,180,0.75)" font-family="Inter,sans-serif">EED threshold</text>
        <polygon points="100,238 208,218 352,184 532,136 712,76 712,270 100,270" fill="rgba(211,93,92,0.07)" clip-path="url(#fc)"/>
        <polygon points="100,238 208,230 352,218 532,204 712,196 712,270 100,270" fill="rgba(44,173,132,0.09)" clip-path="url(#fc)"/>
        <polyline points="100,238 208,218 352,184 532,136 712,76" stroke="#d35d5c" stroke-width="2.8" fill="none" stroke-linecap="round" stroke-linejoin="round" clip-path="url(#fc)"/>
        <polyline points="100,238 208,230 352,218 532,204 712,196" stroke="#2cad84" stroke-width="2.8" fill="none" stroke-linecap="round" stroke-linejoin="round" clip-path="url(#fc)"/>
        <circle cx="352" cy="184" r="5" fill="#d35d5c"/>
        <circle cx="352" cy="218" r="5" fill="#2cad84"/>
        <line x1="352" y1="184" x2="352" y2="218" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>
        <rect x="360" y="168" rx="10" ry="10" width="110" height="34" fill="rgba(8,16,15,0.92)" stroke="rgba(255,255,255,0.09)"/>
        <text x="372" y="182" font-size="9" fill="rgba(244,247,245,0.5)" font-family="Inter,sans-serif">Milestone 2030</text>
        <text x="372" y="196" font-size="10" fill="#f4f7f5" font-family="Inter,sans-serif" font-weight="700">Cooling upgrade</text>
        <circle cx="532" cy="204" r="5" fill="#2cad84"/>
        <rect x="542" y="188" rx="10" ry="10" width="110" height="34" fill="rgba(8,16,15,0.92)" stroke="rgba(255,255,255,0.09)"/>
        <text x="554" y="202" font-size="9" fill="rgba(244,247,245,0.5)" font-family="Inter,sans-serif">Milestone 2033</text>
        <text x="554" y="216" font-size="10" fill="#f4f7f5" font-family="Inter,sans-serif" font-weight="700">Workload shift</text>
        <circle cx="712" cy="76" r="5" fill="#d35d5c"/>
        <circle cx="712" cy="196" r="5" fill="#2cad84"/>
        <text x="668" y="68" font-size="10" fill="#d35d5c" font-family="Inter,sans-serif" font-weight="900">BAU</text>
        <text x="634" y="210" font-size="10" fill="#2cad84" font-family="Inter,sans-serif" font-weight="900">Optimized −38%</text>
      </svg>
    </div>
  </div>

  <div class="scenario-list">
    {#each scenarios as scenario, i}
      <div
        class="scenario"
        class:active={activeScenario === i}
        on:click={() => activeScenario = i}
      >
        <div class="scenario-selector">
          <h4>{scenario.title}</h4>
          <span class="scenario-dot"></span>
        </div>
        <p>{scenario.desc}</p>
      </div>
    {/each}
  </div>
</div>

<div class="impact-row">
  <div class="impact-cell">
    <div class="label">Projected CO₂ reduction</div>
    <div class="value" style="color:#2cad84">−38%</div>
    <div class="note">By 2035 under optimised path</div>
  </div>
  <div class="impact-cell">
    <div class="label">Annual energy cost saved</div>
    <div class="value">€2.1M</div>
    <div class="note">Modelled annualised savings</div>
  </div>
  <div class="impact-cell">
    <div class="label">Water use reduction</div>
    <div class="value">−25%</div>
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
  }

  .pill.blue { background: var(--bs); color: #dce8ff; }

  .scenario-list { display: grid; gap: 9px; }

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
  }

  .scenario.active .scenario-dot {
    background: var(--blue);
    border-color: var(--blue);
  }

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
  }

  .impact-cell .note { color: var(--ts); font-size: 12px; }
</style>
