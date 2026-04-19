<script>
  let scrolled = $state(false);

  $effect(() => {
    const onScroll = () => { scrolled = window.scrollY > 20; };
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  });

  function scrollTo(id) {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  }
</script>

<nav class:scrolled>
  <div class="inner w">
    <a href="/" class="logo" aria-label="Flaer home">
      <div class="logo-icon">
        <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
          <rect width="22" height="22" rx="6" fill="url(#lg)"/>
          <path d="M6 11 L11 6 L16 11 L11 16 Z" fill="rgba(255,255,255,0.9)"/>
          <defs>
            <linearGradient id="lg" x1="0" y1="0" x2="22" y2="22">
              <stop offset="0%" stop-color="#23916c"/>
              <stop offset="100%" stop-color="#2cad84"/>
            </linearGradient>
          </defs>
        </svg>
      </div>
      <span class="wordmark">fl<span class="ae">ae</span>r</span>
    </a>

    <ul class="links">
      <li><button onclick={() => scrollTo('platform')}>Platform</button></li>
      <li><button onclick={() => scrollTo('capabilities')}>Capabilities</button></li>
      <li><button onclick={() => scrollTo('pricing')}>Pricing</button></li>
      <li><button onclick={() => scrollTo('readiness')}>Enterprise Readiness</button></li>
    </ul>

    <div class="actions">
      <button class="btn-ghost" onclick={() => scrollTo('cta')}>Sign in</button>
      <button class="btn-primary" onclick={() => scrollTo('cta')}>Request access</button>
    </div>
  </div>
</nav>

<style>
  nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100;
    transition: background 0.3s, box-shadow 0.3s;
  }

  nav.scrolled {
    background: rgba(7, 17, 15, 0.82);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    box-shadow: 0 1px 0 rgba(255,255,255,0.06);
  }

  .inner {
    display: flex;
    align-items: center;
    gap: 40px;
    height: 64px;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;
    margin-right: auto;
  }

  .logo-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    filter: drop-shadow(0 0 8px rgba(44,173,132,0.4));
  }

  .wordmark {
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #f4f7f5;
  }

  .ae {
    color: var(--green-2);
  }

  .links {
    display: flex;
    align-items: center;
    gap: 4px;
    list-style: none;
    margin-left: auto;
  }

  .links button {
    background: none;
    border: none;
    color: rgba(244,247,245,0.7);
    font-size: 14px;
    font-weight: 500;
    padding: 8px 14px;
    border-radius: 8px;
    transition: color 0.15s, background 0.15s;
    cursor: pointer;
  }

  .links button:hover {
    color: #f4f7f5;
    background: rgba(255,255,255,0.06);
  }

  .actions {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;
  }

  @media (max-width: 768px) {
    .links { display: none; }
    .actions .btn-ghost { display: none; }
  }
</style>
