<script lang="ts">
<<<<<<< HEAD
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
=======
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
>>>>>>> ae0735f1784bba2ab4ac95e5f6ad3f993b832f86
