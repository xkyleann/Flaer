<script>
  const pueData = [
    { name: 'Your portfolio', val: 1.52, max: 2.5, you: true },
    { name: 'Hyperscale avg', val: 1.30, max: 2.5 },
    { name: 'EU colos', val: 1.58, max: 2.5 },
    { name: 'APAC avg', val: 1.74, max: 2.5 },
    { name: 'Global avg', val: 1.59, max: 2.5 },
  ];

  const ciData = [
    { name: 'Your portfolio', val: 284, max: 600, you: true },
    { name: 'EU peers', val: 320, max: 600 },
    { name: 'US peers', val: 390, max: 600 },
    { name: 'APAC peers', val: 440, max: 600 },
    { name: 'Global avg', val: 380, max: 600 },
  ];

  const renewData = [
    { name: 'Your portfolio', val: 34, max: 100, you: true },
    { name: 'Top quartile', val: 72, max: 100 },
    { name: 'Median', val: 41, max: 100 },
    { name: 'Bottom quartile', val: 18, max: 100 },
  ];

  const wueData = [
    { name: 'Your portfolio', val: 1.6, max: 3.0, you: true },
    { name: 'Best in class', val: 0.8, max: 3.0 },
    { name: 'Industry avg', val: 1.8, max: 3.0 },
    { name: 'Worst quartile', val: 2.6, max: 3.0 },
  ];
</script>

<div class="bench-grid">
  <div class="bench-card">
    <h3>PUE comparison — industry benchmark</h3>
    <div class="bench-legend">
      <div class="bl-item"><span class="bl-dot you"></span>Your facility</div>
      <div class="bl-item"><span class="bl-dot peer"></span>Peer average</div>
    </div>
    {#each pueData as row}
      <div class="bench-row">
        <div class="bench-name">{row.name}</div>
        <div class="bench-track">
          <div class="bench-fill" class:bench-you={row.you} style="width:{(row.val/row.max*100).toFixed(1)}%"></div>
        </div>
        <div class="bench-val">{row.val}</div>
      </div>
    {/each}
  </div>

  <div class="bench-card">
    <h3>Carbon intensity — global peer comparison</h3>
    <div class="bench-legend">
      <div class="bl-item"><span class="bl-dot you"></span>Your facility</div>
      <div class="bl-item"><span class="bl-dot peer"></span>Peer avg</div>
    </div>
    {#each ciData as row}
      <div class="bench-row">
        <div class="bench-name">{row.name}</div>
        <div class="bench-track">
          <div class="bench-fill" class:bench-you={row.you} style="width:{(row.val/row.max*100).toFixed(1)}%"></div>
        </div>
        <div class="bench-val">{row.val} g</div>
      </div>
    {/each}
  </div>

  <div class="bench-card">
    <h3>Renewable share — portfolio vs. peers</h3>
    {#each renewData as row}
      <div class="bench-row">
        <div class="bench-name">{row.name}</div>
        <div class="bench-track">
          <div class="bench-fill" class:bench-you={row.you} style="width:{row.val}%"></div>
        </div>
        <div class="bench-val">{row.val}%</div>
      </div>
    {/each}
  </div>

  <div class="bench-card">
    <h3>WUE — water efficiency comparison</h3>
    {#each wueData as row}
      <div class="bench-row">
        <div class="bench-name">{row.name}</div>
        <div class="bench-track">
          <div class="bench-fill" class:bench-you={row.you} style="width:{(row.val/row.max*100).toFixed(1)}%"></div>
        </div>
        <div class="bench-val">{row.val}</div>
      </div>
    {/each}
  </div>
</div>

<style>
  .bench-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }

  .bench-card {
    padding: 20px;
    border-radius: 24px;
    background: var(--panel);
    border: 1px solid var(--line);
  }

  .bench-card h3 { font-size: 14px; font-weight: 900; color: var(--text); margin-bottom: 14px; }

  .bench-legend { display: flex; gap: 14px; margin-bottom: 12px; }
  .bl-item { display: flex; align-items: center; gap: 6px; font-size: 11px; color: var(--ts); }

  .bl-dot { width: 9px; height: 9px; border-radius: 50%; }
  .bl-dot.you { background: linear-gradient(90deg, #2cad84, #7faeff); }
  .bl-dot.peer { background: rgba(255,255,255,0.25); }

  .bench-row { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
  .bench-row:last-child { margin-bottom: 0; }

  .bench-name { font-size: 12px; color: var(--ts); width: 110px; flex-shrink: 0; }

  .bench-track {
    flex: 1;
    height: 8px;
    border-radius: 999px;
    background: rgba(255,255,255,0.07);
    overflow: hidden;
  }

  .bench-fill {
    height: 100%;
    border-radius: 999px;
    background: rgba(255,255,255,0.18);
    transition: width 0.4s ease;
  }

  .bench-fill.bench-you {
    background: linear-gradient(90deg, var(--g2), #7faeff);
  }

  .bench-val { font-size: 11px; font-weight: 800; color: var(--text); width: 52px; text-align: right; }
</style>
