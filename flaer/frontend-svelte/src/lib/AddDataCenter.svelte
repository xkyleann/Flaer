<script>
  import { createEventDispatcher } from 'svelte';
  import { authStore } from './stores/authStore.js';
  
  const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

  const dispatch = createEventDispatcher();
  
  let step = 1; // 1: Basic Info, 2: Metrics, 3: Optional
  let loading = false;
  let error = '';
  let success = false;
  
  // Form data
  let formData = {
    name: '',
    location: '',
    latitude: null,
    longitude: null,
    capacity_mw: 100,
    pue: 1.5,
    wue: null,
    cue: null,
    carbon_intensity: 300,
    renewable_pct: 50,
    monitoring_api_url: '',
    monitoring_api_key: ''
  };
  
  // Validation
  let errors = {};
  
  function validateStep1() {
    errors = {};
    if (!formData.name || formData.name.trim().length < 1) {
      errors.name = 'Data center name is required';
    }
    if (!formData.location || formData.location.trim().length < 1) {
      errors.location = 'Location is required';
    }
    return Object.keys(errors).length === 0;
  }
  
  function validateStep2() {
    errors = {};
    if (formData.capacity_mw < 1 || formData.capacity_mw > 10000) {
      errors.capacity_mw = 'Capacity must be between 1 and 10,000 MW';
    }
    if (formData.pue < 1.0 || formData.pue > 3.0) {
      errors.pue = 'PUE must be between 1.0 and 3.0';
    }
    if (formData.carbon_intensity < 0 || formData.carbon_intensity > 1000) {
      errors.carbon_intensity = 'Carbon intensity must be between 0 and 1000 gCO2/kWh';
    }
    if (formData.renewable_pct < 0 || formData.renewable_pct > 100) {
      errors.renewable_pct = 'Renewable percentage must be between 0 and 100';
    }
    return Object.keys(errors).length === 0;
  }
  
  function nextStep() {
    if (step === 1 && !validateStep1()) return;
    if (step === 2 && !validateStep2()) return;
    step++;
  }
  
  function prevStep() {
    step--;
    errors = {};
  }
  
  async function submitForm() {
    if (!validateStep2()) return;
    
    loading = true;
    error = '';
    
    try {
      const token = $authStore.token;
      
      // Clean up data - remove empty optional fields
      const payload = { ...formData };
      if (!payload.latitude) delete payload.latitude;
      if (!payload.longitude) delete payload.longitude;
      if (!payload.wue) delete payload.wue;
      if (!payload.cue) delete payload.cue;
      if (!payload.monitoring_api_url) delete payload.monitoring_api_url;
      if (!payload.monitoring_api_key) delete payload.monitoring_api_key;
      
      const response = await fetch(`${API_URL}/api/data-centers`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });
      
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to create data center');
      }
      
      const newDataCenter = await response.json();
      success = true;
      
      // Wait a moment to show success message
      setTimeout(() => {
        dispatch('created', newDataCenter);
      }, 1500);
      
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  }
  
  function cancel() {
    dispatch('cancel');
  }
  
  // Helper to get PUE status
  function getPUEStatus(pue) {
    if (pue < 1.2) return { label: 'Excellent', color: '#10b981' };
    if (pue < 1.5) return { label: 'Good', color: '#3b82f6' };
    if (pue < 1.75) return { label: 'Fair', color: '#f59e0b' };
    return { label: 'Poor', color: '#ef4444' };
  }
  
  // Helper to get carbon intensity status
  function getCarbonStatus(intensity) {
    if (intensity < 100) return { label: 'Very Low', color: '#10b981' };
    if (intensity < 250) return { label: 'Low', color: '#3b82f6' };
    if (intensity < 400) return { label: 'Medium', color: '#f59e0b' };
    return { label: 'High', color: '#ef4444' };
  }
  
  $: pueStatus = getPUEStatus(formData.pue);
  $: carbonStatus = getCarbonStatus(formData.carbon_intensity);
</script>

<div class="add-datacenter-modal">
  <div class="modal-overlay" on:click={cancel}></div>
  
  <div class="modal-content">
    {#if success}
      <div class="success-screen">
        <div class="success-icon">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline points="22 4 12 14.01 9 11.01" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h2>Data Center Added Successfully</h2>
        <p>Your facility is now being tracked. You'll see it in your portfolio shortly.</p>
      </div>
    {:else}
      <div class="modal-header">
        <h2>Connect Your Data Center</h2>
        <button class="close-btn" on:click={cancel}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <line x1="18" y1="6" x2="6" y2="18" stroke-width="2" stroke-linecap="round"/>
            <line x1="6" y1="6" x2="18" y2="18" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </button>
      </div>
      
      <div class="progress-bar">
        <div class="progress-step" class:active={step >= 1} class:completed={step > 1}>
          <div class="step-number">1</div>
          <div class="step-label">Basic Info</div>
        </div>
        <div class="progress-line" class:completed={step > 1}></div>
        <div class="progress-step" class:active={step >= 2} class:completed={step > 2}>
          <div class="step-number">2</div>
          <div class="step-label">Metrics</div>
        </div>
        <div class="progress-line" class:completed={step > 2}></div>
        <div class="progress-step" class:active={step >= 3}>
          <div class="step-number">3</div>
          <div class="step-label">Optional</div>
        </div>
      </div>
      
      <div class="modal-body">
        {#if error}
          <div class="error-message">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="10" stroke-width="2"/>
              <line x1="12" y1="8" x2="12" y2="12" stroke-width="2" stroke-linecap="round"/>
              <line x1="12" y1="16" x2="12.01" y2="16" stroke-width="2" stroke-linecap="round"/>
            </svg>
            {error}
          </div>
        {/if}
        
        {#if step === 1}
          <div class="form-step">
            <h3>Basic Information</h3>
            <p class="step-description">Tell us about your data center facility</p>
            
            <div class="form-group">
              <label for="name">Data Center Name *</label>
              <input
                id="name"
                type="text"
                bind:value={formData.name}
                placeholder="e.g., Virginia DC-1, Frankfurt Main"
                class:error={errors.name}
              />
              {#if errors.name}
                <span class="error-text">{errors.name}</span>
              {/if}
            </div>
            
            <div class="form-group">
              <label for="location">Location *</label>
              <input
                id="location"
                type="text"
                bind:value={formData.location}
                placeholder="e.g., Ashburn, Virginia, USA"
                class:error={errors.location}
              />
              {#if errors.location}
                <span class="error-text">{errors.location}</span>
              {/if}
              <span class="help-text">City, State/Region, Country</span>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="latitude">Latitude (Optional)</label>
                <input
                  id="latitude"
                  type="number"
                  step="0.000001"
                  bind:value={formData.latitude}
                  placeholder="38.9072"
                />
              </div>
              
              <div class="form-group">
                <label for="longitude">Longitude (Optional)</label>
                <input
                  id="longitude"
                  type="number"
                  step="0.000001"
                  bind:value={formData.longitude}
                  placeholder="-77.0369"
                />
              </div>
            </div>
            <span class="help-text">Coordinates help with map visualization</span>
          </div>
        {/if}
        
        {#if step === 2}
          <div class="form-step">
            <h3>Sustainability Metrics</h3>
            <p class="step-description">Current performance indicators for your facility</p>
            
            <div class="form-group">
              <label for="capacity">Total Capacity (MW) *</label>
              <input
                id="capacity"
                type="number"
                min="1"
                max="10000"
                bind:value={formData.capacity_mw}
                class:error={errors.capacity_mw}
              />
              {#if errors.capacity_mw}
                <span class="error-text">{errors.capacity_mw}</span>
              {/if}
            </div>
            
            <div class="form-group">
              <label for="pue">
                PUE (Power Usage Effectiveness) *
                <span class="metric-badge" style="background: {pueStatus.color}20; color: {pueStatus.color}">
                  {pueStatus.label}
                </span>
              </label>
              <input
                id="pue"
                type="number"
                step="0.01"
                min="1.0"
                max="3.0"
                bind:value={formData.pue}
                class:error={errors.pue}
              />
              {#if errors.pue}
                <span class="error-text">{errors.pue}</span>
              {:else}
                <span class="help-text">1.0 = perfect efficiency, 1.2 = excellent, 1.5 = good, >1.75 = needs improvement</span>
              {/if}
            </div>
            
            <div class="form-group">
              <label for="carbon">
                Grid Carbon Intensity (gCO2/kWh) *
                <span class="metric-badge" style="background: {carbonStatus.color}20; color: {carbonStatus.color}">
                  {carbonStatus.label}
                </span>
              </label>
              <input
                id="carbon"
                type="number"
                min="0"
                max="1000"
                bind:value={formData.carbon_intensity}
                class:error={errors.carbon_intensity}
              />
              {#if errors.carbon_intensity}
                <span class="error-text">{errors.carbon_intensity}</span>
              {:else}
                <span class="help-text">Check your local grid operator for current values</span>
              {/if}
            </div>
            
            <div class="form-group">
              <label for="renewable">Renewable Energy (%) *</label>
              <div class="slider-container">
                <input
                  id="renewable"
                  type="range"
                  min="0"
                  max="100"
                  bind:value={formData.renewable_pct}
                  class="slider"
                />
                <span class="slider-value">{formData.renewable_pct}%</span>
              </div>
              <span class="help-text">Percentage of energy from renewable sources</span>
            </div>
          </div>
        {/if}
        
        {#if step === 3}
          <div class="form-step">
            <h3>Optional Metrics</h3>
            <p class="step-description">Additional sustainability indicators (can be added later)</p>
            
            <div class="form-group">
              <label for="wue">WUE - Water Usage Effectiveness (L/kWh)</label>
              <input
                id="wue"
                type="number"
                step="0.1"
                min="0.1"
                max="10"
                bind:value={formData.wue}
                placeholder="e.g., 1.8"
              />
              <span class="help-text">Liters of water per kWh of IT equipment energy</span>
            </div>
            
            <div class="form-group">
              <label for="cue">CUE - Carbon Usage Effectiveness</label>
              <input
                id="cue"
                type="number"
                step="0.01"
                min="0"
                max="2"
                bind:value={formData.cue}
                placeholder="e.g., 0.45"
              />
              <span class="help-text">Total CO2 emissions / IT equipment energy</span>
            </div>
            
            <div class="integration-section">
              <h4>Monitoring Integration (Coming Soon)</h4>
              <p>Connect your monitoring system for real-time metrics</p>
              
              <div class="form-group">
                <label for="api-url">Monitoring API URL</label>
                <input
                  id="api-url"
                  type="url"
                  bind:value={formData.monitoring_api_url}
                  placeholder="https://monitoring.example.com/api"
                  disabled
                />
              </div>
              
              <div class="form-group">
                <label for="api-key">API Key</label>
                <input
                  id="api-key"
                  type="password"
                  bind:value={formData.monitoring_api_key}
                  placeholder="Your API key"
                  disabled
                />
              </div>
            </div>
          </div>
        {/if}
      </div>
      
      <div class="modal-footer">
        {#if step > 1}
          <button class="btn btn-secondary" on:click={prevStep} disabled={loading}>
            Back
          </button>
        {:else}
          <button class="btn btn-secondary" on:click={cancel}>
            Cancel
          </button>
        {/if}
        
        {#if step < 3}
          <button class="btn btn-primary" on:click={nextStep}>
            Next
          </button>
        {:else}
          <button class="btn btn-primary" on:click={submitForm} disabled={loading}>
            {#if loading}
              <span class="spinner"></span>
              Adding...
            {:else}
              Add Data Center
            {/if}
          </button>
        {/if}
      </div>
    {/if}
  </div>
</div>

<style>
  .add-datacenter-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
  }
  
  .modal-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(4px);
  }
  
  .modal-content {
    position: relative;
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 12px;
    width: 100%;
    max-width: 600px;
    max-height: 90vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }
  
  .modal-header {
    padding: 24px;
    border-bottom: 1px solid #333;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .modal-header h2 {
    margin: 0;
    font-size: 24px;
    font-weight: 600;
    color: #fff;
  }
  
  .close-btn {
    background: none;
    border: none;
    color: #999;
    cursor: pointer;
    padding: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: color 0.2s;
  }
  
  .close-btn:hover {
    color: #fff;
  }
  
  .progress-bar {
    display: flex;
    align-items: center;
    padding: 24px;
    background: #0f0f0f;
  }
  
  .progress-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    flex: 1;
  }
  
  .step-number {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #333;
    color: #666;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    transition: all 0.3s;
  }
  
  .progress-step.active .step-number {
    background: #3b82f6;
    color: #fff;
  }
  
  .progress-step.completed .step-number {
    background: #10b981;
    color: #fff;
  }
  
  .step-label {
    font-size: 12px;
    color: #666;
    transition: color 0.3s;
  }
  
  .progress-step.active .step-label {
    color: #fff;
  }
  
  .progress-line {
    height: 2px;
    background: #333;
    flex: 1;
    margin: 0 8px;
    margin-bottom: 24px;
    transition: background 0.3s;
  }
  
  .progress-line.completed {
    background: #10b981;
  }
  
  .modal-body {
    flex: 1;
    overflow-y: auto;
    padding: 24px;
  }
  
  .form-step h3 {
    margin: 0 0 8px 0;
    font-size: 20px;
    font-weight: 600;
    color: #fff;
  }
  
  .step-description {
    margin: 0 0 24px 0;
    color: #999;
    font-size: 14px;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }
  
  label {
    display: block;
    margin-bottom: 8px;
    color: #fff;
    font-size: 14px;
    font-weight: 500;
  }
  
  input[type="text"],
  input[type="number"],
  input[type="url"],
  input[type="password"] {
    width: 100%;
    padding: 10px 12px;
    background: #0f0f0f;
    border: 1px solid #333;
    border-radius: 6px;
    color: #fff;
    font-size: 14px;
    transition: border-color 0.2s;
  }
  
  input:focus {
    outline: none;
    border-color: #3b82f6;
  }
  
  input.error {
    border-color: #ef4444;
  }
  
  input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .help-text {
    display: block;
    margin-top: 4px;
    font-size: 12px;
    color: #666;
  }
  
  .error-text {
    display: block;
    margin-top: 4px;
    font-size: 12px;
    color: #ef4444;
  }
  
  .error-message {
    padding: 12px;
    background: #ef444420;
    border: 1px solid #ef4444;
    border-radius: 6px;
    color: #ef4444;
    font-size: 14px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .metric-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  
  .slider-container {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  
  .slider {
    flex: 1;
    height: 6px;
    border-radius: 3px;
    background: #333;
    outline: none;
    -webkit-appearance: none;
  }
  
  .slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #3b82f6;
    cursor: pointer;
  }
  
  .slider::-moz-range-thumb {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #3b82f6;
    cursor: pointer;
    border: none;
  }
  
  .slider-value {
    min-width: 45px;
    text-align: right;
    color: #fff;
    font-weight: 600;
  }
  
  .integration-section {
    margin-top: 32px;
    padding: 20px;
    background: #0f0f0f;
    border: 1px solid #333;
    border-radius: 8px;
  }
  
  .integration-section h4 {
    margin: 0 0 4px 0;
    font-size: 16px;
    color: #fff;
  }
  
  .integration-section p {
    margin: 0 0 16px 0;
    font-size: 13px;
    color: #666;
  }
  
  .modal-footer {
    padding: 20px 24px;
    border-top: 1px solid #333;
    display: flex;
    justify-content: space-between;
    gap: 12px;
  }
  
  .btn {
    padding: 10px 20px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .btn-primary {
    background: #3b82f6;
    color: #fff;
  }
  
  .btn-primary:hover:not(:disabled) {
    background: #2563eb;
  }
  
  .btn-secondary {
    background: #333;
    color: #fff;
  }
  
  .btn-secondary:hover:not(:disabled) {
    background: #444;
  }
  
  .btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .spinner {
    width: 16px;
    height: 16px;
    border: 2px solid #ffffff40;
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  .success-screen {
    padding: 60px 40px;
    text-align: center;
  }
  
  .success-icon {
    width: 64px;
    height: 64px;
    margin: 0 auto 24px;
    color: #10b981;
  }
  
  .success-screen h2 {
    margin: 0 0 12px 0;
    font-size: 24px;
    color: #fff;
  }
  
  .success-screen p {
    margin: 0;
    color: #999;
    font-size: 14px;
  }
</style>
