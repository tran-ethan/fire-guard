<script lang="ts">
    import mapboxgl from "mapbox-gl";
    import { onMount } from "svelte";
    mapboxgl.accessToken =
        "pk.eyJ1IjoicGFyc2FqYWZhcmlhbiIsImEiOiJjbHhxbDljdzYwY2ZpMmxwbnR1dTQ2YThyIn0.4zJwGh7wfpqCorynBky0DQ";

    let map: mapboxgl.Map;

    onMount(() => {
        const link = document.createElement("link");
        link.href = "https://api.mapbox.com/mapbox-gl-js/v2.6.1/mapbox-gl.css";
        link.rel = "stylesheet";
        document.head.appendChild(link);

        map = new mapboxgl.Map({
            container: "map",
            center: [0, 0],
            zoom: 2
        });
    });
</script>

<div id="map">

</div>

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
