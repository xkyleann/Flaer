<script>
  import { onMount, tick } from 'svelte';

  const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

  let messages = [];
  let inputValue = '';
  let isThinking = false;
  let chatEl;
  let inputEl;
  let userContext = 'planner';

  const quickActions = [
    { label: 'Weekly digest', prompt: 'Generate my weekly consumption digest',
      icon: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>` },
    { label: 'Check anomalies', prompt: 'Check for anomalies across all facilities',
      icon: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>` },
    { label: 'Top actions', prompt: 'What are the top 3 carbon reduction actions I should take?',
      icon: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="13 17 18 12 13 7"/><polyline points="6 17 11 12 6 7"/></svg>` },
    { label: 'Score Stockholm', prompt: 'Score Stockholm for a new 120MW data center',
      icon: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>` },
    { label: 'PUE explained', prompt: 'Explain PUE and how to improve it',
      icon: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>` },
    { label: 'CSRD status', prompt: 'What do I need to report under CSRD?',
      icon: `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>` },
  ];

  const capabilities = [
    { label: 'Emissions forecasting', desc: 'CO₂ trajectory to 2035' },
    { label: 'Anomaly detection', desc: 'PUE, WUE, energy spikes' },
    { label: 'Site scoring', desc: 'MCDA across 14 dimensions' },
    { label: 'CSRD reporting', desc: 'EU compliance readiness' },
    { label: 'Carbon reduction', desc: 'Ranked action recommendations' },
    { label: 'Grid intelligence', desc: 'Carbon intensity by region' },
  ];

  const sources = ['IEA World Energy Outlook 2024', 'IPCC AR6 Climate Scenarios', 'GHG Protocol Scope 2', 'EU ETS Carbon Pricing'];

  onMount(() => {
    history = [];
    push('assistant', getWelcome());
    inputEl?.focus();
  });

  function getWelcome() {
    return `**Welcome to flaer AI** — your sustainability intelligence layer.

I analyse your portfolio in real time and surface what matters: emissions trends, efficiency anomalies, site risks, and the actions with the highest carbon-and-cost impact.

Ask me anything, or choose a quick action on the right.`;
  }

  function push(role, content, streaming = false) {
    messages = [...messages, { role, content, streaming, id: Date.now() }];
    scrollDown();
  }

  async function scrollDown() {
    await tick();
    if (chatEl) chatEl.scrollTop = chatEl.scrollHeight;
  }

  function md(text) {
    return text
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/^### (.+)$/gm, '<span class="md-h3">$1</span>')
      .replace(/^## (.+)$/gm, '<span class="md-h2">$1</span>')
      .replace(/^# (.+)$/gm, '<span class="md-h1">$1</span>')
      .replace(/^- (.+)$/gm, '<span class="md-li">$1</span>')
      .replace(/^(\d+)\. (.+)$/gm, '<span class="md-oli"><em>$1.</em> $2</span>')
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\n{2,}/g, '<br><br>')
      .replace(/\n/g, '<br>');
  }

  async function send() {
    const text = inputValue.trim();
    if (!text || isThinking) return;
    inputValue = '';
    push('user', text);
    isThinking = true;
    await scrollDown();

    try {
      const reply = await getReply(text);
      await streamReply(reply);
    } catch (e) {
      push('assistant', `**Error:** ${e.message || 'Something went wrong. Please try again.'}`);
    } finally {
      isThinking = false;
      await scrollDown();
      inputEl?.focus();
    }
  }

  async function streamReply(text) {
    const id = Date.now();
    messages = [...messages, { role: 'assistant', content: '', streaming: true, id }];
    await tick();
    chatEl.scrollTop = chatEl.scrollHeight;

    const words = text.split(' ');
    let built = '';
    for (let i = 0; i < words.length; i++) {
      built += (i > 0 ? ' ' : '') + words[i];
      messages = messages.map(m => m.id === id ? { ...m, content: built } : m);
      if (i % 4 === 0) {
        await tick();
        chatEl.scrollTop = chatEl.scrollHeight;
        await new Promise(r => setTimeout(r, 18));
      }
    }
    messages = messages.map(m => m.id === id ? { ...m, streaming: false } : m);
    await tick();
    chatEl.scrollTop = chatEl.scrollHeight;
  }

  // Conversation history for multi-turn context
  let history = [];

  async function getReply(msg) {
    const lower = msg.toLowerCase();
    const token = localStorage.getItem('access_token');
    const user = JSON.parse(localStorage.getItem('user_info') || '{}');

    // Add user message to history
    history = [...history, { role: 'user', content: msg }];

    // Try Claude API first
    if (token) {
      try {
        const res = await fetch(`${API_URL}/api/ai/chat`, {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
          body: JSON.stringify({ messages: history })
        });
        if (res.ok) {
          const data = await res.json();
          history = [...history, { role: 'assistant', content: data.reply }];
          return data.reply;
        }
        // 503 = key not configured → fall through to local intelligence
        if (res.status !== 503) {
          const err = await res.json().catch(() => ({}));
          throw new Error(err.detail || 'Chat failed');
        }
      } catch (e) {
        if (!e.message?.includes('503') && !e.message?.includes('key not configured')) throw e;
      }
    }

    if (lower.includes('weekly digest') || lower.includes('consumption summary')) {
      if (token && user.organization_id) {
        const res = await fetch(`${API_URL}/api/ai/weekly-digest`, {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
          body: JSON.stringify({ organization_id: user.organization_id })
        });
        if (res.ok) {
          const d = await res.json();
          return d.markdown || formatDigest(d.digest);
        }
      }
      return localDigest();
    }

    if (lower.includes('anomal') || lower.includes('check')) {
      if (token) {
        const res = await fetch(`${API_URL}/api/dashboard/datacenters`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const dcs = await res.json();
          return formatAnomalies(dcs);
        }
      }
      return localAnomalies();
    }

    const locMatch = lower.match(/\b(stockholm|frankfurt|singapore|virginia|dublin|montreal|oregon|tokyo|mumbai|bahrain|warsaw)\b/);
    if ((lower.includes('score') || lower.includes('assess') || lower.includes('evaluate')) && locMatch) {
      if (token) {
        const res = await fetch(`${API_URL}/api/ai/score-location/${locMatch[1]}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const d = await res.json();
          return formatScore(d.score_data, locMatch[1]);
        }
      }
      return localScore(locMatch[1]);
    }

    if (lower.includes('action') || lower.includes('recommend') || lower.includes('reduce')) {
      return localActions();
    }

    if (lower.includes('pue')) return localPUE();
    if (lower.includes('wue')) return localWUE();
    if (lower.includes('csrd') || lower.includes('compliance') || lower.includes('report')) return localCSRD();
    if (lower.includes('scope 2') || lower.includes('scope2')) return localScope2();
    if (lower.includes('carbon') || lower.includes('emission')) return localCarbon();
    if (lower.includes('renewable') || lower.includes('ppa')) return localPPA();
    if (lower.includes('cooling')) return localCooling();
    if (lower.includes('forecast') || lower.includes('2030') || lower.includes('2035')) return localForecast();

    return localGeneric(msg);
  }

  function formatDigest(d) {
    return `**Weekly Consumption Digest**

**Energy** ${d.energy_mwh} MWh · ${d.energy_change_pct > 0 ? '+' : ''}${d.energy_change_pct}% week-on-week
**Carbon** ${d.carbon_tco2} tCO₂e · Scope 2 = ${d.scope2_pct}%
**PUE** ${d.pue} · **WUE** ${d.wue} L/kWh · **Renewable** ${d.renewable_pct}%

**Top actions this week:**
${d.top_actions.map((a, i) => `${i+1}. ${a.action} — ${a.impact}`).join('\n')}

**Trend:** ${d.trend}`;
  }

  function formatAnomalies(dcs) {
    const flags = dcs.flatMap(dc => {
      const a = [];
      if (dc.pue > 1.75) a.push(`**${dc.name}** PUE ${dc.pue} — above 1.75 threshold`);
      if (dc.wue > 1.8) a.push(`**${dc.name}** WUE ${dc.wue} L/kWh — above 1.8 threshold`);
      return a;
    });
    if (!flags.length) return `**Anomaly scan complete — ${dcs.length} facilities checked**\n\nNo threshold breaches detected. PUE ≤ 1.75 and WUE ≤ 1.8 L/kWh across all sites. Next recommended check: week-on-week energy spike (>5%).`;
    return `**Anomaly Detection — ${flags.length} breach${flags.length > 1 ? 'es' : ''} found**\n\n${flags.map(f => `- ${f}`).join('\n')}\n\n**Recommended:** Prioritise Scope 2 reduction — purchased electricity is typically 90%+ of data center emissions.`;
  }

  function formatScore(s, loc) {
    return `**${loc.toUpperCase()} — Sustainability Score ${s.composite_score}/100**

- Grid Carbon: ${s.grid_carbon_score}/100 (${s.grid_carbon_intensity} gCO₂/kWh)
- Renewable availability: ${s.renewable_score}/100 (${s.renewable_availability}% grid share)
- Water stress: ${s.water_score}/100
- Climate risk: ${s.climate_score}/100
- Regulatory fit: ${s.regulatory_score}/100

**Strongest dimension:** ${s.best_dimension}
**Key risk:** ${s.biggest_risk}

${s.rationale}`;
  }

  // Local intelligent fallbacks
  const scoreData = {
    stockholm: { score: 94, carbon: '13 gCO₂/kWh', renewable: '98%', water: 'Low stress', risk: 'FX (SEK)', note: 'Best carbon position in Europe. Tier-1 recommendation for a zero-carbon mandate.' },
    montreal: { score: 91, carbon: '29 gCO₂/kWh', renewable: '97%', water: 'Low stress', risk: 'Spring flood', note: 'Best value in North America. Hydro-Québec 20-year price lock available.' },
    oregon: { score: 74, carbon: '95 gCO₂/kWh', renewable: '89%', water: 'Moderate', risk: 'Seismic Zone 3', note: 'Strong connectivity but seismic exposure and water stress require mitigation.' },
    frankfurt: { score: 68, carbon: '380 gCO₂/kWh', renewable: '54%', water: 'Low stress', risk: 'High carbon grid', note: 'Excellent connectivity but coal-heavy grid creates CSRD exposure.' },
    singapore: { score: 61, carbon: '408 gCO₂/kWh', renewable: '4%', water: 'High stress', risk: 'DC moratorium', note: 'National 1,260 MW cap in force. High carbon and cooling OPEX.' },
    warsaw: { score: 59, carbon: '670 gCO₂/kWh', renewable: '28%', water: 'Low stress', risk: 'Coal grid', note: 'Lowest CapEx on shortlist but highest carbon liability. EU Taxonomy compliance risk.' },
  };

  function localScore(loc) {
    const s = scoreData[loc] || { score: 72, carbon: 'N/A', renewable: 'N/A', water: 'N/A', risk: 'N/A', note: 'Full assessment requires live data connection.' };
    return `**${loc.charAt(0).toUpperCase() + loc.slice(1)} — MCDA Score ${s.score}/100**

- Grid carbon: ${s.carbon}
- Renewable mix: ${s.renewable}
- Water stress: ${s.water}
- Key risk: ${s.risk}

**Assessment:** ${s.note}

Use the **Site Selection** screen for the full 14-dimension MCDA breakdown, Gantt timeline, and financial model.`;
  }

  function localDigest() {
    return `**Weekly Consumption Digest — N. Virginia cluster**

**Energy** 28,400 MWh · +3.2% week-on-week
**Carbon** 11,680 tCO₂e · Scope 2 = 94%
**PUE** 1.52 · **WUE** 0.78 L/kWh · **Renewable** 61%

**Top 3 actions this week:**
1. Shift 15% batch workload to Oregon (91% renewable) — saves ~420 tCO₂e/wk
2. Raise server inlet temperature 2°C → reduces cooling load 6% → ~180 MWh/wk
3. Renegotiate PPA with Dominion Energy — current tariff $71/MWh vs market $58/MWh

**Trend:** Emissions up 3.2% driven by Q2 capacity ramp. On track for −8% full-year target if cooling upgrade proceeds as planned.

_Connect live facility data in Settings to personalise this digest._`;
  }

  function localAnomalies() {
    return `**Anomaly Scan — Portfolio overview**

**2 soft flags detected (below hard threshold):**

- **N. Virginia** PUE 1.52 — trending up 0.04 since last week. Cooling optimisation recommended before summer peak.
- **Singapore** WUE 1.08 L/kWh — approaching 1.8 threshold. Cooling tower blowdown rate should be reviewed.

**All other facilities within normal bounds.**

Connect live telemetry in Settings to run real-time threshold monitoring across all 6 facilities.`;
  }

  function localActions() {
    return `**Top Carbon Reduction Actions — Ranked by impact**

1. **Workload shift → Oregon / Stockholm** — move 20% of batch compute to highest-renewable sites. *Estimated saving: −2,800 tCO₂e/yr*

2. **PPA renegotiation — N. Virginia** — current grid tariff $71/MWh vs available renewable PPA at $54/MWh. *Saving: ~$4.2M/yr + Scope 2 reduction*

3. **Cooling upgrade — Singapore** — install adiabatic pre-coolers. PUE 1.58 → 1.40 target. *Saving: −1,200 MWh/yr, −490 tCO₂e/yr*

4. **Server inlet temperature increase** — raise from 18°C to 21°C across N. Virginia and Frankfurt. Low-risk, immediate. *Saving: −6% cooling energy*

5. **Water-side economiser — Frankfurt** — Rhine river cooling feasibility complete. Capital cost ~€1.8M, payback 3.2 years.

Use the **Actions** screen to assign owners, set deadlines, and track progress.`;
  }

  function localPUE() {
    return `**Power Usage Effectiveness (PUE)**

PUE = Total Facility Energy ÷ IT Equipment Energy

- **1.0** — theoretical perfect (all energy goes to compute)
- **1.2–1.3** — hyperscale best-in-class (Google, Microsoft)
- **1.4–1.5** — good enterprise target
- **1.5–1.75** — industry average
- **>1.75** — action required (flaer alert threshold)

**Your portfolio average: 1.47**

**How to improve PUE:**
- Raise server inlet temperature to 21–27°C (ASHRAE A2 class)
- Install hot/cold aisle containment
- Deploy free-air or adiabatic cooling where climate allows
- Virtualise and consolidate underutilised servers (>40% idle = waste)

A PUE improvement from 1.52 → 1.40 at N. Virginia saves ~3,200 MWh/yr.`;
  }

  function localWUE() {
    return `**Water Usage Effectiveness (WUE)**

WUE = Annual Site Water Usage (litres) ÷ IT Energy (kWh)

- **<0.5 L/kWh** — best in class (air-cooled, low humidity)
- **0.5–1.0** — good
- **1.0–1.8** — acceptable
- **>1.8 L/kWh** — flaer alert threshold

**Your portfolio average: 0.74 L/kWh**

WUE matters most in water-stressed regions (Singapore, US Southwest). Strategies:
- Free-air cooling eliminates evaporative loss entirely
- Cooling tower blowdown optimisation (target 5–6 cycles of concentration)
- Closed-loop liquid cooling for high-density racks
- Grey water or recycled municipal supply agreements`;
  }

  function localCSRD() {
    return `**CSRD Compliance Status — EU Corporate Sustainability Reporting Directive**

**Applies from FY2024** for large EU companies (>500 employees or listed). Mandatory from FY2025 for mid-size.

**What you must report:**
- Scope 1, 2 & 3 GHG emissions (GHG Protocol aligned)
- Energy consumption and renewable mix (EU Taxonomy)
- Water withdrawal and consumption (WUE)
- Climate transition plan (1.5°C pathway alignment)
- EU Taxonomy alignment % of revenue/CapEx/OpEx

**Flaer covers:** Scope 1+2, energy mix, WUE, PUE, EU Taxonomy data centre criteria (>50% renewable, PUE <1.5 for Taxonomy alignment).

**Gap: Scope 3** — supply chain emissions require vendor data collection. Start with Scope 3 Category 11 (use of sold products) if applicable.

Go to **Reports** to generate a draft CSRD-aligned disclosure.`;
  }

  function localScope2() {
    return `**Scope 2 Emissions — Your largest lever**

Scope 2 = purchased electricity emissions. For data centres this is typically **90–95% of total footprint**.

**Two accounting methods:**

**Location-based** — uses average grid emission factor. Simple but penalises you for grid mix regardless of what you buy.

**Market-based** — uses contractual instruments (RECs, GOs, PPAs). Allows you to claim zero if you hold matching certificates.

**Your portfolio — market-based:**
- N. Virginia: 61% renewable → Scope 2 = 11,680 tCO₂e/wk
- Stockholm: 98% renewable → near-zero Scope 2
- Singapore: 4% renewable → highest intensity site

**Priority action:** Increase PPA coverage at N. Virginia and Singapore. A $54/MWh PPA at Virginia would reduce Scope 2 by ~38% and save $4.1M/yr vs grid tariff.`;
  }

  function localCarbon() {
    return `**Carbon Intelligence — Portfolio summary**

**Total portfolio: 142,840 tCO₂e/yr** (market-based Scope 2)

**By site:**
- N. Virginia — 48,200 tCO₂e (34%) — highest priority
- Singapore — 31,400 tCO₂e (22%) — grid-constrained
- Frankfurt — 22,100 tCO₂e (15%) — coal grid exposure
- Oregon — 18,900 tCO₂e (13%) — improving
- Montréal — 12,640 tCO₂e (9%) — near-zero potential
- Stockholm — 9,600 tCO₂e (7%) — lowest intensity

**2030 pathway:** −38% reduction achievable via PPA renegotiation (N. Virginia), Singapore cooling upgrade, and 25% workload shift to Montréal/Stockholm.

Open **Forecast** to model SSP5-8.5 and optimised scenarios side by side.`;
  }

  function localPPA() {
    return `**Renewable Energy & PPAs**

**Power Purchase Agreements (PPAs)** let you lock in long-term renewable electricity prices directly from a generator — typically 10–20 years.

**Benefits:**
- Price certainty vs volatile grid tariff
- Scope 2 market-based accounting to zero
- Additionality claim (new renewable capacity, not RECs from existing plants)

**Your current status:**
- Stockholm: 98% hydro/wind PPA — exemplary
- Montréal: 97% Hydro-Québec base load — locked to 2034
- Oregon: 89% — mix of RECs and bundled PPA
- N. Virginia: 61% — gap of 39% is your biggest Scope 2 exposure

**PPA market rates (Q2 2026):**
- US East: ~$52–58/MWh solar/wind PPA
- Nordic: ~$28–34/MWh hydro
- Germany: ~$61–69/MWh offshore wind

N. Virginia PPA at $54/MWh vs $71/MWh grid = **$4.2M/yr saving** on 30,000 MWh gap.`;
  }

  function localCooling() {
    return `**Cooling Strategy & Efficiency**

Cooling accounts for **30–40% of total data centre energy** and is the primary driver of high PUE.

**Cooling technology by climate suitability:**

- **Free-air (economiser)** — best for Stockholm, Montréal, Oregon. Eliminates mechanical cooling for 8–10 months/yr. PUE → 1.20–1.30.
- **Adiabatic pre-cooling** — adds evaporative stage before DX. Effective in Frankfurt, Oregon. PUE → 1.30–1.40.
- **Water-side economiser** — river/lake cooling loop. High CapEx, low OPEX. Viable for N. Virginia (Potomac), Frankfurt (Rhine).
- **Rear-door heat exchangers** — for high-density GPU/AI racks (>25kW/rack). No raised floor required.
- **Liquid cooling (direct-to-chip)** — NVIDIA H100 clusters require it. WUE ~0.1 L/kWh.

**Singapore** is your hardest case: 27.5°C ambient year-round, limited free-cooling hours. District cooling network subscription is the best available option.`;
  }

  function localForecast() {
    return `**Emissions Forecast — 2030 / 2035**

**Business-as-usual (SSP5-8.5):**
By 2035: +8% increase above 2025 baseline. Driven by capacity growth (+9%/yr demand) outpacing grid decarbonisation at current PPA coverage.

**Optimised pathway:**
By 2035: −38% vs 2025. Requires:
- 80% renewable procurement by 2027 (PPA)
- PUE improvement 1.47 → 1.30 avg (cooling upgrades)
- 25% workload shift to Stockholm/Montréal by 2028

**Key milestone — 2030:**
EED (Energy Efficiency Directive) threshold applies. N. Virginia and Singapore are at-risk sites. Cooling upgrade at both is on the critical path.

**Carbon cost exposure:**
At €110/tCO₂e (EU ETS 2030 projection), BAU path = **€15.7M carbon liability** by 2030 vs €8.2M on optimised path.

Open **Forecast** to run SSP5-8.5, balanced, and custom scenarios with your own slider assumptions.`;
  }

  function localGeneric(msg) {
    return `I can help with:

- **Emissions & carbon** — Scope 1/2/3, reduction pathways, CSRD reporting
- **Efficiency metrics** — PUE, WUE, CUE analysis and benchmarks
- **Site selection** — MCDA scoring for new data centre locations
- **Forecasting** — 2030/2035 emissions under climate scenarios
- **Renewable energy** — PPA strategy, grid carbon intensity, RECs
- **Cooling** — technology options, free-air viability, liquid cooling
- **Compliance** — CSRD, EU Taxonomy, GHG Protocol

Try a specific question or use a quick action on the right.`;
  }

  function onKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
  }

  function useQuick(q) {
    inputValue = q.prompt;
    send();
  }
</script>

<div class="ai-shell">

  <!-- Chat column -->
  <div class="chat-col">
    <!-- Header -->
    <div class="ai-header">
      <div class="ai-hd-left">
        <div class="ai-avatar">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>
          </svg>
        </div>
        <div>
          <div class="ai-name">flaer AI</div>
          <div class="ai-sub">Sustainability intelligence · Powered by Anthropic</div>
        </div>
      </div>
      <div class="ai-status">
        <span class="status-dot"></span>
        Ready
      </div>
    </div>

    <!-- Messages -->
    <div class="chat-messages" bind:this={chatEl}>
      {#each messages as msg (msg.id)}
        <div class="msg-row" class:user={msg.role === 'user'} class:assistant={msg.role === 'assistant'}>
          {#if msg.role === 'assistant'}
            <div class="msg-icon">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>
              </svg>
            </div>
          {/if}
          <div class="msg-bubble">
            <div class="msg-text" class:streaming={msg.streaming}>{@html md(msg.content)}</div>
          </div>
        </div>
      {/each}

      {#if isThinking}
        <div class="msg-row assistant">
          <div class="msg-icon">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>
            </svg>
          </div>
          <div class="msg-bubble thinking">
            <span></span><span></span><span></span>
          </div>
        </div>
      {/if}
    </div>

    <!-- Input -->
    <div class="chat-input-wrap">
      <textarea
        bind:this={inputEl}
        bind:value={inputValue}
        on:keydown={onKey}
        placeholder="Ask about emissions, PUE, site selection, CSRD, forecasts…"
        rows="2"
        disabled={isThinking}
        class="chat-input"
      ></textarea>
      <button class="send-btn" on:click={send} disabled={!inputValue.trim() || isThinking} aria-label="Send">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>
        </svg>
      </button>
    </div>
  </div>

  <!-- Right panel -->
  <div class="side-panel">

    <div class="side-section">
      <div class="side-label">QUICK ACTIONS</div>
      <div class="quick-grid">
        {#each quickActions as q}
          <button class="quick-btn" on:click={() => useQuick(q)} disabled={isThinking}>
            <span class="quick-icon">{@html q.icon}</span>
            <span>{q.label}</span>
          </button>
        {/each}
      </div>
    </div>

    <div class="side-section">
      <div class="side-label">CAPABILITIES</div>
      {#each capabilities as c}
        <div class="cap-row">
          <div class="cap-dot"></div>
          <div>
            <div class="cap-name">{c.label}</div>
            <div class="cap-desc">{c.desc}</div>
          </div>
        </div>
      {/each}
    </div>

    <div class="side-section">
      <div class="side-label">DATA SOURCES</div>
      {#each sources as s}
        <div class="source-row">
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
          {s}
        </div>
      {/each}
    </div>

    <div class="side-disclaimer">
      Responses use pre-loaded intelligence and, where available, live telemetry. Always verify material decisions with primary data sources.
    </div>

  </div>
</div>

<style>
  .ai-shell {
    display: grid;
    grid-template-columns: 1fr 260px;
    gap: 14px;
    height: 100%;
  }

  /* ── Chat column ── */
  .chat-col {
    display: flex;
    flex-direction: column;
    border-radius: 22px;
    overflow: hidden;
    background: linear-gradient(180deg, rgba(255,255,255,0.055), rgba(255,255,255,0.028));
    border: 1px solid rgba(255,255,255,0.08);
  }

  .ai-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 18px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    flex-shrink: 0;
  }

  .ai-hd-left { display: flex; align-items: center; gap: 11px; }

  .ai-avatar {
    width: 34px; height: 34px;
    border-radius: 10px;
    background: linear-gradient(135deg, rgba(44,173,132,0.25), rgba(44,173,132,0.1));
    border: 1px solid rgba(44,173,132,0.3);
    display: flex; align-items: center; justify-content: center;
    color: #2cad84;
    flex-shrink: 0;
  }

  .ai-name { font-size: 14px; font-weight: 900; color: var(--text); }
  .ai-sub  { font-size: 11px; color: var(--ts); margin-top: 1px; }

  .ai-status {
    display: flex; align-items: center; gap: 6px;
    font-size: 11.5px; font-weight: 600; color: #2cad84;
  }

  .status-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #2cad84;
    box-shadow: 0 0 6px #2cad84;
    animation: pulse-dot 2s infinite;
  }

  @keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
  }

  /* Messages */
  .chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    scrollbar-width: thin;
    scrollbar-color: rgba(255,255,255,0.1) transparent;
  }

  .msg-row {
    display: flex;
    gap: 10px;
    align-items: flex-start;
  }

  .msg-row.user {
    flex-direction: row-reverse;
  }

  .msg-icon {
    width: 28px; height: 28px;
    border-radius: 8px;
    background: rgba(44,173,132,0.12);
    border: 1px solid rgba(44,173,132,0.2);
    display: flex; align-items: center; justify-content: center;
    color: #2cad84;
    flex-shrink: 0;
    margin-top: 2px;
  }

  .msg-bubble {
    max-width: 72%;
    padding: 11px 15px;
    border-radius: 16px;
    font-size: 13.5px;
    line-height: 1.65;
  }

  .msg-row.user .msg-bubble {
    background: linear-gradient(135deg, #2cad84, #1e9470);
    color: white;
    border-radius: 16px 4px 16px 16px;
  }

  .msg-row.assistant .msg-bubble {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    color: var(--text);
    border-radius: 4px 16px 16px 16px;
  }

  .msg-bubble.thinking {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 14px 18px;
  }

  .msg-bubble.thinking span {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--tm);
    animation: bounce 1.3s infinite;
  }
  .msg-bubble.thinking span:nth-child(2) { animation-delay: 0.15s; }
  .msg-bubble.thinking span:nth-child(3) { animation-delay: 0.30s; }

  @keyframes bounce {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
    30% { transform: translateY(-6px); opacity: 1; }
  }

  /* Markdown styles inside bubbles */
  :global(.msg-text strong) { color: #2cad84; font-weight: 700; }
  :global(.msg-row.user .msg-text strong) { color: rgba(255,255,255,0.9); }
  :global(.msg-text .md-h1) { display: block; font-size: 15px; font-weight: 900; color: var(--text); margin: 6px 0 4px; }
  :global(.msg-text .md-h2) { display: block; font-size: 13.5px; font-weight: 800; color: var(--text); margin: 5px 0 3px; }
  :global(.msg-text .md-h3) { display: block; font-size: 12.5px; font-weight: 700; color: var(--tm); margin: 4px 0 2px; text-transform: uppercase; letter-spacing: 0.05em; }
  :global(.msg-text .md-li) { display: block; padding-left: 14px; position: relative; margin: 2px 0; }
  :global(.msg-text .md-li::before) { content: '·'; position: absolute; left: 4px; color: #2cad84; }
  :global(.msg-text .md-oli) { display: block; padding-left: 18px; position: relative; margin: 2px 0; }
  :global(.msg-text .md-oli em) { position: absolute; left: 0; font-style: normal; color: #2cad84; font-weight: 700; }
  :global(.msg-text code) { background: rgba(44,173,132,0.12); color: #8ef0cc; padding: 1px 5px; border-radius: 4px; font-size: 12px; font-family: 'JetBrains Mono', monospace; }

  .msg-text.streaming::after {
    content: '▌';
    color: #2cad84;
    animation: blink 0.8s step-end infinite;
  }
  @keyframes blink { 50% { opacity: 0; } }

  /* Input */
  .chat-input-wrap {
    display: flex;
    gap: 10px;
    padding: 14px 16px;
    border-top: 1px solid rgba(255,255,255,0.07);
    background: rgba(0,0,0,0.15);
    flex-shrink: 0;
    align-items: flex-end;
  }

  .chat-input {
    flex: 1;
    padding: 10px 14px;
    border-radius: 13px;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.05);
    color: var(--text);
    font-size: 13.5px;
    font-family: inherit;
    resize: none;
    line-height: 1.5;
    transition: border-color 0.2s, box-shadow 0.2s;
  }

  .chat-input:focus {
    outline: none;
    border-color: rgba(44,173,132,0.4);
    box-shadow: 0 0 0 3px rgba(44,173,132,0.1);
  }

  .chat-input:disabled { opacity: 0.5; cursor: not-allowed; }
  .chat-input::placeholder { color: var(--ts); }

  .send-btn {
    width: 40px; height: 40px;
    border-radius: 12px;
    border: none;
    background: linear-gradient(135deg, #2cad84, #1e9470);
    color: white;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    transition: all 0.18s;
    box-shadow: 0 3px 10px rgba(44,173,132,0.25);
  }

  .send-btn:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 5px 14px rgba(44,173,132,0.35);
  }

  .send-btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none; box-shadow: none; }

  /* ── Side panel ── */
  .side-panel {
    display: flex;
    flex-direction: column;
    gap: 10px;
    overflow-y: auto;
    padding-right: 2px;
    scrollbar-width: thin;
    scrollbar-color: rgba(255,255,255,0.08) transparent;
  }

  .side-section {
    background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.025));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 14px;
  }

  .side-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: var(--tm);
    margin-bottom: 10px;
  }

  .quick-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 7px;
  }

  .quick-btn {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 7px;
    padding: 9px 10px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.04);
    color: var(--ts);
    font-size: 11.5px;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.16s;
    text-align: left;
  }

  .quick-btn:hover:not(:disabled) {
    background: rgba(44,173,132,0.1);
    border-color: rgba(44,173,132,0.25);
    color: #8ef0cc;
    transform: translateY(-1px);
  }

  .quick-btn:disabled { opacity: 0.5; cursor: not-allowed; }

  .quick-icon { display: flex; align-items: center; color: #2cad84; }

  .cap-row {
    display: flex;
    align-items: flex-start;
    gap: 9px;
    padding: 7px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
  }
  .cap-row:last-child { border-bottom: none; }

  .cap-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #2cad84;
    flex-shrink: 0;
    margin-top: 5px;
  }

  .cap-name { font-size: 12px; font-weight: 700; color: var(--text); }
  .cap-desc { font-size: 11px; color: var(--ts); margin-top: 1px; }

  .source-row {
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 11px;
    color: var(--ts);
    padding: 4px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
  }
  .source-row:last-child { border-bottom: none; }
  .source-row svg { color: #2cad84; flex-shrink: 0; }

  .side-disclaimer {
    font-size: 10.5px;
    color: var(--ts);
    line-height: 1.5;
    padding: 10px 12px;
    border-radius: 12px;
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.05);
  }
</style>
