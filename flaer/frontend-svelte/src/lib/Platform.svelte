<script>
  import { onMount } from 'svelte';

  let statsVisible = false;
  let platformVisible = false;
  let statsEl;
  let platformEl;
  let scrollProgress = 0;

  // Sparkline data (24h carbon intensity, normalized)
  const chartPoints = [62,68,72,65,58,55,60,64,70,74,69,63,60,58,56,54,50,48,52,58,62,60,57,55];
  const w = 400;
  const h = 80;
  const pad = 6;

  function buildPath(pts) {
    const max = Math.max(...pts);
    const min = Math.min(...pts);
    const range = max - min || 1;
    const step = (w - pad * 2) / (pts.length - 1);
    return pts.map((v, i) => {
      const x = pad + i * step;
      const y = h - pad - ((v - min) / range) * (h - pad * 2);
      return `${i === 0 ? 'M' : 'L'} ${x.toFixed(1)},${y.toFixed(1)}`;
    }).join(' ');
  }

  function buildArea(pts) {
    const linePath = buildPath(pts);
    const max = Math.max(...pts);
    const min = Math.min(...pts);
    const range = max - min || 1;
    const step = (w - pad * 2) / (pts.length - 1);
    const lastX = pad + (pts.length - 1) * step;
    return `${linePath} L ${lastX.toFixed(1)},${h - pad} L ${pad},${h - pad} Z`;
  }

  const linePath = buildPath(chartPoints);
  const areaPath = buildArea(chartPoints);

  const metrics = [
    { location: 'Frankfurt', value: 284, badge: 'amber', trend: '+2.4%', arrow: 'up' },
    { location: 'Dublin',    value: 198, badge: 'green', trend: '-0.8%', arrow: 'down' },
    { location: 'Stockholm', value: 18,  badge: 'green', trend: '-5.2%', arrow: 'down' },
    { location: 'Warsaw',    value: 701, badge: 'red',   trend: '-1.1%', arrow: 'down' },
  ];

  const features = [
    {
      icon: 'zap',
      title: 'Carbon intensity signals',
      body: 'Real-time grid data from 40+ operators. 5-minute resolution.',
    },
    {
      icon: 'trending',
      title: 'Ten-year forecasting',
      body: 'ML models trained on 15 years of grid data project trajectories through 2035.',
    },
    {
      icon: 'clipboard',
      title: 'CSRD reporting',
      body: 'Auto-generate audit-ready reports from infrastructure telemetry.',
    },
  ];

  onMount(() => {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.target === statsEl && e.isIntersecting) statsVisible = true;
        if (e.target === platformEl && e.isIntersecting) platformVisible = true;
      });
    }, { threshold: 0.1 });

    if (statsEl) io.observe(statsEl);
    if (platformEl) io.observe(platformEl);

    // Scroll progress for parallax
    const handleScroll = () => {
      if (platformEl) {
        const rect = platformEl.getBoundingClientRect();
        const windowHeight = window.innerHeight;
        const progress = Math.max(0, Math.min(1, 1 - (rect.top / windowHeight)));
        scrollProgress = progress;
      }
    };

    window.addEventListener('scroll', handleScroll);
    handleScroll();

    return () => {
      io.disconnect();
      window.removeEventListener('scroll', handleScroll);
    };
  });
</script>

<!-- ═══════════════════════════════════════════════════
     Part A — Number wall
════════════════════════════════════════════════════ -->
<section id="platform" class="stats-section">
  <!-- Animated background gradient -->
  <div class="stats-bg-gradient" aria-hidden="true"></div>
  
  <div class="stats-inner w" bind:this={statsEl} class:visible={statsVisible}>
    <div class="stats-eyebrow">
      <span class="eyebrow-icon">✦</span>
      Proven at scale
    </div>

    <div class="stats-wall">
      <div class="stat-block stat-block-1">
        <div class="stat-val">
          <span class="stat-number">47</span>
          <span class="stat-shimmer"></span>
        </div>
        <div class="stat-label">tCO₂ tracked per minute</div>
      </div>
      <div class="stat-sep" aria-hidden="true"></div>
      <div class="stat-block stat-block-2">
        <div class="stat-val">
          <span class="stat-number">&euro;2.1M</span>
          <span class="stat-shimmer"></span>
        </div>
        <div class="stat-label">average annual savings per portfolio</div>
      </div>
      <div class="stat-sep" aria-hidden="true"></div>
      <div class="stat-block stat-block-3">
        <div class="stat-val">
          <span class="stat-number">100%</span>
          <span class="stat-shimmer"></span>
        </div>
        <div class="stat-label">CSRD audit readiness</div>
      </div>
    </div>
  </div>
</section>

<!-- ═══════════════════════════════════════════════════
     Part B — Intelligence layer
════════════════════════════════════════════════════ -->
<section class="platform-section">
  <!-- Subtle top separator -->
  <div class="section-line" aria-hidden="true"></div>

  <!-- Parallax background elements -->
  <div class="parallax-orb parallax-orb-1" style="transform: translateY({scrollProgress * 100}px)" aria-hidden="true"></div>
  <div class="parallax-orb parallax-orb-2" style="transform: translateY({scrollProgress * -80}px)" aria-hidden="true"></div>

  <div class="platform-inner w" bind:this={platformEl} class:visible={platformVisible}>

    <!-- Left copy -->
    <div class="platform-copy">
      <div class="p-eyebrow">
        <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
          <circle cx="6" cy="6" r="5" stroke="currentColor" stroke-width="1.5"/>
          <path d="M6 3v3l2 1.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        The platform
      </div>

      <h2>The carbon layer your<br />infrastructure is missing.</h2>

      <p class="p-body">
        Most infrastructure teams are flying blind on carbon. Flaer adds a continuous intelligence layer — connecting grid operators, cloud APIs, and compliance frameworks into a single system of record.
      </p>

      <div class="feature-list">
        {#each features as f, i}
          <div class="feature-row" style="transition-delay: {0.1 + i * 0.1}s">
            <div class="feature-icon" aria-hidden="true">
              {#if f.icon === 'zap'}
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
                </svg>
              {:else if f.icon === 'trending'}
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
                  <polyline points="17 6 23 6 23 12"/>
                </svg>
              {:else}
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
                  <rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>
                </svg>
              {/if}
            </div>
            <div class="feature-text">
              <div class="f-title">{f.title}</div>
              <div class="f-body">{f.body}</div>
            </div>
          </div>
        {/each}
      </div>
    </div>

    <!-- Right metrics card with enhanced glass effect -->
    <div class="metrics-card" style="transform: translateY({scrollProgress * -30}px)">
      <div class="mc-head">
        <span class="mc-title">
          <span class="pulse-indicator"></span>
          EU region &middot; Carbon intensity
        </span>
        <span class="mc-period">Last 24h</span>
      </div>

      <!-- Sparkline chart -->
      <div class="chart-wrap">
        <svg viewBox="0 0 {w} {h}" width="100%" preserveAspectRatio="none" aria-hidden="true">
          <defs>
            <linearGradient id="plat-area-grad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#2cad84" stop-opacity="0.22"/>
              <stop offset="100%" stop-color="#2cad84" stop-opacity="0"/>
            </linearGradient>
          </defs>
          <path d={areaPath} fill="url(#plat-area-grad)"/>
          <path d={linePath} fill="none" stroke="#2cad84" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <div class="chart-labels">
          <span>00:00</span>
          <span>06:00</span>
          <span>12:00</span>
          <span>18:00</span>
          <span>Now</span>
        </div>
      </div>

      <!-- Location tiles -->
      <div class="tiles">
        {#each metrics as m}
          <div class="tile">
            <div class="tile-loc">{m.location}</div>
            <div class="tile-val">{m.value} <span class="tile-unit">gCO₂</span></div>
            <div class="tile-badge badge--{m.badge}">
              {#if m.arrow === 'down'}
                <svg width="9" height="9" viewBox="0 0 12 12" fill="none" aria-hidden="true">
                  <path d="M6 2v8M2 7l4 4 4-4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              {:else}
                <svg width="9" height="9" viewBox="0 0 12 12" fill="none" aria-hidden="true">
                  <path d="M6 10V2M2 5l4-4 4 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              {/if}
              {m.trend}
            </div>
          </div>
        {/each}
      </div>
    </div>
  </div>
</section>

<style>
  /* ─── Stats section ──────────────────────────────────────── */
  .stats-section {
    background: #000;
    padding: 120px 0 100px;
    position: relative;
    overflow: hidden;
  }

  .stats-bg-gradient {
    position: absolute;
    inset: 0;
    background:
      radial-gradient(ellipse 60% 50% at 50% 50%, rgba(44,173,132,0.08), transparent 70%),
      radial-gradient(ellipse 40% 40% at 80% 50%, rgba(183,149,99,0.06), transparent 60%);
    animation: stats-gradient-shift 15s ease-in-out infinite;
    pointer-events: none;
  }

  @keyframes stats-gradient-shift {
    0%, 100% {
      transform: scale(1) rotate(0deg);
      opacity: 0.6;
    }
    50% {
      transform: scale(1.1) rotate(5deg);
      opacity: 0.8;
    }
  }

  .stats-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
  }

  .stats-inner {
    display: flex;
    flex-direction: column;
    align-items: center;
    opacity: 0;
    transform: translateY(40px);
    transition: opacity 0.9s var(--ease-out), transform 0.9s var(--ease-out);
  }

  .stats-inner.visible {
    opacity: 1;
    transform: translateY(0);
  }

  .stats-eyebrow {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.35);
    margin-bottom: 56px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .eyebrow-icon {
    font-size: 14px;
    color: var(--green);
    animation: icon-pulse 3s ease-in-out infinite;
  }

  @keyframes icon-pulse {
    0%, 100% {
      opacity: 0.6;
      transform: scale(1);
    }
    50% {
      opacity: 1;
      transform: scale(1.2);
    }
  }

  .stats-wall {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    gap: 0;
  }

  .stat-block {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 0 48px;
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.8s var(--ease-out), transform 0.8s var(--ease-out);
  }

  .stats-inner.visible .stat-block-1 {
    opacity: 1;
    transform: translateY(0);
    transition-delay: 0.2s;
  }

  .stats-inner.visible .stat-block-2 {
    opacity: 1;
    transform: translateY(0);
    transition-delay: 0.4s;
  }

  .stats-inner.visible .stat-block-3 {
    opacity: 1;
    transform: translateY(0);
    transition-delay: 0.6s;
  }

  .stat-val {
    font-size: clamp(56px, 6vw, 88px);
    font-weight: 700;
    letter-spacing: -0.04em;
    line-height: 1;
    color: #f5f5f7;
    margin-bottom: 14px;
    position: relative;
    display: inline-block;
  }

  .stat-number {
    position: relative;
    z-index: 1;
    background: linear-gradient(135deg, #f5f5f7 0%, rgba(44,173,132,0.8) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .stat-shimmer {
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.22) 50%, transparent 100%);
    animation: shimmer 3.5s ease-in-out infinite;
    pointer-events: none;
  }

  .stat-label {
    font-size: 15px;
    font-weight: 400;
    color: rgba(255,255,255,0.5);
    letter-spacing: -0.015em;
    line-height: 1.4;
    max-width: 200px;
  }

  .stat-sep {
    width: 1px;
    height: 80px;
    background: rgba(255,255,255,0.1);
    flex-shrink: 0;
  }

  /* ─── Platform section ───────────────────────────────────── */
  .platform-section {
    background: #000;
    padding: 100px 0 140px;
    position: relative;
    overflow: hidden;
  }

  .section-line {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
  }

  .platform-section::before {
    content: '';
    position: absolute;
    inset: 0;
    background: rgba(255,255,255,0.015);
    pointer-events: none;
  }

  /* ─── Parallax orbs ──────────────────────────────────────── */
  .parallax-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(100px);
    opacity: 0.3;
    pointer-events: none;
    will-change: transform;
  }

  .parallax-orb-1 {
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(127,174,255,0.3), transparent 70%);
    top: 10%;
    right: 10%;
  }

  .parallax-orb-2 {
    width: 350px;
    height: 350px;
    background: radial-gradient(circle, rgba(44,173,132,0.25), transparent 70%);
    bottom: 20%;
    left: 15%;
  }

  .platform-inner {
    display: grid;
    grid-template-columns: 1fr 1.15fr;
    gap: 80px;
    align-items: center;
    opacity: 0;
    transform: translateY(40px);
    transition: opacity 0.9s var(--ease-out) 0.1s, transform 0.9s var(--ease-out) 0.1s;
  }

  .platform-inner.visible {
    opacity: 1;
    transform: translateY(0);
  }

  /* ─── Copy ───────────────────────────────────────────────── */
  .p-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--green);
    margin-bottom: 20px;
  }

  h2 {
    font-size: clamp(32px, 3.6vw, 52px);
    font-weight: 700;
    line-height: 1.06;
    letter-spacing: -0.03em;
    color: #f5f5f7;
    margin-bottom: 24px;
  }

  .p-body {
    font-size: 18px;
    line-height: 1.56;
    color: rgba(255,255,255,0.52);
    margin-bottom: 44px;
    letter-spacing: -0.018em;
    max-width: 480px;
  }

  .feature-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .feature-row {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 18px 20px;
    border-radius: var(--radius-md);
    border: 1px solid transparent;
    transition: background 0.3s var(--ease-out), border-color 0.3s var(--ease-out), transform 0.3s var(--ease-out);
  }

  .feature-row:hover {
    background: rgba(255,255,255,0.04);
    border-color: rgba(255,255,255,0.08);
    transform: translateX(4px);
  }

  .feature-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, rgba(44,173,132,0.14), rgba(127,174,255,0.10));
    border: 1px solid rgba(255,255,255,0.09);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--green);
    flex-shrink: 0;
    margin-top: 1px;
  }

  .f-title {
    font-size: 16px;
    font-weight: 600;
    color: rgba(255,255,255,0.9);
    letter-spacing: -0.02em;
    margin-bottom: 5px;
  }

  .f-body {
    font-size: 14px;
    line-height: 1.5;
    color: rgba(255,255,255,0.45);
    letter-spacing: -0.01em;
  }

  /* ─── Metrics card with enhanced glass effect ─────────────── */
  .metrics-card {
    background: rgba(10,10,12,0.7);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: var(--radius-xl);
    overflow: hidden;
    backdrop-filter: blur(60px) saturate(180%);
    -webkit-backdrop-filter: blur(60px) saturate(180%);
    box-shadow:
      0 0 0 1px rgba(255,255,255,0.06),
      0 50px 100px -20px rgba(0,0,0,0.8),
      0 0 80px rgba(44,173,132,0.08),
      inset 0 1px 0 rgba(255,255,255,0.1),
      inset 0 0 100px rgba(44,173,132,0.02);
    transition: transform 0.6s var(--ease-out), box-shadow 0.6s var(--ease-out);
    will-change: transform;
  }

  .metrics-card:hover {
    box-shadow:
      0 0 0 1px rgba(255,255,255,0.08),
      0 60px 120px -20px rgba(0,0,0,0.9),
      0 0 100px rgba(44,173,132,0.12),
      inset 0 1px 0 rgba(255,255,255,0.12),
      inset 0 0 120px rgba(44,173,132,0.04);
  }

  .pulse-indicator {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--green);
    margin-right: 8px;
    animation: pulse-indicator 2s ease-in-out infinite;
    box-shadow: 0 0 10px var(--green);
  }

  @keyframes pulse-indicator {
    0%, 100% {
      opacity: 1;
      transform: scale(1);
    }
    50% {
      opacity: 0.5;
      transform: scale(0.8);
    }
  }

  .mc-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 24px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
  }

  .mc-title {
    font-size: 13px;
    font-weight: 600;
    color: rgba(255,255,255,0.65);
    letter-spacing: -0.01em;
  }

  .mc-period {
    font-size: 11px;
    color: rgba(255,255,255,0.35);
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.09);
    padding: 4px 12px;
    border-radius: 980px;
    letter-spacing: -0.01em;
  }

  .chart-wrap {
    padding: 24px 24px 8px;
  }

  .chart-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
    padding: 0 4px;
  }

  .chart-labels span {
    font-size: 10px;
    color: rgba(255,255,255,0.25);
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.01em;
  }

  /* ─── Tiles ──────────────────────────────────────────────── */
  .tiles {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
  }

  .tile {
    padding: 20px 24px;
    border-top: 1px solid rgba(255,255,255,0.07);
    transition: background 0.25s var(--ease-out);
    cursor: default;
  }

  .tile:hover {
    background: rgba(255,255,255,0.03);
  }

  .tile:nth-child(odd) {
    border-right: 1px solid rgba(255,255,255,0.07);
  }

  .tile-loc {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: rgba(255,255,255,0.3);
    margin-bottom: 6px;
  }

  .tile-val {
    font-size: 26px;
    font-weight: 700;
    color: rgba(255,255,255,0.92);
    letter-spacing: -0.03em;
    margin-bottom: 8px;
    line-height: 1;
  }

  .tile-unit {
    font-size: 12px;
    font-weight: 400;
    color: rgba(255,255,255,0.3);
    margin-left: 2px;
  }

  .tile-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 9px;
    border-radius: 980px;
    letter-spacing: -0.01em;
  }

  .badge--green {
    background: rgba(44,173,132,0.12);
    border: 1px solid rgba(44,173,132,0.25);
    color: #2cad84;
  }

  .badge--amber {
    background: rgba(255,159,10,0.12);
    border: 1px solid rgba(255,159,10,0.25);
    color: #ff9f0a;
  }

  .badge--red {
    background: rgba(255,69,58,0.12);
    border: 1px solid rgba(255,69,58,0.25);
    color: #ff453a;
  }

  /* ─── Responsive ─────────────────────────────────────────── */
  @media (max-width: 1024px) {
    .platform-inner {
      grid-template-columns: 1fr;
      gap: 56px;
    }

    .p-body {
      max-width: 100%;
    }
  }

  @media (max-width: 700px) {
    .stats-wall {
      flex-direction: column;
      gap: 40px;
    }

    .stat-sep {
      width: 80px;
      height: 1px;
    }

    .stat-block {
      padding: 0 24px;
    }
  }
</style>
