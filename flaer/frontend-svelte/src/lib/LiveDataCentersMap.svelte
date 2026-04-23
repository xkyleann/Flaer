<script>
  import { onMount, onDestroy } from 'svelte';
  import { fade } from 'svelte/transition';
  
  let visible = false;
  let activeCenter = null;
  let liveData = null;
  let lastUpdate = null;
  let refreshInterval = null;
  const API_URL = 'http://127.0.0.1:5001';
  
  let dataCenters = [
    // North America - Low carbon (hydro/wind heavy grids)
    { id: 1, name: 'US-East-1', city: 'N. Virginia', x: 25, y: 35, status: 'optimal', load: 67, carbon: 0.385, temp: 22, capacity: '850 MW', renewable: 45 },
    { id: 2, name: 'US-West-2', city: 'Oregon', x: 15, y: 32, status: 'optimal', load: 54, carbon: 0.095, temp: 20, capacity: '720 MW', renewable: 89 },
    { id: 14, name: 'US-Central-1', city: 'Iowa', x: 20, y: 33, status: 'optimal', load: 59, carbon: 0.412, temp: 21, capacity: '640 MW', renewable: 58 },
    { id: 9, name: 'CA-Central-1', city: 'Montreal', x: 22, y: 30, status: 'optimal', load: 51, carbon: 0.029, temp: 19, capacity: '580 MW', renewable: 97 },
    
    // Europe - Mixed (Nordic very low, Central moderate)
    { id: 3, name: 'EU-Central-1', city: 'Frankfurt', x: 52, y: 28, status: 'optimal', load: 72, carbon: 0.338, temp: 23, capacity: '920 MW', renewable: 52 },
    { id: 4, name: 'EU-West-1', city: 'Dublin', x: 48, y: 25, status: 'optimal', load: 61, carbon: 0.295, temp: 21, capacity: '780 MW', renewable: 68 },
    { id: 12, name: 'EU-North-1', city: 'Stockholm', x: 54, y: 22, status: 'optimal', load: 48, carbon: 0.013, temp: 18, capacity: '650 MW', renewable: 98 },
    { id: 15, name: 'EU-South-1', city: 'Milan', x: 53, y: 32, status: 'optimal', load: 55, carbon: 0.289, temp: 22, capacity: '590 MW', renewable: 61 },
    
    // Asia-Pacific - Higher carbon (coal-heavy grids except hydro regions)
    { id: 6, name: 'AP-Northeast-1', city: 'Tokyo', x: 85, y: 35, status: 'optimal', load: 69, carbon: 0.462, temp: 22, capacity: '1100 MW', renewable: 38 },
    { id: 13, name: 'AP-East-1', city: 'Hong Kong', x: 78, y: 45, status: 'warning', load: 76, carbon: 0.678, temp: 24, capacity: '480 MW', renewable: 12 },
    { id: 5, name: 'AP-Southeast-1', city: 'Singapore', x: 75, y: 55, status: 'warning', load: 84, carbon: 0.408, temp: 26, capacity: '720 MW', renewable: 28 },
    { id: 7, name: 'AP-South-1', city: 'Mumbai', x: 70, y: 48, status: 'optimal', load: 58, carbon: 0.708, temp: 24, capacity: '620 MW', renewable: 24 },
    
    // South America - Hydro-dominant (very low carbon)
    { id: 8, name: 'SA-East-1', city: 'São Paulo', x: 35, y: 68, status: 'optimal', load: 45, carbon: 0.082, temp: 21, capacity: '540 MW', renewable: 83 },
    
    // Middle East & Africa - Solar potential but currently fossil-heavy
    { id: 10, name: 'ME-South-1', city: 'Bahrain', x: 60, y: 45, status: 'optimal', load: 63, carbon: 0.632, temp: 25, capacity: '420 MW', renewable: 18 },
    { id: 11, name: 'AF-South-1', city: 'Cape Town', x: 55, y: 75, status: 'optimal', load: 42, carbon: 0.912, temp: 20, capacity: '380 MW', renewable: 8 }
  ];
  
  const connections = [
    [1, 3], [1, 14], [2, 6], [3, 4], [3, 12], [5, 6], [5, 7], [6, 13], [7, 10], [8, 1], [9, 1], [10, 3], [11, 10], [12, 3], [13, 5], [14, 2], [15, 3]
  ];
  
  async function fetchLiveData() {
    try {
      const response = await fetch(`${API_URL}/api/carbon/live`);
      if (response.ok) {
        const data = await response.json();
        liveData = data;
        lastUpdate = new Date(data.timestamp);
        
        // Update data centers with live data
        dataCenters = dataCenters.map(dc => {
          const regionKey = dc.name.toLowerCase().replace(/[.\s]/g, '-');
          const liveRegionData = data.regions[regionKey];
          
          if (liveRegionData) {
            return {
              ...dc,
              carbon: liveRegionData.carbon / 1000, // Convert to kgCO₂/kWh
              renewable: liveRegionData.renewable,
              status: liveRegionData.carbon > 500 ? 'warning' : 'optimal'
            };
          }
          return dc;
        });
      }
    } catch (error) {
      console.error('Error fetching live carbon data:', error);
    }
  }
  
  onMount(() => {
    setTimeout(() => { visible = true; }, 200);
    
    // Initial fetch
    fetchLiveData();
    
    // Refresh every 5 minutes
    refreshInterval = setInterval(fetchLiveData, 5 * 60 * 1000);
  });
  
  onDestroy(() => {
    if (refreshInterval) {
      clearInterval(refreshInterval);
    }
  });
  
  function handleCenterClick(center) {
    activeCenter = activeCenter?.id === center.id ? null : center;
  }
  
  function getStatusColor(status) {
    return status === 'optimal' ? '#2cad84' : status === 'warning' ? '#b79563' : '#d35d5c';
  }
</script>

<div class="live-map-section" class:visible>
  <div class="map-header">
    <div class="header-left">
      <div class="live-indicator">
        <span class="pulse-dot"></span>
        <span class="live-text">Live Network Status</span>
        {#if lastUpdate}
          <span class="last-update">Updated {new Date(lastUpdate).toLocaleTimeString()}</span>
        {/if}
      </div>
      <h2>Global Data Center Network</h2>
      <p>Real-time monitoring of 15 data centers across 6 continents • Data refreshes every 5 minutes</p>
    </div>
    <div class="header-stats">
      <div class="stat-card">
        <div class="stat-value">99.99%</div>
        <div class="stat-label">Uptime</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">0.378</div>
        <div class="stat-label">Avg Carbon (kgCO₂/kWh)</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">60%</div>
        <div class="stat-label">Avg Load</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">52%</div>
        <div class="stat-label">Renewable Mix</div>
      </div>
    </div>
  </div>
  
  <div class="map-container">
    <svg class="world-map" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
      <!-- World map outline (simplified continents) -->
      <g class="continents" opacity="0.15">
        <!-- North America -->
        <path d="M10,25 L12,20 L18,18 L22,20 L25,22 L28,25 L30,30 L28,35 L25,38 L20,40 L15,38 L12,35 L10,30 Z" fill="currentColor"/>
        <!-- South America -->
        <path d="M28,50 L30,45 L33,43 L36,45 L38,50 L40,58 L38,65 L35,70 L32,72 L29,70 L27,65 L26,58 Z" fill="currentColor"/>
        <!-- Europe -->
        <path d="M48,20 L50,18 L54,18 L57,20 L58,24 L57,28 L54,30 L50,30 L48,28 Z" fill="currentColor"/>
        <!-- Africa -->
        <path d="M50,35 L52,33 L56,33 L59,36 L60,42 L59,50 L57,58 L54,65 L51,68 L48,65 L47,58 L48,50 L49,42 Z" fill="currentColor"/>
        <!-- Asia -->
        <path d="M60,20 L65,18 L72,18 L78,20 L82,24 L85,30 L84,36 L80,40 L75,42 L70,40 L65,36 L62,30 L60,24 Z" fill="currentColor"/>
        <!-- Australia -->
        <path d="M75,55 L78,53 L82,53 L85,55 L87,58 L86,62 L83,65 L79,66 L76,64 L74,60 Z" fill="currentColor"/>
      </g>
      
      <!-- Connection lines -->
      <g class="connections">
        {#each connections as [from, to]}
          {@const fromCenter = dataCenters.find(c => c.id === from)}
          {@const toCenter = dataCenters.find(c => c.id === to)}
          <line 
            x1={fromCenter.x} 
            y1={fromCenter.y} 
            x2={toCenter.x} 
            y2={toCenter.y}
            class="connection-line"
            style="--delay: {Math.random() * 2}s"
          />
        {/each}
      </g>
      
      <!-- Data centers -->
      <g class="data-centers">
        {#each dataCenters as center}
          <g 
            class="data-center" 
            class:active={activeCenter?.id === center.id}
            on:click={() => handleCenterClick(center)}
            on:keydown={(e) => e.key === 'Enter' && handleCenterClick(center)}
            role="button"
            tabindex="0"
            aria-label="{center.name} - {center.city}"
          >
            <!-- Pulse rings -->
            <circle 
              cx={center.x} 
              cy={center.y} 
              r="2.5" 
              class="pulse-ring"
              style="--color: {getStatusColor(center.status)}; --delay: {center.id * 0.2}s"
            />
            <circle 
              cx={center.x} 
              cy={center.y} 
              r="2.5" 
              class="pulse-ring pulse-ring-2"
              style="--color: {getStatusColor(center.status)}; --delay: {center.id * 0.2 + 0.5}s"
            />
            
            <!-- Center dot -->
            <circle 
              cx={center.x} 
              cy={center.y} 
              r="1.2" 
              class="center-dot"
              style="fill: {getStatusColor(center.status)}"
            />
            
            <!-- Label -->
            <text 
              x={center.x} 
              y={center.y - 4} 
              class="center-label"
              text-anchor="middle"
            >
              {center.city}
            </text>
          </g>
        {/each}
      </g>
    </svg>
    
    <!-- Active center details -->
    {#if activeCenter}
      <div class="center-details" transition:fade>
        <div class="details-header">
          <h3>{activeCenter.name}</h3>
          <button class="close-btn" on:click={() => activeCenter = null} aria-label="Close">×</button>
        </div>
        <div class="details-location">{activeCenter.city}</div>
        <div class="details-metrics">
          <div class="metric">
            <div class="metric-label">Current Load</div>
            <div class="metric-value">{activeCenter.load}%</div>
            <div class="metric-bar">
              <div class="metric-fill" style="width: {activeCenter.load}%; background: {getStatusColor(activeCenter.status)}"></div>
            </div>
          </div>
          <div class="metric">
            <div class="metric-label">Carbon Intensity</div>
            <div class="metric-value">{activeCenter.carbon} kgCO₂/kWh</div>
            <div class="metric-bar">
              <div class="metric-fill" style="width: {(activeCenter.carbon / 1.0) * 100}%; background: {activeCenter.carbon > 0.5 ? '#d35d5c' : activeCenter.carbon > 0.3 ? '#b79563' : '#2cad84'}"></div>
            </div>
          </div>
          <div class="metric">
            <div class="metric-label">Renewable Energy</div>
            <div class="metric-value">{activeCenter.renewable}%</div>
            <div class="metric-bar">
              <div class="metric-fill" style="width: {activeCenter.renewable}%; background: linear-gradient(90deg, #2cad84, #5fc49a)"></div>
            </div>
          </div>
          <div class="metric-row">
            <div class="metric-half">
              <div class="metric-label">Capacity</div>
              <div class="metric-value-small">{activeCenter.capacity}</div>
            </div>
            <div class="metric-half">
              <div class="metric-label">Temperature</div>
              <div class="metric-value-small">{activeCenter.temp}°C</div>
            </div>
          </div>
          <div class="metric">
            <div class="metric-label">Status</div>
            <div class="metric-badge" style="background: {getStatusColor(activeCenter.status)}20; color: {getStatusColor(activeCenter.status)}">
              {activeCenter.status.toUpperCase()}
            </div>
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  .live-map-section {
    padding: 120px 0;
    background: linear-gradient(180deg, #000000 0%, #0a0a0a 100%);
    position: relative;
    overflow: hidden;
    opacity: 0;
    transform: translateY(40px);
    transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
  }
  
  .live-map-section.visible {
    opacity: 1;
  
  .last-update {
    margin-left: 12px;
    font-size: 10px;
    font-weight: 600;
    color: rgba(244,247,245,0.4);
    text-transform: none;
    letter-spacing: normal;
  }
    transform: translateY(0);
  }
  
  .live-map-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(44,173,132,0.3), transparent);
  }
  
  .map-header {
    max-width: 1200px;
    margin: 0 auto 60px;
    padding: 0 24px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 48px;
  }
  
  .header-left {
    flex: 1;
  }
  
  .live-indicator {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border-radius: 999px;
    background: rgba(44,173,132,0.12);
    border: 1px solid rgba(44,173,132,0.25);
    margin-bottom: 20px;
  }
  
  .pulse-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #2cad84;
    animation: pulse 2s ease-in-out infinite;
  }
  
  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.3); }
  }
  
  .live-text {
    font-size: 12px;
    font-weight: 700;
    color: #2cad84;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  
  .map-header h2 {
    font-size: 48px;
    font-weight: 900;
    color: #f4f7f5;
    margin: 0 0 12px 0;
    letter-spacing: -0.03em;
    line-height: 1.1;
  }
  
  .map-header p {
    font-size: 18px;
    color: rgba(244,247,245,0.6);
    margin: 0;
    line-height: 1.5;
  }
  
  .header-stats {
    display: flex;
    gap: 16px;
  }
  
  .stat-card {
    padding: 20px 24px;
    border-radius: 16px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(20px);
    min-width: 140px;
  }
  
  .stat-value {
    font-size: 32px;
    font-weight: 900;
    color: #2cad84;
    margin-bottom: 4px;
    letter-spacing: -0.02em;
  }
  
  .stat-label {
    font-size: 11px;
    font-weight: 700;
    color: rgba(244,247,245,0.5);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  
  .map-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
    position: relative;
  }
  
  .world-map {
    width: 100%;
    height: auto;
    color: rgba(244,247,245,0.8);
  }
  
  .connections {
    opacity: 0.3;
  }
  
  .connection-line {
    stroke: #2cad84;
    stroke-width: 0.15;
    stroke-dasharray: 2 2;
    animation: dash 20s linear infinite;
    animation-delay: var(--delay);
  }
  
  @keyframes dash {
    to { stroke-dashoffset: -100; }
  }
  
  .data-center {
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .data-center:hover .center-dot,
  .data-center.active .center-dot {
    r: 1.5;
  }
  
  .pulse-ring {
    fill: none;
    stroke: var(--color);
    stroke-width: 0.3;
    opacity: 0;
    animation: pulse-ring 3s ease-out infinite;
    animation-delay: var(--delay);
  }
  
  .pulse-ring-2 {
    animation-delay: calc(var(--delay) + 1s);
  }
  
  @keyframes pulse-ring {
    0% {
      r: 1.2;
      opacity: 1;
    }
    100% {
      r: 4;
      opacity: 0;
    }
  }
  
  .center-dot {
    filter: drop-shadow(0 0 3px currentColor);
    transition: all 0.3s ease;
  }
  
  .center-label {
    font-size: 2.5px;
    font-weight: 700;
    fill: rgba(244,247,245,0.7);
    pointer-events: none;
    letter-spacing: 0.02em;
  }
  
  .center-details {
    position: absolute;
    top: 50%;
    right: 24px;
    transform: translateY(-50%);
    width: 320px;
    padding: 24px;
    border-radius: 20px;
    background: rgba(10,10,10,0.95);
    border: 1.5px solid rgba(44,173,132,0.3);
    backdrop-filter: blur(40px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
  }
  
  .details-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 8px;
  }
  
  .details-header h3 {
    font-size: 20px;
    font-weight: 900;
    color: #f4f7f5;
    margin: 0;
    letter-spacing: -0.02em;
  }
  
  .close-btn {
    background: none;
    border: none;
    color: rgba(244,247,245,0.5);
    font-size: 28px;
    line-height: 1;
    cursor: pointer;
    padding: 0;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: color 0.3s ease;
  }
  
  .close-btn:hover {
    color: #f4f7f5;
  }
  
  .details-location {
    font-size: 14px;
    color: rgba(244,247,245,0.6);
    margin-bottom: 20px;
  }
  
  .details-metrics {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  
  .metric {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  
  .metric-label {
    font-size: 11px;
    font-weight: 700;
    color: rgba(244,247,245,0.5);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  
  .metric-value {
    font-size: 18px;
    font-weight: 900;
    color: #2cad84;
    letter-spacing: -0.02em;
  
  .metric-value-small {
    font-size: 16px;
    font-weight: 900;
    color: #2cad84;
    letter-spacing: -0.02em;
  }
  
  .metric-row {
    display: flex;
    gap: 12px;
  }
  
  .metric-half {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  }
  
  .metric-bar {
    height: 6px;
    border-radius: 999px;
    background: rgba(255,255,255,0.1);
    overflow: hidden;
  }
  
  .metric-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  }
  
  .metric-badge {
    display: inline-flex;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.05em;
    align-self: flex-start;
  }
  
  @media (max-width: 1024px) {
    .map-header {
      flex-direction: column;
      gap: 32px;
    }
    
    .header-stats {
      width: 100%;
      justify-content: space-between;
    }
    
    .stat-card {
      flex: 1;
      min-width: 0;
    }
    
    .center-details {
      position: static;
      transform: none;
      width: 100%;
      margin-top: 24px;
    }
  }
  
  @media (max-width: 768px) {
    .live-map-section {
      padding: 80px 0;
    }
    
    .map-header h2 {
      font-size: 36px;
    }
    
    .header-stats {
      flex-direction: column;
    }
    
    .stat-card {
      width: 100%;
    }
  }
</style>