import mapboxgl from "mapbox-gl";
import FireSvg from "../components/FireSvg.svelte";

export function createFireMarker(width?: number, height?: number, color?: string) {
  const marker = document.createElement("div");
  marker.className = "fire-marker";

  const props: { width?: string; height?: string, color?: string } = {};

  // Conditionally add props if they are defined
  if (width !== undefined) {
    props.width = width.toString();
  }
  if (height !== undefined) {
    props.height = height.toString();
  }
  if (color !== undefined) {
    props.color = color.toString();
  }

  new FireSvg({
    target: marker,
    props,
  });

  return new mapboxgl.Marker(marker);
}

export function createPredictFireMarker(width?: number, height?: number) {
  return createFireMarker(width, height, "red");
}