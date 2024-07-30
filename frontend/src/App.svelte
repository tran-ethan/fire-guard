<script lang="ts">
  import Map from "./components/Map.svelte";
  import Filters from "./components/Filters.svelte";
  import { onMount } from "svelte";
  import { getWildFire } from "./lib/wildfires";

  onMount(async () => {
    try {
      const fire = await getWildFire("0jvL5inL2advNxnbz13c");
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

  <Map />
  <Filters />
</main>
