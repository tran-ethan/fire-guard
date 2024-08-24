import mapboxgl from "mapbox-gl";
import FireSvg from "../components/FireSvg.svelte";

export function createFireMarker(width?: number, height?: number, color?: string, weather?: JSON) {
  const marker = document.createElement("div");
  marker.className = "fire-marker";

  const props: { width?: string; height?: string, color?: string, weather?: JSON } = {};

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

  // Add hover event listeners
  marker.addEventListener('mouseenter', () => {
    console.log("Marker hovered: ", weather);
    // Add any additional hover behavior here
  });

  marker.addEventListener('mouseleave', () => {
    console.log("Marker unhovered");
    // Add any additional unhover behavior here
  });

  return new mapboxgl.Marker(marker);
}

export function createPredictFireMarker(width?: number, height?: number) {
  return createFireMarker(width, height, "red");
}