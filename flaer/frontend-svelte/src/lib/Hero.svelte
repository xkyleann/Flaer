<script>
  import { onMount } from 'svelte';
  import AIInsights from './AIInsights.svelte';
  import DashboardPreview from './DashboardPreview.svelte';
  import BookingModal from './BookingModal.svelte';

  let heroVisible = false;
  let showcaseVisible = false;
  let showcaseEl;
  let mouseX = 0;
  let mouseY = 0;
  let scrollY = 0;
  let showDashboardPreview = false;
  let showBookingModal = false;

  onMount(() => {
    setTimeout(() => { heroVisible = true; }, 80);

    const obs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) { showcaseVisible = true; obs.disconnect(); }
      });
    }, { threshold: 0.15 });

    if (showcaseEl) obs.observe(showcaseEl);

    // Mouse parallax effect
    const handleMouseMove = (e) => {
      mouseX = (e.clientX / window.innerWidth - 0.5) * 20;
      mouseY = (e.clientY / window.innerHeight - 0.5) * 20;
    };

    // Scroll effect
    const handleScroll = () => {
      scrollY = window.scrollY;
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('scroll', handleScroll);

    return () => {
      obs.disconnect();
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('scroll', handleScroll);
    };
  });
</script>

<section id="hero">
  <!-- Animated gradient orbs -->
  <div class="orb orb-1" style="transform: translate({mouseX * 0.5}px, {mouseY * 0.5}px)" aria-hidden="true"></div>
  <div class="orb orb-2" style="transform: translate({mouseX * -0.3}px, {mouseY * 0.3}px)" aria-hidden="true"></div>
  <div class="orb orb-3" style="transform: translate({mouseX * 0.4}px, {mouseY * -0.4}px)" aria-hidden="true"></div>

  <!-- Dot grid background -->
  <div class="dot-grid" aria-hidden="true"></div>

  <!-- Radial glow from top-center -->
  <div class="glow-top" style="transform: translateY({scrollY * 0.3}px)" aria-hidden="true"></div>

  <!-- Floating particles -->
  <div class="particles" aria-hidden="true">
    {#each Array(20) as _, i}
      <div class="particle" style="
        left: {Math.random() * 100}%;
        top: {Math.random() * 100}%;
        animation-delay: {Math.random() * 5}s;
        animation-duration: {15 + Math.random() * 10}s;
      "></div>
    {/each}
  </div>

  <!-- Content -->
  <div class="hero-inner w" style="transform: translateY({scrollY * 0.15}px)">
    <!-- Product positioning -->
    <div class="eyebrow-badge" class:visible={heroVisible}>
      <span class="badge-dot" aria-hidden="true"></span>
      <span>Flaer &middot; data center carbon intelligence</span>
    </div>

    <!-- Headline -->
    <h1 class:visible={heroVisible}>
      <span class="word word-1">Clearer carbon</span><br />
      <span class="word word-2">decisions for your</span><br />
      <span class="word word-3">data center</span>
      <span class="grad-text-enhanced">portfolio.</span>
    </h1>

    <!-- Sub-copy -->
    <p class="sub" class:visible={heroVisible}>
      Measure operational emissions, compare facilities, and organise reporting evidence<br class="br-desktop" />
      in one practical workspace for infrastructure teams.
    </p>

    <!-- CTAs -->
    <div class="ctas" class:visible={heroVisible}>
      <button
        class="btn-primary"
        on:click={() => showBookingModal = true}
      >
        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" style="margin-right: 6px;">
          <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.5" fill="none"/>
          <path d="M6 5l5 3-5 3V5z"/>
        </svg>
        Book a consultation
      </button>
      <button
        class="btn-ghost"
        on:click={() => document.getElementById('capabilities')?.scrollIntoView({ behavior: 'smooth' })}
      >
        Explore capabilities <span class="arrow" aria-hidden="true">&rarr;</span>
      </button>
    </div>

    <!-- Product showcase -->
    <div class="showcase" bind:this={showcaseEl} class:visible={showcaseVisible} aria-label="Flaer dashboard preview">

      <!-- Product Workspace Badge -->
      <div class="demo-badge">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
          <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.5"/>
          <path d="M6 5l5 3-5 3V5z" fill="currentColor"/>
        </svg>
        <span>Illustrative product workspace</span>
      </div>

      <!-- Portfolio Overview Container -->
      <div class="portfolio-wrapper">
      <div class="portfolio-container">
        
        <!-- Left Column: AI Insights -->
        <div class="portfolio-left">
          <AIInsights />
        </div>

        <!-- Center Column: Main Dashboard Card -->
        <div class="portfolio-center">
          <div
            class="main-card glass-animate clickable-card"
            on:click={() => showDashboardPreview = true}
            role="button"
            tabindex="0"
            on:keypress={(e) => e.key === 'Enter' && (showDashboardPreview = true)}
          >
            <div class="click-hint">Open workspace preview</div>
            
            <!-- Card Header -->
            <div class="main-card-header">
              <div class="mc-title-row">
                <span class="live-pip" aria-hidden="true"></span>
                <span class="mc-label">Portfolio overview <span class="sample-label">Sample data</span></span>
              </div>
              <div class="mc-meta">
                <span class="mc-badge mc-badge--mode hover-lift">Operational view</span>
                <span class="mc-badge hover-lift">Reporting period</span>
                <span class="mc-badge hover-lift">
                  <svg width="12" height="12" viewBox="0 0 12 12" fill="none" style="margin-right: 4px;">
                    <rect x="1" y="1" width="10" height="10" rx="2" stroke="currentColor" stroke-width="1.5" fill="none"/>
                    <circle cx="6" cy="6" r="2" fill="currentColor"/>
                  </svg>
                  14 facilities
                </span>
                <span class="mc-badge hover-lift">Updated today</span>
              </div>
            </div>

        <!-- Premium SVG world map -->
        <div class="map-wrap">
          <svg viewBox="0 0 800 360" width="100%" class="world-map" aria-hidden="true">
            <defs>
              <!-- Enhanced gradients with Flaer colors -->
              <radialGradient id="map-glow-g" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#2cad84" stop-opacity="0.4"/>
                <stop offset="100%" stop-color="#2cad84" stop-opacity="0"/>
              </radialGradient>
              <radialGradient id="map-glow-r" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#d35d5c" stop-opacity="0.4"/>
                <stop offset="100%" stop-color="#d35d5c" stop-opacity="0"/>
              </radialGradient>
              <radialGradient id="map-glow-a" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#b67e3d" stop-opacity="0.4"/>
                <stop offset="100%" stop-color="#b67e3d" stop-opacity="0"/>
              </radialGradient>
              
              <!-- Map background gradient -->
              <linearGradient id="map-bg" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="rgba(44,173,132,0.03)"/>
                <stop offset="100%" stop-color="rgba(16,32,27,0.05)"/>
              </linearGradient>
              
              <!-- Animated connection line gradient -->
              <linearGradient id="connection-grad">
                <stop offset="0%" stop-color="#2cad84" stop-opacity="0"/>
                <stop offset="50%" stop-color="#2cad84" stop-opacity="0.6"/>
                <stop offset="100%" stop-color="#2cad84" stop-opacity="0"/>
              </linearGradient>
            </defs>

            <!-- Map background -->
            <rect width="800" height="360" fill="url(#map-bg)" rx="16"/>

            <!-- Enhanced continent outlines with premium styling -->
            <!-- North America -->
            <path d="M 95,80 L 110,70 L 150,68 L 185,72 L 200,85 L 205,100 L 195,115 L 190,135 L 175,155 L 160,165 L 150,175 L 140,185 L 125,190 L 110,180 L 100,165 L 92,145 L 88,125 L 90,105 Z"
              fill="rgba(44,173,132,0.06)" stroke="rgba(44,173,132,0.2)" stroke-width="1.2" class="continent"/>
            <!-- Greenland -->
            <path d="M 190,40 L 215,35 L 228,45 L 220,60 L 205,65 L 192,55 Z"
              fill="rgba(44,173,132,0.04)" stroke="rgba(44,173,132,0.15)" stroke-width="1" class="continent"/>
            <!-- South America -->
            <path d="M 175,205 L 195,200 L 210,215 L 215,240 L 210,270 L 200,295 L 185,305 L 172,295 L 162,275 L 160,250 L 162,225 Z"
              fill="rgba(44,173,132,0.06)" stroke="rgba(44,173,132,0.2)" stroke-width="1.2" class="continent"/>
            <!-- Europe -->
            <path d="M 370,65 L 385,58 L 400,62 L 415,68 L 418,80 L 410,90 L 420,98 L 415,108 L 405,115 L 395,112 L 385,118 L 375,115 L 365,105 L 362,90 L 368,78 Z"
              fill="rgba(44,173,132,0.06)" stroke="rgba(44,173,132,0.2)" stroke-width="1.2" class="continent"/>
            <!-- Scandinavia -->
            <path d="M 390,40 L 400,35 L 410,42 L 412,55 L 405,60 L 395,58 L 388,50 Z"
              fill="rgba(44,173,132,0.05)" stroke="rgba(44,173,132,0.18)" stroke-width="1" class="continent"/>
            <!-- Africa -->
            <path d="M 370,130 L 395,125 L 415,130 L 425,150 L 420,175 L 415,200 L 400,220 L 385,230 L 368,220 L 355,200 L 350,175 L 352,150 Z"
              fill="rgba(44,173,132,0.06)" stroke="rgba(44,173,132,0.2)" stroke-width="1.2" class="continent"/>
            <!-- Middle East -->
            <path d="M 430,100 L 455,95 L 480,100 L 490,115 L 480,125 L 460,125 L 440,120 L 428,112 Z"
              fill="rgba(44,173,132,0.05)" stroke="rgba(44,173,132,0.18)" stroke-width="1" class="continent"/>
            <!-- Russia / Central Asia -->
            <path d="M 430,50 L 470,40 L 530,38 L 580,42 L 620,50 L 640,65 L 630,80 L 610,85 L 580,82 L 545,85 L 510,80 L 480,82 L 455,80 L 432,72 Z"
              fill="rgba(44,173,132,0.06)" stroke="rgba(44,173,132,0.2)" stroke-width="1.2" class="continent"/>
            <!-- India -->
            <path d="M 530,120 L 545,115 L 558,120 L 562,140 L 558,160 L 548,172 L 535,165 L 525,150 L 522,135 Z"
              fill="rgba(44,173,132,0.05)" stroke="rgba(44,173,132,0.18)" stroke-width="1" class="continent"/>
            <!-- South East Asia -->
            <path d="M 590,120 L 615,115 L 635,120 L 645,135 L 640,148 L 625,152 L 608,148 L 595,138 Z"
              fill="rgba(44,173,132,0.05)" stroke="rgba(44,173,132,0.18)" stroke-width="1" class="continent"/>
            <!-- China / East Asia -->
            <path d="M 580,60 L 625,58 L 660,65 L 680,80 L 678,100 L 665,112 L 645,115 L 620,110 L 600,105 L 578,95 L 572,80 Z"
              fill="rgba(44,173,132,0.06)" stroke="rgba(44,173,132,0.2)" stroke-width="1.2" class="continent"/>
            <!-- Japan -->
            <path d="M 690,75 L 700,70 L 710,78 L 708,90 L 698,95 L 688,88 Z"
              fill="rgba(44,173,132,0.05)" stroke="rgba(44,173,132,0.18)" stroke-width="1" class="continent"/>
            <!-- Australia -->
            <path d="M 620,220 L 655,215 L 690,220 L 710,240 L 708,265 L 690,278 L 660,280 L 632,272 L 615,255 L 612,235 Z"
              fill="rgba(44,173,132,0.06)" stroke="rgba(44,173,132,0.2)" stroke-width="1.2" class="continent"/>

            <!-- Premium grid lines -->
            <line x1="0" y1="90" x2="800" y2="90" stroke="rgba(44,173,132,0.08)" stroke-width="0.5" stroke-dasharray="6,10" class="grid-line"/>
            <line x1="0" y1="180" x2="800" y2="180" stroke="rgba(44,173,132,0.08)" stroke-width="0.5" stroke-dasharray="6,10" class="grid-line"/>
            <line x1="0" y1="270" x2="800" y2="270" stroke="rgba(44,173,132,0.08)" stroke-width="0.5" stroke-dasharray="6,10" class="grid-line"/>
            <line x1="200" y1="0" x2="200" y2="360" stroke="rgba(44,173,132,0.08)" stroke-width="0.5" stroke-dasharray="6,10" class="grid-line"/>
            <line x1="400" y1="0" x2="400" y2="360" stroke="rgba(44,173,132,0.08)" stroke-width="0.5" stroke-dasharray="6,10" class="grid-line"/>
            <line x1="600" y1="0" x2="600" y2="360" stroke="rgba(44,173,132,0.08)" stroke-width="0.5" stroke-dasharray="6,10" class="grid-line"/>

            <!-- Animated connection lines -->
            <g class="connections">
              <line x1="392" y1="85" x2="358" y2="78" stroke="url(#connection-grad)" stroke-width="1.5" class="connection-line" style="--delay: 0s"/>
              <line x1="392" y1="85" x2="400" y2="52" stroke="url(#connection-grad)" stroke-width="1.5" class="connection-line" style="--delay: 0.5s"/>
              <line x1="392" y1="85" x2="418" y2="75" stroke="url(#connection-grad)" stroke-width="1.5" class="connection-line" style="--delay: 1s"/>
              <line x1="168" y1="108" x2="392" y2="85" stroke="url(#connection-grad)" stroke-width="1.2" class="connection-line" style="--delay: 1.5s"/>
              <line x1="694" y1="92" x2="392" y2="85" stroke="url(#connection-grad)" stroke-width="1.2" class="connection-line" style="--delay: 2s"/>
              <line x1="624" y1="188" x2="694" y2="92" stroke="url(#connection-grad)" stroke-width="1.2" class="connection-line" style="--delay: 2.5s"/>
            </g>

            <!-- Enhanced data center points with Flaer colors -->
            <!-- Frankfurt (amber) -->
            <g class="data-center">
              <circle cx="392" cy="85" r="20" fill="url(#map-glow-a)" class="dc-glow-outer"/>
              <circle cx="392" cy="85" r="8" fill="rgba(182,126,61,0.3)" stroke="#b67e3d" stroke-width="2" class="dc-ring"/>
              <circle cx="392" cy="85" r="4" fill="#b67e3d" class="dc-core"/>
            </g>

            <!-- Dublin (green) -->
            <g class="data-center">
              <circle cx="358" cy="78" r="20" fill="url(#map-glow-g)" class="dc-glow-outer"/>
              <circle cx="358" cy="78" r="8" fill="rgba(44,173,132,0.3)" stroke="#2cad84" stroke-width="2" class="dc-ring"/>
              <circle cx="358" cy="78" r="4" fill="#2cad84" class="dc-core"/>
            </g>

            <!-- Stockholm (green) -->
            <g class="data-center">
              <circle cx="400" cy="52" r="20" fill="url(#map-glow-g)" class="dc-glow-outer"/>
              <circle cx="400" cy="52" r="8" fill="rgba(44,173,132,0.3)" stroke="#2cad84" stroke-width="2" class="dc-ring"/>
              <circle cx="400" cy="52" r="4" fill="#2cad84" class="dc-core"/>
            </g>

            <!-- Warsaw (red) -->
            <g class="data-center">
              <circle cx="418" cy="75" r="20" fill="url(#map-glow-r)" class="dc-glow-outer"/>
              <circle cx="418" cy="75" r="8" fill="rgba(211,93,92,0.3)" stroke="#d35d5c" stroke-width="2" class="dc-ring"/>
              <circle cx="418" cy="75" r="4" fill="#d35d5c" class="dc-core"/>
            </g>

            <!-- Virginia, US (amber) -->
            <g class="data-center">
              <circle cx="168" cy="108" r="20" fill="url(#map-glow-a)" class="dc-glow-outer"/>
              <circle cx="168" cy="108" r="8" fill="rgba(182,126,61,0.3)" stroke="#b67e3d" stroke-width="2" class="dc-ring"/>
              <circle cx="168" cy="108" r="4" fill="#b67e3d" class="dc-core"/>
            </g>

            <!-- Oregon, US (green) -->
            <g class="data-center">
              <circle cx="108" cy="100" r="20" fill="url(#map-glow-g)" class="dc-glow-outer"/>
              <circle cx="108" cy="100" r="8" fill="rgba(44,173,132,0.3)" stroke="#2cad84" stroke-width="2" class="dc-ring"/>
              <circle cx="108" cy="100" r="4" fill="#2cad84" class="dc-core"/>
            </g>

            <!-- Singapore (red) -->
            <g class="data-center">
              <circle cx="624" cy="188" r="20" fill="url(#map-glow-r)" class="dc-glow-outer"/>
              <circle cx="624" cy="188" r="8" fill="rgba(211,93,92,0.3)" stroke="#d35d5c" stroke-width="2" class="dc-ring"/>
              <circle cx="624" cy="188" r="4" fill="#d35d5c" class="dc-core"/>
            </g>

            <!-- Tokyo (amber) -->
            <g class="data-center">
              <circle cx="694" cy="92" r="20" fill="url(#map-glow-a)" class="dc-glow-outer"/>
              <circle cx="694" cy="92" r="8" fill="rgba(182,126,61,0.3)" stroke="#b67e3d" stroke-width="2" class="dc-ring"/>
              <circle cx="694" cy="92" r="4" fill="#b67e3d" class="dc-core"/>
            </g>
          </svg>
        </div>

            <!-- Card Footer Stats -->
            <div class="mc-footer">
              <div class="mc-stat">
                <span class="mc-stat-label">Avg. Intensity</span>
                <span class="mc-stat-val">318 <span class="mc-unit">gCO₂/kWh</span></span>
              </div>
              <div class="mc-divider" aria-hidden="true"></div>
              <div class="mc-stat">
                <span class="mc-stat-label">High Risk</span>
                <span class="mc-stat-val c-red">3 sites</span>
              </div>
              <div class="mc-divider" aria-hidden="true"></div>
              <div class="mc-stat">
                <span class="mc-stat-label">Monthly footprint</span>
                <span class="mc-stat-val">1.24M <span class="mc-unit">tCO₂</span></span>
              </div>
              <div class="mc-divider" aria-hidden="true"></div>
              <div class="mc-stat">
                <span class="mc-stat-label">Evidence complete</span>
                <span class="mc-stat-val c-green">83%</span>
              </div>
            </div>

            <div class="business-panel">
              <div class="facility-table">
                <div class="panel-head">
                  <span>Facilities to review</span>
                  <strong>3 items</strong>
                </div>
                <div class="facility-row">
                  <span>N. Virginia</span>
                  <strong>412 gCO₂/kWh</strong>
                  <em>Cooling action</em>
                </div>
                <div class="facility-row">
                  <span>Singapore</span>
                  <strong>408 gCO₂/kWh</strong>
                  <em>Procurement risk</em>
                </div>
                <div class="facility-row">
                  <span>Stockholm</span>
                  <strong class="c-green">13 gCO₂/kWh</strong>
                  <em>Best performer</em>
                </div>
              </div>

              <div class="action-queue">
                <div class="panel-head">
                  <span>Suggested next steps</span>
                  <strong>Estimates shown</strong>
                </div>
                <div class="action-line">
                  <span>Shift flexible workloads to Stockholm</span>
                  <strong>-18%</strong>
                </div>
                <div class="action-line">
                  <span>Optimize N. Virginia cooling controls</span>
                  <strong>€610K</strong>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column: Floating Metric Cards -->
        <div class="portfolio-right">
          
          <!-- Metric Card 1: Portfolio Emissions -->
          <div
            class="metric-card metric-card--1 glass-animate interactive-card"
            on:click={() => showDashboardPreview = true}
            on:keypress={(e) => e.key === 'Enter' && (showDashboardPreview = true)}
            role="button"
            tabindex="0"
            aria-label="View portfolio emissions details"
          >
            <div class="card-glow"></div>
            <div class="metric-header">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" class="metric-icon" aria-hidden="true">
                <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.5" fill="none"/>
                <path d="M10 6v4l3 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              <span class="metric-label">Reporting status</span>
            </div>
            <div class="metric-value counter-animate">8/12</div>
            <div class="metric-unit">evidence sets validated</div>
            <div class="metric-trend c-green">
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
                <path d="M2 9L6 5L9 7L12 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>4 items need an owner</span>
            </div>
          </div>

          <!-- Metric Card 2: Weekly Carbon Trend -->
          <div
            class="metric-card metric-card--2 glass-animate interactive-card"
            on:click={() => showDashboardPreview = true}
            on:keypress={(e) => e.key === 'Enter' && (showDashboardPreview = true)}
            role="button"
            tabindex="0"
            aria-label="View weekly carbon trend analytics"
          >
            <div class="card-glow"></div>
            <div class="metric-header">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" class="metric-icon" aria-hidden="true">
                <rect x="3" y="3" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5" fill="none"/>
                <path d="M7 13V10M10 13V7M13 13V9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              <span class="metric-label">Operational coverage</span>
            </div>
            <div class="metric-bars" aria-hidden="true">
              <div class="metric-bar bar-animate" style="--h: 55%; --c: rgba(44,173,132,0.7); --delay: 0s"></div>
              <div class="metric-bar bar-animate" style="--h: 70%; --c: rgba(44,173,132,0.7); --delay: 0.1s"></div>
              <div class="metric-bar bar-animate" style="--h: 48%; --c: rgba(44,173,132,0.7); --delay: 0.2s"></div>
              <div class="metric-bar bar-animate" style="--h: 82%; --c: rgba(182,126,61,0.7); --delay: 0.3s"></div>
              <div class="metric-bar bar-animate" style="--h: 63%; --c: rgba(44,173,132,0.7); --delay: 0.4s"></div>
              <div class="metric-bar bar-animate" style="--h: 40%; --c: rgba(44,173,132,0.7); --delay: 0.5s"></div>
              <div class="metric-bar bar-animate" style="--h: 35%; --c: rgba(44,173,132,0.9); --delay: 0.6s"></div>
            </div>
            <div class="metric-sub">PUE, WUE, CUE and energy mix by site</div>
          </div>

          <!-- Metric Card 3: 2035 Trajectory -->
          <div
            class="metric-card metric-card--3 glass-animate interactive-card"
            on:click={() => showDashboardPreview = true}
            on:keypress={(e) => e.key === 'Enter' && (showDashboardPreview = true)}
            role="button"
            tabindex="0"
            aria-label="View 2035 emissions trajectory forecast"
          >
            <div class="card-glow"></div>
            <div class="metric-header">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" class="metric-icon" aria-hidden="true">
                <path d="M3 10h14M10 3l7 7-7 7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span class="metric-label">Site assessment</span>
            </div>
            <div class="metric-value c-green counter-animate">3</div>
            <div class="metric-unit">candidate regions compared</div>
            <div class="metric-badge pulse-badge">
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none" style="margin-right: 4px;" aria-hidden="true">
                <path d="M10 3L4.5 8.5L2 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              Review Singapore grid exposure
            </div>
          </div>

        </div>
      </div>
      </div><!-- /portfolio-wrapper -->
    </div>
  </div>

  <!-- Interactive Dashboard Preview Modal -->
  <DashboardPreview bind:isOpen={showDashboardPreview} />
  <BookingModal open={showBookingModal} onClose={() => showBookingModal = false} />
</section>

<style>
  section {
    min-height: 680px;
    background: linear-gradient(180deg, #0b1714 0%, #07110f 100%);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    padding-bottom: 0;
  }

  /* ── Animated gradient orbs ──────────────────────────────── */
  .orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(120px);
    opacity: 0.4;
    pointer-events: none;
    transition: transform 0.3s ease-out;
    animation: orb-float 20s ease-in-out infinite;
    will-change: transform;
  }

  .orb-1 {
    width: 700px;
    height: 700px;
    background: radial-gradient(circle, rgba(44,173,132,0.28), transparent 65%);
    top: -260px;
    left: 5%;
    animation-delay: 0s;
  }

  .orb-2 {
    width: 520px;
    height: 520px;
    background: radial-gradient(circle, rgba(127,174,255,0.2), transparent 65%);
    top: 15%;
    right: 3%;
    animation-delay: 7s;
  }

  .orb-3 {
    width: 480px;
    height: 480px;
    background: radial-gradient(circle, rgba(183,149,99,0.18), transparent 65%);
    bottom: 8%;
    left: 45%;
    animation-delay: 14s;
  }

  @keyframes orb-float {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33%       { transform: translate(40px, -40px) scale(1.08); }
    66%       { transform: translate(-25px, 25px) scale(0.93); }
  }

  /* ── Floating particles ──────────────────────────────────── */
  .particles {
    position: absolute;
    inset: 0;
    pointer-events: none;
    overflow: hidden;
  }

  .particle {
    position: absolute;
    width: 3px;
    height: 3px;
    background: rgba(44,173,132,0.6);
    border-radius: 50%;
    animation: particle-float linear infinite;
    box-shadow: 0 0 10px rgba(44,173,132,0.8);
  }

  @keyframes particle-float {
    0% {
      transform: translateY(0) translateX(0);
      opacity: 0;
    }
    10% {
      opacity: 1;
    }
    90% {
      opacity: 1;
    }
    100% {
      transform: translateY(-100vh) translateX(50px);
      opacity: 0;
    }
  }

  /* ── Dot grid background ─────────────────────────────────── */
  .dot-grid {
    position: absolute;
    inset: 0;
    background-image: radial-gradient(circle, rgba(255,255,255,0.09) 1px, transparent 1px);
    background-size: 28px 28px;
    mask-image: radial-gradient(ellipse 80% 60% at 50% 50%, black 30%, transparent 80%);
    -webkit-mask-image: radial-gradient(ellipse 80% 60% at 50% 50%, black 30%, transparent 80%);
    pointer-events: none;
    z-index: 0;
  }

  /* ── Top radial glow ─────────────────────────────────────── */
  .glow-top {
    position: absolute;
    top: -120px;
    left: 50%;
    transform: translateX(-50%);
    width: 900px;
    height: 600px;
    background:
      radial-gradient(ellipse 60% 50% at 50% 0%, rgba(44,173,132,0.12), transparent 70%),
      radial-gradient(ellipse 80% 60% at 50% 0%, rgba(127,174,255,0.07), transparent 80%);
    pointer-events: none;
    z-index: 0;
    will-change: transform;
  }

  /* ── Layout ──────────────────────────────────────────────── */
  .hero-inner {
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding-top: 140px;
  }

  /* ── Eyebrow badge ───────────────────────────────────────── */
  .eyebrow-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 16px 6px 10px;
    border-radius: 980px;
    border: 1px solid rgba(44,173,132,0.3);
    background: rgba(44,173,132,0.08);
    font-size: 12px;
    font-weight: 500;
    letter-spacing: -0.01em;
    color: rgba(255,255,255,0.7);
    margin-bottom: 40px;
    opacity: 0;
    transform: translateY(16px);
    transition: opacity 0.7s var(--ease-out), transform 0.7s var(--ease-out);
  }

  .eyebrow-badge.visible {
    opacity: 1;
    transform: translateY(0);
  }

  .badge-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--green);
    animation: pulse-dot 2.5s ease-in-out infinite;
    flex-shrink: 0;
  }

  /* ── Headline with staggered animation ───────────────────── */
  h1 {
    font-size: clamp(42px, 6vw, 72px);
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.03em;
    color: #f5f5f7;
    margin-bottom: 32px;
    max-width: 16ch;
  }

  .word {
    display: inline-block;
    opacity: 0;
    transform: translateY(40px) rotateX(20deg);
    transition: opacity 1s var(--ease-out), transform 1s var(--ease-out);
  }

  h1.visible .word-1 {
    opacity: 1;
    transform: translateY(0) rotateX(0);
    transition-delay: 0.1s;
  }

  h1.visible .word-2 {
    opacity: 1;
    transform: translateY(0) rotateX(0);
    transition-delay: 0.2s;
  }

  h1.visible .word-3 {
    opacity: 1;
    transform: translateY(0) rotateX(0);
    transition-delay: 0.3s;
  }

  h1.visible .word-4 {
    opacity: 1;
    transform: translateY(0) rotateX(0);
    transition-delay: 0.4s;
  }

  .grad-text-enhanced {
    display: inline-block;
    background: linear-gradient(135deg, #2cad84 0%, #7faeff 55%, #b79563 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradient-shift 8s ease infinite;
    opacity: 0;
    transform: translateY(40px) scale(0.9);
    transition: opacity 1s var(--ease-out) 0.5s, transform 1s var(--ease-out) 0.5s;
    filter: drop-shadow(0 0 30px rgba(44,173,132,0.5));
  }

  h1.visible .grad-text-enhanced {
    opacity: 1;
    transform: translateY(0) scale(1);
  }

  @keyframes gradient-shift {
    0%, 100% {
      background-position: 0% 50%;
    }
    50% {
      background-position: 100% 50%;
    }
  }

  /* ── Sub-copy ────────────────────────────────────────────── */
  .sub {
    font-size: 21px;
    line-height: 1.48;
    letter-spacing: -0.022em;
    color: rgba(255,255,255,0.56);
    max-width: 580px;
    margin-bottom: 44px;
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.9s var(--ease-out) 0.24s, transform 0.9s var(--ease-out) 0.24s;
  }

  .sub.visible {
    opacity: 1;
    transform: translateY(0);
  }

  .br-desktop { display: block; }

  /* ── CTAs ────────────────────────────────────────────────── */
  .ctas {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 72px;
    flex-wrap: wrap;
    justify-content: center;
    opacity: 0;
    transform: translateY(16px);
    transition: opacity 0.9s var(--ease-out) 0.36s, transform 0.9s var(--ease-out) 0.36s;
  }

  .ctas.visible {
    opacity: 1;
    transform: translateY(0);
  }

  .arrow { display: inline-block; margin-left: 2px; }

  /* ── Separator ───────────────────────────────────────────── */
  .separator {
    width: min(calc(100% - 48px), var(--max));
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.12) 30%, rgba(255,255,255,0.12) 70%, transparent 100%);
    margin-bottom: 80px;
    flex-shrink: 0;
  }

  /* ── Showcase ────────────────────────────────────────────── */
  .showcase {
    display: none;
    position: relative;
    width: 100%;
    min-height: 660px;
    padding-bottom: 80px;
    opacity: 0;
    transform: translateY(48px);
    transition: opacity 1s var(--ease-out), transform 1s var(--ease-out);
    max-width: 1600px;
    margin: 0 auto;
  }

  .showcase::before {
    content: '';
    position: absolute;
    top: 20%;
    left: 50%;
    transform: translateX(-50%);
    width: 80%;
    height: 60%;
    background: radial-gradient(ellipse, rgba(44,173,132,0.07) 0%, transparent 65%);
    pointer-events: none;
    z-index: 0;
    filter: blur(40px);
  }

  .showcase.visible {
    opacity: 1;
    transform: translateY(0);
  }

  /* ── Demo Badge ──────────────────────────────────────────── */
  .demo-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 18px;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.14);
    color: rgba(255,255,255,0.65);
    font-size: 12.5px;
    font-weight: 600;
    letter-spacing: -0.01em;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    margin: 0 auto 32px;
    width: fit-content;
    z-index: 3;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.12);
  }

  .demo-badge svg {
    color: rgba(44,173,132,0.8);
  }

  /* ── Portfolio Wrapper ───────────────────────────────────── */
  .portfolio-wrapper {
    position: relative;
    border-radius: 32px;
    padding: 16px;
    background: rgba(255,255,255,0.018);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow:
      inset 0 1px 0 rgba(255,255,255,0.07),
      0 40px 80px -20px rgba(0,0,0,0.45),
      0 0 120px rgba(44,173,132,0.04);
  }

  .portfolio-wrapper::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: radial-gradient(ellipse 60% 40% at 50% 0%, rgba(44,173,132,0.06), transparent 70%);
    pointer-events: none;
  }

  /* ── Portfolio Container ─────────────────────────────────── */
  .portfolio-container {
    display: grid;
    grid-template-columns: 340px 1fr 250px;
    gap: 16px;
    align-items: stretch;
  }

  /* ── Portfolio Left (AI Insights) ────────────────────────── */
  .portfolio-left {
    animation: slideInLeft 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.2s backwards;
    display: flex;
    flex-direction: column;
  }

  @keyframes slideInLeft {
    from {
      opacity: 0;
      transform: translateX(-40px);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }

  /* ── Portfolio Center (Main Dashboard) ───────────────────── */
  .portfolio-center {
    animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.3s backwards;
  }

  /* ── Main Dashboard Card ─────────────────────────────────── */
  .main-card {
    position: relative;
    background: linear-gradient(135deg,
      rgba(255,255,255,0.05) 0%,
      rgba(255,255,255,0.02) 50%,
      rgba(44,173,132,0.03) 100%
    );
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 32px;
    overflow: visible;
    backdrop-filter: blur(80px) saturate(200%);
    -webkit-backdrop-filter: blur(80px) saturate(200%);
    box-shadow:
      inset 0 1px 0 rgba(255,255,255,0.18),
      inset 0 0 0 0.5px rgba(255,255,255,0.08),
      0 4px 8px rgba(0,0,0,0.1),
      0 16px 40px -8px rgba(0,0,0,0.5),
      0 48px 96px -20px rgba(0,0,0,0.6),
      0 0 0 1px rgba(0,0,0,0.35),
      0 0 120px rgba(44,173,132,0.08);
    transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    animation: cardFloat 8s ease-in-out infinite;
    z-index: 1;
  }

  @keyframes cardFloat {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
  }

  .main-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(170deg,
      rgba(255,255,255,0.08) 0%,
      rgba(255,255,255,0.02) 40%,
      rgba(44,173,132,0.04) 100%
    );
    pointer-events: none;
    z-index: 0;
    animation: shimmer 3s ease-in-out infinite;
  }

  @keyframes shimmer {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
  }

  .main-card::after {
    content: '';
    position: absolute;
    inset: -2px;
    background: linear-gradient(45deg,
      transparent 0%,
      rgba(44,173,132,0.1) 50%,
      transparent 100%
    );
    border-radius: 32px;
    opacity: 0;
    transition: opacity 0.6s ease;
    pointer-events: none;
    z-index: -1;
  }

  .clickable-card {
    cursor: pointer;
    animation: cardFloat 8s ease-in-out infinite;
  }

  .clickable-card:hover {
    transform: translateY(-12px) scale(1.01);
    border-color: rgba(44,173,132,0.3);
    box-shadow:
      inset 0 1px 0 rgba(255,255,255,0.22),
      inset 0 0 0 0.5px rgba(255,255,255,0.12),
      0 4px 8px rgba(0,0,0,0.12),
      0 20px 48px -8px rgba(0,0,0,0.55),
      0 56px 112px -20px rgba(0,0,0,0.65),
      0 0 0 1px rgba(44,173,132,0.2),
      0 0 160px rgba(44,173,132,0.15);
    animation: none;
  }

  .clickable-card:hover::after {
    opacity: 1;
  }

  .clickable-card:active {
    transform: translateY(-8px) scale(0.99);
  }

  .click-hint {
    position: absolute;
    top: 14px;
    right: 14px;
    padding: 5px 12px;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.16);
    font-size: 10.5px;
    font-weight: 600;
    color: rgba(255,255,255,0.7);
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
    z-index: 100;
    backdrop-filter: blur(20px);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.16);
    letter-spacing: -0.01em;
  }

  .clickable-card:hover .click-hint {
    opacity: 1;
  }

  .main-card-header {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 28px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    background: linear-gradient(180deg,
      rgba(255,255,255,0.04) 0%,
      rgba(255,255,255,0.01) 100%
    );
    backdrop-filter: blur(20px);
  }

  .mc-title-row {
    display: flex;
    align-items: center;
    gap: 11px;
  }

  .live-pip {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--green);
    box-shadow:
      0 0 12px rgba(44,173,132,0.9),
      0 0 24px rgba(44,173,132,0.5);
    animation: pulse-dot 2s ease-in-out infinite;
    flex-shrink: 0;
  }

  @keyframes pulse-dot {
    0%, 100% {
      transform: scale(1);
      opacity: 1;
    }
    50% {
      transform: scale(1.2);
      opacity: 0.8;
    }
  }

  .mc-label {
    font-size: 14px;
    font-weight: 600;
    color: rgba(255,255,255,0.85);
    letter-spacing: -0.03em;
    text-transform: capitalize;
  }

  .sample-label {
    display: inline-block;
    margin-left: 7px;
    color: rgba(244,247,245,0.42);
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.02em;
    text-transform: uppercase;
  }

  .mc-meta {
    display: flex;
    gap: 8px;
  }

  .mc-badge {
    font-size: 11.5px;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.14);
    color: rgba(255,255,255,0.65);
    letter-spacing: -0.02em;
    box-shadow:
      inset 0 1px 0 rgba(255,255,255,0.14),
      0 2px 8px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
  }

  .mc-badge:hover {
    background: rgba(255,255,255,0.12);
    border-color: rgba(255,255,255,0.2);
    transform: translateY(-1px);
  }

  .mc-badge--live {
    background: rgba(44,173,132,0.15);
    border-color: rgba(44,173,132,0.35);
    color: #2cad84;
    box-shadow:
      inset 0 1px 0 rgba(44,173,132,0.2),
      0 2px 12px rgba(44,173,132,0.2);
    animation: badgePulse 3s ease-in-out infinite;
  }

  @keyframes badgePulse {
    0%, 100% { box-shadow: inset 0 1px 0 rgba(44,173,132,0.2), 0 2px 12px rgba(44,173,132,0.2); }
    50% { box-shadow: inset 0 1px 0 rgba(44,173,132,0.3), 0 4px 20px rgba(44,173,132,0.4); }
  }

  .mc-badge--live:hover {
    background: rgba(44,173,132,0.2);
    border-color: rgba(44,173,132,0.45);
  }

  .mc-badge--mode {
    background: rgba(127,174,255,0.12);
    border-color: rgba(127,174,255,0.28);
    color: rgba(214,229,255,0.9);
  }

  .map-wrap {
    position: relative;
    z-index: 1;
    padding: 16px 24px 10px;
  }

  .world-map {
    display: block;
  }

  .dc-glow {
    animation: dc-pulse 3s ease-in-out infinite;
  }

  @keyframes dc-pulse {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
  }

  .mc-footer {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    padding: 20px 28px;
    border-top: 1px solid rgba(255,255,255,0.1);
    background: linear-gradient(180deg,
      rgba(0,0,0,0.15) 0%,
      rgba(0,0,0,0.2) 100%
    );
    gap: 0;
    backdrop-filter: blur(20px);
  }

  .mc-stat {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 5px;
    transition: transform 0.3s ease;
  }

  .mc-stat:hover {
    transform: translateY(-2px);
  }

  .mc-stat-label {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: rgba(255,255,255,0.4);
  }

  .mc-stat-val {
    font-size: 19px;
    font-weight: 700;
    color: rgba(255,255,255,0.95);
    letter-spacing: -0.04em;
    text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    animation: fadeInUp 0.6s ease-out backwards;
  }

  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .mc-stat:nth-child(1) .mc-stat-val { animation-delay: 0.1s; }
  .mc-stat:nth-child(3) .mc-stat-val { animation-delay: 0.2s; }

  .business-panel {
    position: relative;
    z-index: 1;
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    gap: 14px;
    padding: 0 28px 24px;
    background: linear-gradient(180deg, rgba(0,0,0,0.2), rgba(0,0,0,0.08));
  }

  .facility-table,
  .action-queue {
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.035);
    border-radius: 16px;
    overflow: hidden;
  }

  .panel-head,
  .facility-row,
  .action-line {
    display: grid;
    align-items: center;
    gap: 12px;
    padding: 12px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.065);
    text-align: left;
  }

  .panel-head {
    grid-template-columns: 1fr auto;
    background: rgba(255,255,255,0.035);
    color: rgba(244,247,245,0.56);
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  .panel-head strong {
    color: #d2e8dd;
    font-size: 10.5px;
  }

  .facility-row {
    grid-template-columns: 1fr auto minmax(118px, 0.8fr);
    color: rgba(244,247,245,0.78);
    font-size: 12px;
  }

  .facility-row strong,
  .action-line strong {
    color: #f4f7f5;
    font-size: 12px;
  }

  .facility-row em {
    justify-self: end;
    color: rgba(244,247,245,0.46);
    font-style: normal;
    font-size: 11px;
  }

  .action-line {
    grid-template-columns: 1fr auto;
    color: rgba(244,247,245,0.72);
    font-size: 12px;
    line-height: 1.35;
  }

  .facility-row:last-child,
  .action-line:last-child {
    border-bottom: none;
  }
  .mc-stat:nth-child(5) .mc-stat-val { animation-delay: 0.3s; }
  .mc-stat:nth-child(7) .mc-stat-val { animation-delay: 0.4s; }

  .mc-unit {
    font-size: 11.5px;
    font-weight: 500;
    color: rgba(255,255,255,0.45);
    margin-left: 3px;
  }

  .mc-divider {
    width: 1px;
    height: 36px;
    background: linear-gradient(180deg,
      transparent 0%,
      rgba(255,255,255,0.12) 50%,
      transparent 100%
    );
    margin: 0 24px;
    flex-shrink: 0;
  }

  .c-green { color: var(--green); }
  .c-red { color: var(--red); }

  /* ── Portfolio Right (Metric Cards) ──────────────────────── */
  .portfolio-right {
    display: flex;
    flex-direction: column;
    gap: 12px;
    animation: slideInRight 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.4s backwards;
  }

  @keyframes slideInRight {
    from { opacity: 0; transform: translateX(32px); }
    to   { opacity: 1; transform: translateX(0); }
  }

  /* ── Metric Cards ────────────────────────────────────────── */
  .metric-card {
    position: relative;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 22px;
    padding: 18px 20px;
    backdrop-filter: blur(60px) saturate(180%);
    -webkit-backdrop-filter: blur(60px) saturate(180%);
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    overflow: hidden;
    box-shadow:
      inset 0 1px 0 rgba(255,255,255,0.12),
      0 4px 16px rgba(0,0,0,0.18),
      0 12px 32px -8px rgba(0,0,0,0.4);
  }

  .metric-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: linear-gradient(160deg,
      rgba(255,255,255,0.06) 0%,
      transparent 60%
    );
    pointer-events: none;
  }

  .metric-card:hover {
    transform: translateY(-4px);
    border-color: rgba(44,173,132,0.25);
    box-shadow:
      inset 0 1px 0 rgba(255,255,255,0.16),
      0 8px 24px rgba(0,0,0,0.22),
      0 20px 48px -8px rgba(0,0,0,0.42),
      0 0 60px rgba(44,173,132,0.08);
  }

  .metric-card--1 { animation-delay: 0.5s; }
  .metric-card--2 { animation-delay: 0.62s; }
  .metric-card--3 { animation-delay: 0.74s; }

  /* ── Metric Card Elements ────────────────────────────────── */
  .metric-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
  }

  .metric-icon {
    color: rgba(44,173,132,0.6);
    flex-shrink: 0;
  }

  .metric-label {
    font-size: 9.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: rgba(244,247,245,0.4);
  }

  .metric-value {
    font-size: 40px;
    font-weight: 900;
    letter-spacing: -0.05em;
    color: #f4f7f5;
    line-height: 1;
    margin-bottom: 4px;
  }

  .metric-unit {
    font-size: 11.5px;
    color: rgba(244,247,245,0.45);
    margin-bottom: 10px;
    letter-spacing: -0.01em;
  }

  .metric-trend {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: -0.01em;
  }

  .metric-trend svg { flex-shrink: 0; }

  .metric-bars {
    display: flex;
    align-items: flex-end;
    gap: 4px;
    height: 44px;
    margin: 10px 0 6px;
  }

  .metric-bar {
    flex: 1;
    height: var(--h);
    background: var(--c);
    border-radius: 3px 3px 0 0;
    min-height: 4px;
  }

  .metric-sub {
    font-size: 10px;
    color: rgba(244,247,245,0.3);
    letter-spacing: -0.01em;
  }

  .metric-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 5px 11px;
    border-radius: 999px;
    background: rgba(44,173,132,0.1);
    border: 1px solid rgba(44,173,132,0.22);
    font-size: 10.5px;
    font-weight: 600;
    color: #2cad84;
    letter-spacing: -0.01em;
    margin-top: 8px;
    box-shadow: inset 0 1px 0 rgba(44,173,132,0.15);
  }

  @keyframes float-card-anim {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
  }

  .float-card--1:hover,
  .float-card--2:hover,
  .float-card--3:hover {
    animation-play-state: paused;
  }

  /* ── Interactive card enhancements ──────────────────────── */
  .glass-animate {
    animation: glass-fade-in 0.7s cubic-bezier(0.16, 1, 0.3, 1) both;
  }

  @keyframes glass-fade-in {
    from { opacity: 0; transform: translateY(16px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
  }

  .interactive-card {
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }

  .card-glow {
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: radial-gradient(circle at 50% 0%, rgba(255,255,255,0.1), transparent 55%);
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
  }

  .interactive-card:hover .card-glow {
    opacity: 1;
  }

  .card-tooltip {
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%) translateY(4px);
    white-space: nowrap;
    font-size: 10px;
    font-weight: 600;
    color: rgba(255,255,255,0.6);
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.14);
    padding: 4px 10px;
    border-radius: 999px;
    opacity: 0;
    transition: opacity 0.25s ease, transform 0.25s ease;
    pointer-events: none;
    backdrop-filter: blur(20px);
  }

  .interactive-card:hover .card-tooltip {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }

  .bar-animate {
    transform-origin: bottom;
    animation: bar-grow 0.5s var(--ease-out) both;
    animation-delay: var(--delay, 0s);
  }

  @keyframes bar-grow {
    from { transform: scaleY(0); }
    to   { transform: scaleY(1); }
  }

  .counter-animate {
    animation: counter-pop 0.6s var(--ease-out) both;
    animation-delay: 0.3s;
  }

  @keyframes counter-pop {
    from { opacity: 0; transform: scale(0.88); }
    to   { opacity: 1; transform: scale(1); }
  }

  .pulse-badge {
    animation: pulse-badge-anim 2.8s ease-in-out infinite;
  }

  @keyframes pulse-badge-anim {
    0%, 100% { box-shadow: 0 0 0 0 rgba(44,173,132,0.3); }
    50%       { box-shadow: 0 0 0 5px rgba(44,173,132,0); }
  }

  .fc-label {
    font-size: 9.5px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: rgba(255,255,255,0.38);
    margin-bottom: 8px;
  }

  .fc-big {
    font-size: 38px;
    font-weight: 700;
    letter-spacing: -0.04em;
    color: rgba(255,255,255,0.95);
    line-height: 1;
    margin-bottom: 4px;
  }

  .fc-unit {
    font-size: 11.5px;
    color: rgba(255,255,255,0.4);
    letter-spacing: -0.01em;
    margin-bottom: 10px;
  }

  .fc-trend {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: -0.01em;
  }

  .fc-bars {
    display: flex;
    align-items: flex-end;
    gap: 4px;
    height: 44px;
    margin: 8px 0;
  }

  .fc-bar {
    flex: 1;
    height: var(--h);
    background: var(--c);
    border-radius: 3px 3px 0 0;
    min-height: 4px;
  }

  .fc-sub {
    font-size: 10px;
    color: rgba(255,255,255,0.3);
    letter-spacing: -0.01em;
    margin-top: 4px;
  }

  .fc-pill {
    display: inline-flex;
    padding: 4px 10px;
    border-radius: 980px;
    background: rgba(44,173,132,0.1);
    border: 1px solid rgba(44,173,132,0.2);
    font-size: 10.5px;
    font-weight: 600;
    color: #2cad84;
    letter-spacing: -0.01em;
    margin-top: 6px;
    box-shadow: inset 0 1px 0 rgba(44,173,132,0.15);
  }

  /* ── Keyframes ───────────────────────────────────────────── */
  @keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.3; transform: scale(0.7); }
  }

  /* ── Responsive ──────────────────────────────────────────── */
  @media (max-width: 900px) {
    .hero-inner { padding-top: 100px; }

    h1 { font-size: clamp(42px, 6vw, 64px); }

    .sub { font-size: 18px; }

    .br-desktop { display: none; }

    .float-card--1 { right: 0; top: 16px; }
    .float-card--2 { right: 0; top: 190px; min-width: 170px; }
    .float-card--3 { left: 0; top: 40px; }
  }

  @media (max-width: 600px) {
    section { min-height: auto; }
    .float-card { display: none; }
    .mc-footer { flex-wrap: wrap; gap: 16px; }
    .mc-divider { display: none; }
    .mc-stat { min-width: 40%; }
  }

  /* ── Responsive Design ──────────────────────────────────────── */
  @media (max-width: 1600px) {
    .portfolio-container {
      grid-template-columns: 340px 1fr 260px;
      gap: 20px;
    }
  }

  @media (max-width: 1400px) {
    .portfolio-container {
      grid-template-columns: 1fr;
      gap: 24px;
      max-width: 900px;
      margin: 0 auto;
    }

    .portfolio-left,
    .portfolio-center,
    .portfolio-right {
      width: 100%;
    }

    .portfolio-right {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
    }
  }

  @media (max-width: 768px) {
    .hero {
      padding: 80px 20px 60px;
    }

    .hero-content {
      gap: 32px;
    }

    .hero-title {
      font-size: 42px;
      line-height: 1.1;
    }

    .hero-subtitle {
      font-size: 17px;
      max-width: 100%;
    }

    .showcase {
      gap: 16px;
    }

    .ai-panel {
      max-width: 100%;
      padding: 20px;
    }

    .main-card {
      padding: 0;
    }

    .main-card-header {
      padding: 16px 20px;
    }

    .mc-label {
      font-size: 13px;
    }

    .mc-meta {
      gap: 6px;
    }

    .mc-badge {
      padding: 4px 10px;
      font-size: 10px;
    }

    .mc-footer {
      padding: 16px 20px;
      gap: 16px;
    }

    .business-panel {
      grid-template-columns: 1fr;
      padding: 0 20px 20px;
    }

    .facility-row {
      grid-template-columns: 1fr auto;
    }

    .facility-row em {
      grid-column: 1 / -1;
      justify-self: start;
    }

    .mc-stat-val {
      font-size: 17px;
    }

    .mc-stat-label {
      font-size: 10px;
    }

    .float-card {
      padding: 16px;
      min-width: auto;
      width: 100%;
    }

    .fc-big {
      font-size: 32px;
    }

    .fc-bars {
      height: 36px;
    }
  }

  @media (max-width: 480px) {
    .hero {
      padding: 60px 16px 40px;
    }

    .hero-title {
      font-size: 36px;
    }

    .hero-subtitle {
      font-size: 15px;
    }

    .cta-group {
      flex-direction: column;
      width: 100%;
    }

    .cta-primary,
    .cta-secondary {
      width: 100%;
      justify-content: center;
    }

    .ai-panel {
      padding: 16px;
    }

    .main-card-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 12px;
    }

    .mc-footer {
      flex-direction: column;
      gap: 12px;
    }

    .mc-stat {
      width: 100%;
      text-align: center;
    }

    .fc-big {
      font-size: 28px;
    }
  }
</style>
