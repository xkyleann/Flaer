<script>
  import { authStore } from './stores/authStore.js';
  import FlaerLogo from './FlaerLogo.svelte';
  
  let email = '';
  let password = '';
  let confirmPassword = '';
  let fullName = '';
  let company = '';
  let loading = false;
  let error = '';
  let showPassword = false;
  let showConfirmPassword = false;
  
  // Password strength
  $: passwordStrength = calculatePasswordStrength(password);
  $: passwordsMatch = password === confirmPassword && confirmPassword.length > 0;
  
  // Password requirements
  $: requirements = {
    length: password.length >= 8,
    uppercase: /[A-Z]/.test(password),
    lowercase: /[a-z]/.test(password),
    number: /\d/.test(password),
    special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
  };
  
  $: allRequirementsMet = Object.values(requirements).every(r => r);
  
  function calculatePasswordStrength(pwd) {
    if (!pwd) return { level: 0, text: '', color: '' };
    
    let strength = 0;
    if (pwd.length >= 8) strength++;
    if (pwd.length >= 12) strength++;
    if (/[A-Z]/.test(pwd)) strength++;
    if (/[a-z]/.test(pwd)) strength++;
    if (/\d/.test(pwd)) strength++;
    if (/[!@#$%^&*(),.?":{}|<>]/.test(pwd)) strength++;
    
    if (strength <= 2) return { level: 1, text: 'Weak', color: '#ef4444' };
    if (strength <= 4) return { level: 2, text: 'Medium', color: '#f59e0b' };
    return { level: 3, text: 'Strong', color: '#22c55e' };
  }
  
  async function handleRegister(e) {
    e.preventDefault();
    
    if (!allRequirementsMet) {
      error = 'Please meet all password requirements';
      return;
    }
    
    if (password !== confirmPassword) {
      error = 'Passwords do not match';
      return;
    }
    
    loading = true;
    error = '';
    
    try {
      await authStore.register(email, password, fullName, company);
      window.location.hash = '#dashboard';
    } catch (err) {
      error = err.message || 'Registration failed. Please try again.';
    } finally {
      loading = false;
    }
  }
  
  function goToLogin() {
    window.location.hash = '#login';
  }
</script>

<div class="register-container">
  <div class="register-card">
    <div class="logo-section">
      <div class="logo-container">
        <FlaerLogo size={64} id="register-logo" />
      </div>
      <h1>Join Flaer</h1>
      <p>Start your carbon intelligence journey</p>
    </div>
    
    <form on:submit={handleRegister} class="register-form">
      <div class="form-row">
        <div class="form-group">
          <label for="fullName">Full Name</label>
          <input
            id="fullName"
            type="text"
            bind:value={fullName}
            placeholder="John Doe"
            required
            disabled={loading}
          />
        </div>
        
        <div class="form-group">
          <label for="company">Company (Optional)</label>
          <input
            id="company"
            type="text"
            bind:value={company}
            placeholder="Acme Corp"
            disabled={loading}
          />
        </div>
      </div>
      
      <div class="form-group">
        <label for="email">Email Address</label>
        <input
          id="email"
          type="email"
          bind:value={email}
          placeholder="you@company.com"
          required
          disabled={loading}
        />
      </div>
      
      <div class="form-group">
        <label for="password">Password</label>
        <div class="password-input">
          <input
            id="password"
            type={showPassword ? 'text' : 'password'}
            bind:value={password}
            placeholder="Create a strong password"
            required
            disabled={loading}
          />
          <button
            type="button"
            class="toggle-password"
            on:click={() => showPassword = !showPassword}
            tabindex="-1"
          >
            {showPassword ? '👁️' : '👁️‍🗨️'}
          </button>
        </div>
        
        {#if password}
          <div class="password-strength" data-testid="password-strength">
            <div class="strength-bar">
              <div 
                class="strength-fill" 
                style="width: {passwordStrength.level * 33.33}%; background: {passwordStrength.color}"
              ></div>
            </div>
            <span style="color: {passwordStrength.color}">{passwordStrength.text}</span>
          </div>
        {/if}
      </div>
      
      <div class="form-group">
        <label for="confirmPassword">Confirm Password</label>
        <div class="password-input">
          <input
            id="confirmPassword"
            type={showConfirmPassword ? 'text' : 'password'}
            bind:value={confirmPassword}
            placeholder="Confirm your password"
            required
            disabled={loading}
            class:match={passwordsMatch}
            class:no-match={confirmPassword && !passwordsMatch}
          />
          <button
            type="button"
            class="toggle-password"
            on:click={() => showConfirmPassword = !showConfirmPassword}
            tabindex="-1"
          >
            {showConfirmPassword ? '👁️' : '👁️‍🗨️'}
          </button>
        </div>
        {#if confirmPassword && !passwordsMatch}
          <span class="error-text">Passwords do not match</span>
        {/if}
      </div>
      
      <div class="password-requirements">
        <p>Password must contain:</p>
        <ul>
          <li class:met={requirements.length}>
            {requirements.length ? '✓' : '○'} At least 8 characters
          </li>
          <li class:met={requirements.uppercase}>
            {requirements.uppercase ? '✓' : '○'} One uppercase letter
          </li>
          <li class:met={requirements.lowercase}>
            {requirements.lowercase ? '✓' : '○'} One lowercase letter
          </li>
          <li class:met={requirements.number}>
            {requirements.number ? '✓' : '○'} One number
          </li>
          <li class:met={requirements.special}>
            {requirements.special ? '✓' : '○'} One special character
          </li>
        </ul>
      </div>
      
      {#if error}
        <div class="error-message">{error}</div>
      {/if}
      
      <button type="submit" class="submit-btn" disabled={loading || !allRequirementsMet || !passwordsMatch}>
        {#if loading}
          <span class="spinner"></span>
          Creating account...
        {:else}
          Create Account
        {/if}
      </button>
      
      <div class="form-footer">
        <p>Already have an account? <button type="button" class="link-btn" on:click={goToLogin}>Sign in</button></p>
      </div>
    </form>
  </div>
  
  <div class="background-animation">
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
  </div>
</div>

<style>
  .register-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
    position: relative;
    overflow: hidden;
    padding: 2rem;
  }
  
  .background-animation {
    position: absolute;
    inset: 0;
    pointer-events: none;
  }
  
  .particle {
    position: absolute;
    width: 4px;
    height: 4px;
    background: rgba(74, 222, 128, 0.5);
    border-radius: 50%;
    animation: float 20s infinite;
  }
  
  .particle:nth-child(1) { left: 10%; animation-delay: 0s; }
  .particle:nth-child(2) { left: 30%; animation-delay: 4s; }
  .particle:nth-child(3) { left: 50%; animation-delay: 8s; }
  .particle:nth-child(4) { left: 70%; animation-delay: 12s; }
  .particle:nth-child(5) { left: 90%; animation-delay: 16s; }
  
  @keyframes float {
    0%, 100% {
      transform: translateY(100vh) scale(0);
      opacity: 0;
    }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% {
      transform: translateY(-100vh) scale(1);
      opacity: 0;
    }
  }
  
  .register-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 3rem;
    width: 100%;
    max-width: 600px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    animation: slideUp 0.6s ease-out;
    position: relative;
    z-index: 1;
  }
  
  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .logo-section {
    text-align: center;
    margin-bottom: 2.5rem;
  }
  
  .logo-container {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 96px;
    height: 96px;
    margin: 0 auto 1.5rem;
    background: linear-gradient(135deg, rgba(74, 222, 128, 0.1) 0%, rgba(34, 197, 94, 0.1) 100%);
    border: 2px solid rgba(74, 222, 128, 0.2);
    border-radius: 24px;
    animation: logoFloat 3s ease-in-out infinite;
    position: relative;
    transition: all 0.3s ease;
  }
  
  .logo-container::before {
    content: '';
    position: absolute;
    inset: -2px;
    background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
    border-radius: 24px;
    opacity: 0;
    transition: opacity 0.3s ease;
    z-index: -1;
  }
  
  .logo-container:hover {
    transform: scale(1.05);
    border-color: rgba(74, 222, 128, 0.4);
  }
  
  .logo-container:hover::before {
    opacity: 0.15;
  }
  
  @keyframes logoFloat {
    0%, 100% {
      transform: translateY(0px);
    }
    50% {
      transform: translateY(-8px);
    }
  }
  
  .logo-section h1 {
    font-size: 2rem;
    font-weight: 700;
    color: white;
    margin: 0 0 0.5rem 0;
  }
  
  .logo-section p {
    color: rgba(255, 255, 255, 0.6);
    font-size: 0.95rem;
  }
  
  .register-form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .form-group label {
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.9rem;
    font-weight: 500;
  }
  
  .form-group input {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 0.875rem 1rem;
    color: white;
    font-size: 1rem;
    transition: all 0.3s ease;
  }
  
  .form-group input:focus {
    outline: none;
    border-color: #4ade80;
    background: rgba(255, 255, 255, 0.08);
    box-shadow: 0 0 0 3px rgba(74, 222, 128, 0.1);
  }
  
  .form-group input.match {
    border-color: #22c55e;
  }
  
  .form-group input.no-match {
    border-color: #ef4444;
  }
  
  .form-group input::placeholder {
    color: rgba(255, 255, 255, 0.3);
  }
  
  .form-group input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .password-input {
    position: relative;
  }
  
  .password-input input {
    padding-right: 3rem;
  }
  
  .toggle-password {
    position: absolute;
    right: 1rem;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: rgba(255, 255, 255, 0.5);
    cursor: pointer;
    font-size: 1.2rem;
    padding: 0.25rem;
    transition: color 0.2s;
  }
  
  .toggle-password:hover {
    color: rgba(255, 255, 255, 0.8);
  }
  
  .password-strength {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 0.85rem;
    font-weight: 500;
  }
  
  .strength-bar {
    flex: 1;
    height: 4px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 2px;
    overflow: hidden;
  }
  
  .strength-fill {
    height: 100%;
    transition: all 0.3s ease;
  }
  
  .password-requirements {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 1rem;
  }
  
  .password-requirements p {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
    margin: 0 0 0.5rem 0;
  }
  
  .password-requirements ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
  }
  
  .password-requirements li {
    color: rgba(255, 255, 255, 0.5);
    font-size: 0.85rem;
    transition: color 0.3s;
  }
  
  .password-requirements li.met {
    color: #4ade80;
  }
  
  .error-text {
    color: #fca5a5;
    font-size: 0.85rem;
  }
  
  .error-message {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    color: #fca5a5;
    font-size: 0.9rem;
    animation: shake 0.5s;
  }
  
  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-10px); }
    75% { transform: translateX(10px); }
  }
  
  .submit-btn {
    background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
    border: none;
    border-radius: 12px;
    padding: 1rem;
    color: white;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }
  
  .submit-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(74, 222, 128, 0.3);
  }
  
  .submit-btn:active:not(:disabled) {
    transform: translateY(0);
  }
  
  .submit-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  .spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  .form-footer {
    text-align: center;
    margin-top: 1rem;
  }
  
  .form-footer p {
    color: rgba(255, 255, 255, 0.6);
    font-size: 0.9rem;
    margin: 0;
  }
  
  .link-btn {
    background: none;
    border: none;
    color: #4ade80;
    cursor: pointer;
    font-size: inherit;
    text-decoration: underline;
    padding: 0;
    transition: color 0.2s;
  }
  
  .link-btn:hover {
    color: #22c55e;
  }
  
  @media (max-width: 640px) {
    .register-card {
      padding: 2rem 1.5rem;
    }
    
    .form-row {
      grid-template-columns: 1fr;
    }
    
    .logo-section h1 {
      font-size: 1.75rem;
    }
  }
</style>