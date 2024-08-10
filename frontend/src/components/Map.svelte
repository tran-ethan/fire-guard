<script lang="ts">
  import mapboxgl from "mapbox-gl";
  import { onMount } from "svelte";
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

    // // Example point data
    // const points = [
    //   { coordinates: [45.5017, -73.5673], description: "Point 1" },
    //   { coordinates: [-74.6, 40.1], description: "Point 2" },
    //   { coordinates: [-74.4, 40.2], description: "Point 3" },
    // ];

    // // Add points as markers to the map
    // points.forEach((point) => {
    //   const el = document.createElement("div");
    //   el.className = "marker";

    //   new mapboxgl.Marker(el)
    //     .setLngLat(point.coordinates as mapboxgl.LngLatLike)
    //     .setPopup(new mapboxgl.Popup({ offset: 25 }).setText(point.description)) // add popups
    //     .addTo(map);
    // });
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
