<script>
  import Nav from './lib/Nav.svelte';
  import Hero from './lib/Hero.svelte';
  import Platform from './lib/Platform.svelte';
  import Capabilities from './lib/Capabilities.svelte';
  import ForecastChart from './lib/ForecastChart.svelte';
  import Pricing from './lib/Pricing.svelte';
  import Readiness from './lib/Readiness.svelte';
  import CtaBlock from './lib/CtaBlock.svelte';
  import Footer from './lib/Footer.svelte';
</script>

<Nav />
<main>
  <Hero />
  <Platform />
  <Capabilities />
  <ForecastChart />
  <Pricing />
  <Readiness />
  <CtaBlock />
</main>
<Footer />

<style>
  main {
    position: relative;
    z-index: 1;
  }
</style>
