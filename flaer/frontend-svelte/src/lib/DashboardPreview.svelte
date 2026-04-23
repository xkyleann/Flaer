<script>
  import { onMount } from 'svelte';
  
  export let isOpen = false;
  
  let activeTab = 'roi';
  let animatedValue = 0;
  let savingsValue = 0;
  let complianceScore = 0;
  let autoPlayInterval;
  
  $: if (isOpen) {
    startAnimations();
    startAutoPlay();
  } else {
    stopAutoPlay();
  }
  
  function startAnimations() {
    animatedValue = 0;
    savingsValue = 0;
    complianceScore = 0;
    
    const emissionsInterval = setInterval(() => {
      if (animatedValue < 47) animatedValue += 1;
      else clearInterval(emissionsInterval);
    }, 30);
    
    const savingsInterval = setInterval(() => {
      if (savingsValue < 2.4) savingsValue += 0.1;
      else clearInterval(savingsInterval);
    }, 50);
    
    const complianceInterval = setInterval(() => {
      if (complianceScore < 98) complianceScore += 1;
      else clearInterval(complianceInterval);
    }, 30);
  }
  
  function startAutoPlay() {
    const tabs = ['roi', 'realtime', 'compliance', 'forecast'];
    let currentIndex = 0;
    
    autoPlayInterval = setInterval(() => {
      currentIndex = (currentIndex + 1) % tabs.length;
      activeTab = tabs[currentIndex];
    }, 6000);
  }
  
  function stopAutoPlay() {
    if (autoPlayInterval) clearInterval(autoPlayInterval);
  }
  
  function handleTabClick(tab) {
    stopAutoPlay();
    activeTab = tab;
  }
  
  function closeModal() {
    isOpen = false;
  }
  
  function handleBackdropClick(e) {
    if (e.target === e.currentTarget) closeModal();
  }
</script>

{#if isOpen}
  <div class="modal-backdrop" on:click={handleBackdropClick} role="dialog" aria-modal="true">
    <div class="modal-content">
      <!-- Header -->
      <div class="modal-header">
        <div class="header-left">
          <div class="live-indicator">
            <span class="live-dot"></span>
            <span>Live Demo • Auto-playing</span>
          </div>
          <h2>$2.1M ARR • 40+ Enterprise Clients • 98% Retention</h2>
          <p class="header-subtitle">Powering CSRD compliance for Fortune 500 infrastructure teams</p>
        </div>
        <button class="close-btn" on:click={closeModal} aria-label="Close">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>
      
      <!-- Tabs -->
      <div class="dashboard-tabs">
        <button class="tab" class:active={activeTab === 'roi'} on:click={() => handleTabClick('roi')}>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" style="margin-right: 8px;">
            <path d="M8 2a6 6 0 100 12A6 6 0 008 2zm0 1a5 5 0 110 10A5 5 0 018 3zm-.5 2v3.5H5v1h3.5V5h-1z"/>
          </svg>
          ROI & Business Value
        </button>
        <button class="tab" class:active={activeTab === 'realtime'} on:click={() => handleTabClick('realtime')}>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" style="margin-right: 8px;">
            <path d="M8 2l1.5 4.5L14 8l-4.5 1.5L8 14l-1.5-4.5L2 8l4.5-1.5L8 2z"/>
          </svg>
          Real-Time Monitoring
        </button>
        <button class="tab" class:active={activeTab === 'compliance'} on:click={() => handleTabClick('compliance')}>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" style="margin-right: 8px;">
            <path d="M8 1l6 2v4c0 3.5-2 6-6 8-4-2-6-4.5-6-8V3l6-2zm0 1.5L3 4v3c0 2.8 1.5 4.8 5 6.5 3.5-1.7 5-3.7 5-6.5V4l-5-1.5z"/>
          </svg>
          CSRD Compliance
        </button>
        <button class="tab" class:active={activeTab === 'forecast'} on:click={() => handleTabClick('forecast')}>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" style="margin-right: 8px;">
            <path d="M2 12l2-6 3 4 3-8 3 6 1-2"/>
          </svg>
          AI Forecast
        </button>
      </div>
      
      <!-- Content -->
      <div class="dashboard-body">
        {#if activeTab === 'roi'}
          <div class="roi-view">
            <div class="roi-hero">
              <div class="mega-stat">
                <div class="mega-label">Average Customer Savings</div>
                <div class="mega-value">${savingsValue.toFixed(1)}M<span class="unit">/year</span></div>
                <div class="mega-sub">32% reduction in carbon-related costs</div>
              </div>
              <div class="highlights">
                <div class="highlight">
                  <div class="h-icon"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h8l-1 8 10-12h-8l1-8z"/></svg></div>
                  <div class="h-value">6 months</div>
                  <div class="h-label">Average ROI</div>
                </div>
                <div class="highlight">
                  <div class="h-icon"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg></div>
                  <div class="h-value">$847K</div>
                  <div class="h-label">Annual Savings</div>
                </div>
                <div class="highlight">
                  <div class="h-icon"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg></div>
                  <div class="h-value">98%</div>
                  <div class="h-label">Retention Rate</div>
                </div>
              </div>
            </div>
            
            <h3 class="section-title">Proven Business Impact</h3>
            <div class="value-grid">
              <div class="value-card">
                <div class="v-header">
                  <span class="v-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg></span>
                  <span class="v-title">Cost Reduction</span>
                </div>
                <div class="v-metric">$2.4M saved</div>
                <div class="v-desc">Across 40+ enterprise clients in 2025</div>
                <div class="v-breakdown">
                  <div class="b-item"><span>Energy optimization</span><span>$1.2M</span></div>
                  <div class="b-item"><span>Compliance automation</span><span>$800K</span></div>
                  <div class="b-item"><span>Carbon credit trading</span><span>$400K</span></div>
                </div>
              </div>
              
              <div class="value-card">
                <div class="v-header">
                  <span class="v-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1l6 2v4c0 3.5-2 6-6 8-4-2-6-4.5-6-8V3l6-2z"/></svg></span>
                  <span class="v-title">Risk Mitigation</span>
                </div>
                <div class="v-metric">$5.2M</div>
                <div class="v-desc">Potential fines avoided through compliance</div>
                <div class="v-breakdown">
                  <div class="b-item"><span>CSRD compliance</span><span class="badge">100%</span></div>
                  <div class="b-item"><span>EED reporting</span><span class="badge">Automated</span></div>
                  <div class="b-item"><span>Audit readiness</span><span class="badge">Real-time</span></div>
                </div>
              </div>
              
              <div class="value-card">
                <div class="v-header">
                  <span class="v-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg></span>
                  <span class="v-title">Operational Efficiency</span>
                </div>
                <div class="v-metric">87% faster</div>
                <div class="v-desc">Reporting and compliance workflows</div>
                <div class="v-breakdown">
                  <div class="b-item"><span>Manual reporting time</span><span>−156 hrs/mo</span></div>
                  <div class="b-item"><span>Data accuracy</span><span class="badge">99.7%</span></div>
                  <div class="b-item"><span>Team productivity</span><span>+43%</span></div>
                </div>
              </div>
            </div>
          </div>
        {:else if activeTab === 'realtime'}
          <div class="realtime-view">
            <h3 class="section-title">Live Carbon Intelligence</h3>
            <p class="section-sub">Tracking {animatedValue} tCO₂/min across 11,000+ data centers in 40+ regions</p>
            
            <div class="metrics-grid">
              <div class="metric-card">
                <div class="m-label">Real-time Emissions</div>
                <div class="m-value">{animatedValue} <span class="m-unit">tCO₂/min</span></div>
                <div class="m-trend positive">↓ 12% reduction</div>
              </div>
              <div class="metric-card">
                <div class="m-label">Active Data Centers</div>
                <div class="m-value">11 <span class="m-unit">sites</span></div>
                <div class="m-status">● All operational</div>
              </div>
              <div class="metric-card">
                <div class="m-label">Carbon Intensity</div>
                <div class="m-value">342 <span class="m-unit">gCO₂/kWh</span></div>
                <div class="m-trend neutral">→ Stable</div>
              </div>
            </div>
            
            <div class="map-preview">
              <div class="map-title">Global Portfolio</div>
              <svg viewBox="0 0 600 300" width="100%">
                <rect width="600" height="300" fill="rgba(44,173,132,0.05)"/>
                <circle cx="150" cy="120" r="8" fill="#2cad84" class="pulse"/>
                <circle cx="270" cy="105" r="8" fill="#2cad84" class="pulse"/>
                <circle cx="480" cy="135" r="8" fill="#2cad84" class="pulse"/>
                <circle cx="525" cy="112" r="8" fill="#b67e3d" class="pulse"/>
                <circle cx="420" cy="210" r="8" fill="#2cad84" class="pulse"/>
              </svg>
            </div>
          </div>
        {:else if activeTab === 'compliance'}
          <div class="compliance-view">
            <div class="compliance-hero">
              <div class="score-card">
                <div class="score-label">CSRD Compliance Score</div>
                <div class="score-circle">
                  <svg viewBox="0 0 200 200" width="180" height="180">
                    <circle cx="100" cy="100" r="85" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="10"/>
                    <circle cx="100" cy="100" r="85" fill="none" stroke="#2cad84" stroke-width="10"
                            stroke-dasharray="534" stroke-dashoffset="{534 - (534 * complianceScore / 100)}"
                            transform="rotate(-90 100 100)" class="progress"/>
                    <text x="100" y="100" text-anchor="middle" dy=".3em" class="score-text">{complianceScore}%</text>
                  </svg>
                </div>
                <div class="score-badge">✓ Fully Compliant</div>
              </div>
              
              <div class="compliance-stats">
                <div class="c-stat">
                  <div class="cs-icon">📋</div>
                  <div class="cs-value">100%</div>
                  <div class="cs-label">Automated Reporting</div>
                </div>
                <div class="c-stat">
                  <div class="cs-icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div>
                  <div class="cs-value">&lt; 2 hrs</div>
                  <div class="cs-label">Audit Prep</div>
                </div>
                <div class="c-stat">
                  <div class="cs-icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg></div>
                  <div class="cs-value">Zero</div>
                  <div class="cs-label">Violations</div>
                </div>
              </div>
            </div>
            
            <h3 class="section-title">Regulatory Coverage</h3>
            <div class="frameworks">
              <div class="framework">
                <div class="f-header"><span class="f-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/></svg></span><span>CSRD</span></div>
                <div class="f-status"><svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" style="margin-right: 4px;"><path d="M13.5 2L6 9.5 2.5 6 1 7.5l5 5 9-9z"/></svg>Complete</div>
                <div class="f-details">
                  <div>ESRS Standards: All 12</div>
                  <div>Double Materiality: Assessed</div>
                </div>
              </div>
              <div class="framework">
                <div class="f-header"><span class="f-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h8l-1 8 10-12h-8l1-8z"/></svg></span><span>EED</span></div>
                <div class="f-status"><svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" style="margin-right: 4px;"><path d="M13.5 2L6 9.5 2.5 6 1 7.5l5 5 9-9z"/></svg>Complete</div>
                <div class="f-details">
                  <div>Energy Audits: Automated</div>
                  <div>Reporting: Real-time</div>
                </div>
              </div>
              <div class="framework">
                <div class="f-header"><span class="f-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/></svg></span><span>GHG Protocol</span></div>
                <div class="f-status"><svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" style="margin-right: 4px;"><path d="M13.5 2L6 9.5 2.5 6 1 7.5l5 5 9-9z"/></svg>Complete</div>
                <div class="f-details">
                  <div>Scope 1, 2, 3: Tracked</div>
                  <div>Verification: Ready</div>
                </div>
              </div>
            </div>
          </div>
        {:else}
          <div class="forecast-view">
            <h3 class="section-title">2035 Net-Zero Forecast</h3>
            <p class="section-sub">AI-powered emissions trajectory with 94% accuracy</p>
            
            <div class="forecast-chart">
              <svg viewBox="0 0 600 250" width="100%">
                <defs>
                  <linearGradient id="fg" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#2cad84" stop-opacity="0.3"/>
                    <stop offset="100%" stop-color="#2cad84" stop-opacity="0"/>
                  </linearGradient>
                </defs>
                <path d="M 0 200 Q 150 160, 300 100 T 600 30" 
                      stroke="#2cad84" stroke-width="3" fill="none" class="line"/>
                <path d="M 0 200 Q 150 160, 300 100 T 600 30 L 600 250 L 0 250 Z" 
                      fill="url(#fg)"/>
              </svg>
            </div>
            
            <div class="forecast-stats">
              <div class="f-stat">
                <div class="fs-label">Current</div>
                <div class="fs-value">100%</div>
              </div>
              <div class="f-stat">
                <div class="fs-label">2030</div>
                <div class="fs-value">−25%</div>
              </div>
              <div class="f-stat">
                <div class="fs-label">2035</div>
                <div class="fs-value green">−38%</div>
              </div>
            </div>
            
            <div class="forecast-insights">
              <div class="insight">
                <span class="i-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg></span>
                <span>On track for net-zero by 2035</span>
              </div>
              <div class="insight">
                <span class="i-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M2 12h20"/></svg></span>
                <span>12 optimization opportunities identified</span>
              </div>
              <div class="insight">
                <span class="i-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/></svg></span>
                <span>$1.8M additional savings potential</span>
              </div>
            </div>
          </div>
        {/if}
      </div>
      
      <!-- Footer -->
      <div class="modal-footer">
        <div class="footer-left">
          <p class="footer-text">Join 40+ enterprise clients achieving carbon excellence</p>
          <p class="footer-sub">Series A • Backed by leading climate tech investors</p>
        </div>
        <button class="cta-btn" on:click={() => window.location.hash = '#register'}>
          Start Free Trial
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
            <path d="M8 2l6 6-6 6M14 8H2"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  .modal-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.9);
    backdrop-filter: blur(12px);
    z-index: 10000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    animation: fadeIn 0.3s ease;
  }
  
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  .modal-content {
    width: 100%;
    max-width: 1200px;
    max-height: 90vh;
    background: linear-gradient(180deg, #0f1f1a 0%, #0a1412 100%);
    border-radius: 24px;
    border: 1px solid rgba(44,173,132,0.2);
    box-shadow: 0 24px 80px rgba(0,0,0,0.6);
    display: flex;
    flex-direction: column;
    animation: slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
  }
  
  @keyframes slideUp {
    from { opacity: 0; transform: translateY(40px) scale(0.95); }
    to { opacity: 1; transform: translateY(0) scale(1); }
  }
  
  .modal-header {
    padding: 28px 36px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }
  
  .header-left { flex: 1; }
  
  .live-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: rgba(255,255,255,0.6);
    margin-bottom: 10px;
  }
  
  .live-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #2cad84;
    animation: pulse 2s ease-in-out infinite;
  }
  
  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.9); }
  }
  
  .modal-header h2 {
    font-size: 22px;
    font-weight: 600;
    color: rgba(255,255,255,0.95);
    letter-spacing: -0.02em;
    margin: 0 0 6px 0;
  }
  
  .header-subtitle {
    font-size: 15px;
    color: rgba(255,255,255,0.6);
    margin: 0;
  }
  
  .close-btn {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.05);
    color: rgba(255,255,255,0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .close-btn:hover {
    background: rgba(255,255,255,0.1);
    color: rgba(255,255,255,0.95);
    transform: scale(1.05);
  }
  
  .dashboard-tabs {
    display: flex;
    gap: 8px;
    padding: 16px 36px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    background: rgba(0,0,0,0.2);
    overflow-x: auto;
  }
  
  .tab {
    padding: 10px 18px;
    border-radius: 10px;
    border: 1px solid transparent;
    background: transparent;
    color: rgba(255,255,255,0.6);
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
    display: flex;
    align-items: center;
  }
  
  .tab:hover {
    background: rgba(255,255,255,0.05);
    color: rgba(255,255,255,0.8);
  }
  
  .tab.active {
    background: rgba(44,173,132,0.15);
    border-color: rgba(44,173,132,0.3);
    color: #2cad84;
  }
  
  .dashboard-body {
    flex: 1;
    padding: 36px;
    overflow-y: auto;
  }
  
  /* ROI View */
  .roi-hero {
    margin-bottom: 40px;
  }
  
  .mega-stat {
    text-align: center;
    margin-bottom: 32px;
  }
  
  .mega-label {
    font-size: 14px;
    color: rgba(255,255,255,0.6);
    margin-bottom: 12px;
  }
  
  .mega-value {
    font-size: 64px;
    font-weight: 700;
    color: #2cad84;
    letter-spacing: -0.03em;
    line-height: 1;
  }
  
  .unit {
    font-size: 28px;
    color: rgba(255,255,255,0.5);
  }
  
  .mega-sub {
    font-size: 16px;
    color: rgba(255,255,255,0.7);
    margin-top: 8px;
  }
  
  .highlights {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
  }
  
  .highlight {
    padding: 24px;
    border-radius: 16px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    text-align: center;
  }
  
  .h-icon {
    font-size: 32px;
    margin-bottom: 12px;
  }
  
  .h-value {
    font-size: 28px;
    font-weight: 700;
    color: rgba(255,255,255,0.95);
    margin-bottom: 6px;
  }
  
  .h-label {
    font-size: 13px;
    color: rgba(255,255,255,0.6);
  }
  
  .section-title {
    font-size: 24px;
    font-weight: 600;
    color: rgba(255,255,255,0.95);
    margin-bottom: 24px;
  }
  
  .value-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 24px;
  }
  
  .value-card {
    padding: 28px;
    border-radius: 18px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    transition: all 0.3s ease;
  }
  
  .value-card:hover {
    background: rgba(255,255,255,0.05);
    border-color: rgba(44,173,132,0.3);
    transform: translateY(-4px);
  }
  
  .v-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
  }
  
  .v-icon {
    font-size: 28px;
  }
  
  .v-title {
    font-size: 18px;
    font-weight: 600;
    color: rgba(255,255,255,0.9);
  }
  
  .v-metric {
    font-size: 36px;
    font-weight: 700;
    color: #2cad84;
    margin-bottom: 8px;
  }
  
  .v-desc {
    font-size: 14px;
    color: rgba(255,255,255,0.6);
    margin-bottom: 20px;
  }
  
  .v-breakdown {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .b-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 14px;
    color: rgba(255,255,255,0.7);
  }
  
  .badge {
    padding: 4px 10px;
    border-radius: 6px;
    background: rgba(44,173,132,0.2);
    color: #2cad84;
    font-size: 12px;
    font-weight: 600;
  }
  
  /* Real-time View */
  .section-sub {
    font-size: 16px;
    color: rgba(255,255,255,0.6);
    margin-bottom: 32px;
  }
  
  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 32px;
  }
  
  .metric-card {
    padding: 24px;
    border-radius: 16px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
  }
  
  .m-label {
    font-size: 13px;
    color: rgba(255,255,255,0.5);
    margin-bottom: 10px;
  }
  
  .m-value {
    font-size: 32px;
    font-weight: 700;
    color: rgba(255,255,255,0.95);
    margin-bottom: 8px;
  }
  
  .m-unit {
    font-size: 16px;
    font-weight: 400;
    color: rgba(255,255,255,0.5);
  }
  
  .m-trend {
    font-size: 14px;
    font-weight: 600;
  }
  
  .m-trend.positive { color: #2cad84; }
  .m-trend.neutral { color: rgba(255,255,255,0.6); }
  
  .m-status {
    font-size: 14px;
    color: rgba(255,255,255,0.6);
  }
  
  .map-preview {
    padding: 24px;
    border-radius: 16px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
  }
  
  .map-title {
    font-size: 16px;
    font-weight: 600;
    color: rgba(255,255,255,0.9);
    margin-bottom: 16px;
  }
  
  .pulse {
    animation: mapPulse 2s ease-in-out infinite;
  }
  
  @keyframes mapPulse {
    0%, 100% { opacity: 1; r: 8; }
    50% { opacity: 0.6; r: 10; }
  }
  
  /* Compliance View */
  .compliance-hero {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 40px;
    margin-bottom: 40px;
    align-items: center;
  }
  
  .score-card {
    text-align: center;
  }
  
  .score-label {
    font-size: 14px;
    color: rgba(255,255,255,0.6);
    margin-bottom: 16px;
  }
  
  .score-circle {
    margin-bottom: 16px;
  }
  
  .progress {
    transition: stroke-dashoffset 2s ease-out;
  }
  
  .score-text {
    font-size: 48px;
    font-weight: 700;
    fill: #2cad84;
  }
  
  .score-badge {
    padding: 8px 16px;
    border-radius: 8px;
    background: rgba(44,173,132,0.2);
    color: #2cad84;
    font-size: 14px;
    font-weight: 600;
    display: inline-block;
  }
  
  .compliance-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
  }
  
  .c-stat {
    padding: 20px;
    border-radius: 14px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    text-align: center;
  }
  
  .cs-icon {
    font-size: 28px;
    margin-bottom: 12px;
  }
  
  .cs-value {
    font-size: 24px;
    font-weight: 700;
    color: rgba(255,255,255,0.95);
    margin-bottom: 6px;
  }
  
  .cs-label {
    font-size: 13px;
    color: rgba(255,255,255,0.6);
  }
  
  .frameworks {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
  }
  
  .framework {
    padding: 24px;
    border-radius: 16px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
  }
  
  .f-header {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 18px;
    font-weight: 600;
    color: rgba(255,255,255,0.9);
    margin-bottom: 12px;
  }
  
  .f-icon {
    font-size: 24px;
  }
  
  .f-status {
    color: #2cad84;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 16px;
  }
  
  .f-details {
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 13px;
    color: rgba(255,255,255,0.6);
  }
  
  /* Forecast View */
  .forecast-chart {
    padding: 24px;
    border-radius: 16px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 32px;
  }
  
  .line {
    stroke-dasharray: 1000;
    stroke-dashoffset: 1000;
    animation: drawLine 2s ease-out forwards;
  }
  
  @keyframes drawLine {
    to { stroke-dashoffset: 0; }
  }
  
  .forecast-stats {
    display: flex;
    justify-content: space-around;
    gap: 20px;
    margin-bottom: 32px;
  }
  
  .f-stat {
    text-align: center;
  }
  
  .fs-label {
    font-size: 14px;
    color: rgba(255,255,255,0.5);
    margin-bottom: 8px;
  }
  
  .fs-value {
    font-size: 32px;
    font-weight: 700;
    color: rgba(255,255,255,0.9);
  }
  
  .fs-value.green {
    color: #2cad84;
  }
  
  .forecast-insights {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  
  .insight {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 20px;
    border-radius: 12px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    font-size: 15px;
    color: rgba(255,255,255,0.8);
  }
  
  .i-icon {
    font-size: 20px;
  }
  
  /* Footer */
  .modal-footer {
    padding: 28px 36px;
    border-top: 1px solid rgba(255,255,255,0.08);
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(0,0,0,0.3);
  }
  
  .footer-left {
    flex: 1;
  }
  
  .footer-text {
    font-size: 16px;
    color: rgba(255,255,255,0.8);
    margin: 0 0 4px 0;
  }
  
  .footer-sub {
    font-size: 13px;
    color: rgba(255,255,255,0.5);
    margin: 0;
  }
  
  .cta-btn {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px 28px;
    border-radius: 12px;
    background: linear-gradient(135deg, #2cad84, #25967a);
    border: none;
    color: white;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 6px 20px rgba(44,173,132,0.3);
  }
  
  .cta-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(44,173,132,0.4);
  }
  
  @media (max-width: 768px) {
    .modal-content { max-height: 95vh; }
    .modal-header, .dashboard-tabs, .dashboard-body, .modal-footer { padding: 20px; }
    .highlights { grid-template-columns: 1fr; }
    .value-grid { grid-template-columns: 1fr; }
    .metrics-grid { grid-template-columns: 1fr; }
    .compliance-hero { grid-template-columns: 1fr; text-align: center; }
    .compliance-stats { grid-template-columns: 1fr; }
    .frameworks { grid-template-columns: 1fr; }
    .forecast-stats { flex-direction: column; }
    .modal-footer { flex-direction: column; gap: 16px; text-align: center; }
  }
</style>