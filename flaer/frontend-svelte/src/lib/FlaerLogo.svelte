<script>
  export let size = 32;
  export let id = 'logo';
</script>

<!--
  Flaer logomark — two overlapping leaf/feather shapes forming an "F".
  No background container — transparent, works on any surface.
-->
<svg
  width={size}
  height={size}
  viewBox="0 0 40 40"
  fill="none"
  aria-hidden="true"
  class="flaer-mark"
>
  <defs>
    <linearGradient id="{id}-top" x1="8" y1="6" x2="34" y2="26" gradientUnits="userSpaceOnUse">
      <stop offset="0%"   stop-color="#1d8a6a"/>
      <stop offset="55%"  stop-color="#2cad84"/>
      <stop offset="100%" stop-color="#4ecfa0"/>
    </linearGradient>
    <linearGradient id="{id}-bot" x1="14" y1="22" x2="32" y2="38" gradientUnits="userSpaceOnUse">
      <stop offset="0%"   stop-color="#5fca9a"/>
      <stop offset="100%" stop-color="#c4965a"/>
    </linearGradient>
  </defs>

  <!-- Upper wing: the top bar + spine of the F -->
  <path
    d="M 8,30
       C 7,23 8,14 13,8
       C 17,3 25,2 33,7
       C 37,10 36,17 30,20
       C 24,23 17,23 15,27
       Z"
    fill="url(#{id}-top)"
  />

  <!-- Lower leaf: the middle crossbar of the F -->
  <path
    d="M 15,27
       C 17,23 25,22 30,24
       C 34,26 33,32 28,34
       C 23,37 15,35 13,30
       C 12,28 13,27 15,27
       Z"
    fill="url(#{id}-bot)"
  />
</svg>

<style>
  .flaer-mark {
    display: block;
    flex-shrink: 0;
  }
</style>
