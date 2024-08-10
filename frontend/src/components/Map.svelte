<script lang="ts">
  import mapboxgl from "mapbox-gl";
  import { onMount } from "svelte";
  import { createFireMarker } from "../lib/utils";
  mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_ACCESS_TOKEN as string;
  let map: mapboxgl.Map;

  onMount(() => {
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

    // Example point data
    const points = [
      { coordinates: [-79.347015, 43.65107], description: "Toronto, Ontario" },
      { coordinates: [-73.561668, 45.508888], description: "Montreal, Quebec" },
      {
        coordinates: [-123.120738, 49.282729],
        description: "Vancouver, British Columbia",
      },
      {
        coordinates: [-114.071883, 51.044733],
        description: "Calgary, Alberta",
      },
      {
        coordinates: [-113.493823, 53.546124],
        description: "Edmonton, Alberta",
      },
      { coordinates: [-75.697193, 45.42153], description: "Ottawa, Ontario" },
      {
        coordinates: [-97.138374, 49.895136],
        description: "Winnipeg, Manitoba",
      },
      {
        coordinates: [-71.207981, 46.813878],
        description: "Quebec City, Quebec",
      },
      {
        coordinates: [-79.871102, 43.255721],
        description: "Hamilton, Ontario",
      },
      {
        coordinates: [-80.492533, 43.451639],
        description: "Kitchener, Ontario",
      },
    ];

    points.forEach((point) => {
      const fireMarker = createFireMarker(40, 40);
      fireMarker
        .setLngLat(point.coordinates as mapboxgl.LngLatLike)
        .setPopup(new mapboxgl.Popup({ offset: 25 }).setText(point.description))
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
