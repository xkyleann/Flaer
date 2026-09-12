<script>
  import { onMount, onDestroy } from 'svelte';
  import 'mapbox-gl/dist/mapbox-gl.css';

  let mapContainer;
  let map;
  let mapboxgl;
  let markers = [];
  let selected = null;
  let mapError = '';

  const MAPBOX_TOKEN =
    import.meta.env.VITE_MAPBOX_TOKEN ||
    'pk.eyJ1IjoiYmVya2lubmJlbGVyIiwiYSI6ImNtb2tqcTZ5MzAyMjkycHFsbml6aHdzb3MifQ.HjyuZunhCOe7tMg3mWALcg';

  const facilities = [
    { id: 'virginia', name: 'N. Virginia', region: 'US East', lng: -77.0, lat: 38.9, risk: 'high', pue: 1.42, wue: 1.8, renewable: 48, carbon: 412 },
    { id: 'oregon', name: 'Oregon', region: 'US West', lng: -120.55, lat: 44.0, risk: 'low', pue: 1.27, wue: 0.9, renewable: 89, carbon: 95 },
    { id: 'montreal', name: 'Montreal', region: 'Canada', lng: -73.57, lat: 45.5, risk: 'low', pue: 1.16, wue: 0.5, renewable: 97, carbon: 29 },
    { id: 'dublin', name: 'Dublin', region: 'EU West', lng: -6.26, lat: 53.35, risk: 'medium', pue: 1.31, wue: 1.0, renewable: 68, carbon: 295 },
    { id: 'frankfurt', name: 'Frankfurt', region: 'EU Central', lng: 8.68, lat: 50.11, risk: 'medium', pue: 1.24, wue: 1.2, renewable: 72, carbon: 284 },
    { id: 'stockholm', name: 'Stockholm', region: 'Nordic', lng: 18.07, lat: 59.33, risk: 'low', pue: 1.08, wue: 0.4, renewable: 98, carbon: 22 },
    { id: 'singapore', name: 'Singapore', region: 'APAC', lng: 103.82, lat: 1.35, risk: 'high', pue: 1.38, wue: 2.1, renewable: 35, carbon: 408 },
    { id: 'tokyo', name: 'Tokyo', region: 'APAC', lng: 139.69, lat: 35.68, risk: 'medium', pue: 1.45, wue: 1.5, renewable: 38, carbon: 462 },
    { id: 'mumbai', name: 'Mumbai', region: 'AP South', lng: 72.88, lat: 19.08, risk: 'high', pue: 1.62, wue: 1.9, renewable: 24, carbon: 708 },
    { id: 'sao-paulo', name: 'Sao Paulo', region: 'LATAM', lng: -46.63, lat: -23.55, risk: 'low', pue: 1.34, wue: 0.8, renewable: 83, carbon: 82 },
    { id: 'cape-town', name: 'Cape Town', region: 'Africa', lng: 18.42, lat: -33.92, risk: 'high', pue: 1.59, wue: 2.0, renewable: 8, carbon: 912 }
  ];

  function colorFor(risk) {
    if (risk === 'high') return '#d35d5c';
    if (risk === 'medium') return '#b67e3d';
    return '#2cad84';
  }

  function bgFor(risk) {
    if (risk === 'high') return 'rgba(211,93,92,0.16)';
    if (risk === 'medium') return 'rgba(182,126,61,0.16)';
    return 'rgba(44,173,132,0.18)';
  }

  onMount(async () => {
    try {
      const mbx = await import('mapbox-gl');
      mapboxgl = mbx.default;
      mapboxgl.accessToken = MAPBOX_TOKEN;

      map = new mapboxgl.Map({
        container: mapContainer,
        style: 'mapbox://styles/mapbox/dark-v11',
        center: [12, 24],
        zoom: 1.25,
        projection: 'globe',
        attributionControl: false
      });

      map.addControl(new mapboxgl.NavigationControl({ showCompass: false }), 'top-right');

      map.on('load', () => {
        map.setFog({
          color: 'rgb(7,17,15)',
          'high-color': 'rgb(30,78,92)',
          'horizon-blend': 0.025,
          'space-color': 'rgb(6,14,12)',
          'star-intensity': 0.45
        });
        addMarkers();
      });

      map.on('error', (event) => {
        mapError = event?.error?.message || 'Mapbox failed to load.';
      });
    } catch (error) {
      mapError = error?.message || 'Mapbox failed to initialize.';
    }
  });

  onDestroy(() => {
    markers.forEach((marker) => marker.remove());
    if (map) map.remove();
  });

  function addMarkers() {
    if (!map || !mapboxgl) return;

    markers = facilities.map((facility) => {
      const color = colorFor(facility.risk);
      const el = document.createElement('button');
      el.type = 'button';
      el.className = 'portfolio-marker';
      el.style.color = color;
      el.setAttribute('aria-label', `${facility.name} facility`);
      el.innerHTML = `
        <span class="portfolio-marker-ring" style="background:${bgFor(facility.risk)}">
          <span class="portfolio-marker-dot" style="background:${color}"></span>
        </span>
      `;

      el.addEventListener('click', () => {
        selected = facility;
        map.flyTo({ center: [facility.lng, facility.lat], zoom: 4.2, duration: 1300 });
      });

      return new mapboxgl.Marker(el).setLngLat([facility.lng, facility.lat]).addTo(map);
    });
  }
</script>

<div class="portfolio-map-shell">
  <div bind:this={mapContainer} class="portfolio-map"></div>

  {#if mapError}
    <div class="map-error">{mapError}</div>
  {/if}

  <div class="map-legend">
    <div class="ml-item"><span class="ml-dot high"></span>Needs action</div>
    <div class="ml-item"><span class="ml-dot medium"></span>Watch</div>
    <div class="ml-item"><span class="ml-dot low"></span>On track</div>
  </div>

  <div class="map-summary">
    {#if selected}
      <div class="summary-title">{selected.name}</div>
      <div class="summary-sub">{selected.region}</div>
      <div class="summary-grid">
        <span>PUE <strong>{selected.pue}</strong></span>
        <span>WUE <strong>{selected.wue}</strong></span>
        <span>Grid <strong>{selected.carbon}g</strong></span>
        <span>Renewable <strong>{selected.renewable}%</strong></span>
      </div>
    {:else}
      <div class="summary-title">11 facilities</div>
      <div class="summary-sub">Click a marker for PUE, WUE, carbon, and renewable mix.</div>
    {/if}
  </div>
</div>

<style>
  .portfolio-map-shell {
    position: relative;
    min-height: 450px;
    height: 100%;
    overflow: hidden;
    border-radius: 0 0 22px 22px;
    background: #07110f;
  }

  .portfolio-map {
    position: absolute;
    inset: 0;
  }

  :global(.portfolio-marker) {
    appearance: none;
    padding: 0;
    border: 0;
    background: transparent;
    cursor: pointer;
  }

  :global(.portfolio-marker-ring) {
    width: 25px;
    height: 25px;
    border-radius: 999px;
    display: grid;
    place-items: center;
    box-shadow: 0 0 0 1px currentColor;
    transition: transform 0.18s ease;
  }

  :global(.portfolio-marker:hover .portfolio-marker-ring) {
    transform: scale(1.22);
  }

  :global(.portfolio-marker-dot) {
    width: 9px;
    height: 9px;
    border-radius: 999px;
    box-shadow: 0 0 14px currentColor;
  }

  .map-legend,
  .map-summary {
    position: absolute;
    z-index: 2;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(6,14,12,0.78);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
  }

  .map-legend {
    left: 16px;
    bottom: 16px;
    display: flex;
    gap: 10px;
    padding: 8px 12px;
    border-radius: 999px;
  }

  .ml-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-weight: 800;
    color: rgba(244,247,245,0.72);
  }

  .ml-dot {
    width: 8px;
    height: 8px;
    border-radius: 999px;
  }

  .ml-dot.high { background: #d35d5c; }
  .ml-dot.medium { background: #b67e3d; }
  .ml-dot.low { background: #2cad84; }

  .map-summary {
    right: 16px;
    bottom: 16px;
    width: min(320px, calc(100% - 32px));
    padding: 14px;
    border-radius: 14px;
  }

  .summary-title {
    font-size: 16px;
    font-weight: 900;
    color: #f4f7f5;
  }

  .summary-sub {
    margin-top: 3px;
    font-size: 12px;
    color: rgba(244,247,245,0.58);
  }

  .summary-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-top: 12px;
  }

  .summary-grid span {
    padding: 8px;
    border-radius: 9px;
    background: rgba(255,255,255,0.055);
    color: rgba(244,247,245,0.55);
    font-size: 11px;
    font-weight: 700;
  }

  .summary-grid strong {
    display: block;
    color: #f4f7f5;
    font-size: 14px;
    margin-top: 2px;
  }

  .map-error {
    position: absolute;
    inset: 16px;
    display: grid;
    place-items: center;
    z-index: 3;
    border-radius: 14px;
    background: rgba(6,14,12,0.82);
    color: rgba(244,247,245,0.72);
    font-size: 13px;
    text-align: center;
  }

  @media (max-width: 760px) {
    .portfolio-map-shell { min-height: 390px; }
    .map-legend {
      top: 12px;
      bottom: auto;
      left: 12px;
      right: 12px;
      justify-content: center;
      border-radius: 12px;
      flex-wrap: wrap;
    }
    .map-summary {
      left: 12px;
      right: 12px;
      bottom: 12px;
      width: auto;
    }
  }
</style>
