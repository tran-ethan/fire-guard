<script lang="ts">
  import Coordinates from "../components/Coordinates.svelte";
  import Filters from "../components/Filters.svelte";
  import Map from "../components/Map.svelte";
  import mapboxgl from "mapbox-gl";
  import { onMount } from "svelte";
  import { createFireMarker } from "../lib/utils";
  import { getWildFires } from "../lib/wildfires";
  import Prediction from "../components/Prediction.svelte";
  import Overlay from "../components/Overlay.svelte";


  mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_ACCESS_TOKEN as string;
  let map: mapboxgl.Map;

  function sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async function addFireMarkers(old_fires_json: any[], map: any) {
    for (const fire of old_fires_json) {
      const fireMarker = createFireMarker(map, JSON.stringify(fire), undefined, 30, 30);
      fireMarker.setLngLat([fire.lon, fire.lat]).addTo(map);
      await sleep(1);
    }
  }

  onMount(async () => {
    const link = document.createElement("link");
    link.href = "https://api.mapbox.com/mapbox-gl-js/v2.6.1/mapbox-gl.css";
    link.rel = "stylesheet";
    document.head.appendChild(link);

    map = new mapboxgl.Map({
      container: "map",
      center: [-85, 59],
      zoom: 3,
    });

    // Define bounds that conform to the `LngLatBoundsLike` object.
    const bounds = [
      [-141.00194, 41.68139], // [west, south]
      [-52.61944, 83.11139], // [east, north]
    ];
    // Set the map's max bounds.
    map.setMaxBounds(bounds as mapboxgl.LngLatBoundsLike);

    // Example of how to use the get-fires POST endpoint

    // let startDate = "01-05-2005"
    // let endDate = "03-05-2005"

    // const fires = await getWildFires(startDate, endDate);

    // const old_fires = fires.old
    // const live_fires = fires.live

    // const old_fires_json = JSON.parse(old_fires);
    // const live_fires_json = JSON.parse(live_fires);

    // addFireMarkers(old_fires_json, map);
    // addFireMarkers(live_fires_json, map);
  });
</script>

<div>
  <title on:click={() => (window.location.href = "/")}>
    <!-- <img src="logo.png" alt="Icon" class="icon" /> -->
    Fire Guard
  </title>
  <!-- <Overlay /> -->

  <home on:click={() => (window.location.href = "/")}> Home </home>

  <Map/>
  <Filters map={map}/>
  <Coordinates map={map} />
  <Prediction />
</div>
