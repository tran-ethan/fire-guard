<script lang="ts">
  import MapPage from "./pages/MapPage.svelte";

  const routes: {
    [key: string]: any;
  } = {
    "/map": MapPage,
  };
</script>

<main>
  <MapPage />
</main>
