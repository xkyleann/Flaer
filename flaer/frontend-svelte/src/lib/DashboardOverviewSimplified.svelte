<script>
  import { onMount, onDestroy } from 'svelte';
  import 'mapbox-gl/dist/mapbox-gl.css';

  let mapContainer;
  let map;
  let mapboxgl;
  let markers = [];

  const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN ||
    'pk.eyJ1IjoiYmVya2lubmJlbGVyIiwiYSI6ImNtb2tqcTZ5MzAyMjkycHFsbml6aHdzb3MifQ.HjyuZunhCOe7tMg3mWALcg';

  // 14 data centers matching sidebar badge
  const dataCenters = [
    { name: 'N. Virginia', lng: -77.0, lat: 38.9, status: 'warning', emissions: '412 gCO₂/kWh', capacity: '850 MW', renewable: 45, pue: 1.82 },
    { name: 'Oregon', lng: -120.55, lat: 44.0, status: 'excellent', emissions: '95 gCO₂/kWh', capacity: '720 MW', renewable: 89, pue: 1.18 },
    { name: 'Iowa', lng: -93.1, lat: 42.0, status: 'good', emissions: '412 gCO₂/kWh', capacity: '640 MW', renewable: 58, pue: 1.45 },
    { name: 'Montreal', lng: -73.57, lat: 45.5, status: 'excellent', emissions: '29 gCO₂/kWh', capacity: '580 MW', renewable: 97, pue: 1.15 },
    { name: 'Frankfurt', lng: 8.68, lat: 50.11, status: 'good', emissions: '338 gCO₂/kWh', capacity: '920 MW', renewable: 52, pue: 1.52 },
    { name: 'Dublin', lng: -6.26, lat: 53.35, status: 'good', emissions: '295 gCO₂/kWh', capacity: '780 MW', renewable: 68, pue: 1.38 },
    { name: 'Stockholm', lng: 18.07, lat: 59.33, status: 'excellent', emissions: '13 gCO₂/kWh', capacity: '650 MW', renewable: 98, pue: 1.08 },
    { name: 'Milan', lng: 9.19, lat: 45.46, status: 'good', emissions: '289 gCO₂/kWh', capacity: '590 MW', renewable: 61, pue: 1.42 },
    { name: 'Tokyo', lng: 139.69, lat: 35.68, status: 'good', emissions: '462 gCO₂/kWh', capacity: '1100 MW', renewable: 38, pue: 1.60 },
    { name: 'Hong Kong', lng: 114.17, lat: 22.32, status: 'critical', emissions: '678 gCO₂/kWh', capacity: '480 MW', renewable: 12, pue: 1.88 },
    { name: 'Singapore', lng: 103.82, lat: 1.35, status: 'warning', emissions: '408 gCO₂/kWh', capacity: '720 MW', renewable: 28, pue: 1.75 },
    { name: 'Mumbai', lng: 72.88, lat: 19.08, status: 'critical', emissions: '708 gCO₂/kWh', capacity: '620 MW', renewable: 24, pue: 1.72 },
    { name: 'Sao Paulo', lng: -46.63, lat: -23.55, status: 'excellent', emissions: '82 gCO₂/kWh', capacity: '540 MW', renewable: 83, pue: 1.28 },
    { name: 'Bahrain', lng: 50.56, lat: 26.07, status: 'warning', emissions: '632 gCO₂/kWh', capacity: '420 MW', renewable: 18, pue: 1.68 },
  ];

  function getStatusColor(status) {
    return {
      'excellent': '#2cad84',
      'good': '#7faeff',
      'warning': '#b67e3d',
      'critical': '#d35d5c'
    }[status] || '#7faeff';
  }

  function getStatusLabel(status) {
    return {
      'excellent': 'Excellent',
      'good': 'Good',
      'warning': 'Needs Attention',
      'critical': 'Critical'
    }[status] || 'Good';
  }

  onMount(async () => {
    try {
      const mbx = await import('mapbox-gl');
      mapboxgl = mbx.default;
      mapboxgl.accessToken = MAPBOX_TOKEN;

      map = new mapboxgl.Map({
        container: mapContainer,
        style: 'mapbox://styles/mapbox/dark-v11',
        center: [20, 30],
        zoom: 1.5,
        projection: 'globe',
        attributionControl: false
      });

      map.addControl(new mapboxgl.NavigationControl({ showCompass: false }), 'top-right');

      map.on('load', () => {
        map.setFog({
          color: 'rgb(6,14,12)',
          'high-color': 'rgb(36,92,110)',
          'horizon-blend': 0.02,
          'space-color': 'rgb(11, 20, 18)',
          'star-intensity': 0.6
        });

        createMarkers();
      });
    } catch (error) {
      console.error('Mapbox error:', error);
    }
  });

  function createMarkers() {
    if (!map || !mapboxgl) return;

    dataCenters.forEach(dc => {
      const el = document.createElement('div');
      el.className = 'custom-marker';
      el.style.backgroundColor = getStatusColor(dc.status);
      el.style.width = '16px';
      el.style.height = '16px';
      el.style.borderRadius = '50%';
      el.style.border = `3px solid ${getStatusColor(dc.status)}40`;
      el.style.boxShadow = `0 0 20px ${getStatusColor(dc.status)}80`;
      el.style.cursor = 'pointer';

      const popup = new mapboxgl.Popup({ offset: 25, closeButton: false })
        .setHTML(`
          <div style="padding: 8px; min-width: 200px;">
            <div style="font-weight: 700; font-size: 14px; margin-bottom: 6px; color: #f4f7f5;">${dc.name}</div>
            <div style="font-size: 12px; color: rgba(244,247,245,0.7); margin-bottom: 8px;">
              Status: <span style="color: ${getStatusColor(dc.status)}; font-weight: 600;">${getStatusLabel(dc.status)}</span>
            </div>
            <div style="font-size: 11px; color: rgba(244,247,245,0.6); line-height: 1.6;">
              <div>Emissions: <strong>${dc.emissions}</strong></div>
              <div>Capacity: <strong>${dc.capacity}</strong></div>
              <div>Renewable: <strong>${dc.renewable}%</strong></div>
            </div>
          </div>
        `);

      const marker = new mapboxgl.Marker(el)
        .setLngLat([dc.lng, dc.lat])
        .setPopup(popup)
        .addTo(map);

      markers.push(marker);
    });
  }

  onDestroy(() => {
    markers.forEach(m => m.remove());
    if (map) map.remove();
  });
</script>

<div class="simplified-overview">
  <!-- Key Metrics Row -->
  <div class="metrics-row">
    <div class="metric-card">
      <div class="metric-icon">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
          <circle cx="12" cy="12" r="9" stroke="#2cad84" stroke-width="2"/>
          <path d="M12 3 C12 3 8 8 8 12 C8 16 12 21 12 21 C12 21 16 16 16 12 C16 8 12 3 12 3Z" stroke="#2cad84" stroke-width="1.5" fill="none"/>
          <line x1="3" y1="12" x2="21" y2="12" stroke="#2cad84" stroke-width="1.5"/>
        </svg>
      </div>
      <div class="metric-content">
        <div class="metric-label">Total Facilities</div>
        <div class="metric-value">14</div>
        <div class="metric-sub">Across 5 continents</div>
      </div>
    </div>

    <div class="metric-card">
      <div class="metric-icon">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
          <path d="M13 2L3 14h8l-1 8 10-12h-8l1-8z" stroke="#7faeff" stroke-width="2" stroke-linejoin="round" fill="none"/>
        </svg>
      </div>
      <div class="metric-content">
        <div class="metric-label">Total Capacity</div>
        <div class="metric-value">9,590 MW</div>
        <div class="metric-sub trend-up">+8% this quarter</div>
      </div>
    </div>

    <div class="metric-card">
      <div class="metric-icon">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
          <path d="M12 2 L15 8 L22 9 L17 14 L18 21 L12 18 L6 21 L7 14 L2 9 L9 8 Z" stroke="#2cad84" stroke-width="2" fill="none"/>
        </svg>
      </div>
      <div class="metric-content">
        <div class="metric-label">Renewable Energy</div>
        <div class="metric-value">54%</div>
        <div class="metric-sub trend-up">+12% vs last year</div>
      </div>
    </div>

    <div class="metric-card">
      <div class="metric-icon">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
          <rect x="3" y="3" width="18" height="18" rx="2" stroke="#b67e3d" stroke-width="2"/>
          <line x1="3" y1="9" x2="21" y2="9" stroke="#b67e3d" stroke-width="2"/>
          <line x1="3" y1="15" x2="21" y2="15" stroke="#b67e3d" stroke-width="2"/>
          <line x1="9" y1="3" x2="9" y2="21" stroke="#b67e3d" stroke-width="2"/>
          <line x1="15" y1="3" x2="15" y2="21" stroke="#b67e3d" stroke-width="2"/>
        </svg>
      </div>
      <div class="metric-content">
        <div class="metric-label">Avg Carbon Intensity</div>
        <div class="metric-value">356 g</div>
        <div class="metric-sub">gCO₂/kWh</div>
      </div>
    </div>
  </div>

  <!-- Map Section -->
  <div class="map-section">
    <div class="map-header">
      <h3>Global Data Center Portfolio</h3>
      <div class="map-legend">
        <div class="legend-item">
          <span class="legend-dot excellent"></span>
          <span>Excellent</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot good"></span>
          <span>Good</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot warning"></span>
          <span>Needs Attention</span>
        </div>
      </div>
    </div>
    <div class="map-container" bind:this={mapContainer}></div>
  </div>

  <!-- Quick Stats Grid -->
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-header">
        <span class="stat-title">Best Performer</span>
        <span class="stat-badge excellent">Excellent</span>
      </div>
      <div class="stat-location">Stockholm</div>
      <div class="stat-details">
        <div class="stat-row">
          <span>Carbon Intensity</span>
          <strong>13 gCO₂/kWh</strong>
        </div>
        <div class="stat-row">
          <span>Renewable</span>
          <strong>98%</strong>
        </div>
      </div>
    </div>

    <div class="stat-card">
      <div class="stat-header">
        <span class="stat-title">Needs Improvement</span>
        <span class="stat-badge warning">Action Required</span>
      </div>
      <div class="stat-location">N. Virginia</div>
      <div class="stat-details">
        <div class="stat-row">
          <span>Carbon Intensity</span>
          <strong>412 gCO₂/kWh</strong>
        </div>
        <div class="stat-row">
          <span>Renewable</span>
          <strong>45%</strong>
        </div>
      </div>
    </div>

    <div class="stat-card">
      <div class="stat-header">
        <span class="stat-title">This Month</span>
      </div>
      <div class="stat-location">Portfolio Summary</div>
      <div class="stat-details">
        <div class="stat-row">
          <span>Total Emissions</span>
          <strong>1.24M tCO₂e</strong>
        </div>
        <div class="stat-row trend-down">
          <span>vs Last Month</span>
          <strong>-12.4%</strong>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .simplified-overview {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .metrics-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 16px;
  }

  .metric-card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px;
    background: linear-gradient(135deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    transition: all 0.3s ease;
  }

  .metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(44,173,132,0.3);
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  }

  .metric-icon {
    font-size: 32px;
    flex-shrink: 0;
  }

  .metric-content {
    flex: 1;
    min-width: 0;
  }

  .metric-label {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: rgba(244,247,245,0.5);
    margin-bottom: 4px;
  }

  .metric-value {
    font-size: 28px;
    font-weight: 800;
    color: var(--text);
    line-height: 1;
    margin-bottom: 4px;
  }

  .metric-sub {
    font-size: 12px;
    color: rgba(244,247,245,0.6);
  }

  .trend-up {
    color: #2cad84;
  }

  .trend-down {
    color: #2cad84;
  }

  .map-section {
    background: linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    overflow: hidden;
  }

  .map-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 24px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
  }

  .map-header h3 {
    font-size: 18px;
    font-weight: 700;
    color: var(--text);
    margin: 0;
  }

  .map-legend {
    display: flex;
    gap: 20px;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: rgba(244,247,245,0.7);
  }

  .legend-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
  }

  .legend-dot.excellent {
    background: #2cad84;
    box-shadow: 0 0 8px rgba(44,173,132,0.6);
  }

  .legend-dot.good {
    background: #7faeff;
    box-shadow: 0 0 8px rgba(127,174,255,0.6);
  }

  .legend-dot.warning {
    background: #b67e3d;
    box-shadow: 0 0 8px rgba(182,126,61,0.6);
  }

  .map-container {
    height: 500px;
    width: 100%;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 16px;
  }

  .stat-card {
    padding: 20px;
    background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
  }

  .stat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }

  .stat-title {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: rgba(244,247,245,0.5);
  }

  .stat-badge {
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.03em;
  }

  .stat-badge.excellent {
    background: rgba(44,173,132,0.15);
    color: #2cad84;
  }

  .stat-badge.warning {
    background: rgba(182,126,61,0.15);
    color: #b67e3d;
  }

  .stat-location {
    font-size: 20px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 12px;
  }

  .stat-details {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 13px;
    color: rgba(244,247,245,0.6);
  }

  .stat-row strong {
    color: var(--text);
    font-weight: 600;
  }

  .stat-row.trend-down strong {
    color: #2cad84;
  }

  :global(.mapboxgl-popup-content) {
    background: rgba(11,23,20,0.98) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.6) !important;
  }

  :global(.mapboxgl-popup-tip) {
    border-top-color: rgba(11,23,20,0.98) !important;
  }

  @media (max-width: 1200px) {
    .metrics-row {
      grid-template-columns: repeat(2, 1fr);
    }

    .stats-grid {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 768px) {
    .metrics-row {
      grid-template-columns: 1fr;
    }

    .map-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 12px;
    }

    .map-container {
      height: 400px;
    }
  }
</style>