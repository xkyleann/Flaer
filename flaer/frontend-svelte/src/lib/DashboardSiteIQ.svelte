<script>
  let selectedSite = '';

  const sites = {
    nordic: {
      name: 'Nordic Hub (Sweden / Finland)',
      score: 94,
      rating: '/ 100 — Highly suitable',
      summary: 'Outstanding renewable availability, cool climate, low water stress',
      recClass: 'rec-strong',
      recText: 'Strongly recommended',
      color: '#2cad84',
      factors: [
        { name: 'Renewable energy availability', score: 98, color: '#2cad84', note: 'Grid is 98% renewable (hydro + wind); among cleanest in the world' },
        { name: 'Climate & cooling efficiency', score: 96, color: '#2cad84', note: 'Cold climate enables free cooling 10+ months/year; minimal AC needed' },
        { name: 'Water availability', score: 88, color: '#2cad84', note: 'Abundant freshwater; low stress even under climate scenarios' },
        { name: 'Regulatory environment', score: 94, color: '#2cad84', note: 'Stable, transparent, strong ESG culture; CSRD-ready infrastructure' },
        { name: 'Grid reliability & resilience', score: 92, color: '#2cad84', note: 'Highly reliable Nordic grid; excellent interconnection' },
        { name: 'Land & infrastructure cost', score: 80, color: '#7faeff', note: 'Moderate costs offset by operational savings and incentives' },
      ]
    },
    pnw: {
      name: 'Pacific Northwest, USA',
      score: 82,
      rating: '/ 100 — Good candidate',
      summary: 'Strong hydro renewable mix, mild climate, good connectivity',
      recClass: 'rec-good',
      recText: 'Recommended',
      color: '#7faeff',
      factors: [
        { name: 'Renewable energy availability', score: 85, color: '#2cad84', note: 'Significant hydro capacity; growing wind and solar' },
        { name: 'Climate & cooling efficiency', score: 82, color: '#7faeff', note: 'Mild marine climate reduces cooling needs significantly' },
        { name: 'Water availability', score: 72, color: '#7faeff', note: 'Seasonal variation; summer stress increasing under climate projections' },
        { name: 'Regulatory environment', score: 88, color: '#2cad84', note: 'Stable US regulatory framework; state-level incentives available' },
        { name: 'Grid reliability & resilience', score: 84, color: '#2cad84', note: 'Well-interconnected western grid; some wildfire risk' },
        { name: 'Land & infrastructure cost', score: 70, color: '#7faeff', note: 'Competitive land costs but rising from tech sector demand' },
      ]
    },
    saobrasil: {
      name: 'Southern Brazil',
      score: 76,
      rating: '/ 100 — Good candidate',
      summary: 'High renewable share, competitive costs, but water risk growing',
      recClass: 'rec-good',
      recText: 'Recommended with caveats',
      color: '#7faeff',
      factors: [
        { name: 'Renewable energy availability', score: 82, color: '#7faeff', note: 'Brazilian grid is ~85% renewable but mix varies by region' },
        { name: 'Climate & cooling efficiency', score: 68, color: '#7faeff', note: 'Subtropical climate; cooling costs higher than temperate regions' },
        { name: 'Water availability', score: 60, color: '#b67e3d', note: 'Drought cycles and water scarcity are growing concerns' },
        { name: 'Regulatory environment', score: 74, color: '#7faeff', note: 'Improving but bureaucratic; FX risk should be factored in' },
        { name: 'Grid reliability & resilience', score: 78, color: '#7faeff', note: 'Improving infrastructure; some regional reliability gaps' },
        { name: 'Land & infrastructure cost', score: 86, color: '#2cad84', note: 'Very competitive; strong government incentives for tech investment' },
      ]
    },
    australia: {
      name: 'South-East Australia',
      score: 79,
      rating: '/ 100 — Good candidate',
      summary: 'Fast-growing renewables, stable governance, high connectivity costs',
      recClass: 'rec-good',
      recText: 'Recommended',
      color: '#2cad84',
      factors: [
        { name: 'Renewable energy availability', score: 84, color: '#2cad84', note: 'Rapid renewable buildout; targeting 82% by 2030' },
        { name: 'Climate & cooling efficiency', score: 62, color: '#b67e3d', note: 'Hot summers drive significant cooling energy demand' },
        { name: 'Water availability', score: 70, color: '#7faeff', note: 'Water stress is real; sea-water cooling viable for coastal sites' },
        { name: 'Regulatory environment', score: 90, color: '#2cad84', note: 'Excellent governance, strong ESG reporting framework' },
        { name: 'Grid reliability & resilience', score: 80, color: '#7faeff', note: 'Improving with battery storage; some regional gaps remain' },
        { name: 'Land & infrastructure cost', score: 72, color: '#7faeff', note: 'Moderate costs; connectivity to Asia adds latency value' },
      ]
    },
    texas: {
      name: 'Texas, USA',
      score: 61,
      rating: '/ 100 — Proceed with caution',
      summary: 'Low energy cost but grid resilience and heat stress are concerns',
      recClass: 'rec-caution',
      recText: 'Caution advised',
      color: '#b67e3d',
      factors: [
        { name: 'Renewable energy availability', score: 68, color: '#7faeff', note: 'Large wind capacity but gas dependency creates volatility' },
        { name: 'Climate & cooling efficiency', score: 42, color: '#d35d5c', note: 'Extreme summer heat significantly increases cooling energy use' },
        { name: 'Water availability', score: 50, color: '#b67e3d', note: 'Aquifer depletion is a long-term risk; drought scenarios concerning' },
        { name: 'Regulatory environment', score: 72, color: '#7faeff', note: 'Business-friendly but limited ESG regulatory framework' },
        { name: 'Grid reliability & resilience', score: 44, color: '#d35d5c', note: 'ERCOT isolation and winter storm vulnerability are key risks' },
        { name: 'Land & infrastructure cost', score: 88, color: '#2cad84', note: 'Very competitive land and energy costs; strong incentive programs' },
      ]
    },
    india: {
      name: 'Southern India',
      score: 44,
      rating: '/ 100 — Not recommended',
      summary: 'High carbon intensity, water stress, and heat challenges',
      recClass: 'rec-avoid',
      recText: 'Not recommended currently',
      color: '#d35d5c',
      factors: [
        { name: 'Renewable energy availability', score: 52, color: '#b67e3d', note: 'Solar potential strong but current grid mix remains carbon-heavy' },
        { name: 'Climate & cooling efficiency', score: 28, color: '#d35d5c', note: 'Tropical heat requires year-round intensive cooling — very costly' },
        { name: 'Water availability', score: 35, color: '#d35d5c', note: 'Severe water stress projected; monsoon dependency is a risk' },
        { name: 'Regulatory environment', score: 58, color: '#b67e3d', note: 'Improving but complex; data localisation rules require navigation' },
        { name: 'Grid reliability & resilience', score: 44, color: '#d35d5c', note: 'Frequent outages; substantial backup power investment needed' },
        { name: 'Land & infrastructure cost', score: 82, color: '#7faeff', note: 'Very low costs and a large skilled workforce are positives' },
      ]
    },
  };

  $: site = sites[selectedSite];

  function arcDash(score) {
    const circ = 176;
    const used = Math.round((score / 100) * circ);
    return `${used} ${circ}`;
  }
</script>

<div class="siq-layout">
  <div>
    <div class="siq-intro">Select candidate regions on the map or use the dropdown to analyse suitability for a new data center facility.</div>

    <div class="siq-map-wrap">
      <svg viewBox="0 0 1000 460" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="sl2" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#1a2e28"/>
            <stop offset="100%" stop-color="#12201a"/>
          </linearGradient>
          <radialGradient id="hotA" cx="50%" cy="50%"><stop offset="0%" stop-color="#2cad84" stop-opacity="0.22"/><stop offset="100%" stop-color="#2cad84" stop-opacity="0"/></radialGradient>
          <radialGradient id="hotB" cx="50%" cy="50%"><stop offset="0%" stop-color="#7faeff" stop-opacity="0.18"/><stop offset="100%" stop-color="#7faeff" stop-opacity="0"/></radialGradient>
          <radialGradient id="hotC" cx="50%" cy="50%"><stop offset="0%" stop-color="#b79563" stop-opacity="0.16"/><stop offset="100%" stop-color="#b79563" stop-opacity="0"/></radialGradient>
          <radialGradient id="hotD" cx="50%" cy="50%"><stop offset="0%" stop-color="#d35d5c" stop-opacity="0.14"/><stop offset="100%" stop-color="#d35d5c" stop-opacity="0"/></radialGradient>
        </defs>
        <rect width="1000" height="460" fill="#08120f"/>
        <path d="M60,65 L100,50 L165,46 L225,53 L268,60 L290,86 L284,118 L268,148 L246,172 L214,188 L188,196 L162,200 L140,190 L120,174 L98,162 L78,140 L62,112Z" fill="url(#sl2)" stroke="#1e3028" stroke-width="1"/>
        <path d="M288,28 L340,22 L362,36 L350,58 L318,64 L292,52Z" fill="url(#sl2)" stroke="#1e3028" stroke-width="1"/>
        <path d="M188,222 L246,216 L272,232 L282,268 L276,310 L260,342 L238,366 L212,374 L190,358 L174,326 L168,290 L174,254Z" fill="url(#sl2)" stroke="#1e3028" stroke-width="1"/>
        <path d="M425,62 L460,56 L502,58 L534,66 L544,88 L532,114 L510,129 L484,134 L457,127 L430,116 L414,95Z" fill="url(#sl2)" stroke="#1e3028" stroke-width="1"/>
        <path d="M398,64 L415,57 L422,71 L411,84 L396,78Z" fill="url(#sl2)" stroke="#1e3028" stroke-width="1"/>
        <path d="M456,36 L500,30 L521,40 L515,62 L489,68 L463,59Z" fill="url(#sl2)" stroke="#1e3028" stroke-width="1"/>
        <path d="M428,152 L506,146 L542,163 L558,200 L552,246 L536,284 L514,310 L482,324 L450,318 L426,298 L410,262 L404,220 L410,180Z" fill="url(#sl2)" stroke="#1e3028" stroke-width="1"/>
        <path d="M542,122 L606,116 L636,132 L641,158 L614,172 L572,168 L546,152Z" fill="url(#sl2)" stroke="#1e3028" stroke-width="1"/>
        <path d="M510,36 L718,28 L800,44 L808,72 L774,94 L710,100 L628,98 L542,92 L516,76Z" fill="url(#sl2)" stroke="#1e3028" stroke-width="1"/>
        <path d="M630,168 L672,162 L698,178 L708,214 L696,244 L674,260 L652,254 L630,233 L616,204 L618,182Z" fill="url(#sl2)" stroke="#1e3028" stroke-width="1"/>
        <path d="M712,76 L818,68 L858,80 L868,110 L852,142 L815,157 L774,160 L731,152 L706,130 L703,103Z" fill="url(#sl2)" stroke="#1e3028" stroke-width="1"/>
        <path d="M862,92 L884,86 L897,100 L890,118 L872,121 L860,108Z" fill="url(#sl2)" stroke="#1e3028" stroke-width="1"/>
        <path d="M762,174 L815,166 L836,182 L830,206 L804,214 L772,204 L756,188Z" fill="url(#sl2)" stroke="#1e3028" stroke-width="1"/>
        <path d="M792,278 L885,267 L927,282 L938,324 L916,360 L874,373 L826,368 L790,346 L780,312Z" fill="url(#sl2)" stroke="#1e3028" stroke-width="1"/>
        <!-- Hotspot glow zones -->
        <circle cx="490" cy="60" r="60" fill="url(#hotA)" opacity="0.8"/>
        <circle cx="115" cy="95" r="50" fill="url(#hotB)" opacity="0.7"/>
        <circle cx="226" cy="290" r="45" fill="url(#hotB)" opacity="0.6"/>
        <circle cx="860" cy="330" r="55" fill="url(#hotA)" opacity="0.7"/>
        <circle cx="170" cy="110" r="55" fill="url(#hotC)" opacity="0.6"/>
        <circle cx="665" cy="188" r="50" fill="url(#hotD)" opacity="0.6"/>
        <!-- Candidate markers -->
        <g style="cursor:pointer" on:click={() => selectedSite = 'nordic'}>
          <circle cx="490" cy="60" r="22" fill="rgba(44,173,132,0.15)" stroke="rgba(44,173,132,0.4)" stroke-width="1.5"/>
          <circle cx="490" cy="60" r="7" fill="#2cad84"/>
          <text x="490" y="44" text-anchor="middle" font-size="10" fill="#2cad84" font-family="Inter,sans-serif" font-weight="800">Nordic Hub</text>
          <text x="490" y="85" text-anchor="middle" font-size="9" fill="rgba(44,173,132,0.7)" font-family="Inter,sans-serif">Score: 94</text>
        </g>
        <g style="cursor:pointer" on:click={() => selectedSite = 'pnw'}>
          <circle cx="115" cy="95" r="20" fill="rgba(127,174,255,0.15)" stroke="rgba(127,174,255,0.4)" stroke-width="1.5"/>
          <circle cx="115" cy="95" r="7" fill="#7faeff"/>
          <text x="115" y="79" text-anchor="middle" font-size="10" fill="#7faeff" font-family="Inter,sans-serif" font-weight="800">Pacific NW</text>
          <text x="115" y="118" text-anchor="middle" font-size="9" fill="rgba(127,174,255,0.7)" font-family="Inter,sans-serif">Score: 82</text>
        </g>
        <g style="cursor:pointer" on:click={() => selectedSite = 'saobrasil'}>
          <circle cx="226" cy="290" r="18" fill="rgba(127,174,255,0.13)" stroke="rgba(127,174,255,0.3)" stroke-width="1.5"/>
          <circle cx="226" cy="290" r="6" fill="#7faeff"/>
          <text x="226" y="274" text-anchor="middle" font-size="10" fill="#7faeff" font-family="Inter,sans-serif" font-weight="800">S. Brazil</text>
          <text x="226" y="310" text-anchor="middle" font-size="9" fill="rgba(127,174,255,0.7)" font-family="Inter,sans-serif">Score: 76</text>
        </g>
        <g style="cursor:pointer" on:click={() => selectedSite = 'australia'}>
          <circle cx="860" cy="330" r="22" fill="rgba(44,173,132,0.15)" stroke="rgba(44,173,132,0.4)" stroke-width="1.5"/>
          <circle cx="860" cy="330" r="7" fill="#2cad84"/>
          <text x="860" y="314" text-anchor="middle" font-size="10" fill="#2cad84" font-family="Inter,sans-serif" font-weight="800">SE Australia</text>
          <text x="860" y="355" text-anchor="middle" font-size="9" fill="rgba(44,173,132,0.7)" font-family="Inter,sans-serif">Score: 79</text>
        </g>
        <g style="cursor:pointer" on:click={() => selectedSite = 'texas'}>
          <circle cx="170" cy="130" r="19" fill="rgba(183,149,99,0.13)" stroke="rgba(183,149,99,0.3)" stroke-width="1.5"/>
          <circle cx="170" cy="130" r="6" fill="#b67e3d"/>
          <text x="170" y="114" text-anchor="middle" font-size="10" fill="#b67e3d" font-family="Inter,sans-serif" font-weight="800">Texas</text>
          <text x="170" y="152" text-anchor="middle" font-size="9" fill="rgba(183,149,99,0.7)" font-family="Inter,sans-serif">Score: 61</text>
        </g>
        <g style="cursor:pointer" on:click={() => selectedSite = 'india'}>
          <circle cx="665" cy="190" r="18" fill="rgba(211,93,92,0.12)" stroke="rgba(211,93,92,0.28)" stroke-width="1.5"/>
          <circle cx="665" cy="190" r="6" fill="#d35d5c"/>
          <text x="665" y="174" text-anchor="middle" font-size="10" fill="#d35d5c" font-family="Inter,sans-serif" font-weight="800">S. India</text>
          <text x="665" y="212" text-anchor="middle" font-size="9" fill="rgba(211,93,92,0.7)" font-family="Inter,sans-serif">Score: 44</text>
        </g>
      </svg>
    </div>

    <div class="map-key">
      <div class="mk-item"><span class="mk-dot" style="background:#2cad84"></span>Highly suitable (80–100)</div>
      <div class="mk-item"><span class="mk-dot" style="background:#7faeff"></span>Good (65–79)</div>
      <div class="mk-item"><span class="mk-dot" style="background:#b67e3d"></span>Caution (50–64)</div>
      <div class="mk-item"><span class="mk-dot" style="background:#d35d5c"></span>Avoid (&lt;50)</div>
    </div>
  </div>

  <div class="site-card">
    <div class="site-card-head">
      <h3>Location analysis</h3>
      <p>Select a candidate location to see full suitability report</p>
    </div>
    <div class="site-card-body">
      <select class="site-select" bind:value={selectedSite}>
        <option value="">Choose a location...</option>
        <option value="nordic">Nordic Hub (Sweden / Finland)</option>
        <option value="pnw">Pacific Northwest, USA</option>
        <option value="saobrasil">Southern Brazil</option>
        <option value="australia">South-East Australia</option>
        <option value="texas">Texas, USA</option>
        <option value="india">Southern India</option>
      </select>

      {#if site}
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
            <p>{site.summary}</p>
          </div>
        </div>

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
        <button class="compare-btn">Compare with other locations</button>
      {:else}
        <div class="siq-placeholder">
          <p>Click a location on the map<br>or use the dropdown above</p>
        </div>
      {/if}
    </div>
  </div>
</div>

<style>
  .siq-layout { display: grid; grid-template-columns: 1fr 380px; gap: 16px; align-items: start; }

  .siq-intro { font-size: 13px; color: rgba(244,247,245,0.56); margin-bottom: 10px; }

  .siq-map-wrap {
    position: relative;
    border-radius: 22px;
    overflow: hidden;
    background: linear-gradient(180deg, #091310, #060e0c);
    border: 1px solid rgba(255,255,255,0.08);
  }

  .siq-map-wrap svg { width: 100%; display: block; }

  .map-key { display: flex; gap: 12px; margin-top: 12px; flex-wrap: wrap; }
  .mk-item { display: flex; align-items: center; gap: 6px; font-size: 11px; color: rgba(244,247,245,0.5); font-weight: 700; }
  .mk-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }

  .site-card {
    border-radius: 24px;
    background: linear-gradient(180deg, rgba(255,255,255,0.07), rgba(255,255,255,0.04));
    border: 1px solid rgba(255,255,255,0.09);
    overflow: hidden;
  }

  .site-card-head { padding: 16px 18px; border-bottom: 1px solid rgba(255,255,255,0.08); }
  .site-card-head h3 { font-size: 15px; font-weight: 900; color: #f4f7f5; margin-bottom: 4px; }
  .site-card-head p { font-size: 12px; color: rgba(244,247,245,0.5); }

  .site-card-body { padding: 16px; }

  .site-select {
    width: 100%;
    padding: 10px 14px;
    border-radius: 999px;
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
    border-radius: 18px;
    background: rgba(44,173,132,0.07);
    border: 1px solid rgba(44,173,132,0.14);
    margin-bottom: 14px;
  }

  .score-ring { position: relative; width: 72px; height: 72px; flex-shrink: 0; }
  .score-ring svg { width: 100%; height: 100%; }

  .score-meta strong { display: block; font-size: 28px; font-weight: 900; letter-spacing: -0.05em; color: #f4f7f5; }
  .score-meta span { font-size: 13px; color: rgba(244,247,245,0.6); }
  .score-meta p { font-size: 12px; color: rgba(244,247,245,0.54); margin-top: 4px; }

  .factor-list { display: grid; gap: 9px; margin-bottom: 14px; }

  .factor {
    padding: 12px 14px;
    border-radius: 16px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
  }

  .factor-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 7px; }
  .factor-name { font-size: 12px; font-weight: 800; color: #f4f7f5; }
  .factor-score { font-size: 13px; font-weight: 900; letter-spacing: -0.02em; }
  .factor-bar { height: 5px; border-radius: 999px; background: rgba(255,255,255,0.08); overflow: hidden; }
  .factor-fill { height: 100%; border-radius: 999px; transition: width 0.5s ease; }
  .factor-note { font-size: 11px; color: rgba(244,247,245,0.46); margin-top: 5px; }

  .rec-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 11px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 900;
    margin-top: 12px;
  }

  .rec-strong { background: rgba(44,173,132,0.16); color: #b6ffe7; }
  .rec-good { background: rgba(127,174,255,0.14); color: #dce8ff; }
  .rec-caution { background: rgba(183,149,99,0.16); color: #ffe9c9; }
  .rec-avoid { background: rgba(211,93,92,0.16); color: #ffdede; }

  .compare-btn {
    width: 100%;
    padding: 11px;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.09);
    color: #f4f7f5;
    font-size: 12px;
    font-weight: 800;
    cursor: pointer;
    font-family: inherit;
    margin-top: 10px;
  }

  .siq-placeholder {
    padding: 32px 0;
    text-align: center;
    color: rgba(244,247,245,0.3);
    font-size: 13px;
    font-weight: 700;
    line-height: 1.6;
  }
</style>
