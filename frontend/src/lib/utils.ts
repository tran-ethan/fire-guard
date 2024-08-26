import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { cubicOut } from "svelte/easing";
import type { TransitionConfig } from "svelte/transition";
import mapboxgl from "mapbox-gl";
import FireSvg from "../components/FireSvg.svelte";

export function cn(...inputs: ClassValue[]) {
	return twMerge(clsx(inputs));
}

type FlyAndScaleParams = {
	y?: number;
	x?: number;
	start?: number;
	duration?: number;
};

export const flyAndScale = (
	node: Element,
	params: FlyAndScaleParams = { y: -8, x: 0, start: 0.95, duration: 150 }
): TransitionConfig => {
	const style = getComputedStyle(node);
	const transform = style.transform === "none" ? "" : style.transform;

	const scaleConversion = (
		valueA: number,
		scaleA: [number, number],
		scaleB: [number, number]
	) => {
		const [minA, maxA] = scaleA;
		const [minB, maxB] = scaleB;

		const percentage = (valueA - minA) / (maxA - minA);
		const valueB = percentage * (maxB - minB) + minB;

		return valueB;
	};

	const styleToString = (
		style: Record<string, number | string | undefined>
	): string => {
		return Object.keys(style).reduce((str, key) => {
			if (style[key] === undefined) return str;
			return str + `${key}:${style[key]};`;
		}, "");
	};

	return {
		duration: params.duration ?? 200,
		delay: 0,
		css: (t) => {
			const y = scaleConversion(t, [0, 1], [params.y ?? 5, 0]);
			const x = scaleConversion(t, [0, 1], [params.x ?? 0, 0]);
			const scale = scaleConversion(t, [0, 1], [params.start ?? 0.95, 1]);

			return styleToString({
				transform: `${transform} translate3d(${x}px, ${y}px, 0) scale(${scale})`,
				opacity: t
			});
		},
		easing: cubicOut
	};
};


export function createFireMarker(map: any, weather: string, probability?: number, width?: number, height?: number, color?: string) {
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

  const popup = new mapboxgl.Popup({ offset: 15 });

  // Add hover event listeners
  marker.addEventListener('mouseenter', () => {
    console.log("Marker hovered: ", weather);
    const fields = weather.split(",");

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

    const probabilityContent = probability !== undefined 
      ? `<strong >Probability:</strong> <span style="color: green;">${(probability * 100).toFixed(2)}%</span><br>` 
      : "";

    const popupContent = `
        <div class="popup-box">
            ${probabilityContent}
            <strong>Lat:</strong> ${latValue}°<br>
            <strong>Lon:</strong> ${lonValue}°<br>
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
        </div>
      `;
        
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