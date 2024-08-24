import mapboxgl from "mapbox-gl";
import FireSvg from "../components/FireSvg.svelte";

export function createFireMarker(width?: number, height?: number, color?: string, weather?: JSON, lon?: number, lat?: number, map) {
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

  const popup = new mapboxgl.Popup({ offset: 15 });

  // Add hover event listeners
  marker.addEventListener('mouseenter', () => {
    console.log("Marker hovered: ", weather);
    const fields = weather.split(",");
    const latValue = parseFloat(fields[0].split(':')[1]);
    const lonValue = parseFloat(fields[1].split(':')[1]);
    const date = parseFloat(fields[2].split(':')[1]);
    console.log(latValue);
    const popupContent = `<div class="popup-box">
            <strong>Lat:</strong> ${latValue}<br>
            <strong>Lon:</strong> ${lonValue}<br>
            <strong>Date:</strong> ${date}
        </div>`;
        
    popup.setLngLat([lon, lat])
        .setHTML(popupContent)
        .addTo(map);
  });

  marker.addEventListener('mouseleave', () => {
    console.log("Marker unhovered");
    popup.remove();
  });

  return new mapboxgl.Marker(marker);
}

export function createPredictFireMarker(width?: number, height?: number) {
  return createFireMarker(width, height, "red");
}