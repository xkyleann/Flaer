<script>
  import FlaerLogo from './FlaerLogo.svelte';

  function handleLinkClick(e) {
    const href = e.currentTarget.getAttribute('href');
    if (href && href.startsWith('#')) {
      e.preventDefault();
      const targetId = href.substring(1);
      
      // Check if it's a legal page route
      if (['privacy', 'terms', 'security'].includes(targetId)) {
        window.location.hash = `#${targetId}`;
        return;
      }
      
      // Otherwise, smooth scroll to section on home page
      const targetElement = document.getElementById(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  }
</script>

<footer>
  <div class="inner w">
    <div class="top-section">
      <div class="brand">
        <div class="logo">
          <FlaerLogo size={30} id="footer" />
          <span class="logo-text">Flaer</span>
        </div>
        <p class="tagline">Real-time carbon intelligence<br />for enterprise infrastructure.</p>
      </div>

      <nav class="links">
        <div class="link-group">
          <div class="link-title">Product</div>
          <a href="#platform" on:click={handleLinkClick}>Platform</a>
          <a href="#capabilities" on:click={handleLinkClick}>Capabilities</a>
          <a href="#pricing" on:click={handleLinkClick}>Pricing</a>
        </div>
        <div class="link-group">
          <div class="link-title">Company</div>
          <a href="#readiness" on:click={handleLinkClick}>Enterprise</a>
          <a href="#cta" on:click={handleLinkClick}>Contact</a>
          <a href="/dashboard">Dashboard</a>
        </div>
        <div class="link-group">
          <div class="link-title">Legal</div>
          <a href="#privacy" on:click={handleLinkClick}>Privacy Policy</a>
          <a href="#terms" on:click={handleLinkClick}>Terms of Service</a>
          <a href="#security" on:click={handleLinkClick}>Security</a>
        </div>
      </nav>
    </div>

    <div class="bottom-section">
      <div class="copy">© 2026 Flaer, Inc. All rights reserved.</div>
      <div class="status-pill">
        <span class="status-dot"></span>
        All systems operational
      </div>
    </div>
  </div>
</footer>

<style>
  footer {
    background: var(--paper);
    border-top: 1px solid rgba(0,0,0,0.07);
    padding: 64px 0 36px;
  }

  .inner {
    display: flex;
    flex-direction: column;
    gap: 48px;
  }

  /* ── Top ── */
  .top-section {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 48px;
  }

  .brand {
    display: flex;
    flex-direction: column;
    gap: 16px;
    max-width: 220px;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .logo-text {
    font-size: 20px;
    font-weight: 700;
    letter-spacing: -0.04em;
    color: var(--ink);
  }

  .tagline {
    font-size: 13px;
    line-height: 1.55;
    color: var(--ink-muted);
    letter-spacing: -0.01em;
  }

  /* ── Links ── */
  .links {
    display: flex;
    gap: 72px;
  }

  .link-group {
    display: flex;
    flex-direction: column;
    gap: 11px;
  }

  .link-title {
    font-size: 11px;
    font-weight: 700;
    color: var(--ink);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 4px;
  }

  .link-group a {
    font-size: 13px;
    font-weight: 400;
    color: var(--ink-soft);
    transition: color 0.18s ease;
    letter-spacing: -0.01em;
  }

  .link-group a:hover {
    color: var(--green-2);
  }

  /* ── Bottom ── */
  .bottom-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 28px;
    border-top: 1px solid rgba(0,0,0,0.07);
    gap: 24px;
    flex-wrap: wrap;
  }

  .copy {
    font-size: 12px;
    color: var(--ink-muted);
    letter-spacing: -0.01em;
  }

  .status-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-size: 12px;
    color: var(--ink-soft);
    background: rgba(44,173,132,0.08);
    border: 1px solid rgba(44,173,132,0.18);
    padding: 5px 12px;
    border-radius: 980px;
    letter-spacing: -0.01em;
  }

  .status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--green-2);
    flex-shrink: 0;
    animation: pulse-dot 2.5s ease-in-out infinite;
  }

  @media (max-width: 820px) {
    .top-section { flex-direction: column; gap: 36px; }
    .brand { max-width: 100%; }
    .links { gap: 40px; }
  }

  @media (max-width: 540px) {
    .links { flex-wrap: wrap; gap: 28px; }
    .bottom-section { flex-direction: column; align-items: flex-start; gap: 14px; }
  }
</style>
