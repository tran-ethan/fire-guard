<script lang="ts">
  import Coordinates from "../components/Coordinates.svelte";
  import Filters from "../components/Filters.svelte";
  import Map from "../components/Map.svelte";
</script>

<div>
  <title>
    <img src="logo.png" alt="Icon" class="icon" />
    Fire Guard
  </title>

  <home on:click={() => (window.location.href = "/")}>
    Home
  </home>

  <Map />
  <Filters />
  <Coordinates />
</div>
