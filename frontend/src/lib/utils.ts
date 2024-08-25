import mapboxgl from "mapbox-gl";
import FireSvg from "../components/FireSvg.svelte";

export function createFireMarker(width?: number, height?: number, color?: string, weather?: JSON, map: any) {
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
    console.log(fields);
    const latValue = parseFloat(fields[0].split(':')[1]);
    const lonValue = parseFloat(fields[1].split(':')[1]);
    const date = fields[2].split(':')[1].slice(1, -1);
    const elevation = parseFloat(fields[3].split(':')[1]);
    const mean_temp = parseFloat(fields[4].split(':')[1]);
    const max_temp = parseFloat(fields[5].split(':')[1]);
    const min_temp = parseFloat(fields[6].split(':')[1]);
    const wind = parseFloat(fields[7].split(':')[1]);
    const wind_dir = parseFloat(fields[8].split(':')[1]);
    const precip = parseFloat(fields[9].split(':')[1]);
    const humidity = parseFloat(fields[10].split(':')[1]);
    const pressure = parseFloat(fields[11].split(':')[1]);
    const soil_temp = parseFloat(fields[12].split(':')[1]);
    const soil_moisture = parseFloat(fields[13].split(':')[1]);
    const snow = parseFloat(fields[14].split(':')[1]);

    console.log(latValue);
    const popupContent = `<div class="popup-box">
            <strong>Lat:</strong> ${latValue}<br>
            <strong>Lon:</strong> ${lonValue}<br>
            <strong>Date:</strong> ${date}<br>
            <strong>Elevation:</strong> ${elevation} m<br>
            <strong>Mean temperature:</strong> ${mean_temp}°C<br>
            <strong>Max temperature:</strong> ${max_temp}°C<br>
            <strong>Min temperature:</strong> ${min_temp}°C<br>
            <strong>Wind:</strong> ${wind} km/h<br>
            <strong>Wind direction:</strong> ${wind_dir}°<br>
            <strong>Precipitation:</strong> ${precip} mm<br>
            <strong>Humidity:</strong> ${humidity}%<br>
            <strong>Pressure:</strong> ${pressure} hPa<br>
            <strong>Soil temperature:</strong> ${soil_temp}°C<br>
            <strong>Soil moisture:</strong> ${soil_moisture} m³/m³<br>
            <strong>Snow:</strong> ${snow} cm<br>
        </div>`;
        
    popup.setLngLat([lonValue, latValue])
        .setHTML(popupContent)
        .addTo(map);
  });

  marker.addEventListener('mouseleave', () => {
    console.log("Marker unhovered");
    popup.remove();
  });

  return new mapboxgl.Marker(marker);
}