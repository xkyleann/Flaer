<script>
  import { authStore } from './stores/authStore.js';
  import FlaerLogo from './FlaerLogo.svelte';
  import { onMount } from 'svelte';

  let email = '';
  let password = '';
  let otpCode = '';
  let requiresOTP = false;
  let otpEmail = '';
  let loading = false;
  let error = '';
  let showPassword = false;
  let rememberMe = false;
  let success = false;
  let shake = false;

  onMount(() => {
    const rememberedEmail = localStorage.getItem('remembered_email');
    if (rememberedEmail) {
      email = rememberedEmail;
      rememberMe = true;
    }
  });

  async function handleLogin(e) {
    e.preventDefault();
    loading = true;
    error = '';
    shake = false;

    try {
      const result = await authStore.login(email, password);

      if (result.requiresOTP) {
        requiresOTP = true;
        otpEmail = result.email;
        if (result.otpCode) {
          error = `Development: OTP Code is ${result.otpCode}`;
        }
      } else {
        if (rememberMe) {
          localStorage.setItem('remembered_email', email);
        } else {
          localStorage.removeItem('remembered_email');
        }
        success = true;
        setTimeout(() => { window.location.hash = '#dashboard'; }, 800);
      }
    } catch (err) {
      error = err.message || 'Login failed. Please check your credentials.';
      shake = true;
      setTimeout(() => shake = false, 500);
    } finally {
      loading = false;
    }
  }

  async function handleOTPVerify(e) {
    e.preventDefault();
    loading = true;
    error = '';

    try {
      await authStore.verifyOTP(otpEmail, otpCode);
      window.location.hash = '#dashboard';
    } catch (err) {
      error = err.message || 'Invalid OTP code. Please try again.';
    } finally {
      loading = false;
    }
  }

  function goToRegister() {
    window.location.hash = '#register';
  }
</script>

<div class="login-container">
  <!-- Background -->
  <div class="bg-orb bg-orb-1" aria-hidden="true"></div>
  <div class="bg-orb bg-orb-2" aria-hidden="true"></div>
  <div class="dot-grid" aria-hidden="true"></div>

  <div class="login-card">
    <!-- Inner top highlight -->
    <div class="card-shine" aria-hidden="true"></div>

    {#if !requiresOTP}
      <!-- Header -->
      <div class="card-header">
        <div class="logo-wrap">
          <FlaerLogo size={32} id="login-logo" />
          <span class="logo-wordmark">Flaer</span>
        </div>
        <h1>Welcome back</h1>
        <p>Sign in to your workspace</p>
      </div>

      <form on:submit={handleLogin} class="login-form" class:shake>
        <div class="field">
          <label for="email">Email address</label>
          <input
            id="email"
            type="email"
            bind:value={email}
            placeholder="you@company.com"
            required
            disabled={loading}
            autocomplete="email"
          />
        </div>

        <div class="field">
          <label for="password">Password</label>
          <div class="password-wrap">
            <input
              id="password"
              type={showPassword ? 'text' : 'password'}
              bind:value={password}
              placeholder="Enter your password"
              required
              disabled={loading}
              autocomplete="current-password"
            />
            <button
              type="button"
              class="eye-btn"
              on:click={() => showPassword = !showPassword}
              tabindex="-1"
              aria-label={showPassword ? 'Hide password' : 'Show password'}
            >
              {#if showPassword}
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
                  <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
                  <line x1="1" y1="1" x2="23" y2="23"/>
                </svg>
              {:else}
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
              {/if}
            </button>
          </div>
        </div>

        <div class="form-options">
          <label class="remember-label">
            <input type="checkbox" bind:checked={rememberMe} class="checkbox" />
            <span class="checkbox-custom"></span>
            <span>Remember me</span>
          </label>
          <button type="button" class="text-link" on:click={() => alert('Password reset coming soon.')}>
            Forgot password?
          </button>
        </div>

        {#if error}
          <div class="alert alert-error">
            <svg width="15" height="15" viewBox="0 0 15 15" fill="none"><circle cx="7.5" cy="7.5" r="6.5" stroke="currentColor" stroke-width="1.5"/><path d="M7.5 4.5v4M7.5 10.5v.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
            {error}
          </div>
        {/if}

        {#if success}
          <div class="alert alert-success">
            <svg class="checkmark" viewBox="0 0 22 22" fill="none">
              <circle cx="11" cy="11" r="10" stroke="currentColor" stroke-width="1.5" class="check-circle"/>
              <path d="M6 11.5l3.5 3.5 6.5-7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" class="check-path"/>
            </svg>
            Signed in successfully
          </div>
        {/if}

        <button type="submit" class="submit-btn" disabled={loading || success}>
          {#if loading}
            <span class="spinner" aria-hidden="true"></span>
            Signing in…
          {:else if success}
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8.5l3.5 3.5 6.5-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            Signed in
          {:else}
            Sign in
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 7h8M8 4l3 3-3 3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
          {/if}
        </button>

        <div class="footer-row">
          <span>No account?</span>
          <button type="button" class="text-link" on:click={goToRegister}>Create one</button>
        </div>

      </form>

    {:else}
      <!-- OTP view -->
      <div class="card-header">
        <div class="otp-icon" aria-hidden="true">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none"><rect x="6" y="11" width="16" height="12" rx="3" stroke="#2cad84" stroke-width="1.8"/><path d="M9 11V8a5 5 0 0 1 10 0v3" stroke="#2cad84" stroke-width="1.8" stroke-linecap="round"/><circle cx="14" cy="17" r="1.5" fill="#2cad84"/></svg>
        </div>
        <h1>Two-factor auth</h1>
        <p>Enter the 6-digit code from your authenticator app</p>
      </div>

      <form on:submit={handleOTPVerify} class="login-form">
        <div class="field">
          <label for="otp">Verification code</label>
          <input
            id="otp"
            type="text"
            bind:value={otpCode}
            placeholder="000 000"
            maxlength="6"
            pattern="[0-9]{6}"
            required
            disabled={loading}
            class="otp-input"
            autocomplete="one-time-code"
            inputmode="numeric"
          />
        </div>

        {#if error}
          <div class="alert alert-error">
            <svg width="15" height="15" viewBox="0 0 15 15" fill="none"><circle cx="7.5" cy="7.5" r="6.5" stroke="currentColor" stroke-width="1.5"/><path d="M7.5 4.5v4M7.5 10.5v.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
            {error}
          </div>
        {/if}

        <button type="submit" class="submit-btn" disabled={loading}>
          {#if loading}
            <span class="spinner" aria-hidden="true"></span>
            Verifying…
          {:else}
            Verify code
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 7h8M8 4l3 3-3 3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
          {/if}
        </button>

        <div class="footer-row">
          <button type="button" class="text-link" on:click={() => requiresOTP = false}>
            ← Back to sign in
          </button>
        </div>
      </form>
    {/if}
  </div>
</div>

<style>
  /* ── Reset / globals ──────────────────────── */
  *, *::before, *::after { box-sizing: border-box; }

  /* ── Container ───────────────────────────── */
  .login-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #07110f;
    position: relative;
    overflow: hidden;
    padding: 24px;
    font-family: 'Inter', sans-serif;
    -webkit-font-smoothing: antialiased;
  }

  .dot-grid {
    position: absolute;
    inset: 0;
    background-image: radial-gradient(circle, rgba(255,255,255,0.07) 1px, transparent 1px);
    background-size: 28px 28px;
    mask-image: radial-gradient(ellipse 70% 70% at 50% 50%, black 20%, transparent 80%);
    -webkit-mask-image: radial-gradient(ellipse 70% 70% at 50% 50%, black 20%, transparent 80%);
    pointer-events: none;
  }

  .bg-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(100px);
    pointer-events: none;
  }

  .bg-orb-1 {
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(44,173,132,0.14), transparent 65%);
    top: -200px;
    left: -100px;
    animation: orb 18s ease-in-out infinite;
  }

  .bg-orb-2 {
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(127,174,255,0.1), transparent 65%);
    bottom: -150px;
    right: -100px;
    animation: orb 22s ease-in-out infinite reverse;
  }

  @keyframes orb {
    0%, 100% { transform: translate(0, 0); }
    50% { transform: translate(40px, 30px); }
  }

  /* ── Card ─────────────────────────────────── */
  .login-card {
    position: relative;
    z-index: 1;
    width: 100%;
    max-width: 420px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 28px;
    padding: 40px 36px;
    backdrop-filter: blur(60px) saturate(180%);
    -webkit-backdrop-filter: blur(60px) saturate(180%);
    box-shadow:
      inset 0 1px 0 rgba(255,255,255,0.14),
      inset 0 0 0 0.5px rgba(255,255,255,0.04),
      0 4px 16px rgba(0,0,0,0.12),
      0 24px 56px -8px rgba(0,0,0,0.5),
      0 0 80px rgba(44,173,132,0.05);
    animation: card-in 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
  }

  @keyframes card-in {
    from { opacity: 0; transform: translateY(24px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
  }

  .card-shine {
    position: absolute;
    top: 0;
    left: 10%;
    right: 10%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.18) 40%, rgba(255,255,255,0.18) 60%, transparent);
    border-radius: 999px;
    pointer-events: none;
  }

  /* ── Header ───────────────────────────────── */
  .card-header {
    text-align: center;
    margin-bottom: 32px;
  }

  .logo-wrap {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 20px;
  }

  .logo-wordmark {
    font-size: 18px;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: #f4f7f5;
  }


  .card-header h1 {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: #f4f7f5;
    margin: 0 0 6px;
    line-height: 1.1;
  }

  .card-header p {
    font-size: 13.5px;
    color: rgba(244,247,245,0.46);
    margin: 0;
    letter-spacing: -0.01em;
  }

  .otp-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 56px;
    height: 56px;
    border-radius: 18px;
    background: rgba(44,173,132,0.1);
    border: 1px solid rgba(44,173,132,0.2);
    margin-bottom: 16px;
    box-shadow: inset 0 1px 0 rgba(44,173,132,0.15);
  }

  /* ── Form ─────────────────────────────────── */
  .login-form {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .login-form.shake {
    animation: shake 0.45s cubic-bezier(0.36, 0.07, 0.19, 0.97);
  }

  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    20%       { transform: translateX(-7px); }
    40%       { transform: translateX(7px); }
    60%       { transform: translateX(-5px); }
    80%       { transform: translateX(5px); }
  }

  /* ── Fields ───────────────────────────────── */
  .field {
    display: flex;
    flex-direction: column;
    gap: 7px;
  }

  .field label {
    font-size: 12px;
    font-weight: 600;
    color: rgba(244,247,245,0.6);
    letter-spacing: 0.01em;
  }

  .field input {
    width: 100%;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 14px;
    padding: 12px 14px;
    color: #f4f7f5;
    font-size: 14px;
    font-family: inherit;
    letter-spacing: -0.01em;
    transition: border-color 0.2s, background 0.2s, box-shadow 0.2s;
    outline: none;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
  }

  .field input::placeholder { color: rgba(244,247,245,0.22); }

  .field input:focus {
    border-color: rgba(44,173,132,0.5);
    background: rgba(255,255,255,0.07);
    box-shadow:
      inset 0 1px 0 rgba(255,255,255,0.06),
      0 0 0 3px rgba(44,173,132,0.1);
  }

  .field input:disabled {
    opacity: 0.45;
    cursor: not-allowed;
  }

  /* ── Password field ───────────────────────── */
  .password-wrap { position: relative; }

  .password-wrap input { padding-right: 44px; }

  .eye-btn {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: rgba(244,247,245,0.35);
    cursor: pointer;
    padding: 4px;
    display: flex;
    align-items: center;
    transition: color 0.2s;
    border-radius: 6px;
  }

  .eye-btn:hover { color: rgba(244,247,245,0.7); }

  /* ── OTP input ────────────────────────────── */
  .otp-input {
    text-align: center;
    font-size: 26px !important;
    letter-spacing: 0.3em;
    font-weight: 700 !important;
  }

  /* ── Options row ──────────────────────────── */
  .form-options {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .remember-label {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    font-size: 13px;
    color: rgba(244,247,245,0.55);
    user-select: none;
  }

  .remember-label input.checkbox { display: none; }

  .checkbox-custom {
    width: 16px;
    height: 16px;
    border-radius: 5px;
    border: 1px solid rgba(255,255,255,0.18);
    background: rgba(255,255,255,0.05);
    flex-shrink: 0;
    transition: background 0.2s, border-color 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .remember-label:has(input:checked) .checkbox-custom {
    background: rgba(44,173,132,0.2);
    border-color: rgba(44,173,132,0.5);
  }

  .remember-label:has(input:checked) .checkbox-custom::after {
    content: '';
    display: block;
    width: 8px;
    height: 8px;
    background: #2cad84;
    border-radius: 2px;
  }

  .text-link {
    background: none;
    border: none;
    color: rgba(44,173,132,0.9);
    font-size: 13px;
    font-family: inherit;
    cursor: pointer;
    padding: 0;
    font-weight: 500;
    letter-spacing: -0.01em;
    transition: color 0.15s;
  }

  .text-link:hover { color: #2cad84; }

  /* ── Alerts ───────────────────────────────── */
  .alert {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 11px 14px;
    border-radius: 12px;
    font-size: 13px;
    font-weight: 500;
    letter-spacing: -0.01em;
    animation: alert-in 0.25s ease;
  }

  @keyframes alert-in {
    from { opacity: 0; transform: translateY(-4px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .alert-error {
    background: rgba(211,93,92,0.1);
    border: 1px solid rgba(211,93,92,0.22);
    color: #ffc4c4;
  }

  .alert-success {
    background: rgba(44,173,132,0.1);
    border: 1px solid rgba(44,173,132,0.25);
    color: #b6ffe7;
  }

  /* Animated checkmark */
  .checkmark { width: 20px; height: 20px; flex-shrink: 0; }

  .check-circle {
    stroke-dasharray: 63;
    stroke-dashoffset: 63;
    animation: draw 0.5s ease forwards;
  }

  .check-path {
    stroke-dasharray: 24;
    stroke-dashoffset: 24;
    animation: draw 0.35s ease 0.35s forwards;
  }

  @keyframes draw { to { stroke-dashoffset: 0; } }

  /* ── Submit ───────────────────────────────── */
  .submit-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 13px 20px;
    border-radius: 14px;
    border: none;
    background: linear-gradient(135deg, #d2e8dd 0%, #f0dfbc 100%);
    color: #07110f;
    font-size: 14px;
    font-weight: 700;
    font-family: inherit;
    letter-spacing: -0.01em;
    cursor: pointer;
    transition: filter 0.2s, transform 0.2s, box-shadow 0.2s;
    box-shadow:
      inset 0 1px 0 rgba(255,255,255,0.4),
      0 4px 14px rgba(44,173,132,0.18);
    margin-top: 4px;
  }

  .submit-btn:hover:not(:disabled) {
    filter: brightness(1.05);
    transform: translateY(-1px);
    box-shadow:
      inset 0 1px 0 rgba(255,255,255,0.4),
      0 8px 20px rgba(44,173,132,0.24);
  }

  .submit-btn:active:not(:disabled) {
    transform: translateY(0);
    filter: brightness(0.98);
  }

  .submit-btn:disabled {
    opacity: 0.55;
    cursor: not-allowed;
  }

  .spinner {
    width: 14px;
    height: 14px;
    border: 2px solid rgba(7,17,15,0.3);
    border-top-color: #07110f;
    border-radius: 50%;
    animation: spin 0.75s linear infinite;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  /* ── Footer row ───────────────────────────── */
  .footer-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    font-size: 13px;
    color: rgba(244,247,245,0.4);
    margin-top: 2px;
  }

  @media (max-width: 480px) {
    .login-card { padding: 32px 24px; }
  }
</style>
