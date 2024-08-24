<script lang="ts">
  import { getWildFire } from "./lib/wildfires";
  import { onMount } from "svelte";
  import HomePage from "./pages/HomePage.svelte";
  import MapPage from "./pages/MapPage.svelte";

  let currentRoute = "/map";

  onMount(async () => {
    try {
      const fire = await getWildFire("EFnlJ7dUtmLCF5qhHg1N");
      console.log(fire);
    } catch (error) {
      console.error(error);
    }
  });

  const routes: {
    [key: string]: any;
  } = {
    "/": HomePage,
    "/map": MapPage,
  };

  onMount(() => {
    currentRoute = window.location.pathname;
    window.onpopstate = () => {
      currentRoute = window.location.pathname;
    };
  });
</script>

<main>
  {#if routes[currentRoute]}
    <svelte:component this={routes[currentRoute]} />
  {:else}
    <h1>404 - Page Not Found</h1>
  {/if}
</main>
