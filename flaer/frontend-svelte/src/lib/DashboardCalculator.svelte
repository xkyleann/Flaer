<script>
  let mw = 100;
  let ci = 400;
  let rn = 50;
  let pu = 14;
  let calculationStatus = 'Inputs update instantly';

  $: puVal = (pu / 10).toFixed(1);
  $: baseline = Math.round(mw * 1000 * 8760 * (ci / 1000000));
  $: optimised = Math.round(baseline * (1 - rn / 100) * (1.0 / (pu / 10)));
  $: saved = Math.max(0, baseline - optimised);
  $: costSaved = (saved * 0.12 / 1000).toFixed(1);
  $: cars = Math.round(saved / 4.6 / 1000);
  $: trees = Math.round(saved * 46);
  $: homes = Math.round(saved / 7.2);

  function fmt(n) {
    if (n >= 1000000) return (n / 1000000).toFixed(2) + 'M';
    if (n >= 1000) return (n / 1000).toFixed(0) + 'K';
    return n.toString();
  }

  function recalculate() {
    calculationStatus = `Updated ${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
  }
</script>

<div class="calc-grid">
  <div class="calc-panel">
    <h3>Carbon impact calculator</h3>
    <p>Model how operational changes affect emissions, costs, and real-world equivalents.</p>

    <div class="field">
      <label>Power capacity (MW) — <span>{mw}</span> MW</label>
      <input type="range" min="10" max="500" bind:value={mw}/>
      <div class="range-ends"><span>10 MW</span><span>500 MW</span></div>
    </div>

    <div class="field">
      <label>Current carbon intensity — <span>{ci}</span> gCO₂/kWh</label>
      <input type="range" min="15" max="900" bind:value={ci}/>
      <div class="range-ends"><span>15 gCO₂</span><span>900 gCO₂</span></div>
    </div>

    <div class="field">
      <label>Renewable energy target — <span>{rn}</span>%</label>
      <input type="range" min="0" max="100" bind:value={rn}/>
      <div class="range-ends"><span>0%</span><span>100%</span></div>
    </div>

    <div class="field">
      <label>PUE improvement — <span>{puVal}</span></label>
      <input type="range" min="10" max="25" bind:value={pu}/>
      <div class="range-ends"><span>1.0 (perfect)</span><span>2.5 (poor)</span></div>
    </div>

    <button class="calc-btn" on:click={recalculate}>Recalculate</button>
    <div class="calc-status" role="status">{calculationStatus}</div>
  </div>

  <div class="calc-panel">
    <h3>Projected results</h3>
    <p>Annual operational estimates based on your inputs.</p>

    <div class="results-grid">
      <div class="result-item">
        <div class="label">Baseline CO₂ emissions</div>
        <div class="value">{fmt(baseline)} tCO₂</div>
        <div class="note">Before renewable integration</div>
      </div>
      <div class="result-item">
        <div class="label">Optimised CO₂ emissions</div>
        <div class="value" style="color:#2cad84">{fmt(optimised)} tCO₂</div>
        <div class="note">After renewable &amp; PUE target</div>
      </div>
      <div class="result-item">
        <div class="label">Annual energy cost savings</div>
        <div class="value" style="color:#2cad84">€{costSaved}M</div>
        <div class="note">At €0.12/kWh average rate</div>
      </div>
    </div>

    <div class="equiv-grid">
      <div class="equiv">
        <div class="big">{fmt(cars)}K</div>
        <div class="desc">Cars removed from roads</div>
      </div>
      <div class="equiv">
        <div class="big">{fmt(trees)}M</div>
        <div class="desc">Trees equivalent planted</div>
      </div>
      <div class="equiv">
        <div class="big">{fmt(homes)}K</div>
        <div class="desc">Homes powered by savings</div>
      </div>
      <div class="equiv">
        <div class="big">5–8yr</div>
        <div class="desc">Typical ROI payback</div>
      </div>
    </div>
  </div>
</div>

<style>
  .calc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

  .calc-panel {
    padding: 22px;
    border-radius: 26px;
    background: var(--panel);
    border: 1px solid var(--line);
  }

  .calc-panel h3 { font-size: 16px; font-weight: 900; color: var(--text); margin-bottom: 5px; }
  .calc-panel > p { color: var(--ts); font-size: 13px; margin-bottom: 18px; }
  .calc-status { margin-top: 9px; color: var(--tm); font-size: 10px; }

  .field { margin-bottom: 16px; }

  .field label {
    display: block;
    color: var(--ts);
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 7px;
  }

  .field input[type=range] { width: 100%; accent-color: var(--g2); }

  .range-ends {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: var(--tm);
    margin-top: 4px;
  }

  .calc-btn {
    width: 100%;
    padding: 13px;
    border: none;
    border-radius: 999px;
    background: linear-gradient(135deg, #d2e8dd, #f0dfbc);
    color: #07110f;
    font-size: 14px;
    font-weight: 900;
    cursor: pointer;
    font-family: inherit;
    margin-top: 4px;
  }

  .results-grid { display: grid; gap: 10px; margin-bottom: 14px; }

  .result-item {
    padding: 14px;
    border-radius: 18px;
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--line);
  }

  .result-item .label { font-size: 11px; color: var(--tm); text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 5px; }
  .result-item .value { font-size: 24px; font-weight: 900; letter-spacing: -0.04em; color: var(--text); }
  .result-item .note { font-size: 11px; color: var(--ts); margin-top: 3px; }

  .equiv-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 9px; }

  .equiv {
    padding: 14px;
    border-radius: 16px;
    background: rgba(44,173,132,0.07);
    border: 1px solid rgba(44,173,132,0.14);
    text-align: center;
  }

  .equiv .big { font-size: 22px; font-weight: 900; color: var(--g2); letter-spacing: -0.04em; }
  .equiv .desc { font-size: 10px; color: var(--ts); margin-top: 4px; }
</style>
