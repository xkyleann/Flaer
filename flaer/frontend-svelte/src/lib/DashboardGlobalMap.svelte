<script>
  import { onMount, onDestroy } from 'svelte';
  import 'mapbox-gl/dist/mapbox-gl.css';

  let activeFilter = 'all';
  let selectedDC = null;
  let mapContainer;
  let map;
  let mapboxgl;
  let markers = [];
  let mapError = '';

  const MAPBOX_TOKEN =
    import.meta.env.VITE_MAPBOX_TOKEN ||
    'pk.eyJ1IjoiYmVya2lubmJlbGVyIiwiYSI6ImNtb2tqcTZ5MzAyMjkycHFsbml6aHdzb3MifQ.HjyuZunhCOe7tMg3mWALcg';

  // Add or replace your real data centers here.
  // Required fields for the map are: id, name, risk, lng, and lat.
  const dataCenters = [
    { id: 'nv', name: 'N. Virginia', region: 'US East', risk: 'high', lng: -77.0, lat: 38.9, co2: '412 gCO2/kWh', cap: '240 MW', pue: '1.82', renew: '22%' },
    { id: 'ca', name: 'California', region: 'US West', risk: 'med', lng: -122.0, lat: 37.5, co2: '220 gCO2/kWh', cap: '160 MW', pue: '1.65', renew: '48%' },
    { id: 'sto', name: 'Stockholm', region: 'Nordic', risk: 'low', lng: 18.1, lat: 59.3, co2: '22 gCO2/kWh', cap: '90 MW', pue: '1.18', renew: '92%' },
    { id: 'fra', name: 'Frankfurt', region: 'EU West', risk: 'med', lng: 8.7, lat: 50.1, co2: '284 gCO2/kWh', cap: '320 MW', pue: '1.52', renew: '45%' },
    { id: 'war', name: 'Warsaw', region: 'EU Central', risk: 'low', lng: 21.0, lat: 52.2, co2: '234 gCO2/kWh', cap: '120 MW', pue: '1.44', renew: '58%' },
    { id: 'sgp', name: 'Singapore', region: 'APAC', risk: 'high', lng: 103.8, lat: 1.3, co2: '408 gCO2/kWh', cap: '180 MW', pue: '1.75', renew: '18%' },
    { id: 'tky', name: 'Tokyo', region: 'APAC', risk: 'med', lng: 139.7, lat: 35.7, co2: '340 gCO2/kWh', cap: '200 MW', pue: '1.60', renew: '32%' },
    { id: 'syd', name: 'Sydney', region: 'ANZ', risk: 'low', lng: 151.2, lat: -33.9, co2: '180 gCO2/kWh', cap: '100 MW', pue: '1.38', renew: '65%' },
    { id: 'dxb', name: 'Dubai', region: 'ME', risk: 'med', lng: 55.3, lat: 25.3, co2: '310 gCO2/kWh', cap: '140 MW', pue: '1.70', renew: '28%' },
    { id: 'bra', name: 'Sao Paulo', region: 'LATAM', risk: 'low', lng: -46.6, lat: -23.5, co2: '120 gCO2/kWh', cap: '85 MW', pue: '1.42', renew: '74%' },
  ];

  function riskColor(risk) {
    if (risk === 'high') return '#d35d5c';
    if (risk === 'med') return '#b67e3d';
    return '#2cad84';
  }

  function riskBg(risk) {
    if (risk === 'high') return 'rgba(211,93,92,0.12)';
    if (risk === 'med') return 'rgba(182,126,61,0.12)';
    return 'rgba(44,173,132,0.16)';
  }

  $: filtered = dataCenters.filter((dc) => {
    if (activeFilter === 'all') return true;
    if (activeFilter === 'high') return dc.risk === 'high';
    if (activeFilter === 'med') return dc.risk === 'med';
    if (activeFilter === 'low') return dc.risk === 'low';
    if (activeFilter === 'eu') return ['fra', 'war', 'sto'].includes(dc.id);
    return true;
  });

  onMount(async () => {
    try {
      const mbx = await import('mapbox-gl');
      mapboxgl = mbx.default;
      mapboxgl.accessToken = MAPBOX_TOKEN;

      map = new mapboxgl.Map({
        container: mapContainer,
        style: 'mapbox://styles/mapbox/dark-v11',
        center: [0, 20],
        zoom: 1.35,
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

        updateMarkers();
      });

      map.on('error', (event) => {
        mapError = event?.error?.message || 'Mapbox failed to load.';
      });
    } catch (error) {
      mapError = error?.message || 'Mapbox failed to initialize.';
    }
  });

  onDestroy(() => {
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

    markers = filtered.map((dc) => {
      const el = document.createElement('button');
      el.type = 'button';
      el.className = 'dc-marker';
      el.setAttribute('aria-label', `${dc.name} data center`);
      el.style.color = riskColor(dc.risk);
      el.innerHTML = `
        <span class="marker-outer" style="background: ${riskBg(dc.risk)}">
          <span class="marker-inner" style="background: ${riskColor(dc.risk)}"></span>
        </span>
      `;

      el.addEventListener('click', () => {
        selectedDC = dc;
        map.flyTo({
          center: [dc.lng, dc.lat],
          zoom: 4.25,
          duration: 1500
        });
      });

      return new mapboxgl.Marker(el).setLngLat([dc.lng, dc.lat]).addTo(map);
    });
  }

  $: activeFilter, updateMarkers();
</script>

<section class="global-map-page">
  <div class="gmap-wrap">
    <div bind:this={mapContainer} class="mapbox-container"></div>

    <div class="gmap-filters">
      {#each [['all','All facilities'],['high','High risk'],['med','Medium risk'],['low','Low risk'],['eu','EU regulated']] as [val, lbl]}
        <button class="gf-chip" class:on={activeFilter === val} on:click={() => activeFilter = val}>{lbl}</button>
      {/each}
    </div>

    {#if mapError}
      <div class="map-error">{mapError}</div>
    {/if}

    <div class="map-legend-abs">
      <div class="ml-item"><span class="ml-dot" style="background:#d35d5c"></span>High risk</div>
      <div class="ml-item"><span class="ml-dot" style="background:#b67e3d"></span>Medium</div>
      <div class="ml-item"><span class="ml-dot" style="background:#2cad84"></span>Low risk</div>
    </div>

    <div class="dc-panel">
      {#if selectedDC}
        <div class="dc-panel-header">
          <h3>{selectedDC.name}</h3>
          <span class="dc-risk-badge" style="background:{riskBg(selectedDC.risk)};color:{riskColor(selectedDC.risk)}">{selectedDC.risk} risk</span>
        </div>
        <div class="dc-panel-body">
          <div class="dc-stat-grid">
            <div class="dc-stat"><div class="sl">Carbon Intensity</div><div class="sv">{selectedDC.co2}</div></div>
            <div class="dc-stat"><div class="sl">Capacity</div><div class="sv">{selectedDC.cap}</div></div>
            <div class="dc-stat"><div class="sl">PUE</div><div class="sv">{selectedDC.pue}</div></div>
            <div class="dc-stat"><div class="sl">Renewable</div><div class="sv">{selectedDC.renew}</div></div>
          </div>
          <div class="dc-section-title">Region</div>
          <div class="dc-row"><span>Location</span><strong>{selectedDC.region}</strong></div>
          <div class="dc-row"><span>Coordinates</span><strong>{selectedDC.lat}, {selectedDC.lng}</strong></div>
        </div>
      {:else}
        <div class="dc-panel-placeholder">
          <p>Click a facility on the map to view details</p>
        </div>
      {/if}
    </div>
  </div>
</section>

<style>
  .global-map-page {
    position: relative;
    height: calc(100vh - 104px);
    min-height: 620px;
  }

  .gmap-wrap {
    position: absolute;
    inset: 0;
    overflow: hidden;
    background: linear-gradient(180deg, #091310, #060e0c);
  }

  .mapbox-container {
    position: absolute;
    inset: 0;
  }

  .gmap-filters {
    position: absolute;
    left: 22px;
    bottom: 22px;
    z-index: 10;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    max-width: calc(100% - 420px);
    padding: 10px;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    background: rgba(6,14,12,0.78);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
  }

  .gf-chip {
    padding: 7px 13px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.09);
    background: rgba(255,255,255,0.05);
    color: rgba(244,247,245,0.7);
    font-size: 12px;
    font-weight: 800;
    cursor: pointer;
    transition: 0.14s;
    font-family: inherit;
  }

  .gf-chip.on {
    background: rgba(44,173,132,0.18);
    border-color: rgba(44,173,132,0.30);
    color: #b6ffe7;
  }

  :global(.dc-marker) {
    appearance: none;
    padding: 0;
    border: 0;
    background: transparent;
    cursor: pointer;
  }

  :global(.marker-outer) {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s ease;
    animation: markerPulse 4.8s ease-in-out infinite;
  }

  :global(.marker-outer:hover) { transform: scale(1.2); }

  :global(.marker-inner) {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    box-shadow: 0 0 10px currentColor;
    animation: markerCorePulse 4.8s ease-in-out infinite;
  }

  @keyframes markerPulse {
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

  @keyframes markerCorePulse {
    0%, 100% {
      transform: scale(0.9);
      opacity: 0.72;
    }
    50% {
      transform: scale(1);
      opacity: 1;
    }
  }

  .map-legend-abs {
    position: absolute;
    right: 22px;
    bottom: 22px;
    z-index: 10;
    display: flex;
    gap: 9px;
    padding: 8px 11px;
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
    color: rgba(244,247,245,0.7);
  }

  .ml-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
  }

  .map-error {
    position: absolute;
    inset: 96px 22px 22px;
    z-index: 12;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    border-radius: 18px;
    background: rgba(6,14,12,0.92);
    border: 1px solid rgba(211,93,92,0.35);
    color: #f4c7c7;
    text-align: center;
    font-size: 13px;
    font-weight: 700;
  }

  .dc-panel {
    position: absolute;
    top: 104px;
    right: 22px;
    z-index: 10;
    width: min(340px, calc(100vw - 44px));
    max-height: calc(100% - 160px);
    overflow: auto;
    border-radius: 20px;
    background: rgba(7,17,15,0.82);
    border: 1px solid rgba(255,255,255,0.09);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    box-shadow: 0 20px 56px rgba(0,0,0,0.28);
  }

  .dc-panel-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 160px;
    padding: 32px;
    text-align: center;
    color: rgba(244,247,245,0.46);
    font-size: 13px;
  }

  .dc-panel-header {
    padding: 16px 18px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
  }

  .dc-panel-header h3 {
    font-size: 15px;
    font-weight: 900;
    color: #f4f7f5;
    margin: 0;
  }

  .dc-risk-badge {
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 10px;
    font-weight: 900;
    text-transform: capitalize;
  }

  .dc-panel-body { padding: 16px; }

  .dc-stat-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 14px;
  }

  .dc-stat {
    padding: 12px;
    border-radius: 14px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
  }

  .sl {
    font-size: 10px;
    color: rgba(244,247,245,0.46);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 5px;
  }

  .sv {
    font-size: 20px;
    font-weight: 900;
    letter-spacing: -0.04em;
    color: #f4f7f5;
  }

  .dc-section-title {
    font-size: 12px;
    font-weight: 800;
    color: rgba(244,247,245,0.54);
    text-transform: uppercase;
    letter-spacing: 0.09em;
    margin: 14px 0 8px;
  }

  .dc-row {
    display: flex;
    justify-content: space-between;
    gap: 16px;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    font-size: 13px;
  }

  .dc-row span { color: rgba(244,247,245,0.56); }
  .dc-row strong { color: #f4f7f5; text-align: right; }

  @media (max-width: 900px) {
    .global-map-page {
      min-height: 720px;
    }

    .dc-panel {
      top: auto;
      left: 16px;
      right: 16px;
      bottom: 86px;
      width: auto;
      max-height: 280px;
    }

    .gmap-filters {
      left: 16px;
      right: 16px;
      bottom: 16px;
      max-width: none;
    }

    .map-legend-abs {
      top: 92px;
      right: 16px;
      bottom: auto;
    }
  }
</style>
