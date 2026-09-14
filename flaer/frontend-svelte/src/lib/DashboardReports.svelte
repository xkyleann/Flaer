<script>
  import { dataCenters } from './data.js';
  
  let selectedDataCenter = 'us-east-1';
  let reportType = 'comprehensive';
  let timeframe = 'annual';
  let generating = false;
  let reportGenerated = false;
  
  const reportTypes = [
    { id: 'comprehensive', name: 'Sustainability data brief', desc: 'Structure for verified operational inputs' },
    { id: 'csrd', name: 'CSRD readiness checklist', desc: 'Identify evidence needed for CSRD reporting' },
    { id: 'eed', name: 'EED readiness checklist', desc: 'Identify energy reporting evidence needed' },
    { id: 'sfdr', name: 'SFDR input checklist', desc: 'Identify sustainability-finance data gaps' },
    { id: 'carbon-footprint', name: 'Carbon Footprint Analysis', desc: 'Detailed emissions breakdown and trends' },
    { id: 'water-usage', name: 'Water Usage Report', desc: 'WUE metrics and water consumption analysis' },
  ];
  
  const timeframes = [
    { id: 'monthly', name: 'Monthly', period: 'Last 30 days' },
    { id: 'quarterly', name: 'Quarterly', period: 'Last 90 days' },
    { id: 'annual', name: 'Annual', period: 'Last 12 months' },
    { id: 'custom', name: 'Custom Range', period: 'Select dates' },
  ];
  
  function generateReport() {
    generating = true;
    // Simulate report generation
    setTimeout(() => {
      generating = false;
      reportGenerated = true;
    }, 2000);
  }
  
  async function downloadReport(format) {
    const type = reportTypes.find((report) => report.id === reportType)?.name;
    const payload = {
      document_status: 'draft_workspace_output',
      facility: selectedDC?.name,
      report_type: type,
      timeframe: timeframes.find((item) => item.id === timeframe)?.name,
      generated_at: new Date().toISOString(),
      notice: 'This draft contains illustrative structure only. Verify all operational and compliance data before external use.'
    };
    const filename = `flaer-${reportType}-${selectedDataCenter}`;
    let blob;
    if (format === 'json') {
      blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    } else if (format === 'excel') {
      const rows = Object.entries(payload).map(([key, value]) => `${key},"${String(value).replaceAll('"', '""')}"`);
      blob = new Blob([`field,value\n${rows.join('\n')}`], { type: 'text/csv;charset=utf-8' });
    } else {
      const { default: jsPDF } = await import('jspdf');
      const pdf = new jsPDF();
      pdf.setFontSize(18); pdf.text('Flaer draft report', 16, 20);
      pdf.setFontSize(10); pdf.text(`Facility: ${payload.facility}`, 16, 32);
      pdf.text(`Report type: ${payload.report_type}`, 16, 39);
      pdf.text(`Timeframe: ${payload.timeframe}`, 16, 46);
      const lines = pdf.splitTextToSize(payload.notice, 176);
      pdf.text(lines, 16, 60);
      pdf.save(`${filename}.pdf`);
      return;
    }
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url; link.download = `${filename}.${format === 'excel' ? 'csv' : 'json'}`;
    document.body.appendChild(link); link.click(); link.remove(); URL.revokeObjectURL(url);
  }
  
  $: selectedDC = dataCenters.find(dc => dc.id === selectedDataCenter);
</script>

<div class="reports-container">
  <div class="report-status"><span></span><div><strong>Draft workspace only.</strong> A generated document is not a compliance report or certification. Connect authorised operational data and obtain expert review before external use.</div></div>
  <!-- Report Configuration -->
  <div class="config-section">
    <div class="config-card">
      <h3>Report Configuration</h3>
      
      <div class="form-group">
        <label>Select Data Center</label>
        <select bind:value={selectedDataCenter} class="select-input">
          {#each dataCenters as dc}
            <option value={dc.id}>{dc.name} ({dc.region})</option>
          {/each}
        </select>
      </div>
      
      <div class="form-group">
        <label>Report Type</label>
        <div class="report-types">
          {#each reportTypes as type}
            <div 
              class="report-type-card" 
              class:selected={reportType === type.id}
              on:click={() => reportType = type.id}
              on:keypress={(e) => e.key === 'Enter' && (reportType = type.id)}
              role="button"
              tabindex="0"
            >
              <div class="type-name">{type.name}</div>
              <div class="type-desc">{type.desc}</div>
            </div>
          {/each}
        </div>
      </div>
      
      <div class="form-group">
        <label>Timeframe</label>
        <div class="timeframe-options">
          {#each timeframes as tf}
            <button 
              class="timeframe-btn" 
              class:active={timeframe === tf.id}
              on:click={() => timeframe = tf.id}
            >
              <div class="tf-name">{tf.name}</div>
              <div class="tf-period">{tf.period}</div>
            </button>
          {/each}
        </div>
      </div>
      
      <button class="generate-btn" on:click={generateReport} disabled={generating}>
        {#if generating}
          <span class="spinner"></span>
          Generating Report...
        {:else}
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" stroke-width="2"/>
            <polyline points="14 2 14 8 20 8" stroke="currentColor" stroke-width="2"/>
            <line x1="12" y1="18" x2="12" y2="12" stroke="currentColor" stroke-width="2"/>
            <line x1="9" y1="15" x2="15" y2="15" stroke="currentColor" stroke-width="2"/>
          </svg>
          Generate Report
        {/if}
      </button>
    </div>
  </div>
  
  <!-- Report Preview/Results -->
  <div class="preview-section">
    {#if reportGenerated}
      <div class="report-preview">
        <div class="preview-header">
          <h3>Draft report structure</h3>
          <div class="preview-meta">
            <span class="meta-item">{selectedDC?.name}</span>
            <span class="meta-divider">•</span>
            <span class="meta-item">{reportTypes.find(r => r.id === reportType)?.name}</span>
            <span class="meta-divider">•</span>
            <span class="meta-item">{timeframes.find(t => t.id === timeframe)?.name}</span>
          </div>
        </div>
        
        <div class="report-content">
          <!-- Executive Summary -->
          <div class="report-section">
            <h4>Input summary — requires verification</h4>
            <div class="summary-grid">
              <div class="summary-card">
                <div class="summary-label">Total Carbon Emissions</div>
                <div class="summary-value">{(selectedDC?.intensity * 8760 * 0.5).toLocaleString()} tCO₂e</div>
                <div class="summary-trend negative">Awaiting verified meter data</div>
              </div>
              <div class="summary-card">
                <div class="summary-label">Renewable Energy %</div>
                <div class="summary-value">{Math.round(100 - (selectedDC?.intensity / 10))}%</div>
                <div class="summary-trend positive">Awaiting energy-procurement evidence</div>
              </div>
              <div class="summary-card">
                <div class="summary-label">PUE (Power Usage Effectiveness)</div>
                <div class="summary-value">1.{Math.floor(Math.random() * 3 + 2)}</div>
                <div class="summary-trend positive">Awaiting facility telemetry</div>
              </div>
              <div class="summary-card">
                <div class="summary-label">WUE (Water Usage Effectiveness)</div>
                <div class="summary-value">0.{Math.floor(Math.random() * 9 + 1)} L/kWh</div>
                <div class="summary-trend positive">Awaiting water-meter data</div>
              </div>
            </div>
          </div>
          
          <!-- Climate Impact Metrics -->
          <div class="report-section">
            <h4>Climate Impact Metrics</h4>
            <div class="metrics-list">
              <div class="metric-row">
                <span class="metric-label">Scope 1 Emissions (Direct)</span>
                <span class="metric-value">245 tCO₂e</span>
              </div>
              <div class="metric-row">
                <span class="metric-label">Scope 2 Emissions (Electricity)</span>
                <span class="metric-value">{(selectedDC?.intensity * 8760 * 0.45).toLocaleString()} tCO₂e</span>
              </div>
              <div class="metric-row">
                <span class="metric-label">Scope 3 Emissions (Indirect)</span>
                <span class="metric-value">1,234 tCO₂e</span>
              </div>
              <div class="metric-row">
                <span class="metric-label">Carbon Intensity</span>
                <span class="metric-value">{selectedDC?.intensity} gCO₂/kWh</span>
              </div>
              <div class="metric-row">
                <span class="metric-label">Equivalent to</span>
                <span class="metric-value">{Math.round(selectedDC?.intensity * 8760 * 0.5 / 4.6)} cars off the road</span>
              </div>
            </div>
          </div>
          
          <!-- Compliance Status -->
          <div class="report-section">
            <h4>Regulatory evidence status</h4>
            <div class="compliance-grid">
              <div class="compliance-card compliant">
                <div class="compliance-icon">?</div>
                <div class="compliance-name">CSRD</div>
                <div class="compliance-status">Not assessed</div>
              </div>
              <div class="compliance-card compliant">
                <div class="compliance-icon">?</div>
                <div class="compliance-name">EED</div>
                <div class="compliance-status">Not assessed</div>
              </div>
              <div class="compliance-card warning">
                <div class="compliance-icon">!</div>
                <div class="compliance-name">SFDR</div>
                <div class="compliance-status">Evidence required</div>
              </div>
              <div class="compliance-card compliant">
                <div class="compliance-icon">?</div>
                <div class="compliance-name">ISO 14001</div>
                <div class="compliance-status">Not assessed</div>
              </div>
            </div>
          </div>
          
          <!-- Recommendations -->
          <div class="report-section">
            <h4>Recommendations</h4>
            <div class="recommendations-list">
              <div class="recommendation-item">
                <div class="rec-priority high">High Priority</div>
                <div class="rec-text">Increase renewable energy procurement to 85% by Q4 2026</div>
                <div class="rec-impact">Potential reduction: 2,450 tCO₂e/year</div>
              </div>
              <div class="recommendation-item">
                <div class="rec-priority medium">Medium Priority</div>
                <div class="rec-text">Implement advanced cooling optimization to improve PUE to 1.2</div>
                <div class="rec-impact">Potential reduction: 890 tCO₂e/year</div>
              </div>
              <div class="recommendation-item">
                <div class="rec-priority medium">Medium Priority</div>
                <div class="rec-text">Deploy water recycling system to reduce WUE by 30%</div>
                <div class="rec-impact">Water savings: 45,000 L/day</div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="report-actions">
          <button class="action-btn" on:click={() => downloadReport('pdf')}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke="currentColor" stroke-width="2"/>
              <polyline points="7 10 12 15 17 10" stroke="currentColor" stroke-width="2"/>
              <line x1="12" y1="15" x2="12" y2="3" stroke="currentColor" stroke-width="2"/>
            </svg>
            Download PDF
          </button>
          <button class="action-btn" on:click={() => downloadReport('excel')}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" stroke-width="2"/>
              <polyline points="14 2 14 8 20 8" stroke="currentColor" stroke-width="2"/>
            </svg>
            Export Excel
          </button>
          <button class="action-btn" on:click={() => downloadReport('json')}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <polyline points="16 18 22 12 16 6" stroke="currentColor" stroke-width="2"/>
              <polyline points="8 6 2 12 8 18" stroke="currentColor" stroke-width="2"/>
            </svg>
            API Export (JSON)
          </button>
          <button class="action-btn secondary" on:click={() => reportGenerated = false}>
            Generate New Report
          </button>
        </div>
      </div>
    {:else}
      <div class="empty-state">
        <svg width="120" height="120" viewBox="0 0 24 24" fill="none">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" stroke-width="1.5"/>
          <polyline points="14 2 14 8 20 8" stroke="currentColor" stroke-width="1.5"/>
          <line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" stroke-width="1.5"/>
          <line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" stroke-width="1.5"/>
          <polyline points="10 9 9 9 8 9" stroke="currentColor" stroke-width="1.5"/>
        </svg>
        <h3>No Report Generated</h3>
        <p>Configure your report settings and click "Generate Report" to create a comprehensive climate impact analysis for your data center.</p>
      </div>
    {/if}
  </div>
</div>

<style>
  .reports-container {
    display: grid;
    grid-template-columns: 400px 1fr;
    gap: 24px;
    height: 100%;
  }

  .report-status { display: flex; gap: 9px; align-items: flex-start; grid-column: 1 / -1; padding: 11px 13px; border: 1px solid rgba(182,126,61,.25); border-radius: 12px; background: rgba(182,126,61,.08); color: rgba(244,247,245,.67); font-size: 12px; line-height: 1.45; }
  .report-status strong { color: #f0d6a7; }
  .report-status span { width: 7px; height: 7px; flex: 0 0 7px; margin-top: 5px; border-radius: 50%; background: #b67e3d; }
  
  .config-section {
    display: flex;
    flex-direction: column;
  }
  
  .config-card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 24px;
  }
  
  .config-card h3 {
    font-size: 18px;
    font-weight: 600;
    color: var(--text);
    margin: 0 0 24px 0;
  }
  
  .form-group {
    margin-bottom: 24px;
  }
  
  .form-group label {
    display: block;
    font-size: 13px;
    font-weight: 600;
    color: var(--ts);
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  
  .select-input {
    width: 100%;
    padding: 12px 16px;
    background: var(--bg2);
    border: 1px solid var(--line);
    border-radius: 8px;
    color: var(--text);
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .select-input:hover {
    border-color: var(--line2);
  }
  
  .select-input:focus {
    outline: none;
    border-color: var(--green);
    box-shadow: 0 0 0 3px var(--gs);
  }
  
  .report-types {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  
  .report-type-card {
    padding: 12px 16px;
    background: var(--bg2);
    border: 1px solid var(--line);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .report-type-card:hover {
    border-color: var(--line2);
    background: var(--panel2);
  }
  
  .report-type-card.selected {
    border-color: var(--green);
    background: var(--gs);
  }
  
  .type-name {
    font-size: 14px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 4px;
  }
  
  .type-desc {
    font-size: 12px;
    color: var(--tm);
  }
  
  .timeframe-options {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }
  
  .timeframe-btn {
    padding: 12px;
    background: var(--bg2);
    border: 1px solid var(--line);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
  }
  
  .timeframe-btn:hover {
    border-color: var(--line2);
    background: var(--panel2);
  }
  
  .timeframe-btn.active {
    border-color: var(--green);
    background: var(--gs);
  }
  
  .tf-name {
    font-size: 14px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 2px;
  }
  
  .tf-period {
    font-size: 11px;
    color: var(--tm);
  }
  
  .generate-btn {
    width: 100%;
    padding: 14px 24px;
    background: var(--green);
    border: none;
    border-radius: 8px;
    color: white;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-top: 8px;
  }
  
  .generate-btn:hover:not(:disabled) {
    background: var(--g2);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px var(--gs);
  }
  
  .generate-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  .spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255,255,255,0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  .preview-section {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
  }
  
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: 60px 40px;
    text-align: center;
  }
  
  .empty-state svg {
    stroke: var(--tm);
    margin-bottom: 24px;
    opacity: 0.5;
  }
  
  .empty-state h3 {
    font-size: 20px;
    font-weight: 600;
    color: var(--text);
    margin: 0 0 12px 0;
  }
  
  .empty-state p {
    font-size: 14px;
    color: var(--tm);
    max-width: 400px;
    line-height: 1.6;
  }
  
  .report-preview {
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  
  .preview-header {
    padding: 24px;
    border-bottom: 1px solid var(--line);
  }
  
  .preview-header h3 {
    font-size: 18px;
    font-weight: 600;
    color: var(--text);
    margin: 0 0 8px 0;
  }
  
  .preview-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: var(--tm);
  }
  
  .meta-divider {
    color: var(--line2);
  }
  
  .report-content {
    flex: 1;
    overflow-y: auto;
    padding: 24px;
  }
  
  .report-section {
    margin-bottom: 32px;
  }
  
  .report-section:last-child {
    margin-bottom: 0;
  }
  
  .report-section h4 {
    font-size: 16px;
    font-weight: 600;
    color: var(--text);
    margin: 0 0 16px 0;
  }
  
  .summary-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .summary-card {
    padding: 16px;
    background: var(--bg2);
    border: 1px solid var(--line);
    border-radius: 8px;
  }
  
  .summary-label {
    font-size: 12px;
    color: var(--tm);
    margin-bottom: 8px;
  }
  
  .summary-value {
    font-size: 24px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 4px;
  }
  
  .summary-trend {
    font-size: 12px;
    font-weight: 600;
  }
  
  .summary-trend.positive {
    color: var(--green);
  }
  
  .summary-trend.negative {
    color: var(--red);
  }
  
  .metrics-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .metric-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    background: var(--bg2);
    border: 1px solid var(--line);
    border-radius: 8px;
  }
  
  .metric-label {
    font-size: 14px;
    color: var(--ts);
  }
  
  .metric-value {
    font-size: 14px;
    font-weight: 600;
    color: var(--text);
  }
  
  .compliance-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
  }
  
  .compliance-card {
    padding: 16px;
    background: var(--bg2);
    border: 1px solid var(--line);
    border-radius: 8px;
    text-align: center;
  }
  
  .compliance-card.compliant {
    border-color: var(--green);
    background: var(--gs);
  }
  
  .compliance-card.warning {
    border-color: var(--amber);
    background: var(--as);
  }
  
  .compliance-icon {
    font-size: 24px;
    margin-bottom: 8px;
  }
  
  .compliance-card.compliant .compliance-icon {
    color: var(--green);
  }
  
  .compliance-card.warning .compliance-icon {
    color: var(--amber);
  }
  
  .compliance-name {
    font-size: 14px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 4px;
  }
  
  .compliance-status {
    font-size: 12px;
    color: var(--tm);
  }
  
  .recommendations-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .recommendation-item {
    padding: 16px;
    background: var(--bg2);
    border: 1px solid var(--line);
    border-radius: 8px;
  }
  
  .rec-priority {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
  }
  
  .rec-priority.high {
    background: var(--rs);
    color: var(--red);
  }
  
  .rec-priority.medium {
    background: var(--as);
    color: var(--amber);
  }
  
  .rec-text {
    font-size: 14px;
    color: var(--text);
    margin-bottom: 6px;
  }
  
  .rec-impact {
    font-size: 12px;
    color: var(--green);
    font-weight: 600;
  }
  
  .report-actions {
    display: flex;
    gap: 12px;
    padding: 24px;
    border-top: 1px solid var(--line);
  }
  
  .action-btn {
    flex: 1;
    padding: 12px 20px;
    background: var(--green);
    border: none;
    border-radius: 8px;
    color: white;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }
  
  .action-btn:hover {
    background: var(--g2);
    transform: translateY(-1px);
  }
  
  .action-btn.secondary {
    background: var(--panel2);
    color: var(--text);
    border: 1px solid var(--line);
  }
  
  .action-btn.secondary:hover {
    background: var(--bg2);
    border-color: var(--line2);
  }
  
  @media (max-width: 1400px) {
    .reports-container {
      grid-template-columns: 1fr;
    }
    
    .compliance-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
</style>
