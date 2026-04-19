<footer>
  <div class="inner w">
    <div class="logo">
      <div class="logo-icon">
        <svg width="20" height="20" viewBox="0 0 22 22" fill="none">
          <rect width="22" height="22" rx="6" fill="url(#lg-footer)"/>
          <path d="M6 11 L11 6 L16 11 L11 16 Z" fill="rgba(255,255,255,0.85)"/>
          <defs>
            <linearGradient id="lg-footer" x1="0" y1="0" x2="22" y2="22">
              <stop offset="0%" stop-color="#23916c"/>
              <stop offset="100%" stop-color="#2cad84"/>
            </linearGradient>
          </defs>
        </svg>
      </div>
      <span>fl<span class="ae">ae</span>r</span>
    </div>

    <nav class="links">
      <a href="#platform">Platform</a>
      <a href="#capabilities">Capabilities</a>
      <a href="#pricing">Pricing</a>
      <a href="#readiness">Enterprise</a>
      <a href="#cta">Contact</a>
    </nav>

    <div class="copy">© 2026 Flaer · Warsaw, Poland</div>
  </div>
</footer>

<style>
  footer {
    background: var(--paper);
    border-top: 1px solid rgba(0,0,0,0.08);
    padding: 28px 0 36px;
  }

  .inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    flex-wrap: wrap;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 9px;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--ink);
  }

  .logo-icon {
    display: flex;
    align-items: center;
  }

  .ae { color: var(--green); }

  .links {
    display: flex;
    gap: 22px;
    flex-wrap: wrap;
  }

  .links a {
    font-size: 13.5px;
    color: var(--ink-soft);
    transition: color 0.15s;
  }

  .links a:hover { color: var(--green); }

  .copy {
    font-size: 13px;
    color: var(--ink-muted);
  }

  @media (max-width: 640px) {
    .links { display: none; }
  }
</style>
