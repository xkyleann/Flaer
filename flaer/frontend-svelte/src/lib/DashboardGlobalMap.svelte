<script>
  import { onMount, onDestroy } from 'svelte';
  import 'mapbox-gl/dist/mapbox-gl.css';
  import { europeanPortfolio, portfolioDataNotice } from './europeanPortfolio.js';

  let activeFilter = 'all';
  let selectedDC = null;
  let mapContainer;
  let map;
  let mapboxgl;
  let markers = [];
  let mapError = '';
  let resizeObserver;

  const MAPBOX_TOKEN =
    import.meta.env.VITE_MAPBOX_TOKEN ||
    'pk.eyJ1IjoiYmVya2lubmJlbGVyIiwiYSI6ImNtb2tqcTZ5MzAyMjkycHFsbml6aHdzb3MifQ.HjyuZunhCOe7tMg3mWALcg';

  const dataCenters = europeanPortfolio.map((facility) => ({
    ...facility,
    risk: facility.risk === 'medium' ? 'med' : facility.risk,
    co2: `${facility.carbon} gCO₂/kWh`,
    cap: `${facility.capacity} MW`,
    pue: facility.pue.toFixed(2),
    renew: `${facility.renewable}%`
  }));

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

  function fallbackPosition(dc) {
    // Simple geographic projection for the resilient no-network map state.
    return {
      left: Math.min(94, Math.max(6, ((dc.lng + 12) / 46) * 100)),
      top: Math.min(88, Math.max(8, ((63 - dc.lat) / 30) * 100))
    };
  }

  $: filtered = dataCenters.filter((dc) => {
    if (activeFilter === 'all') return true;
    if (activeFilter === 'high') return dc.risk === 'high';
    if (activeFilter === 'med') return dc.risk === 'med';
    if (activeFilter === 'low') return dc.risk === 'low';
    if (activeFilter === 'eu') return true;
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
        center: [10, 51],
        // Keep the globe presentation while starting close enough for every
        // European portfolio marker to remain readable.
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

        updateMarkers();
        requestAnimationFrame(() => map?.resize());
      });

      map.on('error', (event) => {
        mapError = event?.error?.message || 'Mapbox failed to load.';
      });

      resizeObserver = new ResizeObserver(() => map?.resize());
      resizeObserver.observe(mapContainer);
    } catch (error) {
      mapError = error?.message || 'Mapbox failed to initialize.';
    }
  });

  onDestroy(() => {
    clearMarkers();
    resizeObserver?.disconnect();
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

    {#if mapError}
      <div class="fallback-map" role="img" aria-label="European facility map with all portfolio locations">
        <div class="fallback-grid"></div>
        <div class="fallback-title">European facility portfolio</div>
        <div class="fallback-subtitle">Map service unavailable — showing all configured locations</div>
        {#each filtered as dc}
          {@const position = fallbackPosition(dc)}
          <button
            class="fallback-marker"
            style:left={`${position.left}%`}
            style:top={`${position.top}%`}
            style:--risk-color={riskColor(dc.risk)}
            aria-label={`View ${dc.name}`}
            onclick={() => selectedDC = dc}
          ><span></span></button>
        {/each}
      </div>
    {/if}

    <div class="gmap-filters">
      {#each [['all','All facilities'],['high','High risk'],['med','Medium risk'],['low','Low risk'],['eu','EU regulated']] as [val, lbl]}
        <button class="gf-chip" class:on={activeFilter === val} onclick={() => activeFilter = val}>{lbl}</button>
      {/each}
    </div>

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
          <div class="dc-section-title">Location reference</div>
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
  <div class="source-note"><strong>{portfolioDataNotice.label}.</strong> {portfolioDataNotice.detail}</div>
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

  .fallback-map {
    position: absolute;
    inset: 0;
    z-index: 3;
    overflow: hidden;
    background: radial-gradient(ellipse at 50% 35%, rgba(22,76,63,.48), transparent 58%), #07110f;
  }

  .fallback-grid { position: absolute; inset: 0; opacity: .26; background-image: linear-gradient(rgba(130,210,180,.11) 1px, transparent 1px), linear-gradient(90deg, rgba(130,210,180,.11) 1px, transparent 1px); background-size: 56px 56px; }
  .fallback-title { position: absolute; top: 36px; left: 32px; color: #f4f7f5; font-size: 22px; font-weight: 800; letter-spacing: -.035em; }
  .fallback-subtitle { position: absolute; top: 66px; left: 32px; color: rgba(244,247,245,.55); font-size: 12px; }
  .fallback-marker { position: absolute; z-index: 1; width: 18px; height: 18px; border: 0; padding: 0; border-radius: 50%; background: color-mix(in srgb, var(--risk-color) 22%, transparent); cursor: pointer; transform: translate(-50%, -50%); box-shadow: 0 0 0 1px color-mix(in srgb, var(--risk-color) 62%, transparent), 0 0 20px color-mix(in srgb, var(--risk-color) 46%, transparent); }
  .fallback-marker span { display: block; width: 8px; height: 8px; margin: 5px; border-radius: 50%; background: var(--risk-color); }

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

  .source-note { position: absolute; left: 22px; top: 22px; z-index: 10; max-width: 440px; padding: 10px 12px; border: 1px solid rgba(255,255,255,.08); border-radius: 12px; color: rgba(244,247,245,.63); background: rgba(6,14,12,.72); backdrop-filter: blur(12px); font-size: 11px; line-height: 1.45; }

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
    .source-note { left: 16px; right: 16px; top: 16px; max-width: none; }
  }
</style>
