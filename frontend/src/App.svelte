<script lang="ts">
  import Map from "./components/Map.svelte";
  import { onMount } from "svelte";
  import { getWildFire } from "./lib/wildfires";
  import Navbar from "./components/Navbar.svelte";

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
  <Navbar />
  <Map />
</main>
