<script lang="ts">
  import { coordinatesY } from "../lib/store";
  import { createFireMarker } from "../lib/utils";

  let coordinatesRotated = false;
  let longInput = "";
  let latInput = "";
  let isHovered = false;
  export let map: mapboxgl.Map;

  let yPosition: number;
  $: yPosition = $coordinatesY;

  $: coordinatesStyle = `
    transform: translateY(${yPosition}%);
    transition: transform 0.4s ease;
  `;
  $: hoverStyle = `
    font-size: ${isHovered ? "35px" : "30px"};
    color: ${isHovered ? "rgba(202, 120, 104, 0.895)" : "rgba(180, 159, 155, 0.895)"};
    transition: font-size 0.3s ease, color 0.3s ease;
  `;

  // Combine transformations for text
  $: combinedStyle = `
    transform: translateY(${yPosition + 50}%) translateX(${coordinatesRotated ? 0 : -135}%);
    transition: transform 0.4s ease;
  `;

  $: combinedStyleBttn = `
    transform: translateY(${yPosition + 50}%) translateX(${coordinatesRotated ? 0 : -400}%);
    transition: transform 0.4s ease;
  `;

  function toggleCoordinatesRotation() {
    coordinatesRotated = !coordinatesRotated;
  }

  function onMouseEnter() {
    isHovered = true;
  }

  function onMouseLeave() {
    isHovered = false;
  }

  function predict(lat: number, lon: number) {
    const fireMarker = createFireMarker(30, 30);
    fireMarker.setLngLat([lon, lat]).addTo(map);

    // HTTP post to backend server

    interface PostData {
      args: string[];
    }

    const data: PostData = {
      args: ["--lat", lat.toString(), "--lon", lon.toString()]
    };

    // Make the POST request using fetch
    fetch('http://18.217.35.228:5000/fire-analysis', {
      method: 'POST', // Specify the request method as POST
      headers: {
        'Content-Type': 'application/json', // Specify the content type
      },
      body: JSON.stringify(data) // Convert the data object to a JSON string
    })
    .then(response => response.json())
    .then((data: any) => { // Specify the type of the response data
      console.log('Success:', data); // Handle the response data
    })
    .catch((error: Error) => {
      console.error('Error:', error); // Handle any errors
    });
  }
</script>

<div
  class="coordinates"
  style={coordinatesStyle + hoverStyle}
  on:click={toggleCoordinatesRotation}
  on:mouseenter={onMouseEnter}
  on:mouseleave={onMouseLeave}
>
  Coordinates&nbsp;<span id="last-char" class:rotated={coordinatesRotated}
    >&gt;</span
  >
</div>

<div id="long-text" class="text" style={combinedStyle}>
  Longitude:
  <input type="text" bind:value={longInput} class="text-field" />
</div>

<div id="lat-text" class="text" style={combinedStyle}>
  Latitude:
  <input type="text" bind:value={latInput} class="text-field" />
</div>

<div id="submit-button" class="text" style={combinedStyleBttn}>
  <button
    class="button-30"
    on:click={() => predict(parseFloat(latInput), parseFloat(longInput))}
    >Predict</button
  >
</div>

<style>
  #last-char {
    transition: transform 0.3s ease;
  }

  #last-char.rotated {
    transform: rotate(90deg);
  }

  .coordinates {
    position: absolute;
    top: 22.9%;
    left: 6.5%;
    padding: 10px;
    font-size: 30px; /* Base font size */
    border-radius: 5px;
    font-style: normal;
    z-index: 10;
    font-family: "Lilita One", sans-serif;
    cursor: pointer;
    display: flex;
    align-items: center;
    transition:
      transform 0.4s ease,
      font-size 0.3s ease,
      color 0.3s ease;
  }

  .text-field {
    margin: 0 10px;
    padding: 5px 10px;
    width: 100px;
    max-height: 30px;
    font-size: 18px;
    border: 1px solid rgba(180, 159, 155, 0.895);
    border-radius: 4px;
    outline: none;
    background-color: transparent;
  }

  .text {
    position: absolute;
    font-size: 25px;
    z-index: 10;
    font-family: "Lilita One", sans-serif;
    cursor: pointer;
    color: rgba(180, 159, 155, 0.895);
    transition: transform 0.4s ease;
    transform: translateX(-135%);
  }

  .text.show {
    transform: translateX(0);
  }

  #long-text {
    top: 250px;
    left: 97px;
    padding: 10px;
    border-radius: 5px;
  }

  #lat-text {
    top: 313px;
    left: 97px;
    padding: 10px;
    border-radius: 5px;
  }
  .button-30 {
    align-items: center;
    appearance: none;
    background-color: #d8bfc4;
    border-radius: 4px;
    border-width: 0;
    box-shadow:
      rgba(45, 35, 66, 0.4) 0 2px 4px,
      rgba(45, 35, 66, 0.3) 0 7px 13px -3px,
      #d8bfc4 0 -3px 0 inset;
    box-sizing: border-box;
    color: #917b7b;
    cursor: pointer;
    display: inline-flex;
    height: 48px;
    justify-content: center;
    line-height: 1;
    list-style: none;
    overflow: hidden;
    padding-left: 16px;
    padding-right: 16px;
    position: relative;
    text-align: left;
    text-decoration: none;
    transition:
      box-shadow 0.15s,
      transform 0.15s;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
    white-space: nowrap;
    will-change: box-shadow, transform;
    font-size: 18px;
    z-index: 100;
    top: 17.2%;
    left: 190%;
  }

  .button-30:focus {
    box-shadow:
      #d6d6e7 0 0 0 1.5px inset,
      rgba(45, 35, 66, 0.4) 0 2px 4px,
      rgba(45, 35, 66, 0.3) 0 7px 13px -3px,
      #d6d6e7 0 -3px 0 inset;
  }

  .button-30:hover {
    box-shadow:
      rgba(45, 35, 66, 0.4) 0 4px 8px,
      rgba(45, 35, 66, 0.3) 0 7px 13px -3px,
      #d6d6e7 0 -3px 0 inset;
    transform: translateY(-2px);
  }

  .button-30:active {
    box-shadow: #d6d6e7 0 3px 7px inset;
    transform: translateY(2px);
  }
</style>
