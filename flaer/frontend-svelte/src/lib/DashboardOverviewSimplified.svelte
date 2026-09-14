<script>
  import { onMount, onDestroy } from 'svelte';
  import 'mapbox-gl/dist/mapbox-gl.css';
  import { europeanPortfolio, portfolioDataNotice } from './europeanPortfolio.js';

  let mapContainer;
  let map;
  let mapboxgl;
  let markers = [];
  let mapFailed = false;
  let resizeObserver;
  let activeMapFilter = 'all';
  export let setScreen = () => {};

  const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN ||
    'pk.eyJ1IjoiYmVya2lubmJlbGVyIiwiYSI6ImNtb2tqcTZ5MzAyMjkycHFsbml6aHdzb3MifQ.HjyuZunhCOe7tMg3mWALcg';

  const dataCenters = europeanPortfolio.map((facility) => ({
    ...facility,
    status: facility.risk === 'high' ? 'critical' : facility.risk === 'medium' ? 'good' : 'excellent',
    emissions: `${facility.carbon} gCO₂/kWh`,
    capacity: `${facility.capacity} MW`
  }));

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

  function visibleDataCenters() {
    if (activeMapFilter === 'review') return dataCenters.filter((dc) => dc.status === 'critical' || dc.status === 'good');
    if (activeMapFilter === 'lower-risk') return dataCenters.filter((dc) => dc.status === 'excellent');
    return dataCenters;
  }

  onMount(async () => {
    try {
      const mbx = await import('mapbox-gl');
      mapboxgl = mbx.default;
      mapboxgl.accessToken = MAPBOX_TOKEN;

      map = new mapboxgl.Map({
        container: mapContainer,
        style: 'mapbox://styles/mapbox/dark-v11',
        center: [10, 51],
        // Europe-first framing keeps the 15 configured locations visible.
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
          'space-color': 'rgb(11, 20, 18)',
          'star-intensity': 0.6
        });

        createMarkers();
        requestAnimationFrame(() => map?.resize());
      });
      map.on('error', () => { mapFailed = true; });
      resizeObserver = new ResizeObserver(() => map?.resize());
      resizeObserver.observe(mapContainer);
    } catch (error) {
      console.error('Mapbox error:', error);
      mapFailed = true;
    }
  });

  function createMarkers() {
    if (!map || !mapboxgl) return;

    markers.forEach((marker) => marker.remove());
    markers = [];

    visibleDataCenters().forEach(dc => {
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

  $: activeMapFilter, map?.loaded() && createMarkers();

  onDestroy(() => {
    markers.forEach(m => m.remove());
    resizeObserver?.disconnect();
    if (map) map.remove();
  });
</script>

<div class="simplified-overview">
  <section class="metric-cards" aria-label="Portfolio summary">
    <button type="button" class="summary-card location-card" on:click={() => setScreen('globalmap')} aria-label="Open the facility map">
      <span class="summary-label">Portfolio locations</span>
      <strong>{dataCenters.length}</strong><p>European reference locations</p>
      <span class="summary-action">Open map <b>→</b></span>
    </button>
    <button type="button" class="summary-card" on:click={() => setScreen('globalmap')} aria-label="Review location coverage on the map">
      <span class="summary-label">Map coverage</span>
      <strong>100%</strong><p>All configured locations shown</p>
      <span class="summary-action">Review map <b>→</b></span>
    </button>
    <button type="button" class="summary-card" on:click={() => setScreen('analytics')} aria-label="Open facility metrics">
      <span class="summary-label">Reference water use</span>
      <strong>0.32 <small>L/kWh</small></strong><p>Illustrative until data is verified</p>
      <span class="summary-action">View metrics <b>→</b></span>
    </button>
    <button type="button" class="summary-card" on:click={() => setScreen('actions')} aria-label="Open priority actions">
      <span class="summary-label">Locations to review</span>
      <strong>3 <small>locations</small></strong><p>Resolve source data before action</p>
      <span class="summary-action">Open actions <b>→</b></span>
    </button>
  </section>

  <!-- Map Section -->
  <div class="map-section">
    <div class="map-header">
      <div><h3>European location reference</h3><p class="source-inline">{portfolioDataNotice.source} · Updated {portfolioDataNotice.updated}</p></div>
      <div class="map-tools">
        <div class="map-filters" aria-label="Filter locations on the map">
          <button type="button" class:active={activeMapFilter === 'all'} on:click={() => activeMapFilter = 'all'}>All <span>{dataCenters.length}</span></button>
          <button type="button" class:active={activeMapFilter === 'review'} on:click={() => activeMapFilter = 'review'}>Review <span>{dataCenters.filter((dc) => dc.status === 'critical' || dc.status === 'good').length}</span></button>
          <button type="button" class:active={activeMapFilter === 'lower-risk'} on:click={() => activeMapFilter = 'lower-risk'}>Lower risk <span>{dataCenters.filter((dc) => dc.status === 'excellent').length}</span></button>
        </div>
        <div class="map-legend">
        <div class="legend-item">
          <span class="legend-dot excellent"></span>
          <span>Excellent</span>
        </div>
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
    {#if mapFailed}
      <div class="map-fallback" aria-label="European reference map">
        <div class="fallback-copy">Map service unavailable. All configured European locations remain visible below.</div>
        <div class="fallback-locations">{#each dataCenters as dc}<span>{dc.name}, {dc.country}</span>{/each}</div>
      </div>
    {/if}
  </div>

  <div class="data-note"><strong>Before publishing facility performance:</strong> connect an authorised directory and verified operational telemetry. We do not infer capacity, carbon, PUE, renewable mix, or live availability from map locations.</div>
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

  .metric-cards { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; }
  .summary-card { position: relative; display: block; width: 100%; min-width: 0; min-height: 142px; padding: 18px; overflow: hidden; border: 1px solid rgba(255,255,255,.08); border-radius: 14px; background: rgba(255,255,255,.028); color: inherit; cursor: pointer; font: inherit; text-align: left; }
  .summary-card::before { position: absolute; inset: 0 auto 0 0; width: 2px; background: transparent; content: ''; transition: background .18s ease; }
  .summary-card:hover { border-color: rgba(44,173,132,.28); background: rgba(44,173,132,.055); transition: .18s ease; }
  .summary-card:hover::before, .summary-card:focus-visible::before { background: #2cad84; }
  .summary-card:focus-visible { outline: 2px solid #7fd8ff; outline-offset: 3px; }
  .summary-label { display: block; color: var(--tm); font-size: 10px; font-weight: 750; letter-spacing: .07em; line-height: 1.3; text-transform: uppercase; }
  .summary-card strong { display: block; margin-top: 20px; color: var(--text); font-size: 29px; font-weight: 800; letter-spacing: -.055em; line-height: 1; white-space: nowrap; }
  .summary-card small { color: var(--ts); font-size: 12px; font-weight: 700; letter-spacing: -.02em; }
  .summary-card p { margin: 9px 0 0; color: var(--ts); font-size: 10.5px; line-height: 1.35; }
  .summary-action { position: absolute; right: 18px; bottom: 15px; color: rgba(127,216,255,.72); font-size: 10px; font-weight: 800; opacity: 0; transform: translateX(-4px); transition: opacity .18s ease, transform .18s ease; }
  .summary-action b { margin-left: 4px; font-size: 13px; }
  .summary-card:hover .summary-action, .summary-card:focus-visible .summary-action { opacity: 1; transform: translateX(0); }

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

  .map-tools { display: flex; align-items: center; gap: 20px; }
  .map-filters { display: flex; gap: 5px; padding: 3px; border: 1px solid rgba(255,255,255,.08); border-radius: 9px; background: rgba(0,0,0,.14); }
  .map-filters button { border: 0; border-radius: 6px; padding: 6px 8px; background: transparent; color: var(--tm); cursor: pointer; font: inherit; font-size: 10px; font-weight: 700; white-space: nowrap; }
  .map-filters button span { margin-left: 3px; color: inherit; font-variant-numeric: tabular-nums; }
  .map-filters button:hover { color: var(--text); }
  .map-filters button.active { background: rgba(44,173,132,.16); color: #b9ffe4; }

  .map-header h3 {
    font-size: 18px;
    font-weight: 700;
    color: var(--text);
    margin: 0;
  }

  .source-inline { margin: 5px 0 0; color: rgba(244,247,245,.48); font-size: 11px; }

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

  .map-section { position: relative; }
  .map-fallback { position: absolute; inset: 84px 0 0; display: grid; place-content: center; gap: 20px; padding: 30px; background: radial-gradient(ellipse at 50% 30%, rgba(24,81,66,.5), transparent 58%), #07110f; color: rgba(244,247,245,.75); text-align: center; }
  .fallback-copy { font-size: 14px; font-weight: 700; }
  .fallback-locations { display: flex; max-width: 760px; justify-content: center; flex-wrap: wrap; gap: 8px; }
  .fallback-locations span { padding: 7px 10px; border: 1px solid rgba(44,173,132,.24); border-radius: 999px; background: rgba(44,173,132,.08); color: #b6ffe7; font-size: 11px; }

  .data-note { padding: 16px 18px; border: 1px solid rgba(127,174,255,.18); border-radius: 14px; background: rgba(127,174,255,.06); color: rgba(244,247,245,.68); font-size: 13px; line-height: 1.5; }
  .data-note strong { color: #dceaff; }


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

  }

  @media (max-width: 1100px) { .metric-cards { grid-template-columns: repeat(2, minmax(0, 1fr)); } }

  @media (max-width: 768px) {
    .metric-cards { grid-template-columns: 1fr; }
    .metrics-row {
      grid-template-columns: 1fr;
    }

    .map-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 12px;
    }

    .map-tools { width: 100%; align-items: flex-start; flex-direction: column; gap: 12px; }
    .map-legend { gap: 12px; }

    .map-container {
      height: 400px;
    }
  }
</style>
