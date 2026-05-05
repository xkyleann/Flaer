<script>
  import { onMount, onDestroy } from 'svelte';
  import { fade } from 'svelte/transition';
  import 'mapbox-gl/dist/mapbox-gl.css';

  let visible = false;
  let activeCenter = null;
  let lastUpdate = null;
  let refreshInterval = null;
  let mapContainer;
  let map;
  let mapboxgl;
  let markers = [];
  let mapError = '';

  const API_URL = 'http://127.0.0.1:8000';
  const MAPBOX_TOKEN =
    import.meta.env.VITE_MAPBOX_TOKEN ||
    'pk.eyJ1IjoiYmVya2lubmJlbGVyIiwiYSI6ImNtb2tqcTZ5MzAyMjkycHFsbml6aHdzb3MifQ.HjyuZunhCOe7tMg3mWALcg';

  let dataCenters = [
    { id: 1, regionKey: 'virginia', name: 'US-East-1', city: 'N. Virginia', lng: -77.0, lat: 38.9, status: 'optimal', load: 67, carbon: 0.385, temp: 22, capacity: '850 MW', renewable: 45 },
    { id: 2, regionKey: 'oregon', name: 'US-West-2', city: 'Oregon', lng: -120.55, lat: 44.0, status: 'optimal', load: 54, carbon: 0.095, temp: 20, capacity: '720 MW', renewable: 89 },
    { id: 14, regionKey: 'iowa', name: 'US-Central-1', city: 'Iowa', lng: -93.1, lat: 42.0, status: 'optimal', load: 59, carbon: 0.412, temp: 21, capacity: '640 MW', renewable: 58 },
    { id: 9, regionKey: 'montreal', name: 'CA-Central-1', city: 'Montreal', lng: -73.57, lat: 45.5, status: 'optimal', load: 51, carbon: 0.029, temp: 19, capacity: '580 MW', renewable: 97 },
    { id: 3, regionKey: 'frankfurt', name: 'EU-Central-1', city: 'Frankfurt', lng: 8.68, lat: 50.11, status: 'optimal', load: 72, carbon: 0.338, temp: 23, capacity: '920 MW', renewable: 52 },
    { id: 4, regionKey: 'dublin', name: 'EU-West-1', city: 'Dublin', lng: -6.26, lat: 53.35, status: 'optimal', load: 61, carbon: 0.295, temp: 21, capacity: '780 MW', renewable: 68 },
    { id: 12, regionKey: 'stockholm', name: 'EU-North-1', city: 'Stockholm', lng: 18.07, lat: 59.33, status: 'optimal', load: 48, carbon: 0.013, temp: 18, capacity: '650 MW', renewable: 98 },
    { id: 15, regionKey: 'milan', name: 'EU-South-1', city: 'Milan', lng: 9.19, lat: 45.46, status: 'optimal', load: 55, carbon: 0.289, temp: 22, capacity: '590 MW', renewable: 61 },
    { id: 6, regionKey: 'tokyo', name: 'AP-Northeast-1', city: 'Tokyo', lng: 139.69, lat: 35.68, status: 'optimal', load: 69, carbon: 0.462, temp: 22, capacity: '1100 MW', renewable: 38 },
    { id: 13, regionKey: 'hong-kong', name: 'AP-East-1', city: 'Hong Kong', lng: 114.17, lat: 22.32, status: 'warning', load: 76, carbon: 0.678, temp: 24, capacity: '480 MW', renewable: 12 },
    { id: 5, regionKey: 'singapore', name: 'AP-Southeast-1', city: 'Singapore', lng: 103.82, lat: 1.35, status: 'warning', load: 84, carbon: 0.408, temp: 26, capacity: '720 MW', renewable: 28 },
    { id: 7, regionKey: 'mumbai', name: 'AP-South-1', city: 'Mumbai', lng: 72.88, lat: 19.08, status: 'optimal', load: 58, carbon: 0.708, temp: 24, capacity: '620 MW', renewable: 24 },
    { id: 8, regionKey: 'sao-paulo', name: 'SA-East-1', city: 'Sao Paulo', lng: -46.63, lat: -23.55, status: 'optimal', load: 45, carbon: 0.082, temp: 21, capacity: '540 MW', renewable: 83 },
    { id: 10, regionKey: 'bahrain', name: 'ME-South-1', city: 'Bahrain', lng: 50.56, lat: 26.07, status: 'optimal', load: 63, carbon: 0.632, temp: 25, capacity: '420 MW', renewable: 18 },
    { id: 11, regionKey: 'cape-town', name: 'AF-South-1', city: 'Cape Town', lng: 18.42, lat: -33.92, status: 'optimal', load: 42, carbon: 0.912, temp: 20, capacity: '380 MW', renewable: 8 }
  ];

  function getStatusColor(status) {
    return status === 'optimal' ? '#2cad84' : status === 'warning' ? '#b79563' : '#d35d5c';
  }

  function getStatusBg(status) {
    return status === 'optimal'
      ? 'rgba(44,173,132,0.18)'
      : status === 'warning'
        ? 'rgba(183,149,99,0.18)'
        : 'rgba(211,93,92,0.16)';
  }

  async function fetchLiveData() {
    try {
      const response = await fetch(`${API_URL}/api/carbon/live`);
      if (!response.ok) return;

      const data = await response.json();
      lastUpdate = new Date(data.timestamp);

      dataCenters = dataCenters.map((dc) => {
        const liveRegionData = data.regions?.[dc.regionKey];
        if (!liveRegionData) return dc;

        return {
          ...dc,
          carbon: Number((liveRegionData.carbon / 1000).toFixed(3)),
          renewable: liveRegionData.renewable,
          status: liveRegionData.carbon > 500 ? 'warning' : 'optimal'
        };
      });

      updateMarkers();
    } catch (error) {
      console.error('Error fetching live carbon data:', error);
    }
  }

  onMount(async () => {
    setTimeout(() => { visible = true; }, 200);

    try {
      const mbx = await import('mapbox-gl');
      mapboxgl = mbx.default;
      mapboxgl.accessToken = MAPBOX_TOKEN;

      map = new mapboxgl.Map({
        container: mapContainer,
        style: 'mapbox://styles/mapbox/dark-v11',
        center: [8, 24],
        zoom: 1.25,
        projection: 'globe',
        attributionControl: false
      });

      map.addControl(new mapboxgl.NavigationControl({ showCompass: false }), 'top-right');

      map.on('load', () => {
        map.setFog({
          color: 'rgb(6,14,12)',
          'high-color': 'rgb(36,92,110)',
          'horizon-blend': 0.02,
          'space-color': 'rgb(11,20,18)',
          'star-intensity': 0.55
        });

        updateMarkers();
        fetchLiveData();
      });

      map.on('error', (event) => {
        mapError = event?.error?.message || 'Mapbox failed to load.';
      });
    } catch (error) {
      mapError = error?.message || 'Mapbox failed to initialize.';
    }

    refreshInterval = setInterval(fetchLiveData, 5 * 60 * 1000);
  });

  onDestroy(() => {
    if (refreshInterval) clearInterval(refreshInterval);
    clearMarkers();
    if (map) map.remove();
  });

  function clearMarkers() {
    markers.forEach((marker) => marker.remove());
    markers = [];
  }

  function updateMarkers() {
    if (!map || !map.loaded() || !mapboxgl) return;

    clearMarkers();
    markers = dataCenters.map((center) => {
      const color = getStatusColor(center.status);
      const el = document.createElement('button');
      el.type = 'button';
      el.className = 'live-dc-marker';
      el.style.color = color;
      el.setAttribute('aria-label', `${center.name} - ${center.city}`);
      el.innerHTML = `
        <span class="live-marker-outer" style="background:${getStatusBg(center.status)}">
          <span class="live-marker-inner" style="background:${color}"></span>
        </span>
      `;

      el.addEventListener('click', () => {
        activeCenter = activeCenter?.id === center.id ? null : center;
        map.flyTo({ center: [center.lng, center.lat], zoom: 4, duration: 1400 });
      });

      return new mapboxgl.Marker(el).setLngLat([center.lng, center.lat]).addTo(map);
    });
  }
</script>

<section class="live-map-section" class:visible>
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
      <p>Real-time monitoring of 15 data centers across 6 continents. Data refreshes every 5 minutes.</p>
    </div>
    <div class="header-stats">
      <div class="stat-card">
        <div class="stat-value">99.99%</div>
        <div class="stat-label">Uptime</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">0.378</div>
        <div class="stat-label">Avg Carbon (kgCO2/kWh)</div>
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
    <div bind:this={mapContainer} class="mapbox-live-map"></div>
    {#if mapError}
      <div class="map-error">{mapError}</div>
    {/if}

    <div class="map-legend">
      <div class="legend-item"><span class="legend-dot optimal"></span>Optimal</div>
      <div class="legend-item"><span class="legend-dot warning"></span>Warning</div>
      <div class="legend-item"><span class="legend-dot critical"></span>Critical</div>
    </div>

    {#if activeCenter}
      <div class="center-details" transition:fade>
        <div class="details-header">
          <h3>{activeCenter.name}</h3>
          <button class="close-btn" on:click={() => activeCenter = null} aria-label="Close">x</button>
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
            <div class="metric-value">{activeCenter.carbon} kgCO2/kWh</div>
            <div class="metric-bar">
              <div class="metric-fill" style="width: {Math.min(activeCenter.carbon * 100, 100)}%; background: {activeCenter.carbon > 0.5 ? '#d35d5c' : activeCenter.carbon > 0.3 ? '#b79563' : '#2cad84'}"></div>
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
              <div class="metric-value-small">{activeCenter.temp} C</div>
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
</section>

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

  .header-left { flex: 1; }

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

  .last-update {
    margin-left: 12px;
    font-size: 10px;
    font-weight: 600;
    color: rgba(244,247,245,0.4);
    text-transform: none;
    letter-spacing: normal;
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
    height: 620px;
    margin: 0 auto;
    position: relative;
    overflow: hidden;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.08);
    background: #07110f;
    box-shadow: 0 28px 80px rgba(0,0,0,0.36);
  }

  .mapbox-live-map {
    position: absolute;
    inset: 0;
  }

  .map-container::after {
    content: '';
    position: absolute;
    inset: 0;
    pointer-events: none;
    background:
      radial-gradient(circle at 50% 45%, transparent 45%, rgba(6,14,12,0.28) 100%),
      linear-gradient(180deg, rgba(6,14,12,0.02), rgba(6,14,12,0.26));
  }

  :global(.live-dc-marker) {
    appearance: none;
    padding: 0;
    border: 0;
    background: transparent;
    cursor: pointer;
  }

  :global(.live-marker-outer) {
    width: 26px;
    height: 26px;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: liveMarkerPulse 5s ease-in-out infinite;
  }

  :global(.live-marker-inner) {
    width: 10px;
    height: 10px;
    border-radius: 999px;
    box-shadow: 0 0 10px currentColor;
    animation: liveMarkerCorePulse 5s ease-in-out infinite;
  }

  @keyframes liveMarkerPulse {
    0%, 100% {
      transform: scale(1);
      box-shadow: 0 0 0 0 rgba(244,247,245,0.03);
      opacity: 0.82;
    }
    50% {
      transform: scale(1.28);
      box-shadow: 0 0 22px 5px rgba(244,247,245,0.08);
      opacity: 1;
    }
  }

  @keyframes liveMarkerCorePulse {
    0%, 100% { transform: scale(0.9); opacity: 0.72; }
    50% { transform: scale(1); opacity: 1; }
  }

  .map-error {
    position: absolute;
    inset: 18px;
    z-index: 3;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    border-radius: 18px;
    background: rgba(6,14,12,0.92);
    border: 1px solid rgba(211,93,92,0.35);
    color: #f4c7c7;
    text-align: center;
    font-size: 13px;
    font-weight: 700;
  }

  .map-legend {
    position: absolute;
    left: 22px;
    bottom: 22px;
    z-index: 2;
    display: flex;
    gap: 12px;
    padding: 10px 14px;
    border-radius: 999px;
    background: rgba(6,14,12,0.82);
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-weight: 800;
    color: rgba(244,247,245,0.7);
  }

  .legend-dot {
    width: 8px;
    height: 8px;
    border-radius: 999px;
  }

  .legend-dot.optimal { background: #2cad84; }
  .legend-dot.warning { background: #b79563; }
  .legend-dot.critical { background: #d35d5c; }

  .center-details {
    position: absolute;
    top: 50%;
    right: 24px;
    z-index: 2;
    transform: translateY(-50%);
    width: 320px;
    padding: 24px;
    border-radius: 20px;
    background: rgba(10,10,10,0.92);
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
    font-size: 22px;
    line-height: 1;
    cursor: pointer;
    padding: 0;
    width: 24px;
    height: 24px;
  }

  .close-btn:hover { color: #f4f7f5; }

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

  .metric-value,
  .metric-value-small {
    font-size: 18px;
    font-weight: 900;
    color: #2cad84;
    letter-spacing: -0.02em;
  }

  .metric-value-small { font-size: 16px; }

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

    .map-container {
      margin: 0 24px;
    }

    .center-details {
      position: absolute;
      left: 24px;
      right: 24px;
      top: auto;
      bottom: 76px;
      transform: none;
      width: auto;
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

    .map-container {
      height: 560px;
      margin: 0 16px;
    }

    .map-legend {
      left: 16px;
      right: 16px;
      justify-content: center;
      flex-wrap: wrap;
      border-radius: 16px;
    }
  }
</style>
