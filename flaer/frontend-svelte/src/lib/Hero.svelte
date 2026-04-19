<script>
  import WorldMap from './WorldMap.svelte';

  const stats = [
    { label: '11 data centers · 6 regions' },
    { label: 'CSRD-ready exports' },
    { label: 'Real-time grid signals' },
    { label: '10-year forecasting' },
  ];
</script>

<section id="hero">
  <div class="inner w">
    <!-- Left copy -->
    <div class="copy">
      <div class="kicker">
        <span class="kicker-dot"></span>
        Enterprise carbon intelligence
      </div>

      <h1>Enterprise carbon intelligence.<br><em>Built for infrastructure scale.</em></h1>

      <p class="sub">
        Flaer gives infrastructure and sustainability teams real-time carbon intensity signals, ten-year forecasts, and CSRD-aligned reporting — across every cloud region your workloads touch.
      </p>

      <div class="ctas">
        <button class="btn-primary" onclick={() => document.getElementById('cta')?.scrollIntoView({ behavior: 'smooth' })}>
          Request access
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2.5 7h9M8 3.5 11.5 7 8 10.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
        <button class="btn-ghost" onclick={() => document.getElementById('platform')?.scrollIntoView({ behavior: 'smooth' })}>
          See the platform
        </button>
      </div>

      <div class="stats">
        {#each stats as s}
          <div class="stat-chip">
            <span class="chip-dot"></span>
            {s.label}
          </div>
        {/each}
      </div>
    </div>

    <!-- Right dashboard card -->
    <div class="dashboard-card">
      <div class="card-header">
        <div class="card-title">
          <span class="title-dot"></span>
          Live infrastructure · Carbon risk view
        </div>
        <div class="card-pills">
          <span class="pill pill-green">Live</span>
          <span class="pill pill-ghost">11 DCs</span>
        </div>
      </div>

      <div class="map-container">
        <WorldMap />
      </div>

      <div class="card-footer">
        <div class="footer-stat">
          <span class="fs-label">Avg. intensity</span>
          <span class="fs-val">318 <span>gCO₂/kWh</span></span>
        </div>
        <div class="footer-divider"></div>
        <div class="footer-stat">
          <span class="fs-label">High risk DCs</span>
          <span class="fs-val c-red">5</span>
        </div>
        <div class="footer-divider"></div>
        <div class="footer-stat">
          <span class="fs-label">CSRD deadline</span>
          <span class="fs-val">Jan 2026</span>
        </div>
      </div>
    </div>
  </div>
</section>

<style>
  section {
    padding: 140px 0 80px;
    position: relative;
  }

  .inner {
    display: grid;
    grid-template-columns: 1fr 1.15fr;
    gap: 56px;
    align-items: center;
  }

  .copy {
    display: flex;
    flex-direction: column;
  }

  .kicker {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--green-2);
    margin-bottom: 22px;
    padding: 8px 14px;
    background: rgba(44,173,132,0.10);
    border: 1px solid rgba(44,173,132,0.20);
    border-radius: 99px;
    width: fit-content;
  }

  .kicker-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--green-2);
    animation: pulse-dot 2s ease-in-out infinite;
  }

  h1 {
    font-size: clamp(30px, 4.2vw, 50px);
    font-weight: 900;
    line-height: 1.08;
    letter-spacing: -0.03em;
    color: #f4f7f5;
    margin-bottom: 22px;
  }

  h1 em {
    font-style: normal;
    background: linear-gradient(135deg, #c8ede0 0%, var(--green-2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .sub {
    font-size: 16px;
    line-height: 1.65;
    color: rgba(244,247,245,0.65);
    margin-bottom: 34px;
    max-width: 480px;
  }

  .ctas {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 36px;
    flex-wrap: wrap;
  }

  .stats {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }

  .stat-chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    font-weight: 500;
    color: rgba(244,247,245,0.55);
    padding: 6px 12px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 99px;
  }

  .chip-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--green-2);
    opacity: 0.6;
  }

  /* Dashboard card */
  .dashboard-card {
    background: rgba(12, 24, 20, 0.88);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: var(--radius-xl);
    overflow: hidden;
    box-shadow:
      0 0 0 1px rgba(44,173,132,0.07),
      0 40px 100px rgba(0,0,0,0.5),
      inset 0 1px 0 rgba(255,255,255,0.06);
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
  }

  .card-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11.5px;
    font-weight: 600;
    color: rgba(244,247,245,0.5);
    letter-spacing: 0.03em;
  }

  .title-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--green-2);
    animation: pulse-dot 2s ease-in-out infinite;
  }

  .card-pills {
    display: flex;
    gap: 6px;
  }

  .pill {
    padding: 3px 10px;
    border-radius: 99px;
    font-size: 11px;
    font-weight: 600;
  }

  .pill-green {
    background: rgba(44,173,132,0.14);
    color: var(--green-2);
    border: 1px solid rgba(44,173,132,0.22);
  }

  .pill-ghost {
    background: rgba(255,255,255,0.05);
    color: rgba(244,247,245,0.4);
    border: 1px solid rgba(255,255,255,0.08);
  }

  .map-container {
    padding: 14px 14px 10px;
  }

  .card-footer {
    display: flex;
    align-items: center;
    padding: 13px 20px;
    border-top: 1px solid rgba(255,255,255,0.07);
  }

  .footer-stat {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 3px;
  }

  .fs-label {
    font-size: 10px;
    color: rgba(244,247,245,0.38);
    text-transform: uppercase;
    letter-spacing: 0.07em;
    font-weight: 600;
  }

  .fs-val {
    font-size: 15px;
    font-weight: 700;
    color: #f4f7f5;
  }

  .fs-val span {
    font-size: 10px;
    font-weight: 500;
    color: rgba(244,247,245,0.38);
  }

  .c-red { color: var(--red); }

  .footer-divider {
    width: 1px;
    height: 30px;
    background: rgba(255,255,255,0.07);
    margin: 0 18px;
  }

  @keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.45; transform: scale(0.7); }
  }

  @media (max-width: 920px) {
    .inner {
      grid-template-columns: 1fr;
    }
  }
</style>
