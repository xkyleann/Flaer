<script>
  const principles = [
    ['Coverage first', 'Every mapped location is visible, with geography kept separate from operational measurements.'],
    ['Sources made clear', 'Flaer distinguishes supplied portfolio data, connected sources, and calculated estimates.'],
    ['Decision-ready outputs', 'Signals are organised around a question to answer—not a dashboard metric to admire.']
  ];

  const faqs = [
    ['Which data does Flaer use?', 'Flaer combines customer-supplied facility and operational data with connected market, grid, and regulatory sources. The methodology should identify the source and refresh time of every metric.'],
    ['Is the European map a complete market directory?', 'No. It is a portfolio view: it shows the facilities added to a workspace. Public locations and operational data must be validated before they are used for a business decision.'],
    ['Can Flaer work with our existing tools?', 'Yes. A consultation is the right place to review your current reporting, facility, and procurement workflows and define the most useful integration path.'],
    ['How does a pilot begin?', 'We begin with a focused use case, agree the data needed to assess it, and define the decision or reporting output the pilot must support.']
  ];

  let openFaq = $state(0);
</script>

<section id="methodology" class="methodology">
  <div class="w layout">
    <div class="section-heading">
      <div class="eyebrow">Data methodology</div>
      <h2>Confidence comes from knowing where every signal comes from.</h2>
      <p>Flaer should make the status, source, and refresh timing of data visible—so teams can use the right level of certainty for each decision.</p>
    </div>
    <div class="principles">
      {#each principles as [title, text], i}
        <article><span>{String(i + 1).padStart(2, '0')}</span><div><h3>{title}</h3><p>{text}</p></div></article>
      {/each}
    </div>
  </div>
</section>

<section id="faq" class="faq">
  <div class="w faq-layout">
    <div class="section-heading"><div class="eyebrow">FAQ</div><h2>Questions teams ask before getting started.</h2></div>
    <div class="questions">
      {#each faqs as [question, answer], i}
        <div class:open={openFaq === i} class="question">
          <button type="button" aria-expanded={openFaq === i} onclick={() => openFaq = openFaq === i ? -1 : i}>
            <span>{question}</span><b>{openFaq === i ? '−' : '+'}</b>
          </button>
          {#if openFaq === i}<p>{answer}</p>{/if}
        </div>
      {/each}
    </div>
  </div>
</section>

<style>
  section { padding: 100px 0; }
  .methodology { background: var(--paper); border-block: 1px solid rgba(0,0,0,.07); }
  .faq { background: #f7f9f8; }
  .section-heading { max-width: 650px; }
  .eyebrow { color: var(--green); font-size: 11px; font-weight: 800; letter-spacing: .1em; text-transform: uppercase; margin-bottom: 14px; }
  h2 { color: var(--ink); font-size: clamp(27px, 3.3vw, 42px); line-height: 1.12; letter-spacing: -.035em; }
  .section-heading > p { color: var(--ink-soft); font-size: 15px; line-height: 1.65; margin-top: 18px; }
  article span { color: var(--green); font-size: 11px; font-weight: 800; letter-spacing: .1em; }
  h3 { color: var(--ink); font-size: 17px; letter-spacing: -.02em; margin: 34px 0 10px; }
  article p { color: var(--ink-soft); font-size: 14px; line-height: 1.65; }
  .layout, .faq-layout { display: grid; grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); gap: 80px; align-items: start; }
  .principles { border-top: 1px solid rgba(0,0,0,.1); }
  .principles article { display: grid; grid-template-columns: 36px 1fr; gap: 16px; padding: 25px 0; border-bottom: 1px solid rgba(0,0,0,.1); }
  .principles h3 { margin: 0 0 8px; font-size: 15px; }
  .questions { border-top: 1px solid rgba(0,0,0,.12); }
  .question { border-bottom: 1px solid rgba(0,0,0,.12); }
  .question button { align-items: center; background: none; border: 0; color: var(--ink); cursor: pointer; display: flex; font: inherit; font-size: 15px; font-weight: 700; justify-content: space-between; padding: 20px 0; text-align: left; width: 100%; }
  .question button b { color: var(--green); font-size: 20px; font-weight: 400; }
  .question p { color: var(--ink-soft); font-size: 14px; line-height: 1.65; padding: 0 32px 20px 0; }
  @media (max-width: 760px) { section { padding: 72px 0; } .layout, .faq-layout { grid-template-columns: 1fr; gap: 36px; } }
</style>
