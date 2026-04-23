<script>
  import { onMount } from 'svelte';
  import Navigation from './lib/Navigation.svelte';
  import Hero from './lib/Hero.svelte';
  import Platform from './lib/Platform.svelte';
  import Capabilities from './lib/Capabilities.svelte';
  import ForecastChart from './lib/ForecastChart.svelte';
  import LiveDataCentersMap from './lib/LiveDataCentersMap.svelte';
  import Readiness from './lib/Readiness.svelte';
  import CtaBlock from './lib/CtaBlock.svelte';
  import Footer from './lib/Footer.svelte';
  import Dashboard from './lib/Dashboard.svelte';
  import Login from './lib/Login.svelte';
  import Register from './lib/Register.svelte';
  import Pricing from './lib/Pricing.svelte';
  import PrivacyPolicy from './lib/PrivacyPolicy.svelte';
  import TermsOfService from './lib/TermsOfService.svelte';
  import SecurityPage from './lib/SecurityPage.svelte';
  import { authStore } from './lib/stores/authStore.js';

  let currentRoute = 'home';
  
  onMount(() => {
    authStore.init();
    updateRoute();
    window.addEventListener('hashchange', updateRoute);
    return () => window.removeEventListener('hashchange', updateRoute);
  });
  
  function updateRoute() {
    const hash = window.location.hash.slice(1) || 'home';
    currentRoute = hash;
    
    // Redirect to login if trying to access dashboard without auth
    if (hash === 'dashboard' && !$authStore.isAuthenticated) {
      window.location.hash = '#login';
    }
    
    // Scroll to top when route changes
    window.scrollTo(0, 0);
  }
</script>

<Navigation />

{#if currentRoute === 'home'}
  <main>
    <Hero />
    <div id="platform">
      <Platform />
    </div>
    <LiveDataCentersMap />
    <div id="capabilities">
      <Capabilities />
    </div>
    <ForecastChart />
    <div id="pricing">
      <Readiness />
    </div>
    <div id="cta">
      <CtaBlock />
    </div>
  </main>
  <Footer />
{:else if currentRoute === 'login'}
  <Login />
{:else if currentRoute === 'register'}
  <Register />
{:else if currentRoute === 'dashboard'}
  {#if $authStore.isAuthenticated}
    <Dashboard />
  {:else}
    <div class="loading">Checking authentication...</div>
  {/if}
{:else if currentRoute === 'privacy'}
  <PrivacyPolicy />
{:else if currentRoute === 'terms'}
  <TermsOfService />
{:else if currentRoute === 'security'}
  <SecurityPage />
{/if}

<style>
  main {
    position: relative;
    z-index: 1;
  }

  .loading {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
    color: rgba(255, 255, 255, 0.7);
    font-size: 1rem;
  }

  /* Legal Sections */
  .legal-section {
    background: var(--paper);
    padding: 80px 0;
    border-top: 1px solid rgba(0,0,0,0.07);
  }

  .legal-content {
    max-width: 800px;
    margin: 0 auto;
  }

  .legal-content h2 {
    font-size: 36px;
    font-weight: 700;
    letter-spacing: -0.04em;
    color: var(--ink);
    margin-bottom: 8px;
  }

  .legal-updated {
    font-size: 14px;
    color: var(--ink-muted);
    margin-bottom: 40px;
    font-style: italic;
  }

  .legal-content h3 {
    font-size: 22px;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: var(--ink);
    margin-top: 32px;
    margin-bottom: 16px;
  }

  .legal-content p {
    font-size: 15px;
    line-height: 1.7;
    color: var(--ink-soft);
    margin-bottom: 16px;
    letter-spacing: -0.01em;
  }

  .legal-content ul {
    list-style: none;
    padding: 0;
    margin: 16px 0;
  }

  .legal-content ul li {
    font-size: 15px;
    line-height: 1.7;
    color: var(--ink-soft);
    margin-bottom: 12px;
    padding-left: 24px;
    position: relative;
    letter-spacing: -0.01em;
  }

  .legal-content ul li::before {
    content: '•';
    position: absolute;
    left: 8px;
    color: var(--green-2);
    font-weight: 700;
  }

  .legal-content ul li strong {
    color: var(--ink);
    font-weight: 600;
  }

  .legal-content a {
    color: var(--green-2);
    text-decoration: none;
    border-bottom: 1px solid rgba(44,173,132,0.3);
    transition: border-color 0.2s ease;
  }

  .legal-content a:hover {
    border-bottom-color: var(--green-2);
  }

  @media (max-width: 768px) {
    .legal-section {
      padding: 60px 20px;
    }

    .legal-content h2 {
      font-size: 28px;
    }

    .legal-content h3 {
      font-size: 20px;
    }

    .legal-content p,
    .legal-content ul li {
      font-size: 14px;
    }
  }
</style>
