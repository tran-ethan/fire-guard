<script lang="ts">
  import Map from "./components/Map.svelte";
  import Filters from "./components/Filters.svelte";
  import Coordinates from "./components/Coordinates.svelte";
</script>

<main>
  <h1>
    <img src="logo.png" alt="Icon" class="icon" />
    Fire Guard
  </h1>

  <home> Home </home>

  <Map />
  <Filters />
  <Coordinates />
</main>
