<script>
  let scrolled = false;
  
  if (typeof window !== 'undefined') {
    window.addEventListener('scroll', () => {
      scrolled = window.scrollY > 10;
    });
  }
</script>

<nav class:scrolled>
  <div class="nav-inner">
    <a class="logo" href="/">
      <span class="logo-mark"></span>
      <span>fl<strong>ae</strong>r</span>
    </a>

    <ul class="nav-links">
      <li><a href="#platform">Platform</a></li>
      <li><a href="#capabilities">Capabilities</a></li>
      <li><a href="#pricing">Pricing</a></li>
      <li><a href="/dashboard">Dashboard</a></li>
    </ul>

    <div class="nav-right">
      <a class="btn btn-ghost" href="/dashboard">Open workspace</a>
      <a class="btn btn-primary" href="#cta">Request access</a>
    </div>
  </div>
</nav>

<style>
  nav {
    position: sticky;
    top: 0;
    z-index: 200;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    background: rgba(7,17,15,0.70);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    transition: all 0.3s ease;
  }

  nav.scrolled {
    background: rgba(7,17,15,0.85);
    border-bottom-color: rgba(255,255,255,0.10);
    box-shadow: 0 4px 24px rgba(0,0,0,0.15);
  }

  .nav-inner {
    width: min(calc(100% - 48px), var(--max));
    margin: 0 auto;
    height: 78px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
  }

  .logo {
    display: inline-flex;
    align-items: center;
    gap: 12px;
    color: var(--text);
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.03em;
  }

  .logo-mark {
    width: 32px;
    height: 32px;
    border-radius: 10px;
    background: linear-gradient(135deg, rgba(35,145,108,0.28), rgba(183,149,99,0.28));
    border: 1px solid rgba(255,255,255,0.10);
    display: grid;
    place-items: center;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
    position: relative;
  }

  .logo-mark::before {
    content: "";
    width: 13px;
    height: 13px;
    border-radius: 4px;
    background: linear-gradient(135deg, var(--green-2), var(--gold));
  }

  .logo strong {
    color: var(--green-2);
  }

  .nav-links {
    list-style: none;
    display: flex;
    gap: 30px;
    align-items: center;
  }

  .nav-links a {
    color: var(--text-soft);
    font-size: 14px;
    font-weight: 500;
    transition: color 0.2s ease;
  }

  .nav-links a:hover {
    color: var(--text);
  }

  .nav-right {
    display: flex;
    gap: 12px;
    align-items: center;
  }

  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.18s ease;
    white-space: nowrap;
    border: 1px solid transparent;
    text-decoration: none;
  }

  .btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.12);
  }

  .btn:active {
    transform: translateY(0);
  }

  .btn-ghost {
    padding: 10px 18px;
    color: var(--text);
    border: 1px solid rgba(255,255,255,0.10);
    background: rgba(255,255,255,0.03);
  }

  .btn-ghost:hover {
    background: rgba(255,255,255,0.08);
    border-color: rgba(255,255,255,0.16);
  }

  .btn-primary {
    padding: 10px 18px;
    color: #07110f;
    background: linear-gradient(135deg, #d2e8dd, #f0dfbc);
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 10px 24px rgba(183,149,99,0.18);
  }

  .btn-primary:hover {
    background: linear-gradient(135deg, #ddf0e5, #f5e6c8);
    box-shadow: 0 14px 36px rgba(183,149,99,0.28);
  }

  @media (max-width: 860px) {
    .nav-inner {
      height: auto;
      padding: 16px 0;
      flex-direction: column;
      align-items: start;
    }

    .nav-links {
      gap: 16px;
    }
  }
</style>