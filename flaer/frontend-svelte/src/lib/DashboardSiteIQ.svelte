<script>
  import { onMount, onDestroy } from 'svelte';
  import 'mapbox-gl/dist/mapbox-gl.css';

  let selectedSite = 'nordic';
  let mapContainer;
  let map;
  let mapboxgl;
  let markers = [];
  let mapError = '';

  const MAPBOX_TOKEN =
    import.meta.env.VITE_MAPBOX_TOKEN ||
    'pk.eyJ1IjoiYmVya2lubmJlbGVyIiwiYSI6ImNtb2tqcTZ5MzAyMjkycHFsbml6aHdzb3MifQ.HjyuZunhCOe7tMg3mWALcg';

  const sites = {
    nordic: {
      name: 'Nordic Hub',
      fullName: 'Sweden / Finland',
      lng: 18.07,
      lat: 59.33,
      score: 94,
      rating: 'Highly suitable',
      summary: 'Best sustainability fit: very clean grid, cool climate, strong regulation.',
      recClass: 'rec-strong',
      recText: 'Best option',
      color: '#2cad84',
      factors: [
        { name: 'Renewable energy', score: 98, color: '#2cad84', note: 'Hydro and wind-heavy grid with strong PPA access.' },
        { name: 'Cooling climate', score: 96, color: '#2cad84', note: 'Cold climate enables free cooling most of the year.' },
        { name: 'Water stress', score: 88, color: '#2cad84', note: 'Low water stress and good cooling flexibility.' },
        { name: 'Regulatory fit', score: 94, color: '#2cad84', note: 'Stable, transparent, and CSRD-ready.' }
      ]
    },
    pnw: {
      name: 'Pacific Northwest',
      fullName: 'USA',
      lng: -120.55,
      lat: 44.0,
      score: 82,
      rating: 'Good candidate',
      summary: 'Clean hydro mix and mild climate, with wildfire and seasonal water risk to watch.',
      recClass: 'rec-good',
      recText: 'Recommended',
      color: '#7faeff',
      factors: [
        { name: 'Renewable energy', score: 85, color: '#2cad84', note: 'Strong hydro base with growing wind and solar.' },
        { name: 'Cooling climate', score: 82, color: '#7faeff', note: 'Mild conditions reduce cooling energy demand.' },
        { name: 'Water stress', score: 72, color: '#7faeff', note: 'Seasonal variation is the main constraint.' },
        { name: 'Regulatory fit', score: 88, color: '#2cad84', note: 'Good incentives and mature infrastructure.' }
      ]
    },
    saobrasil: {
      name: 'Southern Brazil',
      fullName: 'Brazil',
      lng: -46.63,
      lat: -23.55,
      score: 76,
      rating: 'Good with caveats',
      summary: 'High renewable share and attractive costs, but water and policy complexity need mitigation.',
      recClass: 'rec-good',
      recText: 'Recommended with caveats',
      color: '#7faeff',
      factors: [
        { name: 'Renewable energy', score: 82, color: '#7faeff', note: 'High renewable grid share, with regional variability.' },
        { name: 'Cooling climate', score: 68, color: '#7faeff', note: 'Higher cooling demand than temperate sites.' },
        { name: 'Water stress', score: 60, color: '#b67e3d', note: 'Drought cycles are an operational risk.' },
        { name: 'Regulatory fit', score: 74, color: '#7faeff', note: 'Improving, but more complex to navigate.' }
      ]
    },
    australia: {
      name: 'South-East Australia',
      fullName: 'Australia',
      lng: 151.2,
      lat: -33.9,
      score: 79,
      rating: 'Good candidate',
      summary: 'Fast renewable growth and strong governance, with heat and distance constraints.',
      recClass: 'rec-good',
      recText: 'Recommended',
      color: '#2cad84',
      factors: [
        { name: 'Renewable energy', score: 84, color: '#2cad84', note: 'Strong wind and solar growth.' },
        { name: 'Cooling climate', score: 62, color: '#b67e3d', note: 'Hot summers increase cooling load.' },
        { name: 'Water stress', score: 70, color: '#7faeff', note: 'Coastal cooling strategies improve feasibility.' },
        { name: 'Regulatory fit', score: 90, color: '#2cad84', note: 'Clear governance and ESG reporting environment.' }
      ]
    },
    texas: {
      name: 'Texas',
      fullName: 'USA',
      lng: -97.74,
      lat: 30.27,
      score: 61,
      rating: 'Proceed with caution',
      summary: 'Low cost and renewable buildout, but grid resilience, heat, and water stress are material risks.',
      recClass: 'rec-caution',
      recText: 'Caution advised',
      color: '#b67e3d',
      factors: [
        { name: 'Renewable energy', score: 68, color: '#7faeff', note: 'Large wind capacity but gas exposure remains.' },
        { name: 'Cooling climate', score: 42, color: '#d35d5c', note: 'Extreme heat materially increases cooling energy.' },
        { name: 'Water stress', score: 50, color: '#b67e3d', note: 'Drought and aquifer risk require water-free cooling.' },
        { name: 'Regulatory fit', score: 72, color: '#7faeff', note: 'Business-friendly, less ESG-driven.' }
      ]
    },
    india: {
      name: 'Southern India',
      fullName: 'India',
      lng: 77.59,
      lat: 12.97,
      score: 44,
      rating: 'Not recommended',
      summary: 'High carbon grid, water stress, and year-round heat make this weak for sustainability.',
      recClass: 'rec-avoid',
      recText: 'Avoid for now',
      color: '#d35d5c',
      factors: [
        { name: 'Renewable energy', score: 52, color: '#b67e3d', note: 'Good solar potential but current grid remains carbon-heavy.' },
        { name: 'Cooling climate', score: 28, color: '#d35d5c', note: 'Tropical heat drives high cooling demand.' },
        { name: 'Water stress', score: 35, color: '#d35d5c', note: 'Severe stress projected in many zones.' },
        { name: 'Regulatory fit', score: 58, color: '#b67e3d', note: 'Improving but complex for data center planning.' }
      ]
    }
  };

  $: site = sites[selectedSite];
  $: selectedSite, focusSite();

  onMount(async () => {
    try {
      const mbx = await import('mapbox-gl');
      mapboxgl = mbx.default;
      mapboxgl.accessToken = MAPBOX_TOKEN;

      map = new mapboxgl.Map({
        container: mapContainer,
        style: 'mapbox://styles/mapbox/dark-v11',
        center: [24, 22],
        zoom: 1.2,
        projection: 'globe',
        attributionControl: false
      });

      map.addControl(new mapboxgl.NavigationControl({ showCompass: false }), 'top-right');
      map.on('load', () => {
        map.setFog({
          color: 'rgb(6,14,12)',
          'high-color': 'rgb(35,90,105)',
          'horizon-blend': 0.02,
          'space-color': 'rgb(7,17,15)',
          'star-intensity': 0.55
        });
        addMarkers();
        focusSite(false);
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

  function addMarkers() {
    if (!map || !mapboxgl) return;
    clearMarkers();

    markers = Object.entries(sites).map(([id, candidate]) => {
      const el = document.createElement('button');
      el.type = 'button';
      el.className = 'site-marker';
      el.style.color = candidate.color;
      el.setAttribute('aria-label', `${candidate.name} site score ${candidate.score}`);
      el.innerHTML = `
        <span class="site-marker-ring" style="background:${candidate.color}24">
          <span class="site-marker-dot" style="background:${candidate.color}"></span>
          <span class="site-marker-score">${candidate.score}</span>
        </span>
      `;
      el.addEventListener('click', () => { selectedSite = id; });
      return new mapboxgl.Marker(el).setLngLat([candidate.lng, candidate.lat]).addTo(map);
    });
  }

  function focusSite(animate = true) {
    if (!map || !site) return;
    map.flyTo({
      center: [site.lng, site.lat],
      zoom: 3.4,
      duration: animate ? 1100 : 0,
      essential: true
    });
  }

  function arcDash(score) {
    const circ = 176;
    const used = Math.round((score / 100) * circ);
    return `${used} ${circ}`;
  }
</script>

<div class="siq-layout">
  <div class="map-column">
    <div class="siq-intro">Pick a candidate location. Scores combine grid carbon, renewables, water stress, climate risk, and regulatory fit.</div>

    <div class="siq-map-wrap">
      <div bind:this={mapContainer} class="site-map"></div>

      {#if mapError}
        <div class="map-error">{mapError}</div>
      {/if}

      <div class="map-key">
        <div class="mk-item"><span class="mk-dot" style="background:#2cad84"></span>80–100 best</div>
        <div class="mk-item"><span class="mk-dot" style="background:#7faeff"></span>65–79 good</div>
        <div class="mk-item"><span class="mk-dot" style="background:#b67e3d"></span>50–64 caution</div>
        <div class="mk-item"><span class="mk-dot" style="background:#d35d5c"></span>&lt;50 avoid</div>
      </div>
    </div>
  </div>

  <div class="site-card">
    <div class="site-card-head">
      <h3>Site score</h3>
      <p>Simple readout for the selected location</p>
    </div>
    <div class="site-card-body">
      <select class="site-select" bind:value={selectedSite}>
        <option value="nordic">Nordic Hub</option>
        <option value="pnw">Pacific Northwest</option>
        <option value="saobrasil">Southern Brazil</option>
        <option value="australia">South-East Australia</option>
        <option value="texas">Texas</option>
        <option value="india">Southern India</option>
      </select>

      <div class="score-ring-wrap">
        <div class="score-ring">
          <svg viewBox="0 0 72 72">
            <circle cx="36" cy="36" r="28" fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="8"/>
            <circle cx="36" cy="36" r="28" fill="none" stroke={site.color} stroke-width="8"
              stroke-dasharray={arcDash(site.score)} stroke-dashoffset="44"
              stroke-linecap="round" transform="rotate(-90 36 36)"/>
          </svg>
        </div>
        <div class="score-meta">
          <strong>{site.score}</strong>
          <span>{site.rating}</span>
          <p>{site.name}, {site.fullName}</p>
        </div>
      </div>

      <p class="site-summary">{site.summary}</p>

      <div class="factor-list">
        {#each site.factors as f}
          <div class="factor">
            <div class="factor-top">
              <div class="factor-name">{f.name}</div>
              <div class="factor-score" style="color:{f.color}">{f.score}/100</div>
            </div>
            <div class="factor-bar">
              <div class="factor-fill" style="width:{f.score}%;background:{f.color};"></div>
            </div>
            <div class="factor-note">{f.note}</div>
          </div>
        {/each}
      </div>

      <div class="rec-badge {site.recClass}">{site.recText}</div>
    </div>
  </div>
</div>

<style>
  .siq-layout {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 380px;
    gap: 16px;
    align-items: start;
  }

  .map-column { min-width: 0; }

  .siq-intro {
    font-size: 13px;
    color: rgba(244,247,245,0.62);
    margin-bottom: 10px;
  }

  .siq-map-wrap {
    position: relative;
    min-height: 620px;
    border-radius: 18px;
    overflow: hidden;
    background: #07110f;
    border: 1px solid rgba(255,255,255,0.08);
  }

  .site-map {
    position: absolute;
    inset: 0;
  }

  :global(.site-marker) {
    appearance: none;
    border: 0;
    padding: 0;
    background: transparent;
    cursor: pointer;
  }

  :global(.site-marker-ring) {
    width: 38px;
    height: 38px;
    border-radius: 999px;
    display: grid;
    place-items: center;
    position: relative;
    box-shadow: 0 0 0 1px currentColor;
    transition: transform 0.18s ease;
  }

  :global(.site-marker:hover .site-marker-ring) { transform: scale(1.16); }

  :global(.site-marker-dot) {
    width: 10px;
    height: 10px;
    border-radius: 999px;
    box-shadow: 0 0 14px currentColor;
  }

  :global(.site-marker-score) {
    position: absolute;
    left: 50%;
    top: 100%;
    transform: translate(-50%, 5px);
    padding: 2px 6px;
    border-radius: 999px;
    background: rgba(6,14,12,0.84);
    border: 1px solid rgba(255,255,255,0.08);
    color: #f4f7f5;
    font-size: 10px;
    font-weight: 900;
  }

  .map-key {
    position: absolute;
    left: 14px;
    bottom: 14px;
    z-index: 3;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    max-width: calc(100% - 28px);
    padding: 9px 12px;
    border-radius: 999px;
    background: rgba(6,14,12,0.78);
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
  }

  .mk-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    color: rgba(244,247,245,0.68);
    font-weight: 800;
  }

  .mk-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
  }

  .map-error {
    position: absolute;
    inset: 14px;
    z-index: 4;
    display: grid;
    place-items: center;
    border-radius: 14px;
    background: rgba(6,14,12,0.86);
    color: rgba(244,247,245,0.72);
    font-size: 13px;
  }

  .site-card {
    border-radius: 18px;
    background: linear-gradient(180deg, rgba(255,255,255,0.07), rgba(255,255,255,0.04));
    border: 1px solid rgba(255,255,255,0.09);
    overflow: hidden;
  }

  .site-card-head {
    padding: 16px 18px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }

  .site-card-head h3 {
    font-size: 15px;
    font-weight: 900;
    color: #f4f7f5;
    margin-bottom: 4px;
  }

  .site-card-head p {
    font-size: 12px;
    color: rgba(244,247,245,0.5);
  }

  .site-card-body { padding: 16px; }

  .site-select {
    width: 100%;
    padding: 10px 14px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.12);
    background: rgba(255,255,255,0.07);
    color: #f4f7f5;
    font-size: 13px;
    font-weight: 700;
    font-family: inherit;
    margin-bottom: 16px;
    cursor: pointer;
  }

  .site-select option { background: #0b1714; }

  .score-ring-wrap {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    border-radius: 14px;
    background: rgba(44,173,132,0.07);
    border: 1px solid rgba(44,173,132,0.14);
    margin-bottom: 12px;
  }

  .score-ring {
    position: relative;
    width: 72px;
    height: 72px;
    flex-shrink: 0;
  }

  .score-ring svg {
    width: 100%;
    height: 100%;
  }

  .score-meta strong {
    display: block;
    font-size: 30px;
    font-weight: 900;
    color: #f4f7f5;
  }

  .score-meta span {
    font-size: 13px;
    color: rgba(244,247,245,0.68);
  }

  .score-meta p {
    font-size: 12px;
    color: rgba(244,247,245,0.52);
    margin-top: 4px;
  }

  .site-summary {
    margin: 0 0 14px;
    padding: 12px;
    border-radius: 12px;
    background: rgba(255,255,255,0.045);
    color: rgba(244,247,245,0.66);
    font-size: 12px;
    line-height: 1.5;
  }

  .factor-list {
    display: grid;
    gap: 9px;
    margin-bottom: 14px;
  }

  .factor {
    padding: 12px 14px;
    border-radius: 12px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
  }

  .factor-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 7px;
    gap: 10px;
  }

  .factor-name {
    font-size: 12px;
    font-weight: 800;
    color: #f4f7f5;
  }

  .factor-score {
    font-size: 13px;
    font-weight: 900;
  }

  .factor-bar {
    height: 5px;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    overflow: hidden;
  }

  .factor-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.5s ease;
  }

  .factor-note {
    font-size: 11px;
    color: rgba(244,247,245,0.48);
    margin-top: 5px;
  }

  .rec-badge {
    display: inline-flex;
    align-items: center;
    padding: 7px 11px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 900;
  }

  .rec-strong { background: rgba(44,173,132,0.16); color: #b6ffe7; }
  .rec-good { background: rgba(127,174,255,0.14); color: #dce8ff; }
  .rec-caution { background: rgba(183,149,99,0.16); color: #ffe9c9; }
  .rec-avoid { background: rgba(211,93,92,0.16); color: #ffdede; }

  @media (max-width: 1020px) {
    .siq-layout { grid-template-columns: 1fr; }
    .siq-map-wrap { min-height: 520px; }
  }

  @media (max-width: 620px) {
    .siq-map-wrap { min-height: 430px; }
    .map-key {
      border-radius: 12px;
      justify-content: center;
    }
  }
</style>
