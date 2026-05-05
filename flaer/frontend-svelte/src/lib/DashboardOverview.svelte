<script>
  import AIInsights from './AIInsights.svelte';
  import PortfolioOverviewMapbox from './PortfolioOverviewMapbox.svelte';
</script>

<section class="sc-portfolio">
  <div class="tri-layout">

    <!-- Left: AI Insights -->
    <div class="col-left">
      <AIInsights />
    </div>

    <!-- Center: Map -->
    <div class="col-map">
      <div class="map-panel">
        <div class="map-topbar">
          <div class="map-tabs">
            <span class="map-tab active">Portfolio overview</span>
          </div>
          <div class="map-chips">
            <div class="map-chip">11 data centers</div>
          </div>
        </div>
        <div class="map-body">
          <PortfolioOverviewMapbox />
          <svg viewBox="0 0 1000 480" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="land" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#1e332d"/>
                <stop offset="100%" stop-color="#162420"/>
              </linearGradient>
              <filter id="glow">
                <feGaussianBlur stdDeviation="6" result="b"/>
                <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
              </filter>
            </defs>
            <rect width="1000" height="480" fill="#0a1412"/>

            <!-- Continent shapes -->
            <path d="M60,70 L100,50 L160,48 L220,55 L260,65 L280,94 L275,130 L260,162 L240,186 L210,200 L185,208 L160,212 L140,200 L120,184 L100,172 L80,152 L65,122Z" fill="url(#land)" stroke="#274039" stroke-width="1"/>
            <path d="M280,28 L330,20 L350,36 L340,60 L310,67 L285,54Z" fill="url(#land)" stroke="#274039" stroke-width="1"/>
            <path d="M185,236 L240,230 L265,247 L275,285 L270,326 L255,358 L235,383 L210,393 L190,378 L175,348 L170,312 L175,270Z" fill="url(#land)" stroke="#274039" stroke-width="1"/>
            <path d="M418,58 L450,52 L490,55 L520,64 L530,86 L520,112 L500,128 L475,133 L450,126 L425,115 L410,94Z" fill="url(#land)" stroke="#274039" stroke-width="1"/>
            <path d="M392,60 L408,52 L415,68 L405,83 L390,76Z" fill="url(#land)" stroke="#274039" stroke-width="1"/>
            <path d="M448,28 L490,22 L510,34 L505,57 L480,63 L455,54Z" fill="url(#land)" stroke="#274039" stroke-width="1"/>
            <path d="M420,152 L495,146 L530,163 L545,200 L540,248 L525,290 L505,322 L475,337 L445,332 L420,311 L405,275 L400,232 L405,190Z" fill="url(#land)" stroke="#274039" stroke-width="1"/>
            <path d="M530,116 L590,110 L620,126 L625,154 L600,168 L560,165 L535,148Z" fill="url(#land)" stroke="#274039" stroke-width="1"/>
            <path d="M500,28 L700,18 L780,36 L790,66 L760,88 L700,94 L620,91 L540,86 L505,70Z" fill="url(#land)" stroke="#274039" stroke-width="1"/>
            <path d="M620,162 L660,155 L685,172 L695,210 L685,242 L665,258 L645,253 L625,232 L610,200 L612,178Z" fill="url(#land)" stroke="#274039" stroke-width="1"/>
            <path d="M700,66 L800,56 L840,72 L850,104 L835,136 L800,152 L760,155 L720,147 L695,125 L692,97Z" fill="url(#land)" stroke="#274039" stroke-width="1"/>
            <path d="M850,84 L870,76 L882,92 L876,110 L860,113 L848,98Z" fill="url(#land)" stroke="#274039" stroke-width="1"/>
            <path d="M750,166 L800,158 L820,176 L815,202 L790,210 L760,199 L745,182Z" fill="url(#land)" stroke="#274039" stroke-width="1"/>
            <path d="M780,285 L870,272 L910,290 L920,334 L900,370 L860,382 L815,376 L780,354 L770,316Z" fill="url(#land)" stroke="#274039" stroke-width="1"/>

            <!-- Connection lines -->
            <line x1="215" y1="120" x2="462" y2="80" stroke="#2cad84" stroke-width="1.2" stroke-dasharray="6,6" opacity=".22"/>
            <line x1="462" y1="80" x2="500" y2="74" stroke="#2cad84" stroke-width="1.2" opacity=".18"/>
            <line x1="500" y1="74" x2="680" y2="110" stroke="#2cad84" stroke-width="1.2" opacity=".16"/>
            <line x1="462" y1="80" x2="410" y2="68" stroke="#2cad84" stroke-width="1" opacity=".14"/>
            <line x1="680" y1="110" x2="858" y2="100" stroke="#2cad84" stroke-width="1" opacity=".14"/>

            <!-- Data center nodes -->
            <g filter="url(#glow)">
              <!-- N. Virginia - red -->
              <circle cx="215" cy="120" r="20" fill="rgba(211,93,92,0.12)"/>
              <circle cx="215" cy="120" r="8" fill="#d35d5c"/>
              <!-- US West - amber -->
              <circle cx="95" cy="108" r="16" fill="rgba(182,126,61,0.12)"/>
              <circle cx="95" cy="108" r="7" fill="#b67e3d"/>
              <!-- Ireland - green -->
              <circle cx="410" cy="68" r="17" fill="rgba(44,173,132,0.18)"/>
              <circle cx="410" cy="68" r="7" fill="#2cad84"/>
              <!-- Frankfurt - amber -->
              <circle cx="462" cy="80" r="15" fill="rgba(182,126,61,0.12)"/>
              <circle cx="462" cy="80" r="7" fill="#b67e3d"/>
              <!-- Stockholm - green -->
              <circle cx="500" cy="74" r="18" fill="rgba(44,173,132,0.20)"/>
              <circle cx="500" cy="74" r="8" fill="#2cad84"/>
              <!-- Singapore - red -->
              <circle cx="790" cy="210" r="18" fill="rgba(211,93,92,0.12)"/>
              <circle cx="790" cy="210" r="8" fill="#d35d5c"/>
              <!-- Tokyo - amber -->
              <circle cx="858" cy="100" r="15" fill="rgba(182,126,61,0.12)"/>
              <circle cx="858" cy="100" r="7" fill="#b67e3d"/>
              <!-- Sydney - green -->
              <circle cx="858" cy="348" r="13" fill="rgba(44,173,132,0.16)"/>
              <circle cx="858" cy="348" r="6" fill="#2cad84"/>
              <!-- Mumbai - red -->
              <circle cx="645" cy="205" r="14" fill="rgba(211,93,92,0.12)"/>
              <circle cx="645" cy="205" r="7" fill="#d35d5c"/>
              <!-- São Paulo - amber -->
              <circle cx="220" cy="338" r="13" fill="rgba(182,126,61,0.12)"/>
              <circle cx="220" cy="338" r="6" fill="#b67e3d"/>
              <!-- Hong Kong - amber -->
              <circle cx="680" cy="110" r="14" fill="rgba(182,126,61,0.12)"/>
              <circle cx="680" cy="110" r="6" fill="#b67e3d"/>
            </g>
          </svg>

          <div class="map-legend">
            <div class="ml-item"><span class="ml-dot" style="background:#d35d5c"></span>High risk</div>
            <div class="ml-item"><span class="ml-dot" style="background:#b67e3d"></span>Medium</div>
            <div class="ml-item"><span class="ml-dot" style="background:#2cad84"></span>Low risk</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right: Enhanced Metric cards -->
    <div class="col-right">
      <div class="metric-card premium-card">
        <div class="card-header">
          <div class="mc-label">PORTFOLIO EMISSIONS</div>
          <div class="info-icon" title="Total carbon emissions across all data centers">ⓘ</div>
        </div>
        <div class="mc-big animated-number">1.24M</div>
        <div class="mc-sub">tCO₂e tracked this month</div>
        <div class="mc-trend trend-green">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 10 L7 4 L12 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          −12.4% MoM
        </div>
        <div class="metric-detail">
          <span class="detail-label">vs. last month:</span>
          <span class="detail-value">1.41M tCO₂e</span>
        </div>
      </div>

      <div class="metric-card premium-card">
        <div class="card-header">
          <div class="mc-label">WEEKLY CARBON INTENSITY</div>
          <div class="info-icon" title="Average carbon intensity per day">ⓘ</div>
        </div>
        <div class="mini-chart enhanced-chart">
          {#each [62, 75, 68, 71, 88, 64, 58] as h, i}
            <div class="bar-container">
              <div class="bar" style="height:{h}%; background:{i === 4 ? '#b67e3d' : 'rgba(44,173,132,0.7)'}">
                <div class="bar-tooltip">{Math.round(h * 3.2)}g</div>
              </div>
              <div class="bar-label">{['M','T','W','T','F','S','S'][i]}</div>
            </div>
          {/each}
        </div>
        <div class="mc-sub" style="margin-top:12px">
          <span class="highlight">58 gCO₂/kWh</span> current avg.
        </div>
      </div>

      <div class="metric-card premium-card">
        <div class="card-header">
          <div class="mc-label">2035 NET-ZERO TRAJECTORY</div>
          <div class="info-icon" title="Projected emissions reduction by 2035">ⓘ</div>
        </div>
        <div class="mc-big mc-green animated-number">−38%</div>
        <div class="mc-sub">on track for net-zero</div>
        <div class="progress-bar">
          <div class="progress-fill" style="width: 38%"></div>
        </div>
        <div class="metric-detail">
          <span class="detail-label">Target:</span>
          <span class="detail-value">−100% by 2035</span>
        </div>
      </div>
    </div>

  </div>
</section>

<style>
  .sc-portfolio { display: flex; flex-direction: column; gap: 0; height: 100%; }

  .tri-layout {
    display: grid;
    grid-template-columns: 320px 1fr 220px;
    gap: 14px;
    align-items: stretch;
    min-height: 520px;
  }

  /* ── Left col ── */
  .col-left {
    display: flex;
    flex-direction: column;
  }

  /* ── Center map ── */
  .col-map { display: flex; flex-direction: column; }

  .map-panel {
    flex: 1;
    border-radius: 22px;
    overflow: hidden;
    background: linear-gradient(180deg, rgba(255,255,255,0.055), rgba(255,255,255,0.025));
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 20px 56px rgba(0,0,0,0.24);
    display: flex;
    flex-direction: column;
  }

  .map-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 18px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
  }

  .map-tabs { display: flex; gap: 8px; }

  .map-tab {
    font-size: 12.5px;
    font-weight: 700;
    color: rgba(244,247,245,0.5);
    cursor: pointer;
    padding: 4px 0;
  }

  .map-tab.active {
    color: #f4f7f5;
    border-bottom: 2px solid #2cad84;
  }

  .map-chips { display: flex; gap: 7px; }

  .map-chip {
    padding: 5px 11px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.05);
    font-size: 11px;
    font-weight: 700;
    color: rgba(244,247,245,0.7);
  }

  .map-body {
    flex: 1;
    position: relative;
    padding: 10px;
  }

  .map-body > svg { display: none; }

  .map-legend {
    position: absolute;
    right: 18px;
    bottom: 18px;
    display: flex;
    gap: 9px;
    padding: 7px 12px;
    border-radius: 999px;
    background: rgba(6,14,12,0.90);
    border: 1px solid rgba(255,255,255,0.07);
  }

  .ml-item {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 10px;
    font-weight: 700;
    color: rgba(244,247,245,0.65);
  }

  .ml-dot { width: 7px; height: 7px; border-radius: 50%; }

  /* ── Right col ── */
  .col-right {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .metric-card {
    flex: 1;
    padding: 20px;
    border-radius: 20px;
    background: linear-gradient(180deg, rgba(255,255,255,0.065), rgba(255,255,255,0.03));
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 12px 28px rgba(0,0,0,0.18);
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 6px;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }
  
  .metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(44,173,132,0.5), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  .metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 36px rgba(0,0,0,0.24);
    border-color: rgba(255,255,255,0.12);
  }
  
  .metric-card:hover::before {
    opacity: 1;
  }
  
  .premium-card {
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }
  
  .info-icon {
    width: 16px;
    height: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    color: rgba(244,247,245,0.4);
    cursor: help;
    transition: all 0.2s ease;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.1);
  }
  
  .info-icon:hover {
    color: rgba(244,247,245,0.8);
    background: rgba(255,255,255,0.05);
    border-color: rgba(255,255,255,0.2);
  }

  .mc-label {
    font-size: 9.5px;
    font-weight: 900;
    letter-spacing: 0.1em;
    color: rgba(244,247,245,0.45);
    text-transform: uppercase;
    margin-bottom: 4px;
  }

  .mc-big {
    font-size: 38px;
    font-weight: 900;
    letter-spacing: -0.06em;
    color: #f4f7f5;
    line-height: 1;
  }

  .mc-green { color: #2cad84; }

  .mc-sub {
    font-size: 11px;
    color: rgba(244,247,245,0.5);
  }

  .mc-trend {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    font-weight: 800;
    margin-top: 4px;
  }

  .trend-green { color: #2cad84; }

  /* Mini bar chart */
  .mini-chart {
    display: flex;
    align-items: flex-end;
    gap: 4px;
    height: 52px;
    margin-top: 8px;
  }

  .bar {
    flex: 1;
    border-radius: 3px 3px 0 0;
    min-height: 6px;
    transition: opacity 0.2s;
  }

  /* Enhanced premium styles */
  .animated-number {
    display: inline-block;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  .enhanced-chart {
    margin-top: 16px;
    padding: 16px;
    background: rgba(0,0,0,0.15);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.05);
  }
  
  .chart-bars {
    display: flex;
    gap: 12px;
    align-items: flex-end;
    height: 120px;
    margin-bottom: 12px;
  }
  
  .chart-bar {
    flex: 1;
    background: linear-gradient(180deg, rgba(44,173,132,0.6), rgba(44,173,132,0.3));
    border-radius: 6px 6px 0 0;
    position: relative;
    cursor: pointer;
    transition: all 0.3s ease;
    animation: barGrow 0.8s ease-out;
  }
  
  @keyframes barGrow {
    from {
      transform: scaleY(0);
      opacity: 0;
    }
    to {
      transform: scaleY(1);
      opacity: 1;
    }
  }
  
  .chart-bar:hover {
    background: linear-gradient(180deg, rgba(44,173,132,0.8), rgba(44,173,132,0.5));
    transform: translateY(-4px);
  }
  
  .bar-tooltip {
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%) translateY(-8px);
    background: rgba(20,20,20,0.95);
    color: rgba(244,247,245,0.95);
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 12px;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  }
  
  .chart-bar:hover .bar-tooltip {
    opacity: 1;
  }
  
  .bar-tooltip::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 4px solid transparent;
    border-top-color: rgba(20,20,20,0.95);
  }
  
  .chart-labels {
    display: flex;
    gap: 12px;
    font-size: 11px;
    color: rgba(244,247,245,0.5);
  }
  
  .chart-label {
    flex: 1;
    text-align: center;
  }
  
  .progress-bar {
    width: 100%;
    height: 8px;
    background: rgba(0,0,0,0.2);
    border-radius: 4px;
    overflow: hidden;
    margin-top: 12px;
    position: relative;
  }
  
  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, rgba(44,173,132,0.8), rgba(44,173,132,0.5));
    border-radius: 4px;
    transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
  }
  
  .progress-fill::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    animation: shimmer 2s infinite;
  }
  
  @keyframes shimmer {
    0% {
      transform: translateX(-100%);
    }
    100% {
      transform: translateX(100%);
    }
  }
  
  .metric-detail {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid rgba(255,255,255,0.05);
    font-size: 13px;
    color: rgba(244,247,245,0.6);
  }
  
  .detail-label {
    font-weight: 500;
  }
  
  .detail-value {
    font-weight: 700;
    color: rgba(244,247,245,0.8);
  }
  
  .highlight {
    color: rgba(44,173,132,0.9);
    font-weight: 600;
  }

  @media (max-width: 1300px) {
    .tri-layout {
      grid-template-columns: 280px 1fr 200px;
    }
  }
</style>
