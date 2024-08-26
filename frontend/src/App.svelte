<script lang="ts">
  // import { getWildFires } from "./lib/wildfires";
  import { onMount } from "svelte";
  import MapPage from "./pages/MapPage.svelte";

  let currentRoute = "/map";

  // onMount(async () => {
  //   try {
  //     //const fire = await getWildFires();
  //     console.log("app");
  //     //console.log(fire);
  //   } catch (error) {
  //     console.error(error);
  //   }
  // });

  const routes: {
    [key: string]: any;
  } = {
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
