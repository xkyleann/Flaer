<script>
  import FlaerLogo from './FlaerLogo.svelte';

  let scrolled = $state(false);

  $effect(() => {
    const onScroll = () => { scrolled = window.scrollY > 30; };
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
      <FlaerLogo size={28} id="nav" />
      <span class="wordmark">fl<span class="ae">ae</span>r</span>
    </a>

    <ul class="links">
      <li><button onclick={() => scrollTo('platform')}>Platform</button></li>
      <li><button onclick={() => scrollTo('capabilities')}>Capabilities</button></li>
      <li><button onclick={() => scrollTo('pricing')}>Pricing</button></li>
      <li><button onclick={() => scrollTo('readiness')}>Enterprise</button></li>
    </ul>

    <div class="actions">
      <button class="btn-ghost-nav" onclick={() => scrollTo('cta')}>Sign in</button>
      <button class="btn-primary-nav" onclick={() => scrollTo('cta')}>Request access</button>
    </div>
  </div>
</nav>

<style>
  nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 900;
    height: 60px;
    transition: background 0.4s ease, box-shadow 0.4s ease, border-color 0.4s ease;
    border-bottom: 1px solid transparent;
  }

  nav.scrolled {
    background: rgba(7, 17, 15, 0.78);
    backdrop-filter: blur(24px) saturate(180%);
    -webkit-backdrop-filter: blur(24px) saturate(180%);
    border-bottom-color: rgba(255, 255, 255, 0.07);
    box-shadow: 0 1px 0 rgba(255,255,255,0.04), 0 8px 32px rgba(0,0,0,0.24);
  }

  .inner {
    display: flex;
    align-items: center;
    gap: 8px;
    height: 60px;
  }

  /* ── Logo ── */
  .logo {
    display: flex;
    align-items: center;
    gap: 9px;
    flex-shrink: 0;
    margin-right: auto;
    transition: opacity 0.2s ease;
  }
  .logo:hover { opacity: 0.82; }

  .wordmark {
    font-size: 19px;
    font-weight: 700;
    letter-spacing: -0.04em;
    color: var(--text);
  }

  .ae {
    color: var(--green-2);
  }

  /* ── Links ── */
  .links {
    display: flex;
    align-items: center;
    gap: 2px;
    list-style: none;
    margin-left: auto;
  }

  .links button {
    background: none;
    border: none;
    color: var(--text-muted);
    font-size: 13.5px;
    font-weight: 500;
    letter-spacing: -0.01em;
    padding: 7px 13px;
    border-radius: 9px;
    transition: color 0.18s ease, background 0.18s ease;
    cursor: pointer;
  }

  .links button:hover {
    color: var(--text);
    background: rgba(255, 255, 255, 0.07);
  }

  /* ── Actions ── */
  .actions {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
    margin-left: 8px;
  }

  .btn-ghost-nav {
    background: none;
    border: none;
    color: var(--text-soft);
    font-size: 13.5px;
    font-weight: 500;
    letter-spacing: -0.01em;
    padding: 7px 13px;
    border-radius: 9px;
    transition: color 0.18s ease, background 0.18s ease;
    cursor: pointer;
  }
  .btn-ghost-nav:hover {
    color: var(--text);
    background: rgba(255,255,255,0.07);
  }

  .btn-primary-nav {
    background: var(--gradient-primary);
    border: none;
    color: #0d1a16;
    font-size: 13.5px;
    font-weight: 600;
    letter-spacing: -0.01em;
    padding: 8px 16px;
    border-radius: 9px;
    cursor: pointer;
    transition: transform 0.25s var(--ease-out), box-shadow 0.25s var(--ease-out), filter 0.25s var(--ease-out);
    box-shadow: 0 2px 10px rgba(44,173,132,0.25), inset 0 1px 0 rgba(255,255,255,0.22);
    position: relative;
    overflow: hidden;
  }
  .btn-primary-nav::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(255,255,255,0.16) 0%, transparent 60%);
    pointer-events: none;
  }
  .btn-primary-nav:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(44,173,132,0.35), inset 0 1px 0 rgba(255,255,255,0.22);
    filter: brightness(1.04);
  }
  .btn-primary-nav:active {
    transform: scale(0.97);
  }

  @media (max-width: 780px) {
    .links { display: none; }
    .btn-ghost-nav { display: none; }
  }

  @media (max-width: 500px) {
    .wordmark { font-size: 17px; }
  }
</style>
