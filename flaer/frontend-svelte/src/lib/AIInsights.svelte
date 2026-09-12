<script>
  import { onMount } from 'svelte';
  
  let visible = false;
  let activeInsight = 0;
  
  const insights = [
    {
      icon: 'DATA',
      title: 'Data-quality checks',
      desc: 'Review missing utility readings and resolve unusual consumption changes before reporting.',
      metric: '4',
      label: 'items to review',
      trend: 'neutral',
      confidence: 83
    },
    {
      icon: 'GRID',
      title: 'Carbon-intensity outliers',
      desc: 'Compare facilities against the portfolio baseline to prioritise operational investigation.',
      metric: '3',
      label: 'sites above baseline',
      trend: 'up',
      confidence: 78
    },
    {
      icon: 'REPORT',
      title: 'Reporting checklist',
      desc: 'Keep source data, calculation notes, and approvals together for a more defensible export.',
      metric: '8/12',
      label: 'evidence sets complete',
      trend: 'neutral',
      confidence: 67
    },
    {
      icon: 'ACTION',
      title: 'Suggested next action',
      desc: 'Investigate cooling performance at the highest-intensity facility before the next review.',
      metric: '1',
      label: 'priority action',
      trend: 'neutral',
      confidence: 72
    }
  ];
  
  onMount(() => {
    setTimeout(() => { visible = true; }, 200);
    
    // Auto-rotate insights
    const interval = setInterval(() => {
      activeInsight = (activeInsight + 1) % insights.length;
    }, 5000);
    
    return () => clearInterval(interval);
  });
  
  function setInsight(index) {
    activeInsight = index;
  }
</script>

<div class="ai-insights" class:visible>
  <div class="ai-header">
    <div class="ai-badge">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <path d="M8 2l1.5 4.5L14 8l-4.5 1.5L8 14l-1.5-4.5L2 8l4.5-1.5L8 2z" fill="url(#ai-grad)"/>
        <defs>
          <linearGradient id="ai-grad" x1="2" y1="2" x2="14" y2="14">
            <stop offset="0%" stop-color="#2cad84"/>
            <stop offset="100%" stop-color="#7facff"/>
          </linearGradient>
        </defs>
      </svg>
      <span>Portfolio signals</span>
    </div>
    <div class="ai-live">
      <span class="pulse-dot"></span>
      Sample data
    </div>
  </div>
  
  <div class="ai-content">
    {#each insights as insight, i}
      <div class="ai-card" class:active={activeInsight === i}>
        <div class="ai-card-icon">{insight.icon}</div>
        <div class="ai-card-body">
          <h4>{insight.title}</h4>
          <p>{insight.desc}</p>
          <div class="ai-metric">
            <div class="am-value">
              <span class="am-number">{insight.metric}</span>
              <span class="am-label">{insight.label}</span>
            </div>
            <div class="am-confidence">
              <div class="confidence-bar">
                <div class="confidence-fill" style="width: {insight.confidence}%"></div>
              </div>
              <span class="confidence-text">{insight.confidence}% confidence</span>
            </div>
          </div>
        </div>
        <div class="ai-trend" class:up={insight.trend === 'up'} class:down={insight.trend === 'down'}>
          {#if insight.trend === 'up'}
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M5 12l5-5 5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          {:else if insight.trend === 'down'}
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M5 8l5 5 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          {:else}
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M5 10h10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          {/if}
        </div>
      </div>
    {/each}
  </div>
  
  <div class="ai-dots">
    {#each insights as _, i}
      <button 
        class="ai-dot" 
        class:active={activeInsight === i}
        on:click={() => setInsight(i)}
        aria-label="View insight {i + 1}"
      ></button>
    {/each}
  </div>
  
  <div class="ai-footer">
    <span class="footer-powered">
      In-product
      <span class="footer-logo">
        <svg width="16" height="16" viewBox="0 0 20 20" fill="none">
          <path d="M10 2L3 7v6c0 4.418 3.134 7.849 7 8 3.866-.151 7-3.582 7-8V7l-7-5z" fill="url(#footer-ai-gradient)" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/>
          <defs>
            <linearGradient id="footer-ai-gradient" x1="3" y1="2" x2="17" y2="18" gradientUnits="userSpaceOnUse">
              <stop stop-color="#2cad84"/>
              <stop offset="1" stop-color="#7facff"/>
            </linearGradient>
          </defs>
        </svg>
      </span>
      guidance
    </span>
    <span class="ai-update">Illustrative workflow</span>
  </div>
</div>

<style>
  .ai-insights {
    position: relative;
    padding: 24px;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(44,173,132,0.08) 0%, rgba(127,172,255,0.08) 100%);
    border: 1.5px solid rgba(44,173,132,0.2);
    backdrop-filter: blur(20px);
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  }
  
  .ai-insights.visible {
    opacity: 1;
    transform: translateY(0);
  }
  
  .ai-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .ai-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px;
    border-radius: 999px;
    background: rgba(44,173,132,0.12);
    border: 1px solid rgba(44,173,132,0.25);
    font-size: 12px;
    font-weight: 800;
    color: #2cad84;
  }
  
  .ai-live {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-weight: 700;
    color: rgba(244,247,245,0.6);
  }
  
  .pulse-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #2cad84;
    animation: pulse 2s ease-in-out infinite;
  }
  
  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.2); }
  }
  
  .ai-content {
    position: relative;
    height: 240px;
    margin-bottom: 16px;
  }
  
  .ai-card {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    padding: 20px;
    border-radius: 16px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    opacity: 0;
    transform: translateX(20px);
    transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    pointer-events: none;
  }
  
  .ai-card.active {
    opacity: 1;
    transform: translateX(0);
    pointer-events: auto;
  }
  
  .ai-card-icon {
    font-size: 32px;
    margin-bottom: 12px;
  }
  
  .ai-card-body h4 {
    font-size: 16px;
    font-weight: 900;
    color: #f4f7f5;
    margin-bottom: 8px;
    letter-spacing: -0.02em;
  }
  
  .ai-card-body p {
    font-size: 13px;
    line-height: 1.5;
    color: rgba(244,247,245,0.7);
    margin-bottom: 16px;
  }
  
  .ai-metric {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 16px;
  }
  
  .am-value {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  
  .am-number {
    font-size: 28px;
    font-weight: 900;
    color: #2cad84;
    letter-spacing: -0.03em;
  }
  
  .am-label {
    font-size: 11px;
    font-weight: 700;
    color: rgba(244,247,245,0.5);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  
  .am-confidence {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  
  .confidence-bar {
    height: 6px;
    border-radius: 999px;
    background: rgba(255,255,255,0.1);
    overflow: hidden;
  }
  
  .confidence-fill {
    height: 100%;
    background: linear-gradient(90deg, #2cad84, #7facff);
    border-radius: 999px;
    transition: width 0.8s cubic-bezier(0.16, 1, 0.3, 1);
  }
  
  .confidence-text {
    font-size: 10px;
    font-weight: 700;
    color: rgba(244,247,245,0.5);
    text-align: right;
  }
  
  .ai-trend {
    position: absolute;
    top: 20px;
    right: 20px;
    width: 40px;
    height: 40px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
  }
  
  .ai-trend.up {
    color: #2cad84;
    background: rgba(44,173,132,0.12);
    border-color: rgba(44,173,132,0.25);
  }
  
  .ai-trend.down {
    color: #d35d5c;
    background: rgba(211,93,92,0.12);
    border-color: rgba(211,93,92,0.25);
  }
  
  .ai-dots {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-bottom: 16px;
  }
  
  .ai-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: rgba(255,255,255,0.2);
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    padding: 0;
  }
  
  .ai-dot:hover {
    background: rgba(255,255,255,0.4);
    transform: scale(1.2);
  }
  
  .ai-dot.active {
    background: #2cad84;
    width: 24px;
    border-radius: 999px;
  }
  
  .ai-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 16px;
    border-top: 1px solid rgba(255,255,255,0.08);
    font-size: 11px;
    font-weight: 700;
    color: rgba(244,247,245,0.5);
  }
  
  .footer-powered {
    display: flex;
    align-items: center;
    gap: 6px;
  }
  
  .footer-logo {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 16px;
    height: 16px;
  }
  
  .footer-logo svg {
    width: 100%;
    height: 100%;
    color: rgba(244,247,245,0.6);
  }
  
  .ai-update {
    color: rgba(244,247,245,0.4);
  }
  
  @media (max-width: 768px) {
    .ai-insights {
      padding: 20px;
    }
    
    .ai-content {
      height: 280px;
    }
    
    .ai-card-body h4 {
      font-size: 15px;
    }
    
    .am-number {
      font-size: 24px;
    }
  }
</style>
