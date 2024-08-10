<script lang="ts">
  import Map from "./lib/MapBox/Map.svelte";
  import Filters from "./lib/MapBox/Filters.svelte";
    import Coordinates from "./lib/MapBox/Coordinates.svelte";

  
</script>

<main>
  <h1>
    <img src="logo.png" alt="Icon" class="icon" />
    Fire Guard
  </h1>

  <home>
    Home
  </home>
  
  
  <Map />
  <Filters />
  <Coordinates />
  
</main>