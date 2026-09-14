<script>
  export let open = false;
  export let onClose = () => {};
  let date = '';
  let time = '';
  let email = '';
  let submitted = false;
  const dates = (() => { const list = []; const cursor = new Date(); while (list.length < 5) { cursor.setDate(cursor.getDate() + 1); if (![0, 6].includes(cursor.getDay())) list.push({ value: cursor.toISOString().slice(0, 10), label: cursor.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short' }) }); } return list; })();
  const times = ['09:30', '11:00', '14:00', '15:30'];
  function submit(event) { event.preventDefault(); if (!date || !time || !email) return; const requests = JSON.parse(localStorage.getItem('consultation_requests') || '[]'); requests.push({ email, date, time, timestamp: new Date().toISOString() }); localStorage.setItem('consultation_requests', JSON.stringify(requests)); submitted = true; }
</script>

{#if open}
  <div class="overlay" role="presentation" on:click={onClose}>
    <section class="modal" role="dialog" aria-modal="true" aria-label="Book a consultation" on:click|stopPropagation>
      <button class="close" on:click={onClose} aria-label="Close">×</button>
      {#if submitted}
        <span class="kicker">REQUEST RECEIVED</span><h2>We’ll confirm your time by email.</h2><p>Your preferred time has been recorded. A Flaer specialist will follow up shortly.</p><button class="primary" on:click={onClose}>Done</button>
      {:else}
        <span class="kicker">PRIVATE CONSULTATION</span><h2>Select a date and time.</h2><p>Choose a preferred 30-minute working session. Times are Central European Time.</p>
        <form on:submit={submit}>
          <div class="dates">{#each dates as option}<button type="button" class:selected={date === option.value} on:click={() => date = option.value}>{option.label}</button>{/each}</div>
          <div class="times">{#each times as value}<button type="button" class:selected={time === value} on:click={() => time = value}>{value}</button>{/each}</div>
          <label>Work email<input required type="email" bind:value={email} placeholder="work@company.com" /></label>
          <button class="primary" type="submit" disabled={!date || !time || !email}>Request selected time</button>
        </form>
      {/if}
    </section>
  </div>
{/if}

<style>
  .overlay { position: fixed; inset: 0; z-index: 1000; display: grid; place-items: center; padding: 20px; background: rgba(2,8,6,.74); backdrop-filter: blur(12px); }.modal { position: relative; width: min(520px, 100%); padding: 30px; border: 1px solid rgba(255,255,255,.14); border-radius: 20px; background: linear-gradient(145deg, #10211c, #07110f); box-shadow: 0 30px 90px rgba(0,0,0,.6); }.close { position: absolute; right: 15px; top: 12px; border: 0; background: transparent; color: rgba(244,247,245,.7); font-size: 25px; cursor: pointer; }.kicker { color: #68d9a5; font-size: 10px; font-weight: 800; letter-spacing: .12em; }.modal h2 { margin: 8px 0; color: #f4f7f5; font-size: 26px; letter-spacing: -.04em; }.modal p { color: rgba(244,247,245,.6); font-size: 13px; line-height: 1.55; }.dates, .times { display: grid; gap: 7px; margin: 18px 0 10px; }.dates { grid-template-columns: repeat(5, 1fr); }.times { grid-template-columns: repeat(4, 1fr); }.dates button, .times button { min-height: 42px; border: 1px solid rgba(255,255,255,.12); border-radius: 9px; background: rgba(255,255,255,.04); color: rgba(244,247,245,.75); font: inherit; font-size: 10px; cursor: pointer; }.dates button.selected, .times button.selected { border-color: rgba(44,173,132,.6); background: rgba(44,173,132,.17); color: #b6ffe7; }label { display: grid; gap: 7px; margin: 18px 0; color: rgba(244,247,245,.7); font-size: 11px; font-weight: 700; }input { padding: 12px; border: 1px solid rgba(255,255,255,.14); border-radius: 9px; background: rgba(255,255,255,.05); color: #f4f7f5; font: inherit; }.primary { width: 100%; padding: 12px; border: 0; border-radius: 10px; background: #dcebdc; color: #07110f; font: inherit; font-size: 12px; font-weight: 900; cursor: pointer; }.primary:disabled { cursor: not-allowed; opacity: .45; }@media(max-width:520px){.modal{padding:24px 18px}.dates{grid-template-columns:repeat(3,1fr)}}
</style>
