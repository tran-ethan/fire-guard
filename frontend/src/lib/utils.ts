import mapboxgl from "mapbox-gl";
import FireSvg from "../components/FireSvg.svelte";

export function createFireMarker(width?: number, height?: number) {
  const marker = document.createElement("div");
  marker.className = "fire-marker";

  const props: { width?: string; height?: string } = {};

  // Conditionally add props if they are defined
  if (width !== undefined) {
    props.width = width.toString();
  }
  if (height !== undefined) {
    props.height = height.toString();
  }

  new FireSvg({
    target: marker,
    props,
  });

  return new mapboxgl.Marker(marker);
}
