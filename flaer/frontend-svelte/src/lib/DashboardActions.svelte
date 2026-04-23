<div class="actions-grid">
  <div class="action-card">
    <div class="priority p-high">High ROI</div>
    <h3>Workload shift — Frankfurt to Stockholm</h3>
    <p>Move flexible compute windows to a lower-intensity regional cluster while maintaining service-level reliability.</p>
    <div class="action-metrics">
      <div class="am-row"><span>CO₂ impact</span><strong>−18%</strong></div>
      <div class="am-row"><span>Annual savings</span><strong>€420K</strong></div>
      <div class="am-row"><span>Effort</span><strong>Medium</strong></div>
      <div class="am-row"><span>Time to value</span><strong>3 months</strong></div>
      <div class="am-row">
        <span>Confidence</span>
        <div class="confidence-bar">
          <div class="conf-track"><div class="conf-fill" style="width:92%"></div></div>
          <strong>92%</strong>
        </div>
      </div>
    </div>
    <div class="action-btns">
      <button class="btn-ghost">View assumptions</button>
      <button class="btn-solid">Simulate impact</button>
    </div>
  </div>

  <div class="action-card med">
    <div class="priority p-med">Medium ROI</div>
    <h3>Cooling optimisation — Northern Virginia</h3>
    <p>Apply targeted cooling control changes to reduce emissions intensity and water demand at the most exposed site.</p>
    <div class="action-metrics">
      <div class="am-row"><span>CO₂ impact</span><strong>−12%</strong></div>
      <div class="am-row"><span>Annual savings</span><strong>€610K</strong></div>
      <div class="am-row"><span>Effort</span><strong>Medium</strong></div>
      <div class="am-row"><span>Time to value</span><strong>2 months</strong></div>
      <div class="am-row">
        <span>Confidence</span>
        <div class="confidence-bar">
          <div class="conf-track"><div class="conf-fill" style="width:95%"></div></div>
          <strong>95%</strong>
        </div>
      </div>
    </div>
    <div class="action-btns">
      <button class="btn-ghost">View assumptions</button>
      <button class="btn-solid">Simulate impact</button>
    </div>
  </div>

  <div class="action-card str">
    <div class="priority p-str">Strategic</div>
    <h3>Renewable procurement — APAC portfolio</h3>
    <p>Increase renewable share for the most carbon-intensive APAC facilities through procurement and partnership strategy.</p>
    <div class="action-metrics">
      <div class="am-row"><span>CO₂ impact</span><strong>Long-term reduction</strong></div>
      <div class="am-row"><span>ROI payback</span><strong>5–8 years</strong></div>
      <div class="am-row"><span>Effort</span><strong>High</strong></div>
      <div class="am-row"><span>Time to value</span><strong>6–12 months</strong></div>
      <div class="am-row">
        <span>Confidence</span>
        <div class="confidence-bar">
          <div class="conf-track"><div class="conf-fill" style="width:88%"></div></div>
          <strong>88%</strong>
        </div>
      </div>
    </div>
    <div class="action-btns">
      <button class="btn-ghost">View assumptions</button>
      <button class="btn-solid">Simulate impact</button>
    </div>
  </div>
</div>

<style>
  .actions-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
  }

  .action-card {
    padding: 20px;
    border-radius: 24px;
    background: linear-gradient(180deg, rgba(255,255,255,0.075), rgba(255,255,255,0.035));
    border: 1px solid var(--line);
    position: relative;
    overflow: hidden;
  }

  .action-card::after {
    content: "";
    position: absolute;
    right: -24px;
    top: -24px;
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(44,173,132,0.14), transparent 68%);
  }

  .action-card.med::after { background: radial-gradient(circle, rgba(127,174,255,0.14), transparent 68%); }
  .action-card.str::after { background: radial-gradient(circle, rgba(183,149,99,0.14), transparent 68%); }

  .priority {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 10px;
    border-radius: 999px;
    font-size: 10px;
    font-weight: 900;
    margin-bottom: 14px;
  }

  .p-high { background: var(--gs); color: #b6ffe7; }
  .p-med { background: var(--bs); color: #dce8ff; }
  .p-str { background: var(--gos); color: #ffe9c9; }

  .action-card h3 {
    font-size: 18px;
    font-weight: 900;
    letter-spacing: -0.04em;
    color: var(--text);
    margin-bottom: 8px;
    line-height: 1.08;
    max-width: 240px;
  }

  .action-card > p {
    color: var(--ts);
    font-size: 13px;
    margin-bottom: 14px;
    min-height: 52px;
  }

  .action-metrics { display: grid; gap: 8px; margin-bottom: 14px; }

  .am-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    font-size: 12px;
    color: var(--ts);
  }

  .am-row:last-child { border-bottom: none; padding-bottom: 0; }
  .am-row strong { color: var(--text); }

  .confidence-bar { display: flex; align-items: center; gap: 8px; }

  .conf-track {
    flex: 1;
    height: 5px;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
  }

  .conf-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--g2), var(--blue));
  }

  .action-btns { display: flex; gap: 8px; margin-top: 14px; }

  .btn-ghost {
    padding: 9px 12px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.10);
    background: rgba(255,255,255,0.05);
    color: var(--text);
    font-size: 11px;
    font-weight: 800;
    cursor: pointer;
    font-family: inherit;
    transition: 0.14s;
  }

  .btn-solid {
    padding: 9px 12px;
    border-radius: 999px;
    border: none;
    background: linear-gradient(135deg, #d2e8dd, #f0dfbc);
    color: #07110f;
    font-size: 11px;
    font-weight: 900;
    cursor: pointer;
    font-family: inherit;
  }

  .btn-ghost:hover { background: rgba(255,255,255,0.09); }
</style>
