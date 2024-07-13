<script>
  import {
    Navbar,
    NavBrand,
  } from "flowbite-svelte";
</script>

<Navbar let:NavContainer class="border bg-white w-full fixed top-0 left-0 z-50 shadow-md border-black p-0 m-0">
  <NavContainer class="m-0 p-0 flex items-center">
    <NavBrand href="/" class="m-0 p-0 flex items-center">
      <img src="/fireguard-logo.webp" class="h-14 m-0 p-0" alt="Fire Guard Logo" />
      <span class="self-center whitespace-nowrap text-xl font-semibold ml-2">Fire Guard</span>
    </NavBrand>
  </NavContainer>
</Navbar>

<style>
  /* Ensure there's no padding or margin applied by default browser styles */
  :global(*) {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  /* Override any potential left margin on the NavBrand */
  :global(.navbar-brand) {
    margin-left: 0 !important;
  }
</style>