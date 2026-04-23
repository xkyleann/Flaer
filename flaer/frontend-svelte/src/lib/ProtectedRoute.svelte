<script>
  import { authStore } from './stores/authStore.js';
  import { navigate } from 'svelte-routing';
  import { onMount } from 'svelte';
  
  export let component;
  
  let isChecking = true;
  let isAuthorized = false;
  
  onMount(() => {
    // Initialize auth store and check authentication
    authStore.init();
    
    const unsubscribe = authStore.subscribe(state => {
      isAuthorized = state.isAuthenticated;
      isChecking = false;
      
      // Redirect to login if not authenticated
      if (!isChecking && !isAuthorized) {
        navigate('/login', { replace: true });
      }
    });
    
    return unsubscribe;
  });
</script>

{#if isChecking}
  <div class="loading-container">
    <div class="loading-spinner"></div>
    <p>Verifying authentication...</p>
  </div>
{:else if isAuthorized}
  <svelte:component this={component} />
{/if}

<style>
  .loading-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
    gap: 1.5rem;
  }
  
  .loading-spinner {
    width: 48px;
    height: 48px;
    border: 4px solid rgba(74, 222, 128, 0.2);
    border-top-color: #4ade80;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  .loading-container p {
    color: rgba(255, 255, 255, 0.7);
    font-size: 1rem;
  }
</style>