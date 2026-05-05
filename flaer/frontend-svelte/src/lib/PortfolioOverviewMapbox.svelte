<script>
  import { onMount, onDestroy } from 'svelte';
  import 'mapbox-gl/dist/mapbox-gl.css';

  let mapContainer;
  let map;
  let mapboxgl;
  let markers = [];
  let mapError = '';

  const MAPBOX_TOKEN =
    import.meta.env.VITE_MAPBOX_TOKEN ||
    'pk.eyJ1IjoiYmVya2lubmJlbGVyIiwiYSI6ImNtb2tqcTZ5MzAyMjkycHFsbml6aHdzb3MifQ.HjyuZunhCOe7tMg3mWALcg';

  const dataCenters = [
    { id: 'nv', name: 'N. Virginia', risk: 'high', lng: -77.0, lat: 38.9 },
    { id: 'ca', name: 'California', risk: 'med', lng: -122.0, lat: 37.5 },
    { id: 'dub', name: 'Dublin', risk: 'low', lng: -6.26, lat: 53.35 },
    { id: 'fra', name: 'Frankfurt', risk: 'med', lng: 8.7, lat: 50.1 },
    { id: 'sto', name: 'Stockholm', risk: 'low', lng: 18.1, lat: 59.3 },
    { id: 'sgp', name: 'Singapore', risk: 'high', lng: 103.8, lat: 1.3 },
    { id: 'tky', name: 'Tokyo', risk: 'med', lng: 139.7, lat: 35.7 },
    { id: 'syd', name: 'Sydney', risk: 'low', lng: 151.2, lat: -33.9 },
    { id: 'mum', name: 'Mumbai', risk: 'high', lng: 72.88, lat: 19.08 },
    { id: 'bra', name: 'Sao Paulo', risk: 'med', lng: -46.6, lat: -23.5 },
    { id: 'hkg', name: 'Hong Kong', risk: 'med', lng: 114.17, lat: 22.32 },
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

      map = new mapboxgl.Map({
        container: mapContainer,
        style: 'mapbox://styles/mapbox/dark-v11',
        center: [8, 24],
        zoom: 1.25,
        projection: 'globe',
        attributionControl: false,
        interactive: true
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
    markers = dataCenters.map((dc) => {
      const el = document.createElement('button');
      el.type = 'button';
      el.className = 'portfolio-dc-marker';
      el.style.color = riskColor(dc.risk);
      el.setAttribute('aria-label', `${dc.name} data center`);
      el.innerHTML = `
        <span class="portfolio-marker-outer" style="background:${riskBg(dc.risk)}">
          <span class="portfolio-marker-inner" style="background:${riskColor(dc.risk)}"></span>
        </span>
      `;

      el.addEventListener('click', () => {
        map.flyTo({ center: [dc.lng, dc.lat], zoom: 3.7, duration: 1400 });
      });

      return new mapboxgl.Marker(el).setLngLat([dc.lng, dc.lat]).addTo(map);
    });
  }
</script>

<div class="portfolio-mapbox">
  <div bind:this={mapContainer} class="portfolio-map"></div>
  {#if mapError}
    <div class="portfolio-map-error">{mapError}</div>
  {/if}
</div>

<style>
  .portfolio-mapbox {
    position: absolute;
    inset: 0;
    background: #0a1412;
  }

  .portfolio-map {
    position: absolute;
    inset: 0;
  }

  .portfolio-map::after {
    content: '';
    position: absolute;
    inset: 0;
    pointer-events: none;
    background:
      radial-gradient(circle at 50% 45%, transparent 42%, rgba(6,14,12,0.32) 100%),
      linear-gradient(180deg, rgba(6,14,12,0.08), rgba(6,14,12,0.22));
  }

  .portfolio-map-error {
    position: absolute;
    inset: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    border-radius: 16px;
    background: rgba(6,14,12,0.92);
    border: 1px solid rgba(211,93,92,0.35);
    color: #f4c7c7;
    text-align: center;
    font-size: 12px;
    font-weight: 700;
  }

  :global(.portfolio-dc-marker) {
    appearance: none;
    padding: 0;
    border: 0;
    background: transparent;
    cursor: pointer;
  }

  :global(.portfolio-marker-outer) {
    width: 22px;
    height: 22px;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: portfolioMarkerPulse 5s ease-in-out infinite;
  }

  :global(.portfolio-marker-inner) {
    width: 9px;
    height: 9px;
    border-radius: 999px;
    box-shadow: 0 0 10px currentColor;
    animation: portfolioMarkerCorePulse 5s ease-in-out infinite;
  }

  @keyframes portfolioMarkerPulse {
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

  @keyframes portfolioMarkerCorePulse {
    0%, 100% {
      transform: scale(0.9);
      opacity: 0.72;
    }
    50% {
      transform: scale(1);
      opacity: 1;
    }
  }
</style>
