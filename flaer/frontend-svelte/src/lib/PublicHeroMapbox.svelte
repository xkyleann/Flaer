<script>
  import { onMount, onDestroy } from 'svelte';
  import 'mapbox-gl/dist/mapbox-gl.css';

  let mapContainer;
  let map;
  let mapboxgl;
  let markers = [];
  let mapError = '';
  let resizeObserver;

  const MAPBOX_TOKEN =
    import.meta.env.VITE_MAPBOX_TOKEN ||
    'pk.eyJ1IjoiYmVya2lubmJlbGVyIiwiYSI6ImNtb2tqcTZ5MzAyMjkycHFsbml6aHdzb3MifQ.HjyuZunhCOe7tMg3mWALcg';

  const sites = [
    { name: 'N. Virginia', risk: 'high', lng: -77.0, lat: 38.9 },
    { name: 'California', risk: 'med', lng: -122.0, lat: 37.5 },
    { name: 'Dublin', risk: 'low', lng: -6.26, lat: 53.35 },
    { name: 'Frankfurt', risk: 'med', lng: 8.7, lat: 50.1 },
    { name: 'Stockholm', risk: 'low', lng: 18.1, lat: 59.3 },
    { name: 'Singapore', risk: 'high', lng: 103.8, lat: 1.3 },
    { name: 'Tokyo', risk: 'med', lng: 139.7, lat: 35.7 },
    { name: 'Sydney', risk: 'low', lng: 151.2, lat: -33.9 },
    { name: 'Mumbai', risk: 'high', lng: 72.88, lat: 19.08 },
    { name: 'Sao Paulo', risk: 'med', lng: -46.6, lat: -23.5 },
    { name: 'Hong Kong', risk: 'med', lng: 114.17, lat: 22.32 },
  ];

  function riskColor(risk) {
    if (risk === 'high') return '#d35d5c';
    if (risk === 'med') return '#b67e3d';
    return '#2cad84';
  }

  function riskBg(risk) {
    if (risk === 'high') return 'rgba(211,93,92,0.14)';
    if (risk === 'med') return 'rgba(182,126,61,0.14)';
    return 'rgba(44,173,132,0.18)';
  }

  onMount(async () => {
    try {
      const mbx = await import('mapbox-gl');
      mapboxgl = mbx.default;
      mapboxgl.accessToken = MAPBOX_TOKEN;

      resizeObserver = new ResizeObserver(() => map?.resize());
      resizeObserver.observe(mapContainer);

      map = new mapboxgl.Map({
        container: mapContainer,
        style: 'mapbox://styles/mapbox/dark-v11',
        center: [10, 24],
        zoom: 1.05,
        projection: 'globe',
        attributionControl: false,
        interactive: false
      });

      map.on('load', () => {
        map.setFog({
          color: 'rgb(6,14,12)',
          'high-color': 'rgb(36,92,110)',
          'horizon-blend': 0.02,
          'space-color': 'rgb(11,20,18)',
          'star-intensity': 0.45
        });
        addMarkers();
        map.resize();
        setTimeout(() => map?.resize(), 250);
        setTimeout(() => map?.resize(), 900);
      });

      map.on('error', (event) => {
        mapError = event?.error?.message || 'Mapbox failed to load.';
      });
    } catch (error) {
      mapError = error?.message || 'Mapbox failed to initialize.';
    }
  });

  onDestroy(() => {
    if (resizeObserver) resizeObserver.disconnect();
    markers.forEach((marker) => marker.remove());
    if (map) map.remove();
  });

  function addMarkers() {
    markers = sites.map((site) => {
      const el = document.createElement('span');
      el.className = 'public-hero-marker';
      el.style.color = riskColor(site.risk);
      el.innerHTML = `
        <span class="public-hero-marker-outer" style="background:${riskBg(site.risk)}">
          <span class="public-hero-marker-inner" style="background:${riskColor(site.risk)}"></span>
        </span>
      `;
      return new mapboxgl.Marker(el).setLngLat([site.lng, site.lat]).addTo(map);
    });
  }
</script>

<div class="hero-mapbox">
  <div bind:this={mapContainer} class="hero-map"></div>
  {#if mapError}
    <div class="hero-map-error">{mapError}</div>
  {/if}
</div>
<svelte:window on:resize={() => map?.resize()} />

<style>
  .hero-mapbox {
    position: relative;
    height: clamp(300px, 34vw, 420px);
    min-height: 300px;
    border-radius: 16px;
    overflow: hidden;
    background: rgba(18,35,30,0.74);
    box-shadow: inset 0 -44px 80px rgba(244,247,245,0.05);
  }

  .hero-map {
    position: absolute;
    inset: 0;
  }

  .hero-mapbox::after {
    content: '';
    position: absolute;
    inset: 0;
    pointer-events: none;
    background:
      radial-gradient(circle at 50% 42%, transparent 42%, rgba(177,205,193,0.10) 100%),
      linear-gradient(180deg,
        rgba(244,247,245,0.02) 0%,
        rgba(189,213,203,0.06) 62%,
        rgba(214,226,221,0.18) 100%
      );
  }

  .hero-map-error {
    position: absolute;
    inset: 16px;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    border-radius: 14px;
    background: rgba(6,14,12,0.92);
    border: 1px solid rgba(211,93,92,0.35);
    color: #f4c7c7;
    text-align: center;
    font-size: 12px;
    font-weight: 700;
  }

  :global(.public-hero-marker) {
    display: block;
  }

  :global(.public-hero-marker-outer) {
    width: 22px;
    height: 22px;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: publicHeroMarkerPulse 5s ease-in-out infinite;
  }

  :global(.public-hero-marker-inner) {
    width: 9px;
    height: 9px;
    border-radius: 999px;
    box-shadow: 0 0 10px currentColor;
    animation: publicHeroMarkerCorePulse 5s ease-in-out infinite;
  }

  @keyframes publicHeroMarkerPulse {
    0%, 100% {
      transform: scale(1);
      box-shadow: 0 0 0 0 rgba(244,247,245,0.03);
      opacity: 0.82;
    }
    50% {
      transform: scale(1.26);
      box-shadow: 0 0 20px 5px rgba(244,247,245,0.08);
      opacity: 1;
    }
  }

  @keyframes publicHeroMarkerCorePulse {
    0%, 100% { transform: scale(0.9); opacity: 0.72; }
    50% { transform: scale(1); opacity: 1; }
  }
</style>
