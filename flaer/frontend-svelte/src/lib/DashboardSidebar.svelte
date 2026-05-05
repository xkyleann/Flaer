<script>
  export let activeScreen = 'portfolio';
  export let setScreen;

  let showAddDataCenter = false;

  const portfolioItems = [
    {
      id: 'portfolio',
      title: 'Overview',
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="7" stroke="#2cad84" stroke-width="1.6"/><ellipse cx="10" cy="10" rx="3.5" ry="7" stroke="#2cad84" stroke-width="1.2"/><line x1="3" y1="10" x2="17" y2="10" stroke="#2cad84" stroke-width="1.2"/></svg>`
    },
    {
      id: 'datacenters',
      title: 'Data centers',
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><rect x="2" y="4" width="16" height="12" rx="2" stroke="#2cad84" stroke-width="1.5"/><line x1="2" y1="8" x2="18" y2="8" stroke="#2cad84" stroke-width="1"/><line x1="2" y1="12" x2="18" y2="12" stroke="#2cad84" stroke-width="1"/><circle cx="5" cy="6" r="1" fill="#2cad84"/><circle cx="5" cy="10" r="1" fill="#2cad84"/><circle cx="5" cy="14" r="1" fill="#2cad84"/></svg>`
    },
    {
      id: 'globalmap',
      title: 'Map',
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="7" stroke="#2cad84" stroke-width="1.6"/><ellipse cx="10" cy="10" rx="3.5" ry="7" stroke="#2cad84" stroke-width="1.2"/><line x1="3" y1="10" x2="17" y2="10" stroke="#2cad84" stroke-width="1.2"/></svg>`
    },
    {
      id: 'facilities',
      title: 'Facilities',
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><path d="M10 2L2 6V18H18V6L10 2Z" stroke="#2cad84" stroke-width="1.4" fill="none"/><line x1="10" y1="2" x2="10" y2="18" stroke="#2cad84" stroke-width="1.2"/></svg>`
    },
    {
      id: 'reports',
      title: 'Reports',
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><rect x="4" y="2" width="12" height="16" rx="2" stroke="#2cad84" stroke-width="1.6"/><line x1="7" y1="6" x2="13" y2="6" stroke="#2cad84" stroke-width="1.3" stroke-linecap="round"/><line x1="7" y1="9" x2="13" y2="9" stroke="#2cad84" stroke-width="1.3" stroke-linecap="round"/><line x1="7" y1="12" x2="11" y2="12" stroke="#2cad84" stroke-width="1.3" stroke-linecap="round"/></svg>`
    },
    {
      id: 'alerts',
      title: 'Alerts',
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><path d="M10 2L2 6V10C2 15 10 18 10 18S18 15 18 10V6L10 2Z" stroke="#2cad84" stroke-width="1.4" fill="none"/><circle cx="10" cy="11" r="1.5" fill="#2cad84"/></svg>`
    }
  ];

  const analyticsItems = [
    {
      id: 'performance',
      title: 'Performance',
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><polyline points="2,14 6,8 10,11 18,3" stroke="#7faeff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>`
    },
    {
      id: 'emissions',
      title: 'Emissions',
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><path d="M8 14C8 12.5 7 11 5 11C3 11 2 12.5 2 14H8Z" stroke="#7faeff" stroke-width="1.4" fill="none"/><path d="M14 10C14 8 13 6 11 6C9 6 8 8 8 10H14Z" stroke="#7faeff" stroke-width="1.4" fill="none"/><path d="M18 14C18 12 17 10 15 10C13 10 12 12 12 14H18Z" stroke="#7faeff" stroke-width="1.4" fill="none"/></svg>`
    },
    {
      id: 'water',
      title: 'Water',
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><path d="M10 2C10 2 7 6 7 9C7 11.76 8.34 14 10 14C11.66 14 13 11.76 13 9C13 6 10 2 10 2Z" stroke="#7faeff" stroke-width="1.4" fill="none"/></svg>`
    },
    {
      id: 'energy',
      title: 'Energy',
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><path d="M8 2L12 10H9L11 18L3 8H7L8 2Z" stroke="#7faeff" stroke-width="1.4" fill="none" stroke-linejoin="round"/></svg>`
    },
    {
      id: 'benchmark',
      title: 'Benchmarks',
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><rect x="2" y="4" width="16" height="12" rx="2" stroke="#7faeff" stroke-width="1.5"/><line x1="7" y1="8" x2="7" y2="14" stroke="#7faeff" stroke-width="1.2" stroke-linecap="round"/><line x1="10" y1="6" x2="10" y2="14" stroke="#7faeff" stroke-width="1.2" stroke-linecap="round"/><line x1="13" y1="10" x2="13" y2="14" stroke="#7faeff" stroke-width="1.2" stroke-linecap="round"/></svg>`
    }
  ];

  const optimizeItems = [
    {
      id: 'actions',
      title: 'Recommendations',
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><rect x="2" y="12" width="4" height="6" rx="1" fill="#b79563" opacity="0.5"/><rect x="8" y="7" width="4" height="11" rx="1" fill="#b79563" opacity="0.75"/><rect x="14" y="2" width="4" height="16" rx="1" fill="#b79563"/></svg>`
    },
    {
      id: 'forecast',
      title: 'Scenarios',
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><polyline points="2,16 6,9 11,12 18,4" stroke="#b79563" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>`
    },
    {
      id: 'targets',
      title: 'Targets',
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="8" stroke="#b79563" stroke-width="1.2"/><circle cx="10" cy="10" r="5" stroke="#b79563" stroke-width="1.2"/><circle cx="10" cy="10" r="2" fill="#b79563"/></svg>`
    }
  ];

  const dataItems = [
    {
      id: 'integrations',
      title: 'Integrations',
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><rect x="2" y="2" width="6" height="6" rx="1" stroke="#9fa8b8" stroke-width="1.2"/><rect x="12" y="2" width="6" height="6" rx="1" stroke="#9fa8b8" stroke-width="1.2"/><rect x="2" y="12" width="6" height="6" rx="1" stroke="#9fa8b8" stroke-width="1.2"/><rect x="12" y="12" width="6" height="6" rx="1" stroke="#9fa8b8" stroke-width="1.2"/><line x1="8" y1="5" x2="12" y2="5" stroke="#9fa8b8" stroke-width="1"/><line x1="5" y1="8" x2="5" y2="12" stroke="#9fa8b8" stroke-width="1"/></svg>`
    },
    {
      id: 'uploads',
      title: 'Uploads',
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><path d="M10 3V13M10 13L6 9M10 13L14 9" stroke="#9fa8b8" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/><rect x="2" y="15" width="16" height="2" rx="1" fill="#9fa8b8" opacity="0.5"/></svg>`
    },
    {
      id: 'api',
      title: 'API',
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><circle cx="4" cy="10" r="2" stroke="#9fa8b8" stroke-width="1.2"/><circle cx="10" cy="10" r="2" stroke="#9fa8b8" stroke-width="1.2"/><circle cx="16" cy="10" r="2" stroke="#9fa8b8" stroke-width="1.2"/><line x1="6" y1="10" x2="8" y2="10" stroke="#9fa8b8" stroke-width="1"/><line x1="12" y1="10" x2="14" y2="10" stroke="#9fa8b8" stroke-width="1"/></svg>`
    }
  ];

  const adminItems = [
    {
      id: 'team',
      title: 'Team',
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><circle cx="6" cy="5" r="2" stroke="#9fa8b8" stroke-width="1.2"/><circle cx="14" cy="5" r="2" stroke="#9fa8b8" stroke-width="1.2"/><path d="M2 16C2 13 4 12 6 12C8 12 10 13 10 16" stroke="#9fa8b8" stroke-width="1.2" fill="none" stroke-linecap="round"/><path d="M10 16C10 13 12 12 14 12C16 12 18 13 18 16" stroke="#9fa8b8" stroke-width="1.2" fill="none" stroke-linecap="round"/></svg>`
    },
    {
      id: 'settings',
      title: 'Settings',
      icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="2.5" stroke="#9fa8b8" stroke-width="1.2"/><circle cx="10" cy="10" r="7" stroke="#9fa8b8" stroke-width="1.2"/><line x1="10" y1="1" x2="10" y2="3" stroke="#9fa8b8" stroke-width="1.2"/><line x1="10" y1="17" x2="10" y2="19" stroke="#9fa8b8" stroke-width="1.2"/></svg>`
    }
  ];

  function toggleAddDataCenter() {
    showAddDataCenter = !showAddDataCenter;
  }
</script>

<aside class="sidebar">
  <div class="health-card">
    <div class="health-label">Portfolio health score</div>
    <div class="health-score">72 <span>/ 100</span></div>
    <div class="health-sub">Moderate exposure — 14 sites require action</div>
    <div class="health-bar"><div class="health-fill"></div></div>
  </div>

  <!-- PORTFOLIO SECTION -->
  <div class="nav-section">
    <div class="nav-section-label">PORTFOLIO</div>
    {#each portfolioItems as item}
      <button
        class="nav-item"
        class:active={activeScreen === item.id}
        on:click={() => setScreen(item.id)}
      >
        <div class="nav-icon">{@html item.icon}</div>
        <span class="nav-item-title">{item.title}</span>
      </button>
    {/each}
    <button class="nav-item add-dc-btn" on:click={toggleAddDataCenter}>
      <div class="nav-icon add-icon">+</div>
      <span class="nav-item-title">Add data center</span>
    </button>
  </div>

  <!-- ANALYTICS SECTION -->
  <div class="nav-section">
    <div class="nav-section-label">ANALYTICS</div>
    {#each analyticsItems as item}
      <button
        class="nav-item"
        class:active={activeScreen === item.id}
        on:click={() => setScreen(item.id)}
      >
        <div class="nav-icon">{@html item.icon}</div>
        <span class="nav-item-title">{item.title}</span>
      </button>
    {/each}
  </div>

  <!-- PLAN & OPTIMIZE SECTION -->
  <div class="nav-section">
    <div class="nav-section-label">PLAN & OPTIMIZE</div>
    {#each optimizeItems as item}
      <button
        class="nav-item"
        class:active={activeScreen === item.id}
        on:click={() => setScreen(item.id)}
      >
        <div class="nav-icon">{@html item.icon}</div>
        <span class="nav-item-title">{item.title}</span>
      </button>
    {/each}
  </div>

  <!-- DATA SECTION -->
  <div class="nav-section">
    <div class="nav-section-label">DATA</div>
    {#each dataItems as item}
      <button
        class="nav-item"
        class:active={activeScreen === item.id}
        on:click={() => setScreen(item.id)}
      >
        <div class="nav-icon">{@html item.icon}</div>
        <span class="nav-item-title">{item.title}</span>
      </button>
    {/each}
  </div>

  <!-- ADMIN SECTION -->
  <div class="nav-section">
    <div class="nav-section-label">ADMIN</div>
    {#each adminItems as item}
      <button
        class="nav-item"
        class:active={activeScreen === item.id}
        on:click={() => setScreen(item.id)}
      >
        <div class="nav-icon">{@html item.icon}</div>
        <span class="nav-item-title">{item.title}</span>
      </button>
    {/each}
  </div>
</aside>

<!-- ADD DATA CENTER MODAL -->
{#if showAddDataCenter}
  <div class="modal-backdrop" on:click={toggleAddDataCenter}>
    <div class="modal-content" on:click|stopPropagation>
      <div class="modal-header">
        <h2>Add data center</h2>
        <p>Register a new data center to your portfolio. All fields marked with <span class="required">*</span> are required.</p>
        <button class="modal-close" on:click={toggleAddDataCenter}>×</button>
      </div>
      
      <div class="modal-steps">
        <div class="step-indicator active">1. Location</div>
        <div class="step-indicator">2. Details</div>
        <div class="step-indicator">3. Capacity & Infrastructure</div>
        <div class="step-indicator">4. Sustainability</div>
        <div class="step-indicator">5. Review</div>
      </div>

      <div class="modal-form">
        <div class="form-section">
          <label>
            Search address <span class="required">*</span>
            <div class="search-input">
              <svg width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="9" cy="9" r="6"/><path d="M13 13L18 18"/>
              </svg>
              <input type="text" placeholder="Frankfurt, Germany" />
              <button>×</button>
            </div>
          </label>

          <label>
            Address <span class="required">*</span>
            <input type="text" placeholder="Enter full address" />
          </label>

          <div class="form-row">
            <label>
              City <span class="required">*</span>
              <input type="text" placeholder="Frankfurt" />
            </label>
            <label>
              Country <span class="required">*</span>
              <select>
                <option>Germany</option>
                <option>United States</option>
                <option>United Kingdom</option>
              </select>
            </label>
            <label>
              Region
              <select>
                <option>Hessen</option>
              </select>
            </label>
          </div>

          <div class="form-row">
            <label>
              Latitude <span class="required">*</span>
              <input type="number" placeholder="50.1109" />
            </label>
            <label>
              Longitude <span class="required">*</span>
              <input type="number" placeholder="8.6821" />
            </label>
            <label>
              Time zone
              <select>
                <option>Europe/Berlin (CET)</option>
              </select>
            </label>
          </div>

          <div class="quick-info">
            <div class="info-item">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="3" y="3" width="14" height="14" rx="2"/>
                <line x1="10" y1="7" x2="10" y2="13"/>
                <line x1="7" y1="10" x2="13" y2="10"/>
              </svg>
              <span>Grid region: DE-LU</span>
            </div>
            <div class="info-item">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M10 2L12 8H18L13.5 11.5L15.5 18L10 14.5L4.5 18L6.5 11.5L2 8H8L10 2Z" fill="currentColor"/>
              </svg>
              <span>Regulatory region: EU</span>
            </div>
            <div class="info-item">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M3 10C3 6.5 5.5 3.5 8.5 3.5C10 3.5 11 4.5 12 6C13 4.5 14 3.5 15.5 3.5C18.5 3.5 21 6.5 21 10C21 15 13 20 12 20C11 20 3 15 3 10Z"/>
              </svg>
              <span>Water stress: Low (10%)</span>
            </div>
            <div class="info-item">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M10 2C10 2 7 6 7 9C7 11.76 8.34 14 10 14C11.66 14 13 11.76 13 9C13 6 10 2 10 2Z" fill="currentColor"/>
              </svg>
              <span>Grid carbon intensity: 127 gCO₂e/kWh (2024 avg)</span>
            </div>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn-secondary" on:click={toggleAddDataCenter}>Cancel</button>
        <button class="btn-primary">Next: Details →</button>
      </div>
    </div>
  </div>
{/if}

<style>
  .sidebar {
    border-right: 1px solid rgba(255,255,255,0.06);
    background: rgba(0,0,0,0.3);
    padding: 16px 12px;
    position: sticky;
    top: 60px;
    height: calc(100vh - 60px);
    overflow-y: auto;
    overflow-x: hidden;
    display: flex;
    flex-direction: column;
    gap: 0;
    scrollbar-width: thin;
    scrollbar-color: rgba(255,255,255,0.1) transparent;
    max-width: 240px;
  }

  .health-card {
    padding: 16px 12px;
    border-radius: 16px;
    background: linear-gradient(135deg, rgba(44,173,132,0.1), rgba(127,174,255,0.05));
    border: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 20px;
  }

  .health-label {
    font-size: 11px;
    color: rgba(255,255,255,0.6);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
    font-weight: 600;
  }

  .health-score {
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 8px;
  }

  .health-score span {
    font-size: 16px;
    color: #2cad84;
    font-weight: 600;
    margin-left: 4px;
  }

  .health-sub {
    font-size: 11px;
    color: rgba(255,255,255,0.6);
    margin-bottom: 12px;
    line-height: 1.4;
  }

  .health-bar {
    height: 4px;
    border-radius: 999px;
    background: rgba(255,255,255,0.1);
    overflow: hidden;
  }

  .health-fill {
    height: 100%;
    background: linear-gradient(90deg, #2cad84, #5c93ff);
    width: 72%;
    box-shadow: 0 0 8px rgba(44,173,132,0.4);
  }

  .nav-section {
    margin-bottom: 18px;
  }

  .nav-section-label {
    padding: 12px 10px 8px;
    color: rgba(255,255,255,0.4);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  .nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 10px;
    border-radius: 12px;
    margin-bottom: 4px;
    color: rgba(255,255,255,0.7);
    border: 1px solid transparent;
    cursor: pointer;
    background: transparent;
    width: 100%;
    text-align: left;
    font-family: inherit;
    font-size: 14px;
    transition: all 0.16s ease;
  }

  .nav-item:hover {
    background: rgba(255,255,255,0.08);
    color: rgba(255,255,255,0.9);
  }

  .nav-item.active {
    background: rgba(44,173,132,0.15);
    border-color: rgba(44,173,132,0.3);
    color: #2cad84;
  }

  .nav-item.add-dc-btn {
    background: rgba(44,173,132,0.08);
    border: 1px dashed rgba(44,173,132,0.3);
    color: #2cad84;
  }

  .nav-item.add-dc-btn:hover {
    background: rgba(44,173,132,0.15);
    border-color: rgba(44,173,132,0.5);
  }

  .nav-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: grid;
    place-items: center;
    flex-shrink: 0;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    font-size: 14px;
    font-weight: 600;
  }

  .nav-item.active .nav-icon {
    background: rgba(44,173,132,0.2);
    border-color: rgba(44,173,132,0.4);
    color: #2cad84;
  }

  .nav-item-title {
    font-size: 13px;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* MODAL STYLES */
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.6);
    display: grid;
    place-items: center;
    z-index: 1000;
    animation: fadeIn 0.2s ease;
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .modal-content {
    background: #1a1f2e;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    width: 90%;
    max-width: 700px;
    max-height: 85vh;
    display: flex;
    flex-direction: column;
    animation: slideUp 0.3s ease;
  }

  @keyframes slideUp {
    from { transform: translateY(40px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }

  .modal-header {
    padding: 24px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    position: relative;
  }

  .modal-header h2 {
    margin: 0 0 8px;
    font-size: 24px;
    color: #ffffff;
  }

  .modal-header p {
    margin: 0;
    font-size: 14px;
    color: rgba(255,255,255,0.6);
  }

  .required {
    color: #ff6b6b;
  }

  .modal-close {
    position: absolute;
    top: 20px;
    right: 20px;
    width: 32px;
    height: 32px;
    border: none;
    background: rgba(255,255,255,0.1);
    color: #ffffff;
    font-size: 24px;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s;
  }

  .modal-close:hover {
    background: rgba(255,255,255,0.15);
  }

  .modal-steps {
    display: flex;
    padding: 0 24px;
    gap: 12px;
    padding-top: 20px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding-bottom: 20px;
    overflow-x: auto;
  }

  .step-indicator {
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px;
    white-space: nowrap;
    background: rgba(255,255,255,0.08);
    color: rgba(255,255,255,0.5);
    border: 1px solid rgba(255,255,255,0.1);
  }

  .step-indicator.active {
    background: rgba(44,173,132,0.15);
    color: #2cad84;
    border-color: rgba(44,173,132,0.3);
  }

  .modal-form {
    flex: 1;
    overflow-y: auto;
    padding: 24px;
  }

  .form-section {
    display: grid;
    gap: 16px;
  }

  label {
    display: grid;
    gap: 8px;
    font-size: 13px;
    font-weight: 600;
    color: #ffffff;
  }

  input[type="text"],
  input[type="number"],
  select {
    padding: 11px 14px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.12);
    background: rgba(255,255,255,0.04);
    color: #ffffff;
    font-size: 13px;
    font-family: inherit;
    transition: border-color 0.2s, background 0.2s;
  }

  input[type="text"]:focus,
  input[type="number"]:focus,
  select:focus {
    outline: none;
    border-color: rgba(44,173,132,0.5);
    background: rgba(44,173,132,0.08);
  }

  input::placeholder {
    color: rgba(255,255,255,0.3);
  }

  .search-input {
    position: relative;
    display: flex;
    align-items: center;
  }

  .search-input svg {
    position: absolute;
    left: 12px;
    color: rgba(255,255,255,0.4);
    pointer-events: none;
  }

  .search-input input {
    width: 100%;
    padding-left: 38px;
  }

  .search-input button {
    position: absolute;
    right: 10px;
    background: none;
    border: none;
    color: rgba(255,255,255,0.4);
    cursor: pointer;
    font-size: 18px;
  }

  .form-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
  }

  .quick-info {
    display: grid;
    gap: 10px;
    padding: 16px;
    background: rgba(44,173,132,0.08);
    border: 1px solid rgba(44,173,132,0.2);
    border-radius: 12px;
    margin-top: 8px;
  }

  .info-item {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 12px;
    color: rgba(255,255,255,0.7);
  }

  .info-item svg {
    width: 18px;
    height: 18px;
    flex-shrink: 0;
    color: #2cad84;
  }

  .modal-footer {
    display: flex;
    gap: 12px;
    padding: 20px 24px;
    border-top: 1px solid rgba(255,255,255,0.06);
  }

  .btn-secondary,
  .btn-primary {
    flex: 1;
    padding: 12px 20px;
    border: none;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.2s;
  }

  .btn-secondary {
    background: rgba(255,255,255,0.08);
    color: #ffffff;
    border: 1px solid rgba(255,255,255,0.12);
  }

  .btn-secondary:hover {
    background: rgba(255,255,255,0.12);
  }

  .btn-primary {
    background: linear-gradient(135deg, #2cad84, #1e8f60);
    color: #ffffff;
  }

  .btn-primary:hover {
    filter: brightness(1.1);
  }
</style>
