<script>
  import AIInsights from './AIInsights.svelte';
  import DashboardPortfolioMap from './DashboardPortfolioMap.svelte';
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
            <span class="map-tab active">Map view</span>
          </div>
          <div class="map-chips">
            <div class="map-chip">15 European facilities</div>
          </div>
        </div>
        <div class="map-body">
          <DashboardPortfolioMap />
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
    padding: 0;
    min-height: 450px;
  }

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
