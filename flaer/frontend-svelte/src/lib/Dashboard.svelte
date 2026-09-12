<script>
  import { onMount, onDestroy } from 'svelte';
  import { authStore } from './stores/authStore.js';
  import FlaerLogo from './FlaerLogo.svelte';
  import DashboardSidebar from './DashboardSidebar.svelte';
  import DashboardOverviewSimplified from './DashboardOverviewSimplified.svelte';
  import DashboardForecast from './DashboardForecast.svelte';
  import DashboardAnalytics from './DashboardAnalytics.svelte';
  import DashboardActions from './DashboardActions.svelte';
  import DashboardCalculator from './DashboardCalculator.svelte';
  import DashboardSiteIQEnhanced from './DashboardSiteIQEnhanced.svelte';
  import DashboardGlobalMap from './DashboardGlobalMap.svelte';
  import DashboardBenchmark from './DashboardBenchmark.svelte';
  import DashboardReports from './DashboardReports.svelte';
  import DashboardComparisonReport from './DashboardComparisonReport.svelte';
  import AIAssistant from './AIAssistant.svelte';

  let activeScreen = 'portfolio';
  let dashboardMode = 'tracking'; // 'tracking' or 'planning'
  let selectedRegion = 'Global portfolio';
  let selectedPeriod = 'Q2 2026';
  let exportingPDF = false;
  let exportDone = false;
  let inactivityTimer;
  let warningTimer;
  let showInactivityWarning = false;
  let remainingSeconds = 60;
  
  const INACTIVITY_TIMEOUT = 8 * 60 * 1000; // 8 minutes in milliseconds
  const WARNING_TIME = 60 * 1000; // Show warning 1 minute before logout

  const screenMeta = {
    portfolio: { title: 'Portfolio overview', sub: 'Your facilities, risk level, and the numbers that need attention.' },
    forecast: { title: 'Forecast', sub: 'See where emissions are heading and what changes the path.' },
    actions: { title: 'Actions', sub: 'The next steps with the highest carbon and cost impact.' },
    analytics: { title: 'Facility metrics', sub: 'PUE, WUE, CUE, energy mix, and operating performance.' },
    globalmap: { title: 'Live map', sub: 'A Mapbox view of facilities and carbon intensity worldwide.' },
    siteiq: { title: 'Site selection', sub: 'Compare candidate locations with clear sustainability scores.' },
    benchmark: { title: 'Benchmark', sub: 'Compare your portfolio against similar operators.' },
    calculator: { title: 'Calculator', sub: 'Estimate emissions, costs, and savings before you act.' },
    'ai-assistant': { title: 'flaer AI', sub: 'Ask about digests, anomalies, actions, or new site choices.' },
    reports: { title: 'Reports', sub: 'Generate board-ready climate and compliance reports.' },
    comparison: { title: 'Comparison report', sub: 'Compare up to 4 facilities side-by-side across all sustainability metrics.' },
  };

  function setScreen(screen) {
    activeScreen = screen;
    resetInactivityTimer(); // Reset timer on screen change
  }

  async function handleExportPDF() {
    if (exportingPDF) return;
    exportingPDF = true;
    exportDone = false;
    try {
      const { default: jsPDF } = await import('jspdf');
      const pdf = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' });
      const W = 297, H = 210;

      // Background
      pdf.setFillColor(9, 24, 15);
      pdf.rect(0, 0, W, H, 'F');

      // Left accent bar
      pdf.setFillColor(44, 173, 132);
      pdf.rect(0, 0, 3, H, 'F');

      // Header band
      pdf.setFillColor(13, 31, 28);
      pdf.rect(3, 0, W - 3, 40, 'F');

      // Logo
      pdf.setTextColor(44, 173, 132);
      pdf.setFontSize(26);
      pdf.setFont('helvetica', 'bold');
      pdf.text('flaer', 14, 18);

      pdf.setTextColor(244, 247, 245);
      pdf.setFontSize(13);
      pdf.text(meta.title, 14, 28);

      pdf.setTextColor(120, 160, 150);
      pdf.setFontSize(9);
      pdf.text(`${selectedRegion}  ·  ${selectedPeriod}`, 14, 36);

      // Top-right metadata
      pdf.setFontSize(8);
      pdf.setTextColor(100, 140, 120);
      pdf.text(`Generated ${new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })}`, W - 14, 14, { align: 'right' });
      pdf.text('CONFIDENTIAL', W - 14, 20, { align: 'right' });
      pdf.setTextColor(44, 173, 132);
      pdf.text('flaer.io', W - 14, 27, { align: 'right' });

      // Section divider
      pdf.setDrawColor(44, 173, 132);
      pdf.setLineWidth(0.3);
      pdf.line(14, 44, W - 14, 44);

      // KPI cards row
      const kpis = [
        { label: 'TOTAL EMISSIONS', value: '142,840 tCO₂e', note: '−8.4% vs prior period', col: [44,173,132] },
        { label: 'ENERGY CONSUMED', value: '89,200 MWh', note: '+2.1% vs prior period', col: [127,174,255] },
        { label: 'AVG PUE', value: '1.47', note: 'Industry best: 1.20', col: [183,149,99] },
        { label: 'RENEWABLE MIX', value: '68%', note: 'Target: 80% by 2026', col: [44,173,132] },
        { label: 'WATER INTENSITY', value: '0.8 L/kWh', note: '−15% vs baseline', col: [127,174,255] },
      ];

      kpis.forEach((k, i) => {
        const x = 14 + i * 56;
        pdf.setFillColor(20, 40, 35);
        pdf.roundedRect(x, 50, 52, 28, 2, 2, 'F');
        pdf.setTextColor(...k.col);
        pdf.setFontSize(7);
        pdf.setFont('helvetica', 'bold');
        pdf.text(k.label, x + 4, 57);
        pdf.setFontSize(13);
        pdf.setTextColor(244, 247, 245);
        pdf.text(k.value, x + 4, 67);
        pdf.setFontSize(7);
        pdf.setFont('helvetica', 'normal');
        pdf.setTextColor(120, 160, 150);
        pdf.text(k.note, x + 4, 73);
      });

      // Facilities table header
      pdf.setFontSize(9);
      pdf.setFont('helvetica', 'bold');
      pdf.setTextColor(44, 173, 132);
      pdf.text('FACILITY BREAKDOWN', 14, 90);

      pdf.setDrawColor(44, 173, 132);
      pdf.setLineWidth(0.2);
      pdf.line(14, 92, W - 14, 92);

      const cols = [38, 58, 88, 118, 148, 178, 208, 238];
      const headers = ['Facility', 'Region', 'Emissions tCO₂e', 'Energy MWh', 'PUE', 'WUE', 'Renewable %', 'Status'];
      pdf.setFontSize(7.5);
      pdf.setFont('helvetica', 'bold');
      pdf.setTextColor(160, 190, 180);
      headers.forEach((h, i) => pdf.text(h, cols[i], 97));

      const rows = [
        ['N. Virginia',    'North America', '48,200',   '30,400', '1.42', '0.72', '62%', 'OPERATIONAL'],
        ['EU-Frankfurt',   'Europe',        '22,100',   '19,800', '1.38', '0.55', '89%', 'OPERATIONAL'],
        ['Singapore',      'Asia Pacific',  '31,400',   '22,600', '1.58', '1.10', '45%', 'CAUTION'],
        ['Oregon',         'North America', '18,900',   '14,200', '1.44', '0.68', '91%', 'OPERATIONAL'],
        ['Montréal',       'North America', '12,640',   '11,200', '1.39', '0.49', '97%', 'OPTIMAL'],
        ['Stockholm',      'Europe',        '9,600',    '8,900',  '1.28', '0.31', '98%', 'OPTIMAL'],
      ];

      pdf.setFont('helvetica', 'normal');
      rows.forEach((row, ri) => {
        const y = 105 + ri * 10;
        if (ri % 2 === 0) {
          pdf.setFillColor(16, 32, 28);
          pdf.rect(12, y - 4, W - 24, 9, 'F');
        }
        pdf.setFontSize(8);
        row.forEach((cell, ci) => {
          const isStatus = ci === 7;
          if (isStatus) {
            const col = cell === 'OPTIMAL' ? [44,173,132] : cell === 'CAUTION' ? [183,149,99] : [200,200,200];
            pdf.setTextColor(...col);
          } else {
            pdf.setTextColor(ci === 0 ? 244 : 160, ci === 0 ? 247 : 190, ci === 0 ? 245 : 180);
          }
          pdf.text(cell, cols[ci], y + 1);
        });
      });

      // Footer
      pdf.setDrawColor(30, 60, 50);
      pdf.setLineWidth(0.3);
      pdf.line(14, H - 12, W - 14, H - 12);
      pdf.setFontSize(7.5);
      pdf.setTextColor(80, 120, 100);
      pdf.setFont('helvetica', 'normal');
      pdf.text('Flaer Sustainability Intelligence Platform · All figures are estimates based on available telemetry data.', 14, H - 7);
      pdf.text('Page 1 of 1', W - 14, H - 7, { align: 'right' });

      const filename = `flaer-${activeScreen}-${selectedPeriod.replace(' ', '-').toLowerCase()}.pdf`;
      pdf.save(filename);
      exportDone = true;
    } catch (e) {
      console.error('PDF export failed:', e);
    } finally {
      exportingPDF = false;
      setTimeout(() => { exportDone = false; }, 3000);
    }
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
      <div class="mode-switcher">
        <button
          class="mode-btn"
          class:active={dashboardMode === 'tracking'}
          on:click={() => { dashboardMode = 'tracking'; activeScreen = 'portfolio'; }}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <rect x="3" y="3" width="7" height="7" rx="1" stroke="currentColor" stroke-width="2"/>
            <rect x="14" y="3" width="7" height="7" rx="1" stroke="currentColor" stroke-width="2"/>
            <rect x="3" y="14" width="7" height="7" rx="1" stroke="currentColor" stroke-width="2"/>
            <rect x="14" y="14" width="7" height="7" rx="1" stroke="currentColor" stroke-width="2"/>
          </svg>
          Track Existing
        </button>
        <button
          class="mode-btn"
          class:active={dashboardMode === 'planning'}
          on:click={() => { dashboardMode = 'planning'; activeScreen = 'siteiq'; }}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" fill="none"/>
            <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Plan New
        </button>
      </div>
      <div class="live-pill">
        <span class="live-dot pulsing"></span>
        <span class="live-text">
          <strong>LIVE</strong> {dashboardMode === 'tracking' ? '14 facilities monitored' : 'Site intelligence active'}
        </span>
        <span class="live-update">Updated 3s ago</span>
      </div>
    </div>
    <div class="nav-right">
      <a href="#home" class="nav-btn">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
        Main site
      </a>
      <button class="nav-btn" title="Share this workspace with your team">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/>
          <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>
        </svg>
        Share
      </button>
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
            <select class="filter-select" bind:value={selectedRegion}>
              <option>Global portfolio</option>
              <option>North America</option>
              <option>Europe</option>
              <option>Asia Pacific</option>
            </select>
            <select class="filter-select" bind:value={selectedPeriod}>
              <option>Q2 2026</option>
              <option>Q1 2026</option>
              <option>Q4 2025</option>
              <option>Q3 2025</option>
            </select>
            <button class="tb-btn primary" on:click={handleExportPDF} disabled={exportingPDF}>
              {#if exportingPDF}
                <span class="tb-spinner"></span>
                Exporting…
              {:else if exportDone}
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                Done
              {:else}
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="7 10 12 15 17 10"/>
                  <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                Export PDF
              {/if}
            </button>
          </div>
        </div>

        {#if activeScreen === 'portfolio'}
          <DashboardOverviewSimplified />
        {:else if activeScreen === 'forecast'}
          <DashboardForecast />
        {:else if activeScreen === 'analytics'}
          <DashboardAnalytics />
        {:else if activeScreen === 'actions'}
          <DashboardActions />
        {:else if activeScreen === 'calculator'}
          <DashboardCalculator />
        {:else if activeScreen === 'siteiq'}
          <DashboardSiteIQEnhanced />
        {:else if activeScreen === 'globalmap'}
          <DashboardGlobalMap />
        {:else if activeScreen === 'benchmark'}
          <DashboardBenchmark />
        {:else if activeScreen === 'ai-assistant'}
          <div class="ai-assistant-container">
            <AIAssistant />
          </div>
        {:else if activeScreen === 'reports'}
          <DashboardReports />
        {:else if activeScreen === 'comparison'}
          <DashboardComparisonReport />
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

  .mode-switcher {
    display: flex;
    gap: 4px;
    padding: 4px;
    background: rgba(0,0,0,0.3);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
  }

  .mode-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border-radius: 8px;
    border: none;
    background: transparent;
    color: rgba(244,247,245,0.6);
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.2s ease;
    white-space: nowrap;
  }

  .mode-btn:hover {
    background: rgba(255,255,255,0.06);
    color: rgba(244,247,245,0.9);
  }

  .mode-btn.active {
    background: linear-gradient(135deg, #2cad84, #23916c);
    color: white;
    box-shadow: 0 2px 8px rgba(44,173,132,0.3);
  }

  .mode-btn svg {
    flex-shrink: 0;
  }

  .nav {
    position: sticky;
    top: 0;
    z-index: 1000;
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
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 14px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.12);
    background: rgba(255,255,255,0.06);
    color: var(--text);
    font-size: 12.5px;
    font-weight: 500;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.2s ease;
    text-decoration: none;
    white-space: nowrap;
  }

  .nav-btn:hover {
    background: rgba(255,255,255,0.1);
    border-color: rgba(255,255,255,0.18);
    transform: translateY(-1px);
  }

  .nav-btn:active {
    transform: translateY(0);
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

  .filter-select {
    padding: 8px 14px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.12);
    background: rgba(255,255,255,0.06);
    color: var(--text);
    font-size: 12.5px;
    font-weight: 500;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.2s ease;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg width='12' height='8' viewBox='0 0 12 8' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 1.5L6 6.5L11 1.5' stroke='%23f4f7f5' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 10px center;
    padding-right: 32px;
    min-width: 140px;
  }

  .filter-select:hover {
    background: rgba(255,255,255,0.09);
    border-color: rgba(255,255,255,0.18);
  }

  .filter-select:focus {
    outline: none;
    border-color: var(--g2);
    box-shadow: 0 0 0 3px rgba(44,173,132,0.15);
  }

  .tb-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.045);
    color: var(--ts);
    font-size: 12.5px;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.2s ease;
    white-space: nowrap;
  }

  .tb-btn.primary {
    background: linear-gradient(135deg, #d2e8dd, #f0dfbc);
    color: #07110f;
    border: none;
    font-weight: 700;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.25), 0 3px 8px rgba(44,173,132,0.2);
  }

  .tb-btn:hover:not(.primary) {
    background: rgba(255,255,255,0.08);
    color: var(--text);
  }

  .tb-btn.primary:hover {
    filter: brightness(1.06);
    transform: translateY(-1px);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.25), 0 4px 12px rgba(44,173,132,0.3);
  }

  .tb-btn.primary:active {
    transform: translateY(0);
  }

  .tb-btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none !important;
  }

  .tb-spinner {
    width: 12px;
    height: 12px;
    border: 2px solid rgba(7,17,15,0.25);
    border-top-color: #07110f;
    border-radius: 50%;
    animation: tb-spin 0.7s linear infinite;
  }

  @keyframes tb-spin { to { transform: rotate(360deg); } }

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


  .ai-assistant-container {
    height: calc(100vh - 200px);
    min-height: 600px;
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
