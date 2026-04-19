<script>
  import { dataCenters } from './data.js';

  let hoveredDC = $state(null);
  let tooltipX = $state(0);
  let tooltipY = $state(0);
  let svgEl = $state(null);

  const riskColor = {
    green: '#2cad84',
    amber: '#b67e3d',
    red: '#d35d5c',
  };

  function onEnter(e, dc) {
    hoveredDC = dc;
    updatePos(e, dc);
  }

  function onMove(e, dc) {
    if (hoveredDC?.id === dc.id) updatePos(e, dc);
  }

  function onLeave() {
    hoveredDC = null;
  }

  function updatePos(e, dc) {
    if (!svgEl) return;
    const rect = svgEl.getBoundingClientRect();
    const scaleX = rect.width / 960;
    const scaleY = rect.height / 500;
    tooltipX = dc.x * scaleX + rect.left;
    tooltipY = dc.y * scaleY + rect.top;
  }
</script>

<div class="map-wrap">
  <svg
    bind:this={svgEl}
    viewBox="0 0 960 500"
    xmlns="http://www.w3.org/2000/svg"
    class="world-svg"
    aria-label="Data center world map"
  >
    <defs>
      <radialGradient id="glow-green" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#2cad84" stop-opacity="0.9"/>
        <stop offset="100%" stop-color="#2cad84" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="glow-amber" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#b67e3d" stop-opacity="0.9"/>
        <stop offset="100%" stop-color="#b67e3d" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="glow-red" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#d35d5c" stop-opacity="0.9"/>
        <stop offset="100%" stop-color="#d35d5c" stop-opacity="0"/>
      </radialGradient>
    </defs>

    <!-- Ocean background -->
    <rect width="960" height="500" fill="rgba(7,17,15,0.0)"/>

    <!-- Grid lines -->
    {#each [100,200,300,400] as y}
      <line x1="0" y1={y} x2="960" y2={y} stroke="rgba(255,255,255,0.04)" stroke-width="1"/>
    {/each}
    {#each [120,240,360,480,600,720,840] as x}
      <line x1={x} y1="0" x2={x} y2="500" stroke="rgba(255,255,255,0.04)" stroke-width="1"/>
    {/each}

    <!-- North America -->
    <path
      d="M 148,97 L 120,75 L 98,80 L 80,95 L 72,112 L 80,130 L 95,142 L 108,158 L 118,170 L 132,176 L 148,182 L 160,195 L 175,215 L 195,240 L 210,250 L 225,250 L 237,240 L 250,228 L 258,212 L 265,198 L 272,183 L 278,165 L 285,148 L 290,130 L 285,112 L 275,100 L 260,92 L 240,85 L 218,80 L 196,78 L 175,82 L 162,90 Z"
      fill="rgba(44,173,132,0.12)"
      stroke="rgba(44,173,132,0.25)"
      stroke-width="1"
    />

    <!-- Greenland -->
    <path
      d="M 352,52 L 372,46 L 395,48 L 415,56 L 422,72 L 415,90 L 400,100 L 380,102 L 360,92 L 348,72 Z"
      fill="rgba(44,173,132,0.10)"
      stroke="rgba(44,173,132,0.2)"
      stroke-width="1"
    />

    <!-- South America -->
    <path
      d="M 248,240 L 265,228 L 282,222 L 300,224 L 318,236 L 333,254 L 344,276 L 350,302 L 350,328 L 342,352 L 328,370 L 308,380 L 288,380 L 268,368 L 252,346 L 242,320 L 238,294 L 240,268 L 244,252 Z"
      fill="rgba(44,173,132,0.12)"
      stroke="rgba(44,173,132,0.25)"
      stroke-width="1"
    />

    <!-- Europe -->
    <path
      d="M 456,80 L 472,70 L 490,66 L 510,68 L 530,72 L 548,80 L 560,92 L 562,106 L 554,116 L 538,120 L 522,118 L 508,124 L 494,130 L 484,122 L 472,112 L 460,100 L 454,88 Z"
      fill="rgba(44,173,132,0.12)"
      stroke="rgba(44,173,132,0.25)"
      stroke-width="1"
    />

    <!-- Africa -->
    <path
      d="M 466,142 L 488,132 L 512,130 L 538,136 L 558,150 L 572,170 L 580,196 L 580,222 L 574,248 L 562,272 L 546,292 L 524,308 L 502,314 L 480,310 L 460,294 L 446,270 L 440,244 L 442,218 L 448,192 L 456,166 L 462,152 Z"
      fill="rgba(44,173,132,0.12)"
      stroke="rgba(44,173,132,0.25)"
      stroke-width="1"
    />

    <!-- Asia -->
    <path
      d="M 558,75 L 598,65 L 645,60 L 695,60 L 745,65 L 795,72 L 840,82 L 870,98 L 882,118 L 876,140 L 858,156 L 836,164 L 812,170 L 784,180 L 758,194 L 742,212 L 724,218 L 704,212 L 682,206 L 660,202 L 638,208 L 620,208 L 605,196 L 592,180 L 578,162 L 564,144 L 554,126 L 550,108 L 553,90 Z"
      fill="rgba(44,173,132,0.12)"
      stroke="rgba(44,173,132,0.25)"
      stroke-width="1"
    />

    <!-- Indian subcontinent -->
    <path
      d="M 652,190 L 672,182 L 692,180 L 706,192 L 712,212 L 705,234 L 688,248 L 668,250 L 650,240 L 640,222 L 640,206 Z"
      fill="rgba(44,173,132,0.12)"
      stroke="rgba(44,173,132,0.25)"
      stroke-width="1"
    />

    <!-- Southeast Asia peninsula -->
    <path
      d="M 738,204 L 752,196 L 760,208 L 762,226 L 754,240 L 742,244 L 730,236 L 728,220 Z"
      fill="rgba(44,173,132,0.10)"
      stroke="rgba(44,173,132,0.2)"
      stroke-width="1"
    />

    <!-- Australia -->
    <path
      d="M 752,300 L 780,286 L 814,278 L 848,284 L 874,300 L 886,322 L 882,348 L 868,364 L 840,372 L 810,368 L 782,350 L 760,328 L 750,308 Z"
      fill="rgba(44,173,132,0.12)"
      stroke="rgba(44,173,132,0.25)"
      stroke-width="1"
    />

    <!-- Japan -->
    <path
      d="M 848,148 L 860,140 L 870,148 L 868,160 L 856,168 L 844,164 L 840,154 Z"
      fill="rgba(44,173,132,0.10)"
      stroke="rgba(44,173,132,0.2)"
      stroke-width="1"
    />

    <!-- Data center nodes -->
    {#each dataCenters as dc}
      {@const col = riskColor[dc.risk]}
      {@const isHovered = hoveredDC?.id === dc.id}

      <!-- Pulse ring -->
      <circle
        cx={dc.x}
        cy={dc.y}
        r={isHovered ? 18 : 12}
        fill="none"
        stroke={col}
        stroke-width="1"
        opacity={isHovered ? 0.5 : 0.25}
        style="transition: r 0.2s, opacity 0.2s;"
      />

      <!-- Outer ring -->
      <circle
        cx={dc.x}
        cy={dc.y}
        r={isHovered ? 10 : 7}
        fill="none"
        stroke={col}
        stroke-width="1.5"
        opacity={isHovered ? 0.8 : 0.5}
        style="transition: r 0.2s, opacity 0.2s;"
      />

      <!-- Core dot -->
      <circle
        class="dc-node"
        role="button"
        tabindex="0"
        aria-label="{dc.name} data center, {dc.intensity} gCO₂/kWh"
        cx={dc.x}
        cy={dc.y}
        r={isHovered ? 5 : 4}
        fill={col}
        opacity="1"
        style="transition: r 0.2s; cursor: pointer; filter: drop-shadow(0 0 6px {col});"
        onmouseenter={(e) => onEnter(e, dc)}
        onmousemove={(e) => onMove(e, dc)}
        onmouseleave={onLeave}
      />
    {/each}
  </svg>

  <!-- Tooltip -->
  {#if hoveredDC}
    {@const col = riskColor[hoveredDC.risk]}
    <div
      class="tooltip"
      style="left: {tooltipX}px; top: {tooltipY}px;"
    >
      <div class="tt-header">
        <span class="tt-dot" style="background: {col};"></span>
        <span class="tt-name">{hoveredDC.name}</span>
        <span class="tt-region">{hoveredDC.region}</span>
      </div>
      <div class="tt-grid">
        <div class="tt-stat">
          <div class="tt-val">{hoveredDC.intensity} <span>gCO₂/kWh</span></div>
          <div class="tt-label">Carbon intensity</div>
        </div>
        <div class="tt-stat">
          <div class="tt-val">{hoveredDC.forecast2035} <span>gCO₂/kWh</span></div>
          <div class="tt-label">2035 forecast</div>
        </div>
        <div class="tt-stat">
          <div class="tt-val" style="color: {col};">{hoveredDC.csrdExposure}</div>
          <div class="tt-label">CSRD exposure</div>
        </div>
        <div class="tt-stat">
          <div class="tt-val {hoveredDC.risk === 'green' ? 'c-green' : hoveredDC.risk === 'amber' ? 'c-amber' : 'c-red'}">{hoveredDC.trend}</div>
          <div class="tt-label">30-day trend</div>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .map-wrap {
    position: relative;
    width: 100%;
  }

  .world-svg {
    width: 100%;
    height: auto;
    display: block;
  }

  .dc-node {
    transition: r 0.2s;
  }

  .tooltip {
    position: fixed;
    z-index: 200;
    transform: translate(-50%, calc(-100% - 16px));
    background: rgba(10, 22, 18, 0.96);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 14px;
    padding: 14px 16px;
    min-width: 210px;
    pointer-events: none;
    backdrop-filter: blur(12px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    animation: fadeInUp 0.15s ease;
  }

  .tt-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
  }

  .tt-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .tt-name {
    font-size: 13px;
    font-weight: 700;
    color: #f4f7f5;
    flex: 1;
  }

  .tt-region {
    font-size: 10px;
    color: rgba(244,247,245,0.45);
    font-family: 'SF Mono', monospace;
  }

  .tt-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }

  .tt-stat {
    display: flex;
    flex-direction: column;
    gap: 3px;
  }

  .tt-val {
    font-size: 14px;
    font-weight: 700;
    color: #f4f7f5;
    line-height: 1.2;
  }

  .tt-val span {
    font-size: 10px;
    font-weight: 500;
    color: rgba(244,247,245,0.5);
  }

  .tt-label {
    font-size: 10.5px;
    color: rgba(244,247,245,0.45);
  }

  .c-green { color: #2cad84; }
  .c-amber { color: #b67e3d; }
  .c-red   { color: #d35d5c; }

  @keyframes fadeInUp {
    from { opacity: 0; transform: translate(-50%, calc(-100% - 8px)); }
    to   { opacity: 1; transform: translate(-50%, calc(-100% - 16px)); }
  }
</style>
