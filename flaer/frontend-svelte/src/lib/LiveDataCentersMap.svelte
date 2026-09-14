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

  const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
  const MAPBOX_TOKEN =
    import.meta.env.VITE_MAPBOX_TOKEN ||
    'pk.eyJ1IjoiYmVya2lubmJlbGVyIiwiYSI6ImNtb2tqcTZ5MzAyMjkycHFsbml6aHdzb3MifQ.HjyuZunhCOe7tMg3mWALcg';

  let dataCenters = [
    { id: 1, regionKey: 'dublin', name: 'EU-West-1', city: 'Dublin', lng: -6.26, lat: 53.35, status: 'optimal', load: 61, carbon: 0.295, temp: 16, capacity: '780 MW', renewable: 68 },
    { id: 2, regionKey: 'london', name: 'EU-UK-1', city: 'London', lng: -0.13, lat: 51.51, status: 'warning', load: 72, carbon: 0.318, temp: 18, capacity: '840 MW', renewable: 54 },
    { id: 3, regionKey: 'amsterdam', name: 'EU-Northwest-1', city: 'Amsterdam', lng: 4.9, lat: 52.37, status: 'warning', load: 67, carbon: 0.362, temp: 17, capacity: '690 MW', renewable: 57 },
    { id: 4, regionKey: 'frankfurt', name: 'EU-Central-1', city: 'Frankfurt', lng: 8.68, lat: 50.11, status: 'warning', load: 74, carbon: 0.338, temp: 19, capacity: '920 MW', renewable: 52 },
    { id: 5, regionKey: 'paris', name: 'EU-West-2', city: 'Paris', lng: 2.35, lat: 48.86, status: 'optimal', load: 58, carbon: 0.071, temp: 18, capacity: '710 MW', renewable: 76 },
    { id: 6, regionKey: 'madrid', name: 'EU-Southwest-1', city: 'Madrid', lng: -3.7, lat: 40.42, status: 'optimal', load: 53, carbon: 0.184, temp: 23, capacity: '560 MW', renewable: 74 },
    { id: 7, regionKey: 'milan', name: 'EU-South-1', city: 'Milan', lng: 9.19, lat: 45.46, status: 'warning', load: 64, carbon: 0.289, temp: 21, capacity: '590 MW', renewable: 61 },
    { id: 8, regionKey: 'zurich', name: 'EU-Alpine-1', city: 'Zurich', lng: 8.54, lat: 47.38, status: 'optimal', load: 49, carbon: 0.082, temp: 16, capacity: '430 MW', renewable: 91 },
    { id: 9, regionKey: 'warsaw', name: 'EU-Central-2', city: 'Warsaw', lng: 21.01, lat: 52.23, status: 'critical', load: 71, carbon: 0.612, temp: 17, capacity: '650 MW', renewable: 29 },
    { id: 10, regionKey: 'stockholm', name: 'EU-North-1', city: 'Stockholm', lng: 18.07, lat: 59.33, status: 'optimal', load: 48, carbon: 0.013, temp: 12, capacity: '650 MW', renewable: 98 },
    { id: 11, regionKey: 'oslo', name: 'EU-North-2', city: 'Oslo', lng: 10.75, lat: 59.91, status: 'optimal', load: 45, carbon: 0.025, temp: 11, capacity: '410 MW', renewable: 99 },
    { id: 12, regionKey: 'helsinki', name: 'EU-North-3', city: 'Helsinki', lng: 24.94, lat: 60.17, status: 'optimal', load: 51, carbon: 0.071, temp: 10, capacity: '470 MW', renewable: 91 },
    { id: 13, regionKey: 'copenhagen', name: 'EU-Nordic-1', city: 'Copenhagen', lng: 12.57, lat: 55.68, status: 'optimal', load: 55, carbon: 0.145, temp: 14, capacity: '520 MW', renewable: 81 },
    { id: 14, regionKey: 'vienna', name: 'EU-Central-3', city: 'Vienna', lng: 16.37, lat: 48.21, status: 'optimal', load: 57, carbon: 0.198, temp: 18, capacity: '480 MW', renewable: 72 },
    { id: 15, regionKey: 'lisbon', name: 'EU-Southwest-2', city: 'Lisbon', lng: -9.14, lat: 38.72, status: 'optimal', load: 50, carbon: 0.201, temp: 22, capacity: '460 MW', renewable: 70 }
  ];

  $: needsReview = dataCenters.filter((center) => center.status !== 'optimal').length;

  function getStatusColor(status) {
    return status === 'optimal' ? '#2cad84' : status === 'warning' ? '#b79563' : '#d35d5c';
  }

  function statusFromCarbon(carbon) {
    if (carbon >= 0.65) return 'critical';
    if (carbon >= 0.4) return 'warning';
    return 'optimal';
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
          status: statusFromCarbon(liveRegionData.carbon / 1000)
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
        // Keep the globe, but start close enough that the Europe-only portfolio
        // is legible instead of collapsing into a vertical strip.
        center: [10, 51],
        zoom: 2.8,
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
        requestAnimationFrame(() => map?.resize());
        fetchLiveData();

        map.on('click', 'facility-core', (event) => {
          const id = Number(event.features?.[0]?.properties?.id);
          const center = dataCenters.find((item) => item.id === id);
          if (!center) return;

          activeCenter = center;
          map.flyTo({ center: [center.lng, center.lat], zoom: 3.2, duration: 1100 });
        });

        map.on('mouseenter', 'facility-core', () => { map.getCanvas().style.cursor = 'pointer'; });
        map.on('mouseleave', 'facility-core', () => { map.getCanvas().style.cursor = ''; });
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

    // Add the visible, clickable markers first. The optional GeoJSON layers below
    // enhance the map but must never prevent facility locations from appearing.
    renderFacilityMarkers();

    const facilities = {
      type: 'FeatureCollection',
      features: dataCenters.map((center) => ({
        type: 'Feature',
        properties: { id: center.id, city: center.city, status: center.status },
        geometry: { type: 'Point', coordinates: [center.lng, center.lat] }
      }))
    };

    const source = map.getSource('facilities');
    if (source) {
      source.setData(facilities);
      return;
    }

    map.addSource('facilities', { type: 'geojson', data: facilities });
    const color = ['match', ['get', 'status'], 'optimal', '#2cad84', 'warning', '#b79563', '#d35d5c'];

    map.addLayer({
      id: 'facility-halo', type: 'circle', source: 'facilities',
      paint: { 'circle-radius': 13, 'circle-color': color, 'circle-opacity': 0.22, 'circle-blur': 0.45 }
    });
    map.addLayer({
      id: 'facility-core', type: 'circle', source: 'facilities',
      paint: { 'circle-radius': 5, 'circle-color': color, 'circle-stroke-color': '#f4f7f5', 'circle-stroke-width': 1.25 }
    });
    map.addLayer({
      id: 'facility-label', type: 'symbol', source: 'facilities',
      layout: {
        'text-field': ['get', 'city'], 'text-size': 10, 'text-offset': [0, 1.35],
        'text-anchor': 'top', 'text-allow-overlap': false
      },
      paint: { 'text-color': '#f4f7f5', 'text-halo-color': '#07110f', 'text-halo-width': 1.5 }
    });

  }

  // DOM markers are deliberately retained as a resilient, high-contrast fallback
  // for the globe view. They also provide keyboard-accessible facility selection.
  function renderFacilityMarkers() {
    clearMarkers();
    markers = dataCenters.map((center) => {
      const color = getStatusColor(center.status);
      const marker = document.createElement('button');
      marker.type = 'button';
      marker.className = 'facility-marker-fallback';
      marker.setAttribute('aria-label', `View ${center.city} facility`);
      marker.title = `${center.city} · ${center.name}`;
      marker.style.setProperty('--facility-color', color);
      marker.innerHTML = `<span class="facility-marker-core"></span><span class="facility-marker-label">${center.city}</span>`;
      marker.addEventListener('click', (event) => {
        event.stopPropagation();
        activeCenter = center;
        map.flyTo({ center: [center.lng, center.lat], zoom: 3.2, duration: 1100 });
      });
      return new mapboxgl.Marker({ element: marker, anchor: 'center' })
        .setLngLat([center.lng, center.lat])
        .addTo(map);
    });
  }
</script>

<section class="live-map-section" class:visible>
  <div class="map-header">
    <div class="header-left">
      <div class="live-indicator">
        <span class="pulse-dot"></span>
        <span class="live-text">Portfolio locations</span>
        {#if lastUpdate}
          <span class="last-update">Updated {new Date(lastUpdate).toLocaleTimeString()}</span>
        {/if}
      </div>
      <h2>European Data Center Network</h2>
      <p>All 15 facilities in the European portfolio. Select a location for operating context.</p>
    </div>
    <div class="header-stats">
      <div class="stat-card">
        <div class="stat-value">15</div>
        <div class="stat-label">Facilities</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">15</div>
        <div class="stat-label">European locations</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{needsReview}</div>
        <div class="stat-label">Need review</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">54%</div>
        <div class="stat-label">Renewable mix</div>
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
    z-index: 2;
  }

  .map-container::after {
    content: '';
    position: absolute;
    inset: 0;
    pointer-events: none;
    background:
      radial-gradient(circle at 50% 45%, transparent 45%, rgba(6,14,12,0.28) 100%),
      linear-gradient(180deg, rgba(6,14,12,0.02), rgba(6,14,12,0.26));
    z-index: 1;
  }

  :global(.facility-marker-fallback) {
    appearance: none;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 0;
    border: 0;
    background: transparent;
    color: var(--facility-color);
    cursor: pointer;
    filter: drop-shadow(0 2px 6px rgba(0,0,0,0.78));
  }

  :global(.facility-marker-core) {
    display: block;
    width: 17px;
    height: 17px;
    flex: 0 0 17px;
    border: 3px solid rgba(244,247,245,0.98);
    border-radius: 50%;
    background: var(--facility-color);
    box-shadow: 0 0 0 4px rgba(7,17,15,0.58), 0 0 18px var(--facility-color);
  }

  :global(.facility-marker-fallback:hover .facility-marker-core),
  :global(.facility-marker-fallback:focus-visible .facility-marker-core) {
    transform: scale(1.25);
  }

  :global(.facility-marker-label) {
    padding: 3px 6px;
    border: 1px solid rgba(255,255,255,0.13);
    border-radius: 5px;
    background: rgba(5,15,12,0.9);
    color: rgba(244,247,245,0.92);
    font-size: 10px;
    font-weight: 750;
    line-height: 1;
    white-space: nowrap;
  }

  :global(.live-dc-marker) {
    appearance: none;
    padding: 0;
    border: 0;
    background: transparent;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    filter: drop-shadow(0 2px 6px rgba(0,0,0,0.6));
  }

  :global(.live-marker-outer) {
    width: 22px;
    height: 22px;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: liveMarkerPulse 5s ease-in-out infinite;
  }

  :global(.live-marker-inner) {
    width: 9px;
    height: 9px;
    border-radius: 999px;
    box-shadow: 0 0 10px currentColor;
    animation: liveMarkerCorePulse 5s ease-in-out infinite;
  }

  :global(.live-marker-label) {
    padding: 3px 6px;
    border-radius: 5px;
    background: rgba(5, 15, 12, 0.86);
    border: 1px solid rgba(255,255,255,0.12);
    color: rgba(244,247,245,0.88);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: -0.01em;
    white-space: nowrap;
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
