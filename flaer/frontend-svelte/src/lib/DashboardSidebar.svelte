<script>
  export let activeScreen = 'portfolio';
  export let setScreen;

  const coreItems = [
    {
      id: 'portfolio',
      title: 'Portfolio review',
      subtitle: 'Where are we exposed?',
      badge: { text: '14', cls: 'nb-red' },
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="7" stroke="#2cad84" stroke-width="1.6"/><ellipse cx="10" cy="10" rx="3.5" ry="7" stroke="#2cad84" stroke-width="1.2"/><line x1="3" y1="10" x2="17" y2="10" stroke="#2cad84" stroke-width="1.2"/></svg>`
    },
    {
      id: 'forecast',
      title: '2035 forecast',
      subtitle: 'Where are we going?',
      badge: null,
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><polyline points="2,16 6,9 11,12 18,4" stroke="#7faeff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/><circle cx="18" cy="4" r="2" fill="#7faeff"/></svg>`
    },
    {
      id: 'actions',
      title: 'Recommended actions',
      subtitle: 'What should we do?',
      badge: { text: '3', cls: 'nb-gold' },
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><rect x="2" y="12" width="4" height="6" rx="1" fill="#b79563" opacity="0.5"/><rect x="8" y="7" width="4" height="11" rx="1" fill="#b79563" opacity="0.75"/><rect x="14" y="2" width="4" height="16" rx="1" fill="#b79563"/></svg>`
    },
  ];

  const deepItems = [
    {
      id: 'analytics',
      title: 'Facility analytics',
      subtitle: 'PUE · WUE · CUE · Mix',
      badge: null,
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="5" stroke="#2cad84" stroke-width="1.6"/><circle cx="10" cy="10" r="2" fill="#2cad84"/><line x1="10" y1="2" x2="10" y2="6" stroke="#2cad84" stroke-width="1.6" stroke-linecap="round"/><line x1="10" y1="14" x2="10" y2="18" stroke="#2cad84" stroke-width="1.6" stroke-linecap="round"/><line x1="2" y1="10" x2="6" y2="10" stroke="#2cad84" stroke-width="1.6" stroke-linecap="round"/><line x1="14" y1="10" x2="18" y2="10" stroke="#2cad84" stroke-width="1.6" stroke-linecap="round"/></svg>`
    },
    {
      id: 'globalmap',
      title: 'Global map',
      subtitle: 'All facilities · live stats',
      badge: { text: 'Live', cls: 'nb-green' },
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="7" stroke="#b79563" stroke-width="1.6"/><ellipse cx="10" cy="10" rx="3.5" ry="7" stroke="#b79563" stroke-width="1.2"/><line x1="3" y1="10" x2="17" y2="10" stroke="#b79563" stroke-width="1.2"/></svg>`
    },
    {
      id: 'siteiq',
      title: 'Site intelligence',
      subtitle: 'Plan your next facility',
      badge: { text: 'New', cls: 'nb-gold' },
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="7" r="4" stroke="#7faeff" stroke-width="1.6"/><path d="M10 11 C5 11 3 17 3 17 L17 17 C17 17 15 11 10 11Z" stroke="#7faeff" stroke-width="1.4" fill="none" stroke-linejoin="round"/></svg>`
    },
    {
      id: 'benchmark',
      title: 'Benchmark',
      subtitle: 'vs. industry peers',
      badge: { text: 'New', cls: 'nb-green' },
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><rect x="2" y="4" width="16" height="12" rx="2" stroke="rgba(244,247,245,0.5)" stroke-width="1.5"/><line x1="7" y1="8" x2="7" y2="14" stroke="rgba(244,247,245,0.5)" stroke-width="1.3" stroke-linecap="round"/><line x1="10" y1="6" x2="10" y2="14" stroke="#2cad84" stroke-width="1.6" stroke-linecap="round"/><line x1="13" y1="10" x2="13" y2="14" stroke="rgba(244,247,245,0.5)" stroke-width="1.3" stroke-linecap="round"/></svg>`
    },
    {
      id: 'calculator',
      title: 'Carbon calculator',
      subtitle: 'Model your impact',
      badge: null,
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><rect x="3" y="3" width="14" height="14" rx="3" stroke="#7faeff" stroke-width="1.6"/><line x1="10" y1="3" x2="10" y2="17" stroke="#7faeff" stroke-width="1.2" opacity="0.6"/><line x1="3" y1="9" x2="17" y2="9" stroke="#7faeff" stroke-width="1.2" opacity="0.6"/><line x1="3" y1="14" x2="17" y2="14" stroke="#7faeff" stroke-width="1.2" opacity="0.6"/></svg>`
    },
    {
      id: 'reports',
      title: 'Climate Reports',
      subtitle: 'CSRD · EED · SFDR',
      badge: { text: 'New', cls: 'nb-gold' },
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><rect x="4" y="2" width="12" height="16" rx="2" stroke="#b79563" stroke-width="1.6"/><line x1="7" y1="6" x2="13" y2="6" stroke="#b79563" stroke-width="1.3" stroke-linecap="round"/><line x1="7" y1="9" x2="13" y2="9" stroke="#b79563" stroke-width="1.3" stroke-linecap="round"/><line x1="7" y1="12" x2="11" y2="12" stroke="#b79563" stroke-width="1.3" stroke-linecap="round"/></svg>`
    },
  ];
</script>

<aside class="sidebar">
  <div class="health-card">
    <div class="health-label">Portfolio health score</div>
    <div class="health-score">72 <span>/ 100</span></div>
    <div class="health-sub">Moderate exposure — 14 sites require action</div>
    <div class="health-bar"><div class="health-fill"></div></div>
  </div>

  <div class="nav-section">
    <div class="nav-section-label">Core workflow</div>
    {#each coreItems as item}
      <button
        class="nav-item"
        class:active={activeScreen === item.id}
        on:click={() => setScreen(item.id)}
      >
        <div class="nav-icon">{@html item.icon}</div>
        <div class="nav-text">
          <strong>{item.title}</strong>
          <span>{item.subtitle}</span>
        </div>
        {#if item.badge}
          <span class="nav-badge {item.badge.cls}">{item.badge.text}</span>
        {/if}
      </button>
    {/each}
  </div>

  <div class="nav-section">
    <div class="nav-section-label">Deep analysis</div>
    {#each deepItems as item}
      <button
        class="nav-item"
        class:active={activeScreen === item.id}
        on:click={() => setScreen(item.id)}
      >
        <div class="nav-icon">{@html item.icon}</div>
        <div class="nav-text">
          <strong>{item.title}</strong>
          <span>{item.subtitle}</span>
        </div>
        {#if item.badge}
          <span class="nav-badge {item.badge.cls}">{item.badge.text}</span>
        {/if}
      </button>
    {/each}
  </div>

  <div class="sidebar-footer">
    <p>Export board-ready reports or share this workspace with your sustainability team.</p>
    <button class="gen-btn">Generate executive brief</button>
  </div>
</aside>

<style>
  .sidebar {
    border-right: 1px solid rgba(255,255,255,0.06);
    background: rgba(255,255,255,0.018);
    padding: 18px 12px;
    position: sticky;
    top: 60px;
    height: calc(100vh - 60px);
    overflow-y: auto;
    overflow-x: hidden;
    display: flex;
    flex-direction: column;
    gap: 0;
    scrollbar-width: thin;
    scrollbar-color: rgba(255,255,255,0.1) transparent;
  }
  .sidebar::-webkit-scrollbar { width: 4px; }
  .sidebar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 4px; }

  .health-card {
    padding: 16px;
    border-radius: 16px;
    background: linear-gradient(135deg, rgba(44,173,132,0.1), rgba(127,174,255,0.06));
    border: 1px solid rgba(44,173,132,0.15);
    margin-bottom: 18px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.06);
  }

  .health-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--tm);
    margin-bottom: 8px;
  }

  .health-score {
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -0.05em;
    color: var(--text);
    line-height: 1;
    margin-bottom: 4px;
  }

  .health-score span {
    font-size: 15px;
    color: var(--g2);
    font-weight: 600;
    margin-left: 3px;
  }

  .health-sub {
    font-size: 11.5px;
    color: var(--ts);
    margin-bottom: 12px;
    line-height: 1.4;
    letter-spacing: -0.01em;
  }

  .health-bar {
    height: 4px;
    border-radius: 999px;
    background: rgba(255,255,255,0.07);
    overflow: hidden;
  }

  .health-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--g2), var(--blue));
    width: 72%;
    box-shadow: 0 0 8px rgba(44,173,132,0.4);
  }

  .nav-section {
    margin-bottom: 4px;
  }

  .nav-section-label {
    padding: 10px 10px 5px;
    color: var(--tm);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }

  .nav-item {
    display: flex;
    gap: 10px;
    align-items: center;
    padding: 9px 10px;
    border-radius: 12px;
    margin-bottom: 2px;
    color: var(--ts);
    border: 1px solid transparent;
    cursor: pointer;
    transition: background 0.16s ease, color 0.16s ease, border-color 0.16s ease;
    background: transparent;
    width: 100%;
    text-align: left;
    font-family: inherit;
  }

  .nav-item:hover {
    background: rgba(255,255,255,0.045);
    color: var(--text);
  }

  .nav-item.active {
    background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.045));
    border-color: rgba(255,255,255,0.09);
    color: var(--text);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.06);
  }

  .nav-icon {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    display: grid;
    place-items: center;
    flex-shrink: 0;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.07);
    transition: background 0.16s ease;
  }

  .nav-item.active .nav-icon {
    background: rgba(255,255,255,0.08);
    border-color: rgba(255,255,255,0.12);
  }

  .nav-text {
    min-width: 0;
    flex: 1;
  }

  .nav-text strong {
    display: block;
    font-size: 12.5px;
    font-weight: 700;
    letter-spacing: -0.02em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .nav-text span {
    display: block;
    font-size: 10.5px;
    color: var(--tm);
    margin-top: 1px;
    letter-spacing: -0.01em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .nav-badge {
    margin-left: auto;
    padding: 2px 7px;
    border-radius: 999px;
    font-size: 10px;
    font-weight: 700;
    flex-shrink: 0;
    letter-spacing: 0;
  }

  .nb-red   { background: var(--rs); color: #ffd6d6; }
  .nb-gold  { background: var(--gos); color: #ffe4bc; }
  .nb-green { background: var(--gs); color: #c8ffe8; }

  .sidebar-footer {
    margin-top: auto;
    padding: 13px;
    border-radius: 14px;
    background: linear-gradient(180deg, rgba(255,255,255,0.055), rgba(255,255,255,0.025));
    border: 1px solid rgba(255,255,255,0.07);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
  }

  .sidebar-footer p {
    color: var(--tm);
    font-size: 11.5px;
    line-height: 1.5;
    margin-bottom: 10px;
    letter-spacing: -0.01em;
  }

  .gen-btn {
    width: 100%;
    padding: 9px;
    border: none;
    border-radius: 9px;
    background: linear-gradient(135deg, #d2e8dd, #f0dfbc);
    color: #07110f;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    font-family: inherit;
    transition: filter 0.2s ease, transform 0.2s ease;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.25), 0 2px 6px rgba(44,173,132,0.12);
  }
  .gen-btn:hover {
    filter: brightness(1.05);
    transform: translateY(-1px);
  }
</style>
