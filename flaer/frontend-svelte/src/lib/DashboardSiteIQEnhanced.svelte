<script>
  import { onMount, onDestroy } from 'svelte';
  import 'mapbox-gl/dist/mapbox-gl.css';

  let mapContainer, map, mapboxgl;
  let markers = [];
  let selectedSite = null;
  let activeSiteTab = 'overview';
  let activePhase = 'screening';

  // Shortlist & report state
  let shortlist = [];
  let generatingReport = false;
  let reportReady = false;
  let showReportModal = false;

  function toggleShortlist(siteId) {
    if (shortlist.includes(siteId)) {
      shortlist = shortlist.filter(id => id !== siteId);
    } else {
      shortlist = [...shortlist, siteId];
    }
  }

  async function handleGenerateReport() {
    if (generatingReport || !selectedSite) return;
    generatingReport = true;
    reportReady = false;
    await new Promise(r => setTimeout(r, 2200));
    generatingReport = false;
    reportReady = true;
    showReportModal = true;
  }

  function closeReportModal() {
    showReportModal = false;
    reportReady = false;
  }

  const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN ||
    'pk.eyJ1IjoiYmVya2lubmJlbGVyIiwiYSI6ImNtb2tqcTZ5MzAyMjkycHFsbml6aHdzb3MifQ.HjyuZunhCOe7tMg3mWALcg';

  const phases = [
    { id: 'screening',   label: 'Site Screening',   desc: 'MCDA multi-criteria analysis' },
    { id: 'feasibility', label: 'Pre-Feasibility',  desc: 'Technical & resource assessment' },
    { id: 'risk',        label: 'Risk Assessment',  desc: 'Risk register & mitigation plan' },
    { id: 'financial',   label: 'Financial Model',  desc: 'CapEx · OpEx · IRR · Timeline' },
  ];

  let weights = { energy: 30, infra: 25, climate: 20, financial: 15, regulatory: 10 };

  const sites = [
    {
      id: 'stockholm', name: 'Stockholm', country: 'Sweden', region: 'Northern Europe',
      lng: 18.07, lat: 59.33, phase: 'feasibility',
      gridCarbon: 13, gridCapacity: 480, powerPrice: 38, ppaPrice: 32, renewable: 98,
      coolingType: 'Free Air + District Heat', avgTemp: 6.5,
      fiberRoutes: 8, connectivity: 'Excellent', waterSource: 'Lake Mälaren', waterStress: 0.18,
      distPort: 8, distAirport: 42,
      climateRisk: 0.12, seismicRisk: 0.08, floodRisk: 0.14, cyberRisk: 0.18, regulatoryRisk: 0.15,
      politicalScore: 9.4,
      landCostMHa: 0.9, capexPerMW: 8.8, opexPerMW: 172000, targetMW: 120,
      constructionMonths: 24, permitMonths: 16, energyYield: 0.94, irr: 15.2, npv: 340, payback: 7.8,
      pros: ['Lowest carbon grid in Europe (13 gCO₂/kWh)', 'Free-air cooling 10+ months/year', 'Grade-A political stability (9.4/10)', 'Large-scale wind & hydro PPAs available'],
      cons: ['Higher land costs vs Eastern EU', 'Seasonal daylight extremes affect operations', 'Limited brownfield industrial sites'],
      recommendation: 'Tier-1 recommendation for a carbon-zero mandate. Best lifecycle carbon position in the European portfolio. Suitable for hyperscale deployment.',
      permitNotes: 'Environmental Impact Assessment mandatory. Municipal zoning approval ~16 months. Strong government support for green DC. SEK exposure requires hedging.',
      risks: [
        { name: 'Grid congestion', likelihood: 2, impact: 3, category: 'technical', mitigation: 'Dedicated HV substation agreement with Svenska kraftnät' },
        { name: 'Permitting delay', likelihood: 2, impact: 2, category: 'regulatory', mitigation: 'Pre-application engagement with municipality' },
        { name: 'Land scarcity', likelihood: 3, impact: 2, category: 'commercial', mitigation: 'Identify 3 alternative brownfield sites' },
        { name: 'Winter outage risk', likelihood: 1, impact: 3, category: 'operational', mitigation: 'N+1 UPS + dual district heat loops' },
        { name: 'FX risk (SEK/USD)', likelihood: 3, impact: 2, category: 'financial', mitigation: '5-year rolling FX hedge programme' },
      ],
    },
    {
      id: 'montreal', name: 'Montreal', country: 'Canada', region: 'North America',
      lng: -73.57, lat: 45.5, phase: 'feasibility',
      gridCarbon: 29, gridCapacity: 620, powerPrice: 42, ppaPrice: 35, renewable: 97,
      coolingType: 'Free Air + River Cooling', avgTemp: 8.2,
      fiberRoutes: 6, connectivity: 'Good', waterSource: 'St. Lawrence River', waterStress: 0.15,
      distPort: 5, distAirport: 22,
      climateRisk: 0.22, seismicRisk: 0.12, floodRisk: 0.25, cyberRisk: 0.20, regulatoryRisk: 0.18,
      politicalScore: 9.1,
      landCostMHa: 0.6, capexPerMW: 9.2, opexPerMW: 158000, targetMW: 150,
      constructionMonths: 20, permitMonths: 14, energyYield: 0.92, irr: 14.8, npv: 410, payback: 8.2,
      pros: ['Hydro-powered grid (97% renewable)', 'Lowest power price in North America', 'Cold climate provides natural free-cooling', 'Large available land at low cost'],
      cons: ['Seismic Zone 2 — structural upgrade required', 'Spring St. Lawrence flood risk', 'Latency disadvantage vs US Tier-1 markets'],
      recommendation: 'Best value proposition for North American expansion. Hydro-Québec base load provides 20-year price stability. Recommended for hyperscale.',
      permitNotes: 'Federal & Québec EIA required. Hydro-Québec grid connection process ~14 months. Brownfield incentive grants available. Bilingual workforce requirement.',
      risks: [
        { name: 'Hydro drought year', likelihood: 2, impact: 4, category: 'environmental', mitigation: 'Dual-supply contract + 30-day on-site backup diesel' },
        { name: 'Spring flooding', likelihood: 3, impact: 3, category: 'environmental', mitigation: 'Site elevation >100yr flood plain + flood barriers' },
        { name: 'Dual permit complexity', likelihood: 2, impact: 2, category: 'regulatory', mitigation: 'Appoint joint federal/provincial liaison team' },
        { name: 'Latency to US hubs', likelihood: 4, impact: 2, category: 'technical', mitigation: 'Dark fibre leases to NYC/Boston PoPs' },
        { name: 'CAD/USD exposure', likelihood: 3, impact: 2, category: 'financial', mitigation: 'USD-denominated revenue contracts where possible' },
      ],
    },
    {
      id: 'oregon', name: 'Oregon', country: 'USA', region: 'North America',
      lng: -120.55, lat: 44.0, phase: 'feasibility',
      gridCarbon: 95, gridCapacity: 520, powerPrice: 55, ppaPrice: 42, renewable: 89,
      coolingType: 'Evaporative + Free Air', avgTemp: 10.8,
      fiberRoutes: 12, connectivity: 'Excellent', waterSource: 'Columbia River', waterStress: 0.38,
      distPort: 85, distAirport: 35,
      climateRisk: 0.45, seismicRisk: 0.55, floodRisk: 0.30, cyberRisk: 0.15, regulatoryRisk: 0.25,
      politicalScore: 8.3,
      landCostMHa: 0.8, capexPerMW: 10.5, opexPerMW: 195000, targetMW: 200,
      constructionMonths: 18, permitMonths: 12, energyYield: 0.90, irr: 12.4, npv: 280, payback: 9.5,
      pros: ['World-class US West Coast connectivity (12 fibre routes)', 'Strong hydro base + offshore wind PPA pipeline', 'Fastest permitting of US shortlist (12 months)', 'Proven hyperscale data centre ecosystem'],
      cons: ['Cascadia subduction zone — major seismic risk', 'Wildfire smoke requires enhanced HVAC filtration', 'Summer water stress constrains evaporative cooling'],
      recommendation: 'Strong operational case for US West Coast presence. Seismic risk requires IBC Zone 4 structural design — factor $1.2M/MW premium. Wildfire resilience plan essential.',
      permitNotes: 'State-level land-use permit ~12 months. Federal environmental review required if within 5km of federal land. Multiple shovel-ready sites available near Prineville.',
      risks: [
        { name: 'Cascadia seismic event (M9)', likelihood: 2, impact: 5, category: 'environmental', mitigation: 'IBC Zone 4 structural design + seismic isolation mounts' },
        { name: 'Wildfire smoke disruption', likelihood: 3, impact: 3, category: 'environmental', mitigation: 'MERV-16 filtration + sealed pressurised buildings' },
        { name: 'Summer water stress', likelihood: 4, impact: 2, category: 'operational', mitigation: 'Adiabatic DX hybrid — switch to DX above 25°C' },
        { name: 'Grid peak curtailment', likelihood: 3, impact: 2, category: 'technical', mitigation: '40 MW on-site battery storage' },
        { name: 'Oregon carbon legislation', likelihood: 3, impact: 3, category: 'regulatory', mitigation: '89% renewable PPA coverage as baseline' },
      ],
    },
    {
      id: 'frankfurt', name: 'Frankfurt', country: 'Germany', region: 'Central Europe',
      lng: 8.68, lat: 50.11, phase: 'screening',
      gridCarbon: 338, gridCapacity: 380, powerPrice: 92, ppaPrice: 68, renewable: 52,
      coolingType: 'DX + Adiabatic', avgTemp: 10.5,
      fiberRoutes: 20, connectivity: 'Excellent', waterSource: 'Rhine / Main', waterStress: 0.62,
      distPort: 210, distAirport: 12,
      climateRisk: 0.35, seismicRisk: 0.15, floodRisk: 0.42, cyberRisk: 0.20, regulatoryRisk: 0.38,
      politicalScore: 8.8,
      landCostMHa: 2.4, capexPerMW: 13.5, opexPerMW: 260000, targetMW: 80,
      constructionMonths: 30, permitMonths: 26, energyYield: 0.87, irr: 9.8, npv: 145, payback: 11.2,
      pros: ['DE-CIX: World\'s largest internet exchange point', 'Prime Central European legal jurisdiction', 'Mature supplier and contractor ecosystem'],
      cons: ['Highest carbon grid on shortlist — CSRD liability', 'Most expensive power and land of all candidates', 'BauGB permitting process: minimum 26 months', 'Rhine low-water events constrain summer cooling'],
      recommendation: 'Justified only for Frankfurt-specific connectivity premium (DE-CIX membership). Carbon offset contracts essential for CSRD compliance. Not recommended as primary European campus.',
      permitNotes: 'BauGB spatial plan compliance + BImSchG environmental permit required. Frankfurt municipality has imposed a 1 GW total DC power cap. Expect 26-month minimum timeline.',
      risks: [
        { name: 'Power price volatility', likelihood: 4, impact: 4, category: 'financial', mitigation: '10-year fixed PPA + 5yr price collar' },
        { name: 'Rhine low-water cooling', likelihood: 3, impact: 3, category: 'operational', mitigation: 'Closed-loop cooling towers — eliminate river dependency' },
        { name: 'CSRD carbon exposure', likelihood: 5, impact: 3, category: 'regulatory', mitigation: '100% renewable PPA + certified offsets for residual' },
        { name: 'Permitting overrun', likelihood: 4, impact: 3, category: 'regulatory', mitigation: 'Pre-application BauGB advisory with Frankfurt City' },
        { name: 'DC power cap breach', likelihood: 3, impact: 4, category: 'regulatory', mitigation: 'Secure allocation pre-application — cap at risk' },
      ],
    },
    {
      id: 'singapore', name: 'Singapore', country: 'Singapore', region: 'Southeast Asia',
      lng: 103.82, lat: 1.35, phase: 'screening',
      gridCarbon: 408, gridCapacity: 160, powerPrice: 135, ppaPrice: 95, renewable: 28,
      coolingType: 'Chilled Water Plant (24/7)', avgTemp: 27.5,
      fiberRoutes: 18, connectivity: 'Excellent', waterSource: 'NEWater + Desalination', waterStress: 0.92,
      distPort: 2, distAirport: 18,
      climateRisk: 0.55, seismicRisk: 0.05, floodRisk: 0.48, cyberRisk: 0.22, regulatoryRisk: 0.28,
      politicalScore: 9.0,
      landCostMHa: 5.8, capexPerMW: 18.5, opexPerMW: 380000, targetMW: 40,
      constructionMonths: 28, permitMonths: 24, energyYield: 0.78, irr: 7.2, npv: 62, payback: 13.5,
      pros: ['Premier APAC connectivity & cable landing hub', 'IMDA data centre regulatory framework', 'Tier-1 political + legal stability'],
      cons: ['Highest cooling cost globally — 27.5°C ambient year-round', 'DC moratorium risk (1,260 MW national cap)', 'Extreme water dependency on treated/desalinated supply', 'Highest CapEx/MW of all shortlisted sites'],
      recommendation: 'Proceed only if Singapore APAC market access is a hard commercial requirement. Green Lane under GreenDC Roadmap 2030 is mandatory — apply 18 months before construction.',
      permitNotes: 'IMDA Green Lane application required. BCA Green Mark Platinum mandatory. Power allocation via EMA — apply before site acquisition. 24-month minimum from application to permit.',
      risks: [
        { name: 'DC moratorium expansion', likelihood: 4, impact: 5, category: 'regulatory', mitigation: 'Secure Green Lane allocation before land purchase' },
        { name: 'Cooling OpEx escalation', likelihood: 5, impact: 3, category: 'operational', mitigation: 'AI-optimised chiller plant — target PUE <1.35' },
        { name: 'Sea level rise (2040)', likelihood: 3, impact: 4, category: 'environmental', mitigation: 'Site 4m above MSL + levee protection' },
        { name: 'Water supply disruption', likelihood: 2, impact: 5, category: 'operational', mitigation: '7-day on-site water storage + recirculation' },
        { name: 'Power price escalation', likelihood: 4, impact: 4, category: 'financial', mitigation: 'Long-term EMA power agreement + PPA from Batam solar' },
      ],
    },
    {
      id: 'warsaw', name: 'Warsaw', country: 'Poland', region: 'Eastern Europe',
      lng: 21.01, lat: 52.23, phase: 'screening',
      gridCarbon: 590, gridCapacity: 290, powerPrice: 74, ppaPrice: 55, renewable: 34,
      coolingType: 'DX + Free Air (winter)', avgTemp: 9.0,
      fiberRoutes: 5, connectivity: 'Good', waterSource: 'Vistula River', waterStress: 0.45,
      distPort: 295, distAirport: 18,
      climateRisk: 0.30, seismicRisk: 0.05, floodRisk: 0.35, cyberRisk: 0.32, regulatoryRisk: 0.42,
      politicalScore: 6.8,
      landCostMHa: 0.35, capexPerMW: 9.8, opexPerMW: 148000, targetMW: 100,
      constructionMonths: 22, permitMonths: 20, energyYield: 0.89, irr: 11.5, npv: 195, payback: 10.1,
      pros: ['Lowest CapEx on shortlist ($9.8M/MW)', 'EU market access + GDPR jurisdiction', 'Growing Warsaw tech and cloud ecosystem', 'Cold winters provide free-air cooling season'],
      cons: ['Highest carbon grid on shortlist — coal-dominant', 'Geopolitical proximity risk (eastern border)', 'CSRD carbon stranding under EU Taxonomy', 'Thin fibre infrastructure outside Warsaw ring'],
      recommendation: 'Cost-attractive but carbon-stranded under EU CSRD. Only viable with 100% renewable PPA coverage and short-term strategy horizon (<2030). Not recommended for long-term anchor campus.',
      permitNotes: 'Polish Environmental Act EIA + Spatial Planning approval ~20 months. EU Taxonomy Article 6 monitoring required. Polish grid stabilisation levy applies from 2027.',
      risks: [
        { name: 'Geopolitical instability', likelihood: 3, impact: 4, category: 'political', mitigation: 'NATO Article 5 jurisdiction — monitor quarterly' },
        { name: 'Carbon stranding (CSRD)', likelihood: 4, impact: 4, category: 'regulatory', mitigation: '100% certified renewable PPA from 2026' },
        { name: 'Renewable PPA scarcity', likelihood: 4, impact: 3, category: 'commercial', mitigation: 'Baltic offshore wind PPA pipeline — 2027 delivery' },
        { name: 'Grid stabilisation levy', likelihood: 4, impact: 2, category: 'financial', mitigation: 'On-site battery BESS to reduce peak draw' },
        { name: 'Talent shortage', likelihood: 3, impact: 2, category: 'operational', mitigation: 'University partnerships + relocation package' },
      ],
    },
  ];

  // Bug fix: weights passed explicitly so Svelte tracks the dependency in $: scored
  function computeScore(s, w) {
    const connMap = { Excellent: 1, Good: 0.75, Fair: 0.5, Poor: 0.25 };
    const energy   = ((1 - Math.min(s.gridCarbon, 600)/600)*0.5 + s.renewable/100*0.3 + (1 - Math.min(s.powerPrice,150)/150)*0.2) * 100;
    const infra    = ((connMap[s.connectivity]||0.5)*0.4 + Math.min(s.fiberRoutes,20)/20*0.3 + (1-Math.min(s.waterStress,1))*0.3) * 100;
    const climate  = ((1-s.climateRisk)*0.3 + (1-s.seismicRisk)*0.25 + (1-s.floodRisk)*0.25 + (1-s.regulatoryRisk)*0.2) * 100;
    const fin      = ((1-Math.min(s.capexPerMW,20)/20)*0.4 + (1-Math.min(s.landCostMHa,6)/6)*0.3 + Math.min(s.irr,20)/20*0.3) * 100;
    const reg      = (s.politicalScore/10*0.6 + (1-s.regulatoryRisk)*0.4) * 100;
    return Math.round(energy*(w.energy/100) + infra*(w.infra/100) + climate*(w.climate/100) + fin*(w.financial/100) + reg*(w.regulatory/100));
  }

  // weights is referenced directly here → Svelte re-runs this when any slider changes
  $: scored = sites.map(s => ({ ...s, score: computeScore(s, weights) })).sort((a,b) => b.score - a.score);
  $: topSite = scored[0];

  // Keep selectedSite in sync when scores recompute after weight changes
  $: if (selectedSite) {
    const updated = scored.find(s => s.id === selectedSite.id);
    if (updated) selectedSite = updated;
  }

  function scoreColor(v) {
    if (v >= 85) return '#2cad84';
    if (v >= 70) return '#7faeff';
    if (v >= 55) return '#b79563';
    return '#d35d5c';
  }
  function phaseColor(p) {
    return { feasibility: '#2cad84', 'construction-ready': '#2cad84', screening: '#b79563' }[p] || '#7faeff';
  }
  function riskZone(l, i) {
    const v = l * i;
    if (v >= 15) return '#d35d5c';
    if (v >= 9)  return '#b79563';
    if (v >= 4)  return '#7faeff';
    return '#2cad84';
  }

  function selectSite(s) {
    selectedSite = s;
    activeSiteTab = 'overview';
    if (map) map.flyTo({ center: [s.lng, s.lat], zoom: 5, duration: 1400, curve: 1.4 });
  }

  let mapLoaded = false;

  // Reactive marker refresh: runs whenever scored changes OR map first loads
  // scored is referenced as a parameter → Svelte tracks it as a dependency
  $: if (mapLoaded) rebuildMarkers(scored);

  function rebuildMarkers(sites) {
    markers.forEach(m => m.remove());
    markers = [];
    sites.forEach(s => {
      const el = document.createElement('div');
      el.className = 'sm-wrap';
      el.innerHTML = `
        <div class="sm-ring" style="border-color:${scoreColor(s.score)};box-shadow:0 0 12px ${scoreColor(s.score)}44">
          <div class="sm-inner" style="background:${scoreColor(s.score)}22;color:${scoreColor(s.score)}">${s.score}</div>
        </div>
        <div class="sm-label">${s.name}</div>
      `;
      el.addEventListener('click', () => selectSite(s));
      markers.push(new mapboxgl.Marker(el).setLngLat([s.lng, s.lat]).addTo(map));
    });
  }

  onMount(async () => {
    try {
      const mbx = await import('mapbox-gl');
      mapboxgl = mbx.default;
      mapboxgl.accessToken = MAPBOX_TOKEN;
      map = new mapboxgl.Map({
        container: mapContainer,
        style: 'mapbox://styles/mapbox/dark-v11',
        center: [10, 35], zoom: 2,
        projection: 'mercator',
        attributionControl: false,
      });
      map.addControl(new mapboxgl.NavigationControl({ showCompass: false }), 'bottom-right');
      // Setting mapLoaded = true triggers the $: reactive block which calls rebuildMarkers(scored)
      map.on('load', () => { mapLoaded = true; });
    } catch(e) { console.error(e); }
  });

  onDestroy(() => { markers.forEach(m => m.remove()); if (map) map.remove(); });
</script>

<div class="planner">

  <!-- Phase gates -->
  <div class="gates">
    {#each phases as ph, i}
      <button class="gate" class:gate-on={activePhase === ph.id} on:click={() => activePhase = ph.id}>
        <div class="gate-num" style={activePhase === ph.id ? 'background:#2cad84;color:#07110f' : ''}>{i+1}</div>
        <div class="gate-text">
          <strong>{ph.label}</strong>
          <span>{ph.desc}</span>
        </div>
      </button>
      {#if i < phases.length - 1}
        <svg class="gate-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none">
          <path d="M9 6l6 6-6 6" stroke="rgba(244,247,245,0.2)" stroke-width="2" stroke-linecap="round"/>
        </svg>
      {/if}
    {/each}
  </div>

  <!-- Body -->
  <div class="body">

    <!-- Left: site list -->
    <aside class="aside">

      {#if activePhase === 'screening'}
        <div class="weight-box">
          <div class="wb-title">MCDA WEIGHTS</div>
          {#each [
            { k: 'energy',     l: 'Energy & Carbon' },
            { k: 'infra',      l: 'Infrastructure' },
            { k: 'climate',    l: 'Climate Risk' },
            { k: 'financial',  l: 'Financial' },
            { k: 'regulatory', l: 'Regulatory' },
          ] as w}
            <div class="wr">
              <span class="wl">{w.l}</span>
              <input type="range" min="5" max="50" bind:value={weights[w.k]} class="wslider" />
              <span class="wv">{weights[w.k]}%</span>
            </div>
          {/each}
        </div>
      {/if}

      <div class="site-list">
        {#each scored as s, i}
          <button class="srow" class:srow-on={selectedSite?.id === s.id} on:click={() => selectSite(s)}>
            <div class="srank">#{i+1}</div>
            <div class="sinfo">
              <div class="sname">{s.name} <span class="scountry">{s.country}</span></div>
              <div class="stags">
                <span class="sphase" style="color:{phaseColor(s.phase)}">{s.phase}</span>
                <span class="scarbon">{s.gridCarbon} gCO₂/kWh</span>
              </div>
            </div>
            <div class="sscore" style="color:{scoreColor(s.score)}">{s.score}</div>
          </button>
        {/each}
      </div>
    </aside>

    <!-- Map -->
    <div class="map-wrap">
      <div class="map-el" bind:this={mapContainer}></div>

      <!-- Legend -->
      <div class="map-legend">
        {#each [['#2cad84','≥85 Excellent'],['#7faeff','70–84 Good'],['#b79563','55–69 Fair'],['#d35d5c','<55 Weak']] as [c,l]}
          <div class="ml-row"><span class="ml-dot" style="background:{c}"></span><span>{l}</span></div>
        {/each}
      </div>
    </div>

    <!-- Detail panel -->
    {#if selectedSite}
      {@const s = selectedSite}
      <div class="detail">
        <div class="dp-head">
          <div class="dp-location">
            <div class="dp-name">{s.name}</div>
            <div class="dp-sub">{s.country} · {s.region}</div>
          </div>
          <div class="dp-score-ring" style="--c:{scoreColor(s.score)}">
            <span class="dsr-num">{s.score}</span>
            <span class="dsr-max">/100</span>
          </div>
          <button class="dp-x" aria-label="Close site detail" on:click={() => selectedSite = null}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M18 6L6 18M6 6l12 12"/></svg>
          </button>
        </div>

        <div class="dp-tabs">
          {#each [['overview','Overview'],['risk','Risk Register'],['financial','Financial']] as [id,label]}
            <button class="dptab" class:dptab-on={activeSiteTab === id} on:click={() => activeSiteTab = id}>{label}</button>
          {/each}
        </div>

        <div class="dp-body">

          <!-- OVERVIEW TAB -->
          {#if activeSiteTab === 'overview'}

            <div class="kv-grid">
              {#each [
                { l: 'Grid Carbon',     v: s.gridCarbon + ' gCO₂/kWh', c: s.gridCarbon < 100 ? '#2cad84' : s.gridCarbon < 300 ? '#7faeff' : '#d35d5c' },
                { l: 'Renewable Share', v: s.renewable + '%',            c: '#2cad84' },
                { l: 'Grid Capacity',   v: s.gridCapacity + ' MW',       c: '#7faeff' },
                { l: 'Grid Tariff',     v: '$' + s.powerPrice + '/MWh',  c: '#b79563' },
                { l: 'PPA Price',       v: '$' + s.ppaPrice + '/MWh',    c: '#2cad84' },
                { l: 'Cooling Type',    v: s.coolingType,                c: '#7faeff' },
                { l: 'Avg Temperature', v: s.avgTemp + '°C',             c: '#b79563' },
                { l: 'Water Stress',    v: (s.waterStress*100).toFixed(0) + '%', c: s.waterStress < 0.3 ? '#2cad84' : '#b79563' },
                { l: 'Fibre Routes',    v: s.fiberRoutes + ' routes',    c: '#7faeff' },
                { l: 'Water Source',    v: s.waterSource,                c: '#2cad84' },
                { l: 'Dist. to Port',   v: s.distPort + ' km',           c: 'var(--ts)' },
                { l: 'Permit Est.',     v: s.permitMonths + ' months',   c: '#b79563' },
              ] as kv}
                <div class="kvcard">
                  <div class="kvl">{kv.l}</div>
                  <div class="kvv" style="color:{kv.c}">{kv.v}</div>
                </div>
              {/each}
            </div>

            <div class="pros-cons">
              <div class="pc-col">
                {#each s.pros as p}
                  <div class="pci pro"><span>+</span>{p}</div>
                {/each}
              </div>
              <div class="pc-col">
                {#each s.cons as c}
                  <div class="pci con"><span>!</span>{c}</div>
                {/each}
              </div>
            </div>

            <div class="rec-box">
              <div class="rec-label">ASSESSMENT CONCLUSION</div>
              <p>{s.recommendation}</p>
            </div>

            <div class="permit-box">
              <div class="rec-label">PERMITTING & REGULATORY</div>
              <p>{s.permitNotes}</p>
              <div class="permit-tl">
                <span>Est. permit timeline</span>
                <strong style="color:#7faeff">{s.permitMonths} months</strong>
              </div>
            </div>

          <!-- RISK TAB -->
          {:else if activeSiteTab === 'risk'}

            <div class="risk-head-label">5×5 RISK MATRIX — {s.name.toUpperCase()}</div>

            <div class="matrix-wrap">
              <!-- outer: y-title left + right-side content -->
              <div class="mat-outer">
                <div class="mat-ytitle-col">IMPACT ↑</div>
                <div class="mat-content-col">
                  <!-- top row: y-labels beside the 5×5 cell grid -->
                  <div class="mat-inner-row">
                    <div class="mat-ylabels">
                      {#each [5,4,3,2,1] as y}<div class="mat-yl">{y}</div>{/each}
                    </div>
                    <div class="mat-cells">
                      {#each [5,4,3,2,1] as y}
                        <div class="mat-row">
                          {#each [1,2,3,4,5] as x}
                            <div class="mat-cell" style="background:{riskZone(x,y)}10;border-color:{riskZone(x,y)}25">
                              {#each s.risks.filter(r => r.likelihood === x && r.impact === y) as r}
                                <div class="rplot" style="background:{riskZone(x,y)}" title="{r.name}">{r.name.slice(0,2).toUpperCase()}</div>
                              {/each}
                            </div>
                          {/each}
                        </div>
                      {/each}
                    </div>
                  </div>
                  <!-- x-labels below cells, offset to align with cells (not y-label column) -->
                  <div class="mat-xrow">
                    <div class="mat-yspacer"></div>
                    <div class="mat-xlabels">
                      {#each [1,2,3,4,5] as x}<div class="mat-xl">{x}</div>{/each}
                    </div>
                  </div>
                  <div class="mat-xrow">
                    <div class="mat-yspacer"></div>
                    <div class="mat-xtitle">LIKELIHOOD →</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="legend-row">
              {#each [['#2cad84','Low'],['#7faeff','Medium'],['#b79563','High'],['#d35d5c','Critical']] as [c,l]}
                <div class="lr-item"><span class="lr-dot" style="background:{c}"></span>{l}</div>
              {/each}
            </div>

            <div class="risk-register">
              {#each s.risks as r}
                <div class="rr-row">
                  <div class="rr-top">
                    <span class="rr-name">{r.name}</span>
                    <span class="rr-cat" style="color:{r.category === 'environmental' ? '#2cad84' : r.category === 'financial' ? '#b79563' : r.category === 'regulatory' ? '#7faeff' : r.category === 'political' ? '#d35d5c' : 'var(--ts)'}">{r.category}</span>
                    <span class="rr-score" style="background:{riskZone(r.likelihood,r.impact)}18;color:{riskZone(r.likelihood,r.impact)}">L{r.likelihood}×I{r.impact}</span>
                  </div>
                  <div class="rr-bars">
                    <div class="rb"><span>Likelihood</span><div class="rb-t"><div style="width:{r.likelihood/5*100}%;background:{riskZone(r.likelihood,r.impact)}"></div></div><span>{r.likelihood}/5</span></div>
                    <div class="rb"><span>Impact</span><div class="rb-t"><div style="width:{r.impact/5*100}%;background:{riskZone(r.likelihood,r.impact)}"></div></div><span>{r.impact}/5</span></div>
                  </div>
                  <div class="rr-mit"><span class="mit-label">MITIGATION</span>{r.mitigation}</div>
                </div>
              {/each}
            </div>

          <!-- FINANCIAL TAB -->
          {:else if activeSiteTab === 'financial'}

            <div class="fin-kpis">
              {#each [
                { l: 'Target Capacity',  v: s.targetMW + ' MW',                                                         sub: 'IT load',                    c: 'var(--text)' },
                { l: 'Est. CapEx',       v: '$' + (s.capexPerMW * s.targetMW).toFixed(0) + 'M',                        sub: '$' + s.capexPerMW + 'M / MW', c: 'var(--text)' },
                { l: 'Annual OpEx',      v: '$' + ((s.opexPerMW * s.targetMW)/1e6).toFixed(1) + 'M',                   sub: '$' + (s.opexPerMW/1000).toFixed(0) + 'k/MW/yr', c: 'var(--text)' },
                { l: 'Project IRR',      v: s.irr + '%',                                                                 sub: '20-yr model',                c: '#2cad84' },
                { l: 'NPV (20 yr)',      v: '$' + s.npv + 'M',                                                          sub: '8% discount rate',           c: '#7faeff' },
                { l: 'Simple Payback',   v: s.payback + ' yrs',                                                         sub: 'From commissioning',         c: 'var(--text)' },
              ] as f}
                <div class="fkcard">
                  <div class="fkl">{f.l}</div>
                  <div class="fkv" style="color:{f.c}">{f.v}</div>
                  <div class="fksub">{f.sub}</div>
                </div>
              {/each}
            </div>

            <div class="section-divider">DEVELOPMENT TIMELINE</div>
            <div class="gantt">
              {#each [
                { phase: 'Site Screening & MCDA', start: 0,  dur: 2,                                          c: '#b79563' },
                { phase: 'Permitting & EIA',       start: 2,  dur: s.permitMonths,                             c: '#7faeff' },
                { phase: 'Design & Engineering',   start: 8,  dur: 10,                                         c: '#2cad84' },
                { phase: 'Civil Construction',     start: s.permitMonths, dur: s.constructionMonths,           c: '#2cad84' },
                { phase: 'M&E Installation',       start: s.permitMonths + 6, dur: s.constructionMonths - 4,   c: '#7faeff' },
                { phase: 'Commissioning & T&C',    start: s.permitMonths + s.constructionMonths, dur: 4,        c: '#b79563' },
              ] as g}
                {@const total = s.permitMonths + s.constructionMonths + 10}
                <div class="gantt-row">
                  <div class="gr-label">{g.phase}</div>
                  <div class="gr-track">
                    <div class="gr-bar" style="left:{g.start/total*100}%;width:{g.dur/total*100}%;background:{g.c}22;border-left:3px solid {g.c}">
                      <span>{g.dur}mo</span>
                    </div>
                  </div>
                </div>
              {/each}
              <div class="gantt-total">Total to commissioning: ~{s.permitMonths + s.constructionMonths + 6} months</div>
            </div>

            <div class="section-divider">POWER ECONOMICS</div>
            <div class="power-grid">
              <div class="pg-row"><span>Grid tariff</span><span>${s.powerPrice}/MWh</span></div>
              <div class="pg-row"><span>PPA price</span><span style="color:#2cad84">${s.ppaPrice}/MWh</span></div>
              <div class="pg-row"><span>Annual PPA saving</span><span style="color:#2cad84">${(((s.powerPrice - s.ppaPrice) * s.targetMW * 8760)/1e6).toFixed(1)}M/yr</span></div>
              <div class="pg-row"><span>Cooling efficiency</span><span>{(s.energyYield * 100).toFixed(0)}% yield</span></div>
              <div class="pg-row"><span>Estimated annual energy</span><span>{(s.targetMW * 8760 / 1000).toFixed(0)} GWh/yr</span></div>
              <div class="pg-row"><span>Carbon liability (CSRD)</span><span style="color:{s.gridCarbon > 200 ? '#d35d5c' : '#2cad84'}">{((s.gridCarbon * s.targetMW * 8760)/1e9).toFixed(1)} ktCO₂e/yr</span></div>
            </div>

          {/if}
        </div>

        <div class="dp-actions">
          <button class="dpa-primary" on:click={handleGenerateReport} disabled={generatingReport}>
            {#if generatingReport}
              <span class="dpa-spinner"></span>
              Generating…
            {:else if reportReady}
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              View Report
            {:else}
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
              Generate Due Diligence Report
            {/if}
          </button>
          <button
            class="dpa-sec"
            class:dpa-shortlisted={selectedSite && shortlist.includes(selectedSite.id)}
            on:click={() => selectedSite && toggleShortlist(selectedSite.id)}
          >
            {#if selectedSite && shortlist.includes(selectedSite.id)}
              <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
              On Shortlist
            {:else}
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
              Add to Shortlist
            {/if}
          </button>
        </div>
      </div>
    {/if}
  </div>

  <!-- Bottom KPI strip -->
  <div class="kpi-strip">
    <div class="kpi-block">
      <span class="kpil">TOP SITE</span>
      <span class="kpiv" style="color:#2cad84">{topSite?.name}, {topSite?.country}</span>
    </div>
    <div class="kpi-sep"></div>
    <div class="kpi-block">
      <span class="kpil">BEST CARBON</span>
      <span class="kpiv">{scored.reduce((b,s) => s.gridCarbon < b.gridCarbon ? s : b, scored[0])?.gridCarbon} gCO₂/kWh</span>
    </div>
    <div class="kpi-sep"></div>
    <div class="kpi-block">
      <span class="kpil">SITES ASSESSED</span>
      <span class="kpiv">{sites.length} candidates</span>
    </div>
    <div class="kpi-sep"></div>
    <div class="kpi-block">
      <span class="kpil">ACTIVE GATE</span>
      <span class="kpiv" style="color:#7faeff">{phases.find(p => p.id === activePhase)?.label}</span>
    </div>
    <div class="kpi-sep"></div>
    <div class="kpi-block">
      <span class="kpil">ASSESSMENT PERIOD</span>
      <span class="kpiv">Q2 2026</span>
    </div>
  </div>

</div>

<!-- Due Diligence Report Modal -->
{#if showReportModal && selectedSite}
  {@const s = selectedSite}
  <div class="modal-overlay" on:click={closeReportModal} role="presentation">
    <div class="modal-box" on:click|stopPropagation role="dialog" aria-label="Due Diligence Report">
      <div class="modal-head">
        <div>
          <div class="modal-tag">PHASE-GATE REPORT · CONFIDENTIAL</div>
          <h2 class="modal-title">Due Diligence Report — {s.name}, {s.country}</h2>
          <div class="modal-sub">Generated {new Date().toLocaleDateString('en-GB', { day:'2-digit', month:'short', year:'numeric' })} · MCDA Score {s.score}/100</div>
        </div>
        <button class="modal-close" on:click={closeReportModal} aria-label="Close report">×</button>
      </div>

      <div class="modal-body">
        <div class="rpt-section">
          <div class="rpt-sec-title">EXECUTIVE SUMMARY</div>
          <p class="rpt-para">{s.recommendation}</p>
          <p class="rpt-para">{s.permitNotes}</p>
        </div>

        <div class="rpt-section">
          <div class="rpt-sec-title">KEY METRICS</div>
          <div class="rpt-metrics">
            <div class="rpt-m"><span>MCDA Score</span><strong style="color:#2cad84">{s.score}/100</strong></div>
            <div class="rpt-m"><span>Target capacity</span><strong>{s.targetMW} MW</strong></div>
            <div class="rpt-m"><span>Grid carbon</span><strong>{s.gridCarbon} gCO₂/kWh</strong></div>
            <div class="rpt-m"><span>Renewable mix</span><strong>{s.renewable}%</strong></div>
            <div class="rpt-m"><span>CapEx/MW</span><strong>€{s.capexPerMW}M</strong></div>
            <div class="rpt-m"><span>IRR</span><strong style="color:#7faeff">{s.irr}%</strong></div>
            <div class="rpt-m"><span>NPV (20yr)</span><strong style="color:#7faeff">${s.npv}M</strong></div>
            <div class="rpt-m"><span>Payback</span><strong>{s.payback} yrs</strong></div>
          </div>
        </div>

        <div class="rpt-section">
          <div class="rpt-sec-title">STRENGTHS & RISKS</div>
          <div class="rpt-pros-cons">
            <div class="rpt-col">
              {#each s.pros as pro}
                <div class="rpt-pro">✓ {pro}</div>
              {/each}
            </div>
            <div class="rpt-col">
              {#each s.cons as con}
                <div class="rpt-con">△ {con}</div>
              {/each}
            </div>
          </div>
        </div>

        <div class="rpt-section">
          <div class="rpt-sec-title">TOP RISKS</div>
          {#each s.risks.slice(0, 3) as r}
            <div class="rpt-risk-row">
              <span class="rpt-risk-name">{r.name}</span>
              <span class="rpt-risk-cat">{r.category}</span>
              <span class="rpt-risk-mit">{r.mitigation}</span>
            </div>
          {/each}
        </div>
      </div>

      <div class="modal-foot">
        <button class="modal-dl" on:click={async () => {
          const [{ default: jsPDF }, { default: html2canvas }] = await Promise.all([import('jspdf'), import('html2canvas')]);
          const el = document.querySelector('.modal-box');
          const canvas = await html2canvas(el, { scale: 2, useCORS: true, backgroundColor: '#0d1f1c', logging: false });
          const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
          const imgW = 210; const imgH = (canvas.height * imgW) / canvas.width;
          pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, 0, imgW, Math.min(imgH, 297));
          pdf.save(`due-diligence-${s.id}.pdf`);
        }}>
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          Export PDF
        </button>
        <button class="modal-shortlist" on:click={() => toggleShortlist(s.id)}>
          {shortlist.includes(s.id) ? '♥ On Shortlist' : '♡ Add to Shortlist'}
        </button>
        <button class="modal-dismiss" on:click={closeReportModal}>Close</button>
      </div>
    </div>
  </div>
{/if}

<style>
  .planner {
    display: flex;
    flex-direction: column;
    height: calc(100vh - 166px);
    gap: 0;
  }

  /* Phase gates */
  .gates {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 10px 0 12px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 12px;
    flex-shrink: 0;
  }
  .gate {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 14px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.08);
    background: transparent;
    color: var(--ts);
    cursor: pointer;
    font-family: inherit;
    transition: all 0.15s ease;
    text-align: left;
  }
  .gate:hover { background: rgba(255,255,255,0.04); color: var(--text); }
  .gate-on {
    background: rgba(44,173,132,0.1) !important;
    border-color: rgba(44,173,132,0.3) !important;
    color: var(--text) !important;
  }
  .gate-num {
    width: 22px; height: 22px;
    border-radius: 50%;
    background: rgba(255,255,255,0.08);
    display: grid; place-items: center;
    font-size: 11px; font-weight: 800;
    flex-shrink: 0;
    transition: all 0.15s;
  }
  .gate-text strong { display: block; font-size: 12px; font-weight: 700; }
  .gate-text span   { display: block; font-size: 10px; color: var(--tm); margin-top: 1px; white-space: nowrap; }
  .gate-arrow { flex-shrink: 0; opacity: 0.4; }

  /* Body */
  .body {
    display: grid;
    grid-template-columns: 248px 1fr;
    gap: 12px;
    flex: 1;
    min-height: 0;
  }

  /* Aside */
  .aside {
    display: flex;
    flex-direction: column;
    gap: 10px;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: rgba(255,255,255,0.08) transparent;
  }

  .weight-box {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 12px 14px;
    flex-shrink: 0;
  }
  .wb-title {
    font-size: 9px; font-weight: 800; letter-spacing: 0.1em;
    color: var(--tm); margin-bottom: 10px;
  }
  .wr {
    display: flex; align-items: center; gap: 8px;
    margin-bottom: 7px; font-size: 11px;
  }
  .wl { flex: 1; color: var(--ts); font-size: 11px; }
  .wslider {
    width: 70px; accent-color: #2cad84;
    cursor: pointer; flex-shrink: 0;
  }
  .wv { font-size: 10px; font-weight: 700; color: var(--text); width: 24px; text-align: right; flex-shrink: 0; }

  .site-list {
    display: flex; flex-direction: column; gap: 4px;
    flex: 1; overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: rgba(255,255,255,0.08) transparent;
  }
  .srow {
    display: flex; align-items: center; gap: 8px;
    padding: 9px 10px;
    border-radius: 10px;
    border: 1px solid transparent;
    background: var(--panel);
    color: var(--ts);
    cursor: pointer; font-family: inherit;
    transition: all 0.15s ease;
    text-align: left;
  }
  .srow:hover { border-color: rgba(255,255,255,0.08); color: var(--text); }
  .srow-on {
    background: rgba(44,173,132,0.07) !important;
    border-color: rgba(44,173,132,0.25) !important;
    color: var(--text) !important;
  }
  .srank { font-size: 10px; font-weight: 800; color: var(--tm); width: 18px; flex-shrink: 0; }
  .sinfo { flex: 1; min-width: 0; }
  .sname { font-size: 12.5px; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .scountry { font-size: 10px; color: var(--tm); font-weight: 400; margin-left: 4px; }
  .stags { display: flex; gap: 6px; margin-top: 3px; align-items: center; }
  .sphase { font-size: 9.5px; font-weight: 700; text-transform: capitalize; }
  .scarbon { font-size: 9.5px; color: var(--tm); }
  .sscore { font-size: 18px; font-weight: 900; letter-spacing: -0.03em; flex-shrink: 0; }

  /* Map */
  .body { position: relative; }
  .map-wrap {
    position: relative;
    border-radius: 14px;
    overflow: hidden;
    background: #07110f;
  }
  .map-el { width: 100%; height: 100%; }
  .map-legend {
    position: absolute; bottom: 16px; left: 16px;
    background: rgba(7,17,15,0.92);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px; padding: 10px 14px;
    backdrop-filter: blur(12px);
    display: flex; flex-direction: column; gap: 5px;
  }
  .ml-row { display: flex; align-items: center; gap: 7px; font-size: 11px; color: var(--ts); }
  .ml-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }

  /* Detail panel */
  .detail {
    position: absolute; right: 22px; top: 0;
    width: 380px; max-height: 100%;
    background: rgba(7,17,15,0.97);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    display: flex; flex-direction: column;
    box-shadow: 0 16px 48px rgba(0,0,0,0.6);
    backdrop-filter: blur(16px);
    overflow: hidden;
    z-index: 10;
  }
  .dp-head {
    display: flex; align-items: center; gap: 10px;
    padding: 16px 16px 12px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    flex-shrink: 0;
  }
  .dp-location { flex: 1; }
  .dp-name { font-size: 17px; font-weight: 800; letter-spacing: -0.03em; color: var(--text); }
  .dp-sub  { font-size: 11px; color: var(--tm); margin-top: 2px; }
  .dp-score-ring {
    width: 52px; height: 52px;
    border-radius: 50%;
    border: 2.5px solid var(--c);
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    background: rgba(0,0,0,0.3);
    flex-shrink: 0;
    box-shadow: 0 0 16px var(--c)33;
  }
  .dsr-num { font-size: 18px; font-weight: 900; color: var(--c); letter-spacing: -0.04em; line-height: 1; }
  .dsr-max { font-size: 9px; color: var(--tm); }
  .dp-x {
    width: 28px; height: 28px; border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.05);
    color: var(--ts); cursor: pointer;
    display: grid; place-items: center;
    flex-shrink: 0;
  }
  .dp-tabs {
    display: flex; gap: 2px; padding: 8px 10px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    flex-shrink: 0;
  }
  .dptab {
    flex: 1; padding: 7px 4px;
    border-radius: 8px; border: none;
    background: transparent; color: var(--tm);
    font-size: 12px; font-weight: 600;
    cursor: pointer; font-family: inherit;
    transition: all 0.15s;
  }
  .dptab:hover { color: var(--ts); background: rgba(255,255,255,0.04); }
  .dptab-on { background: rgba(255,255,255,0.07) !important; color: var(--text) !important; }
  .dp-body { flex: 1; overflow-y: auto; padding: 14px; display: flex; flex-direction: column; gap: 12px; scrollbar-width: thin; }
  .dp-actions {
    display: flex; gap: 8px; padding: 12px 14px;
    border-top: 1px solid rgba(255,255,255,0.06); flex-shrink: 0;
  }
  .dpa-primary {
    flex: 1; padding: 10px 12px;
    background: linear-gradient(135deg,#2cad84,#23916c);
    border: none; border-radius: 9px;
    color: white; font-size: 12px; font-weight: 700;
    cursor: pointer; font-family: inherit;
    transition: all 0.2s;
  }
  .dpa-primary:hover:not(:disabled) { filter: brightness(1.1); transform: translateY(-1px); }
  .dpa-primary:disabled { opacity: 0.75; cursor: not-allowed; transform: none; }
  .dpa-primary {
    display: inline-flex; align-items: center; justify-content: center; gap: 6px;
  }
  .dpa-spinner {
    width: 12px; height: 12px;
    border: 2px solid rgba(255,255,255,0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: dpa-spin 0.7s linear infinite;
    flex-shrink: 0;
  }
  @keyframes dpa-spin { to { transform: rotate(360deg); } }

  .dpa-sec {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 10px 14px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 9px; color: var(--ts);
    font-size: 12px; font-weight: 600;
    cursor: pointer; font-family: inherit;
    transition: all 0.2s; white-space: nowrap;
  }
  .dpa-sec:hover { background: rgba(255,255,255,0.1); color: var(--text); }
  .dpa-shortlisted {
    background: rgba(211,93,92,0.15) !important;
    border-color: rgba(211,93,92,0.35) !important;
    color: #f0a0a0 !important;
  }

  /* Report Modal */
  .modal-overlay {
    position: fixed; inset: 0; z-index: 999;
    background: rgba(0,0,0,0.7);
    backdrop-filter: blur(6px);
    display: flex; align-items: center; justify-content: center;
    padding: 24px;
  }
  .modal-box {
    width: 100%; max-width: 720px; max-height: 85vh;
    background: #0d1f1c;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 24px;
    display: flex; flex-direction: column;
    overflow: hidden;
    box-shadow: 0 24px 80px rgba(0,0,0,0.6);
  }
  .modal-head {
    display: flex; justify-content: space-between; align-items: flex-start;
    padding: 20px 22px 16px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    flex-shrink: 0;
  }
  .modal-tag {
    font-size: 10px; font-weight: 700; letter-spacing: 0.1em;
    color: #b79563; margin-bottom: 6px;
  }
  .modal-title { font-size: 17px; font-weight: 900; color: var(--text); margin-bottom: 4px; }
  .modal-sub { font-size: 12px; color: var(--tm); }
  .modal-close {
    background: none; border: none; color: var(--tm);
    font-size: 22px; cursor: pointer; padding: 0 4px;
    line-height: 1; font-family: inherit; flex-shrink: 0;
  }
  .modal-close:hover { color: var(--text); }
  .modal-body { overflow-y: auto; padding: 16px 22px; flex: 1; }
  .rpt-section { margin-bottom: 20px; }
  .rpt-sec-title {
    font-size: 10px; font-weight: 700; letter-spacing: 0.1em;
    color: var(--tm); margin-bottom: 10px;
    padding-bottom: 6px; border-bottom: 1px solid rgba(255,255,255,0.06);
  }
  .rpt-para { font-size: 13px; color: var(--ts); line-height: 1.6; margin-bottom: 8px; }
  .rpt-metrics {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px;
  }
  .rpt-m {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px; padding: 10px 12px;
    display: flex; flex-direction: column; gap: 4px;
  }
  .rpt-m span { font-size: 10.5px; color: var(--tm); }
  .rpt-m strong { font-size: 14px; color: var(--text); }
  .rpt-pros-cons { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .rpt-col { display: flex; flex-direction: column; gap: 6px; }
  .rpt-pro { font-size: 12.5px; color: #8ef0cc; }
  .rpt-con { font-size: 12.5px; color: #f0c080; }
  .rpt-risk-row {
    display: grid; grid-template-columns: 1fr 100px 2fr; gap: 12px;
    padding: 8px 10px; border-radius: 8px;
    background: rgba(255,255,255,0.03);
    margin-bottom: 6px; align-items: center;
  }
  .rpt-risk-name { font-size: 12.5px; font-weight: 700; color: var(--text); }
  .rpt-risk-cat {
    font-size: 10.5px; font-weight: 600; text-transform: uppercase;
    color: #b79563; letter-spacing: 0.06em;
  }
  .rpt-risk-mit { font-size: 12px; color: var(--ts); }
  .modal-foot {
    display: flex; gap: 8px; padding: 14px 22px;
    border-top: 1px solid rgba(255,255,255,0.08); flex-shrink: 0;
  }
  .modal-dl {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 9px 16px; border-radius: 11px;
    background: linear-gradient(135deg,#2cad84,#23916c);
    border: none; color: white; font-size: 12px; font-weight: 700;
    cursor: pointer; font-family: inherit;
  }
  .modal-dl:hover { filter: brightness(1.08); }
  .modal-shortlist {
    padding: 9px 16px; border-radius: 11px;
    border: 1px solid rgba(211,93,92,0.35);
    background: rgba(211,93,92,0.1);
    color: #f0a0a0; font-size: 12px; font-weight: 600;
    cursor: pointer; font-family: inherit;
  }
  .modal-dismiss {
    margin-left: auto; padding: 9px 16px; border-radius: 11px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    color: var(--ts); font-size: 12px; font-weight: 600;
    cursor: pointer; font-family: inherit;
  }
  .modal-dismiss:hover { background: rgba(255,255,255,0.1); color: var(--text); }

  /* Overview tab */
  .kv-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 6px;
  }
  .kvcard {
    padding: 9px 11px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 9px;
  }
  .kvl { font-size: 9.5px; color: var(--tm); font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; margin-bottom: 4px; }
  .kvv { font-size: 13px; font-weight: 700; letter-spacing: -0.01em; }

  .pros-cons { display: flex; flex-direction: column; gap: 4px; }
  .pci { display: flex; align-items: flex-start; gap: 8px; font-size: 12px; line-height: 1.5; padding: 4px 0; color: var(--ts); }
  .pci span { font-size: 11px; font-weight: 800; flex-shrink: 0; width: 16px; height: 16px; border-radius: 50%; display: grid; place-items: center; margin-top: 1px; }
  .pro span { background: rgba(44,173,132,0.15); color: #2cad84; }
  .con span { background: rgba(182,126,61,0.15); color: #b79563; }

  .rec-box {
    background: rgba(44,173,132,0.07);
    border: 1px solid rgba(44,173,132,0.18);
    border-radius: 10px; padding: 12px;
  }
  .rec-box p { font-size: 12px; color: var(--ts); line-height: 1.6; margin: 0; }
  .rec-label { font-size: 9px; font-weight: 800; letter-spacing: 0.1em; color: #2cad84; margin-bottom: 6px; }

  .permit-box {
    background: rgba(127,174,255,0.06);
    border: 1px solid rgba(127,174,255,0.14);
    border-radius: 10px; padding: 12px;
  }
  .permit-box p { font-size: 12px; color: var(--ts); line-height: 1.6; margin: 0 0 8px; }
  .permit-tl { display: flex; justify-content: space-between; font-size: 12px; color: var(--tm); }

  /* Risk tab */
  .risk-head-label { font-size: 9px; font-weight: 800; letter-spacing: 0.1em; color: var(--tm); }

  .matrix-wrap { display: flex; flex-direction: column; gap: 6px; }

  /* outer: y-title rotated column + content column */
  .mat-outer { display: flex; gap: 4px; align-items: flex-start; }
  .mat-ytitle-col {
    font-size: 9px; font-weight: 700; letter-spacing: 0.1em; color: var(--tm);
    writing-mode: vertical-rl; transform: rotate(180deg);
    align-self: center; flex-shrink: 0;
  }
  .mat-content-col { display: flex; flex-direction: column; gap: 2px; flex: 1; }

  /* y-labels LEFT of cells */
  .mat-inner-row { display: flex; gap: 2px; align-items: flex-start; }
  .mat-ylabels { display: flex; flex-direction: column; gap: 2px; flex-shrink: 0; }
  .mat-yl {
    width: 18px; height: 32px;
    display: grid; place-items: center;
    font-size: 10px; color: var(--tm); font-weight: 700;
  }

  /* cells grid */
  .mat-cells { display: flex; flex-direction: column; gap: 2px; }
  .mat-row { display: flex; gap: 2px; }
  .mat-cell {
    width: 44px; height: 32px;
    border-radius: 5px; border: 1px solid;
    display: flex; align-items: center; justify-content: center;
    gap: 2px; flex-wrap: wrap;
  }
  .rplot {
    padding: 1px 4px; border-radius: 3px;
    font-size: 8px; font-weight: 800; color: #07110f;
    cursor: default;
  }

  /* x-labels below cells, aligned to cell column (not y-label column) */
  .mat-xrow { display: flex; gap: 2px; align-items: center; }
  .mat-yspacer { width: 20px; flex-shrink: 0; } /* matches .mat-yl width */
  .mat-xlabels { display: flex; gap: 2px; }
  .mat-xl {
    width: 44px; height: 18px;
    display: grid; place-items: center;
    font-size: 10px; color: var(--tm); font-weight: 700;
  }
  .mat-xtitle { font-size: 9px; font-weight: 700; letter-spacing: 0.08em; color: var(--tm); }

  /* removed: .mat-grid, .mat-x-title (replaced by mat-outer layout) */

  .legend-row { display: flex; gap: 10px; flex-wrap: wrap; }
  .lr-item { display: flex; align-items: center; gap: 5px; font-size: 11px; color: var(--tm); }
  .lr-dot { width: 8px; height: 8px; border-radius: 2px; }

  .risk-register { display: flex; flex-direction: column; gap: 8px; }
  .rr-row {
    padding: 10px 12px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
  }
  .rr-top { display: flex; align-items: center; gap: 6px; margin-bottom: 7px; flex-wrap: wrap; }
  .rr-name { font-size: 12px; font-weight: 700; color: var(--text); flex: 1; min-width: 0; }
  .rr-cat { font-size: 10px; font-weight: 600; text-transform: capitalize; }
  .rr-score { font-size: 10px; font-weight: 700; padding: 2px 7px; border-radius: 999px; }
  .rr-bars { display: flex; flex-direction: column; gap: 5px; margin-bottom: 7px; }
  .rb { display: flex; align-items: center; gap: 6px; font-size: 10px; color: var(--tm); }
  .rb span:first-child { width: 56px; flex-shrink: 0; }
  .rb span:last-child  { width: 24px; flex-shrink: 0; text-align: right; }
  .rb-t { flex: 1; height: 5px; background: rgba(255,255,255,0.07); border-radius: 999px; overflow: hidden; }
  .rb-t div { height: 100%; border-radius: 999px; transition: width 0.4s ease; }
  .rr-mit { font-size: 11px; color: var(--tm); line-height: 1.5; }
  .mit-label { font-size: 9px; font-weight: 800; letter-spacing: 0.08em; color: var(--tm); display: block; margin-bottom: 2px; }

  /* Financial tab */
  .fin-kpis { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
  .fkcard {
    padding: 10px 12px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 9px;
  }
  .fkl   { font-size: 9.5px; color: var(--tm); font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 4px; }
  .fkv   { font-size: 16px; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 2px; }
  .fksub { font-size: 10px; color: var(--tm); }

  .section-divider { font-size: 9px; font-weight: 800; letter-spacing: 0.1em; color: var(--tm); padding: 4px 0; border-bottom: 1px solid rgba(255,255,255,0.06); }

  .gantt { display: flex; flex-direction: column; gap: 5px; }
  .gantt-row { display: flex; align-items: center; gap: 8px; }
  .gr-label { font-size: 10px; color: var(--tm); width: 110px; flex-shrink: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gr-track { flex: 1; height: 20px; background: rgba(255,255,255,0.04); border-radius: 5px; position: relative; overflow: hidden; }
  .gr-bar {
    position: absolute; top: 0; height: 100%;
    border-radius: 4px; display: flex; align-items: center;
    padding: 0 6px; min-width: 28px;
    font-size: 9px; color: var(--text); font-weight: 600; white-space: nowrap;
  }
  .gantt-total { font-size: 11px; color: #7faeff; font-weight: 600; text-align: right; padding-top: 4px; }

  .power-grid { display: flex; flex-direction: column; gap: 1px; }
  .pg-row {
    display: flex; justify-content: space-between;
    padding: 8px 10px; font-size: 12px;
    background: rgba(255,255,255,0.025);
    border-bottom: 1px solid rgba(255,255,255,0.04);
  }
  .pg-row span:first-child { color: var(--tm); }
  .pg-row span:last-child  { font-weight: 700; color: var(--text); }
  .pg-row:first-child { border-radius: 8px 8px 0 0; }
  .pg-row:last-child  { border-radius: 0 0 8px 8px; border-bottom: none; }

  /* KPI strip */
  .kpi-strip {
    display: flex; align-items: center; gap: 0;
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 12px; padding: 0 6px;
    height: 44px; flex-shrink: 0; margin-top: 10px;
    overflow: hidden;
  }
  .kpi-block { display: flex; flex-direction: column; justify-content: center; padding: 0 14px; }
  .kpil { font-size: 8.5px; font-weight: 800; letter-spacing: 0.1em; color: var(--tm); text-transform: uppercase; }
  .kpiv { font-size: 12px; font-weight: 700; color: var(--text); letter-spacing: -0.01em; white-space: nowrap; }
  .kpi-sep { width: 1px; height: 24px; background: rgba(255,255,255,0.08); flex-shrink: 0; }

  /* Mapbox global marker styles */
  :global(.sm-wrap) { cursor: pointer; }
  :global(.sm-ring) {
    width: 38px; height: 38px; border-radius: 50%;
    border: 2.5px solid;
    display: grid; place-items: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.5);
    transition: transform 0.2s;
    background: rgba(7,17,15,0.85);
  }
  :global(.sm-wrap:hover .sm-ring) { transform: scale(1.15); }
  :global(.sm-inner) { font-size: 12px; font-weight: 900; letter-spacing: -0.03em; }
  :global(.sm-label) {
    margin-top: 3px; text-align: center;
    font-size: 10px; font-weight: 700; color: white;
    background: rgba(0,0,0,0.75); padding: 2px 6px;
    border-radius: 4px; white-space: nowrap;
  }
</style>
