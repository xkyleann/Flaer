<script>
  export let size = 32;
  export let id = 'logo';
</script>

<img
  src="/brand/flaer-logo.png"
  width={size}
  height={size}
  alt=""
  aria-hidden="true"
  class="flaer-mark"
/>

<style>
  .flaer-mark {
    display: block;
    flex-shrink: 0;
    object-fit: cover;
    border-radius: 24%;
  }
</style>
