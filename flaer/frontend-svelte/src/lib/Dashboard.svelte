<script>
  import { onMount, onDestroy } from 'svelte';
  import { authStore } from './stores/authStore.js';
  import FlaerLogo from './FlaerLogo.svelte';
  import DashboardSidebar from './DashboardSidebar.svelte';
  import DashboardOverview from './DashboardOverview.svelte';
  import DashboardForecast from './DashboardForecast.svelte';
  import DashboardAnalytics from './DashboardAnalytics.svelte';
  import DashboardActions from './DashboardActions.svelte';
  import DashboardCalculator from './DashboardCalculator.svelte';
  import DashboardSiteIQ from './DashboardSiteIQ.svelte';
  import DashboardGlobalMap from './DashboardGlobalMap.svelte';
  import DashboardBenchmark from './DashboardBenchmark.svelte';
  import DashboardReports from './DashboardReports.svelte';

  let activeScreen = 'portfolio';
  let inactivityTimer;
  let warningTimer;
  let showInactivityWarning = false;
  let remainingSeconds = 60;
  
  const INACTIVITY_TIMEOUT = 8 * 60 * 1000; // 8 minutes in milliseconds
  const WARNING_TIME = 60 * 1000; // Show warning 1 minute before logout

  const screenMeta = {
    portfolio: { title: 'Portfolio carbon exposure review', sub: 'See which regions and facilities create the most carbon and reporting pressure.' },
    forecast: { title: '2035 forecast & scenario planner', sub: 'Model business-as-usual versus optimised pathways under different climate scenarios.' },
    actions: { title: 'Recommended actions', sub: 'Top interventions ranked by ROI, effort, and confidence level.' },
    analytics: { title: 'Facility analytics', sub: 'Deep metrics: PUE, WUE, CUE, and energy mix per facility.' },
    globalmap: { title: 'Global facility map', sub: 'Live carbon intensity signals across your entire portfolio.' },
    siteiq: { title: 'Site intelligence', sub: 'Analyse and compare candidate locations for your next facility.' },
    benchmark: { title: 'Industry benchmark', sub: 'Compare your portfolio against sector peers on key efficiency metrics.' },
    calculator: { title: 'Carbon impact calculator', sub: 'Model how operational changes affect emissions, costs, and equivalents.' },
    reports: { title: 'Climate Impact Reports', sub: 'Generate comprehensive environmental impact reports for your data centers with CSRD, EED, and SFDR compliance.' },
  };

  function setScreen(screen) {
    activeScreen = screen;
    resetInactivityTimer(); // Reset timer on screen change
  }

  function resetInactivityTimer() {
    // Clear existing timers
    if (inactivityTimer) clearTimeout(inactivityTimer);
    if (warningTimer) clearTimeout(warningTimer);
    
    // Hide warning if shown
    showInactivityWarning = false;
    remainingSeconds = 60;
    
    // Set warning timer (7 minutes)
    warningTimer = setTimeout(() => {
      showInactivityWarning = true;
      startCountdown();
    }, INACTIVITY_TIMEOUT - WARNING_TIME);
    
    // Set logout timer (8 minutes)
    inactivityTimer = setTimeout(() => {
      handleInactivityLogout();
    }, INACTIVITY_TIMEOUT);
  }

  function startCountdown() {
    const countdownInterval = setInterval(() => {
      remainingSeconds--;
      if (remainingSeconds <= 0 || !showInactivityWarning) {
        clearInterval(countdownInterval);
      }
    }, 1000);
  }

  async function handleInactivityLogout() {
    await authStore.logout();
    window.location.hash = '#login';
  }

  function stayActive() {
    resetInactivityTimer();
  }

  onMount(() => {
    // Start inactivity timer
    resetInactivityTimer();
    
    // Track user activity
    const activityEvents = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
    
    activityEvents.forEach(event => {
      document.addEventListener(event, resetInactivityTimer, true);
    });
    
    // Cleanup function
    return () => {
      activityEvents.forEach(event => {
        document.removeEventListener(event, resetInactivityTimer, true);
      });
    };
  });

  onDestroy(() => {
    if (inactivityTimer) clearTimeout(inactivityTimer);
    if (warningTimer) clearTimeout(warningTimer);
  });

  $: meta = screenMeta[activeScreen] || screenMeta.portfolio;
</script>

<div class="dashboard">
  <nav class="nav">
    <div class="nav-logo">
      <FlaerLogo size={26} id="dash" />
      <span>fl<strong>ae</strong>r</span>
    </div>
    <div class="nav-center">
      <div class="live-pill">
        <span class="live-dot pulsing"></span>
        <span class="live-text">
          <strong>LIVE</strong> Real-time data from 38 data centers
        </span>
        <span class="live-update">Updated 3s ago</span>
      </div>
    </div>
    <div class="nav-right">
      <button class="nav-btn">Share workspace</button>
      <button class="nav-btn">← Main site</button>
      <button class="nav-btn primary">Export PDF</button>
    </div>
  </nav>

  <div class="app">
    <DashboardSidebar {activeScreen} {setScreen} />

    <main class="main">
      <div class="workspace">
        <div class="topbar">
          <div class="topbar-left">
            <h2>{meta.title}</h2>
            <p>{meta.sub}</p>
          </div>
          <div class="topbar-right">
            <div class="chip">Global portfolio ▾</div>
            <div class="chip">Q2 2026 ▾</div>
            <button class="tb-btn">Share</button>
            <button class="tb-btn primary">Export PDF</button>
          </div>
        </div>

        {#if activeScreen === 'portfolio'}
          <DashboardOverview />
        {:else if activeScreen === 'forecast'}
          <DashboardForecast />
        {:else if activeScreen === 'analytics'}
          <DashboardAnalytics />
        {:else if activeScreen === 'actions'}
          <DashboardActions />
        {:else if activeScreen === 'calculator'}
          <DashboardCalculator />
        {:else if activeScreen === 'siteiq'}
          <DashboardSiteIQ />
        {:else if activeScreen === 'globalmap'}
          <DashboardGlobalMap />
        {:else if activeScreen === 'benchmark'}
          <DashboardBenchmark />
        {:else if activeScreen === 'reports'}
          <DashboardReports />
        {/if}
      </div>
    </main>
  </div>
  
  <!-- Inactivity Warning Modal -->
  {#if showInactivityWarning}
    <div class="inactivity-overlay">
      <div class="inactivity-modal">
        <div class="inactivity-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="10" stroke="#b67e3d" stroke-width="2"/>
            <path d="M12 8V12L14 14" stroke="#b67e3d" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </div>
        <h3>Session Timeout Warning</h3>
        <p>You've been inactive for a while. For security reasons, you'll be automatically logged out in:</p>
        <div class="countdown">{remainingSeconds}s</div>
        <p class="inactivity-sub">Any unsaved changes will be lost.</p>
        <div class="inactivity-actions">
          <button class="inactivity-btn primary" on:click={stayActive}>
            Stay Logged In
          </button>
          <button class="inactivity-btn" on:click={handleInactivityLogout}>
            Logout Now
          </button>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  :global(*), :global(*::before), :global(*::after) {
    box-sizing: border-box;
  }

  :global(:root) {
    --bg: #07110f;
    --bg2: #0b1714;
    --bg3: #0f1d18;
    --panel: rgba(255,255,255,0.055);
    --panel2: rgba(255,255,255,0.08);
    --line: rgba(255,255,255,0.07);
    --line2: rgba(255,255,255,0.12);
    --text: #f4f7f5;
    --ts: rgba(244,247,245,0.76);
    --tm: rgba(244,247,245,0.46);
    --green: #23916c;
    --g2: #2cad84;
    --gs: rgba(44,173,132,0.16);
    --gold: #b79563;
    --gos: rgba(183,149,99,0.16);
    --blue: #7faeff;
    --bs: rgba(127,174,255,0.16);
    --red: #d35d5c;
    --rs: rgba(211,93,92,0.16);
    --amber: #b67e3d;
    --as: rgba(182,126,61,0.16);
    --sxl: 0 34px 110px rgba(0,0,0,0.38);
    --slg: 0 20px 56px rgba(0,0,0,0.24);
    --smd: 0 12px 28px rgba(0,0,0,0.18);
    --sidebar: 268px;
  }

  .dashboard {
    min-height: 100vh;
    background: radial-gradient(circle at 8% 0%, rgba(44,173,132,0.12), transparent 20%),
                radial-gradient(circle at 90% 0%, rgba(127,174,255,0.09), transparent 20%),
                linear-gradient(180deg, #07110f, #07110f);
    color: var(--text);
    font-family: 'Inter', sans-serif;
    -webkit-font-smoothing: antialiased;
  }

  .nav {
    position: sticky;
    top: 0;
    z-index: 300;
    height: 60px;
    backdrop-filter: blur(24px) saturate(180%);
    -webkit-backdrop-filter: blur(24px) saturate(180%);
    background: rgba(7,17,15,0.84);
    border-bottom: 1px solid rgba(255,255,255,0.07);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
    gap: 16px;
  }

  .nav-logo {
    display: flex;
    align-items: center;
    gap: 9px;
    font-size: 17px;
    font-weight: 800;
    letter-spacing: -0.04em;
    flex-shrink: 0;
  }

  .nav-logo :global(strong) {
    color: var(--g2);
  }

  .nav-center {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .live-pill {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 16px;
    border-radius: 999px;
    background: rgba(44,173,132,0.12);
    border: 1px solid rgba(44,173,132,0.25);
    font-size: 12px;
    letter-spacing: -0.01em;
  }

  .live-text {
    display: flex;
    align-items: center;
    gap: 6px;
    color: rgba(44,173,132,0.95);
    font-weight: 500;
  }

  .live-text strong {
    font-weight: 700;
    color: #2cad84;
    letter-spacing: 0.02em;
  }

  .live-update {
    font-size: 10px;
    color: rgba(44,173,132,0.6);
    font-weight: 500;
    padding-left: 8px;
    border-left: 1px solid rgba(44,173,132,0.2);
  }

  .live-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #2cad84;
    flex-shrink: 0;
  }

  .live-dot.pulsing {
    animation: livePulse 2s ease-in-out infinite;
  }

  @keyframes livePulse {
    0%, 100% {
      box-shadow: 0 0 0 0 rgba(44,173,132,0.7),
                  0 0 8px 2px rgba(44,173,132,0.3);
      transform: scale(1);
    }
    50% {
      box-shadow: 0 0 0 4px rgba(44,173,132,0),
                  0 0 12px 4px rgba(44,173,132,0.1);
      transform: scale(1.1);
    }
  }

  @keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 2px rgba(44,173,132,0.25); }
    50%       { box-shadow: 0 0 0 5px rgba(44,173,132,0.06); }
  }

  .nav-right {
    display: flex;
    gap: 7px;
    align-items: center;
  }

  .nav-btn {
    padding: 7px 13px;
    border-radius: 9px;
    border: 1px solid rgba(255,255,255,0.09);
    background: rgba(255,255,255,0.04);
    color: var(--ts);
    font-size: 12.5px;
    font-weight: 500;
    cursor: pointer;
    font-family: inherit;
    transition: background 0.18s ease, color 0.18s ease;
  }

  .nav-btn:hover {
    background: rgba(255,255,255,0.08);
    color: var(--text);
    border-color: rgba(255,255,255,0.14);
  }

  .nav-btn.primary {
    background: linear-gradient(135deg, #d2e8dd, #f0dfbc);
    color: #07110f;
    border: none;
    font-weight: 600;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.2), 0 2px 8px rgba(44,173,132,0.15);
  }
  .nav-btn.primary:hover {
    filter: brightness(1.04);
    transform: translateY(-1px);
  }

  .app {
    display: grid;
    grid-template-columns: var(--sidebar) 1fr;
    min-height: calc(100vh - 60px);
  }

  .main {
    padding: 22px;
    min-width: 0;
  }

  .workspace {
    border-radius: 24px;
    padding: 22px;
    background: linear-gradient(180deg, rgba(255,255,255,0.038), rgba(255,255,255,0.016));
    border: 1px solid rgba(255,255,255,0.07);
    box-shadow: 0 32px 80px -12px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.06);
    min-height: calc(100vh - 104px);
  }

  .topbar {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 22px;
    padding-bottom: 18px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
  }

  .topbar-left h2 {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: var(--text);
    margin-bottom: 4px;
    line-height: 1.1;
  }

  .topbar-left p {
    color: var(--tm);
    font-size: 12.5px;
    letter-spacing: -0.01em;
  }

  .topbar-right {
    display: flex;
    gap: 7px;
    align-items: center;
    flex-wrap: wrap;
    flex-shrink: 0;
  }

  .chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 6px 12px;
    border-radius: 9px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.045);
    color: var(--ts);
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.15s ease, border-color 0.15s ease;
  }
  .chip:hover {
    background: rgba(255,255,255,0.08);
    border-color: rgba(255,255,255,0.14);
  }

  .tb-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 13px;
    border-radius: 9px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.045);
    color: var(--ts);
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    font-family: inherit;
    transition: background 0.15s ease, color 0.15s ease;
  }

  .tb-btn.primary {
    background: linear-gradient(135deg, #d2e8dd, #f0dfbc);
    color: #07110f;
    border: none;
    font-weight: 600;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.22), 0 2px 6px rgba(44,173,132,0.12);
  }

  .tb-btn:hover:not(.primary) {
    background: rgba(255,255,255,0.08);
    color: var(--text);
  }

  .tb-btn.primary:hover {
    filter: brightness(1.04);
    transform: translateY(-1px);
  }

  /* Inactivity Warning Modal */
  .inactivity-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.85);
    backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10000;
    animation: fadeIn 0.3s ease;
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .inactivity-modal {
    background: linear-gradient(135deg, var(--bg2) 0%, var(--bg3) 100%);
    border: 1px solid var(--line2);
    border-radius: 16px;
    padding: 40px;
    max-width: 480px;
    width: 90%;
    box-shadow: var(--sxl);
    animation: slideUp 0.3s ease;
    text-align: center;
  }

  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .inactivity-icon {
    margin: 0 auto 24px;
    width: 48px;
    height: 48px;
    animation: pulse 2s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.7; transform: scale(1.05); }
  }

  .inactivity-modal h3 {
    font-size: 24px;
    font-weight: 600;
    color: var(--text);
    margin: 0 0 16px 0;
    letter-spacing: -0.02em;
  }

  .inactivity-modal p {
    font-size: 15px;
    line-height: 1.6;
    color: var(--tm);
    margin: 0 0 24px 0;
  }

  .inactivity-sub {
    font-size: 13px !important;
    color: var(--amber) !important;
    margin: 16px 0 24px 0 !important;
  }

  .countdown {
    font-size: 48px;
    font-weight: 700;
    color: var(--amber);
    margin: 24px 0;
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.02em;
  }

  .inactivity-actions {
    display: flex;
    gap: 12px;
    margin-top: 32px;
  }

  .inactivity-btn {
    flex: 1;
    padding: 14px 24px;
    border: 1px solid var(--line2);
    border-radius: 8px;
    background: var(--panel);
    color: var(--ts);
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .inactivity-btn:hover {
    background: var(--panel2);
    border-color: var(--line2);
    transform: translateY(-1px);
  }

  .inactivity-btn.primary {
    background: var(--green);
    border-color: var(--green);
    color: white;
  }

  .inactivity-btn.primary:hover {
    background: var(--g2);
    border-color: var(--g2);
    box-shadow: 0 4px 12px var(--gs);
  }

  @media (max-width: 1200px) {
    .app { grid-template-columns: 1fr; }
  }
</style>
