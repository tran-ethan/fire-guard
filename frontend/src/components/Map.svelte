<script lang="ts">
  import mapboxgl from "mapbox-gl";
  import { onMount } from "svelte";
  import { createFireMarker } from "../lib/utils";
  import { getWildFires } from "../lib/wildfires";
  mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_ACCESS_TOKEN as string;
  let map: mapboxgl.Map;

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

    const fires = await getWildFires();


    fires.forEach((fire) => {
      const fireMarker = createFireMarker(30, 30);
      fireMarker
        .setLngLat([fire.lon, fire.lat])
        .addTo(map);
    });
  });
</script>

<div id="map"></div>

<style>
  #map {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
  }
</style>
