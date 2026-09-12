<script>
  export let activeScreen = 'portfolio';
  export let setScreen;

  const coreItems = [
    {
      id: 'portfolio',
      title: 'Overview',
      subtitle: 'Risk and key numbers',
      badge: { text: '14', cls: 'nb-red' },
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="7" stroke="#2cad84" stroke-width="1.6"/><ellipse cx="10" cy="10" rx="3.5" ry="7" stroke="#2cad84" stroke-width="1.2"/><line x1="3" y1="10" x2="17" y2="10" stroke="#2cad84" stroke-width="1.2"/></svg>`
    },
    {
      id: 'forecast',
      title: 'Forecast',
      subtitle: 'Future emissions',
      badge: null,
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><polyline points="2,16 6,9 11,12 18,4" stroke="#7faeff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/><circle cx="18" cy="4" r="2" fill="#7faeff"/></svg>`
    },
    {
      id: 'actions',
      title: 'Actions',
      subtitle: 'What to do next',
      badge: { text: '3', cls: 'nb-gold' },
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><rect x="2" y="12" width="4" height="6" rx="1" fill="#b79563" opacity="0.5"/><rect x="8" y="7" width="4" height="11" rx="1" fill="#b79563" opacity="0.75"/><rect x="14" y="2" width="4" height="16" rx="1" fill="#b79563"/></svg>`
    },
  ];

  const deepItems = [
    {
      id: 'analytics',
      title: 'Metrics',
      subtitle: 'PUE, WUE, CUE',
      badge: null,
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="5" stroke="#2cad84" stroke-width="1.6"/><circle cx="10" cy="10" r="2" fill="#2cad84"/><line x1="10" y1="2" x2="10" y2="6" stroke="#2cad84" stroke-width="1.6" stroke-linecap="round"/><line x1="10" y1="14" x2="10" y2="18" stroke="#2cad84" stroke-width="1.6" stroke-linecap="round"/><line x1="2" y1="10" x2="6" y2="10" stroke="#2cad84" stroke-width="1.6" stroke-linecap="round"/><line x1="14" y1="10" x2="18" y2="10" stroke="#2cad84" stroke-width="1.6" stroke-linecap="round"/></svg>`
    },
    {
      id: 'globalmap',
      title: 'Live map',
      subtitle: 'Mapbox facility view',
      badge: { text: 'Live', cls: 'nb-green' },
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="7" stroke="#b79563" stroke-width="1.6"/><ellipse cx="10" cy="10" rx="3.5" ry="7" stroke="#b79563" stroke-width="1.2"/><line x1="3" y1="10" x2="17" y2="10" stroke="#b79563" stroke-width="1.2"/></svg>`
    },
    {
      id: 'siteiq',
      title: 'Site selection',
      subtitle: 'Score new locations',
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
      title: 'Calculator',
      subtitle: 'Estimate savings',
      badge: null,
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><rect x="3" y="3" width="14" height="14" rx="3" stroke="#7faeff" stroke-width="1.6"/><line x1="10" y1="3" x2="10" y2="17" stroke="#7faeff" stroke-width="1.2" opacity="0.6"/><line x1="3" y1="9" x2="17" y2="9" stroke="#7faeff" stroke-width="1.2" opacity="0.6"/><line x1="3" y1="14" x2="17" y2="14" stroke="#7faeff" stroke-width="1.2" opacity="0.6"/></svg>`
    },
    {
      id: 'ai-assistant',
      title: 'flaer AI',
      subtitle: 'Ask for help',
      badge: { text: 'AI', cls: 'nb-green' },
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="7" stroke="#2cad84" stroke-width="1.6"/><circle cx="7" cy="9" r="1.5" fill="#2cad84"/><circle cx="13" cy="9" r="1.5" fill="#2cad84"/><path d="M7 13 Q10 15 13 13" stroke="#2cad84" stroke-width="1.4" stroke-linecap="round" fill="none"/></svg>`
    },
    {
      id: 'reports',
      title: 'Reports',
      subtitle: 'Export summaries',
      badge: { text: 'New', cls: 'nb-gold' },
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><rect x="4" y="2" width="12" height="16" rx="2" stroke="#b79563" stroke-width="1.6"/><line x1="7" y1="6" x2="13" y2="6" stroke="#b79563" stroke-width="1.3" stroke-linecap="round"/><line x1="7" y1="9" x2="13" y2="9" stroke="#b79563" stroke-width="1.3" stroke-linecap="round"/><line x1="7" y1="12" x2="11" y2="12" stroke="#b79563" stroke-width="1.3" stroke-linecap="round"/></svg>`
    },
    {
      id: 'comparison',
      title: 'Comparison',
      subtitle: 'Facility vs. facility',
      badge: { text: 'New', cls: 'nb-green' },
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><rect x="2" y="2" width="7" height="7" rx="1.5" stroke="#2cad84" stroke-width="1.5"/><rect x="11" y="2" width="7" height="7" rx="1.5" stroke="#7faeff" stroke-width="1.5"/><rect x="2" y="11" width="7" height="7" rx="1.5" stroke="#b79563" stroke-width="1.5"/><rect x="11" y="11" width="7" height="7" rx="1.5" stroke="#d35d5c" stroke-width="1.5"/></svg>`
    },
  ];
</script>

<aside class="sidebar">
  <div class="health-card">
    <div class="ai-badge">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
        <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" fill="currentColor"/>
      </svg>
      AI-Powered Intelligence
    </div>
    
    <div class="live-indicator">
      <span class="live-dot"></span>
      Live
    </div>

    <div class="health-content">
      <div class="health-metric-label">PORTFOLIO HEALTH</div>
      
      <div class="health-main">
        <div class="health-title">Collaborative Intelligence</div>
        <div class="health-desc">Anonymous benchmarking against 500+ data centers in your industry</div>
      </div>

      <div class="health-ranking">
        <div class="ranking-big">Top 12%</div>
        <div class="ranking-label">YOUR RANKING</div>
      </div>

      <div class="confidence-section">
        <div class="confidence-bar-wrapper">
          <div class="confidence-bar-fill" style="width: 91%"></div>
        </div>
        <div class="confidence-text">91% confidence</div>
      </div>

      <div class="health-footer">
        <div class="footer-item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="3" fill="currentColor"/>
            <path d="M12 1v6m0 6v6M23 12h-6m-6 0H1" stroke="currentColor" stroke-width="2"/>
          </svg>
          Powered by AI Engine
        </div>
        <div class="footer-time">Updated 2 min ago</div>
      </div>
    </div>
  </div>

  <div class="nav-section">
    <div class="nav-section-label">Main</div>
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
    <div class="nav-section-label">Tools</div>
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
    padding: 18px 16px;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(15,29,24,0.95), rgba(11,23,20,0.98));
    border: 1.5px solid rgba(44,173,132,0.25);
    margin-bottom: 18px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
    position: relative;
    overflow: visible;
    width: 100%;
  }

  .health-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(44,173,132,0.5), transparent);
  }

  .ai-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 999px;
    background: rgba(44,173,132,0.15);
    border: 1px solid rgba(44,173,132,0.3);
    color: #2cad84;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.02em;
    margin-bottom: 12px;
  }

  .live-indicator {
    position: absolute;
    top: 20px;
    right: 20px;
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-weight: 600;
    color: var(--text);
  }

  .live-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #2cad84;
    animation: livePulse 2s ease-in-out infinite;
  }

  @keyframes livePulse {
    0%, 100% {
      box-shadow: 0 0 0 0 rgba(44,173,132,0.7);
      opacity: 1;
    }
    50% {
      box-shadow: 0 0 0 4px rgba(44,173,132,0);
      opacity: 0.8;
    }
  }

  .health-content {
    margin-top: 8px;
  }

  .health-metric-label {
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--tm);
    margin-bottom: 16px;
  }

  .health-main {
    margin-bottom: 20px;
  }

  .health-title {
    font-size: 18px;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--text);
    margin-bottom: 8px;
    line-height: 1.2;
  }

  .health-desc {
    font-size: 11.5px;
    line-height: 1.6;
    color: var(--ts);
    letter-spacing: -0.01em;
    word-wrap: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
  }

  .health-ranking {
    background: linear-gradient(135deg, rgba(44,173,132,0.12), rgba(127,174,255,0.08));
    border: 1px solid rgba(44,173,132,0.2);
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
  }

  .health-ranking::before {
    content: 'NET';
    position: absolute;
    top: 8px;
    right: 12px;
    font-size: 32px;
    font-weight: 900;
    letter-spacing: -0.05em;
    color: rgba(255,255,255,0.03);
  }

  .ranking-big {
    font-size: 36px;
    font-weight: 900;
    letter-spacing: -0.04em;
    background: linear-gradient(135deg, #2cad84, #7faeff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
    line-height: 1;
  }

  .ranking-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--tm);
  }

  .confidence-section {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
  }

  .confidence-bar-wrapper {
    flex: 1;
    height: 6px;
    border-radius: 999px;
    background: rgba(0,0,0,0.4);
    overflow: hidden;
    box-shadow: inset 0 1px 2px rgba(0,0,0,0.3);
  }

  .confidence-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #2cad84, #7faeff);
    box-shadow: 0 0 12px rgba(44,173,132,0.6);
    transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .confidence-text {
    font-size: 11px;
    font-weight: 700;
    color: var(--text);
    white-space: nowrap;
  }

  .health-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 12px;
    border-top: 1px solid rgba(255,255,255,0.06);
    font-size: 10px;
    color: var(--tm);
  }

  .footer-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-weight: 500;
  }

  .footer-time {
    font-weight: 500;
    opacity: 0.7;
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
