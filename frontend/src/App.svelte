<script lang="ts">
  import Map from "./components/Map.svelte";
  import Filters from "./components/Filters.svelte";
  import Coordinates from "./components/Coordinates.svelte";
  import { getWildFire } from "./lib/wildfires";
  import { onMount } from "svelte";

  onMount(async () => {
    try {
      const fire = await getWildFire("EFnlJ7dUtmLCF5qhHg1N");
      console.log(fire);
    } catch (error) {
      console.error(error);
    }
  });
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
