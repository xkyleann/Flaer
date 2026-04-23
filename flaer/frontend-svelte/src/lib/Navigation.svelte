<script>
  import FlaerLogo from './FlaerLogo.svelte';
  import { authStore } from './stores/authStore.js';
  import { onMount } from 'svelte';

  let scrolled = false;

  onMount(() => {
    authStore.init();
  });

  if (typeof window !== 'undefined') {
    window.addEventListener('scroll', () => {
      scrolled = window.scrollY > 20;
    });
  }
  
  function handleLogout() {
    authStore.logout();
    window.location.hash = '#home';
  }
  
  function scrollToSection(e, sectionId) {
    e.preventDefault();
    
    // First navigate to home if not already there
    if (window.location.hash !== '#home' && window.location.hash !== '') {
      window.location.hash = '#home';
      setTimeout(() => {
        const element = document.getElementById(sectionId);
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 100);
    } else {
      const element = document.getElementById(sectionId);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  }
</script>

<nav class:scrolled>
  <div class="nav-inner">
    <a class="logo" href="#home">
      <span class="logo-mark">
        <FlaerLogo size={28} id="nav2" />
      </span>
      <span class="logo-text">Flaer</span>
    </a>

    <ul class="nav-links">
      <li><a href="#home" on:click={(e) => scrollToSection(e, 'platform')}>Platform</a></li>
      <li><a href="#home" on:click={(e) => scrollToSection(e, 'capabilities')}>Capabilities</a></li>
      <li><a href="#pricing">Pricing</a></li>
      {#if $authStore.isAuthenticated}
        <li><a href="#dashboard">Dashboard</a></li>
      {/if}
    </ul>

    <div class="nav-right">
      {#if $authStore.isAuthenticated}
        <span class="user-info">{$authStore.user?.email || 'User'}</span>
        <button class="btn btn-ghost" on:click={handleLogout}>Sign out</button>
      {:else}
        <a class="btn btn-ghost" href="#login">Sign in</a>
        <a class="btn btn-primary" href="#register">Get started</a>
      {/if}
    </div>
  </div>
</nav>

<style>
  nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    backdrop-filter: saturate(180%) blur(20px);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
    background: rgba(0,0,0,0.72);
    border-bottom: 0.5px solid rgba(255,255,255,0.1);
    transition: all 0.5s cubic-bezier(0.28, 0.11, 0.32, 1);
  }

  nav.scrolled {
    background: rgba(0,0,0,0.8);
    border-bottom-color: rgba(255,255,255,0.18);
    box-shadow: 0 1px 0 0 rgba(255,255,255,0.05), 0 10px 40px rgba(0,0,0,0.3);
  }

  .nav-inner {
    width: min(calc(100% - 48px), var(--max));
    margin: 0 auto;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 32px;
  }

  .logo {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    color: var(--text);
    font-size: 21px;
    font-weight: 600;
    letter-spacing: -0.022em;
    transition: opacity 0.3s var(--ease-out);
  }

  .logo:hover {
    opacity: 0.8;
  }

  .logo-mark {
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text);
    transition: transform 0.3s var(--ease-out);
  }

  .logo:hover .logo-mark {
    transform: scale(1.05);
  }

  .logo-text {
    background: linear-gradient(135deg, #ffffff 0%, rgba(255,255,255,0.7) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .nav-links {
    list-style: none;
    display: flex;
    gap: 32px;
    align-items: center;
    margin: 0;
    padding: 0;
  }

  .nav-links a {
    color: var(--text-soft);
    font-size: 12px;
    font-weight: 400;
    letter-spacing: -0.01em;
    transition: color 0.3s var(--ease-out);
    position: relative;
  }

  .nav-links a::after {
    content: '';
    position: absolute;
    bottom: -8px;
    left: 0;
    right: 0;
    height: 1px;
    background: var(--text);
    transform: scaleX(0);
    transition: transform 0.3s var(--ease-out);
  }

  .nav-links a:hover {
    color: var(--text);
  }

  .nav-links a:hover::after {
    transform: scaleX(1);
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
    gap: 6px;
    border-radius: 980px;
    font-size: 12px;
    font-weight: 400;
    letter-spacing: -0.01em;
    cursor: pointer;
    transition: all 0.3s var(--ease-out);
    white-space: nowrap;
    text-decoration: none;
    padding: 4px 12px;
  }

  .btn:active {
    transform: scale(0.96);
  }

  .btn-ghost {
    color: var(--text);
    border: none;
    background: transparent;
  }

  .btn-ghost:hover {
    color: var(--text);
    opacity: 0.8;
  }

  .btn-primary {
    color: #fff;
    background: var(--blue);
    border: none;
    box-shadow: 0 2px 8px rgba(10,132,255,0.3);
  }

  .btn-primary:hover {
    background: #0077ed;
    box-shadow: 0 4px 12px rgba(10,132,255,0.4);
    transform: translateY(-1px);
  }

  @media (max-width: 920px) {
    .nav-inner {
      height: auto;
      padding: 12px 0;
      flex-wrap: wrap;
    }

    .nav-links {
      gap: 20px;
      order: 3;
      width: 100%;
      justify-content: center;
    }

    .nav-right {
      order: 2;
    }
  }

  @media (max-width: 640px) {
    .nav-links {
      gap: 16px;
      font-size: 11px;
    }

    .btn {
      font-size: 11px;
      padding: 4px 10px;
    }
  }
  
  .user-info {
    color: var(--text-soft);
    font-size: 12px;
    font-weight: 400;
    letter-spacing: -0.01em;
    max-width: 150px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  @media (max-width: 640px) {
    .user-info {
      display: none;
    }
  }
  </style>