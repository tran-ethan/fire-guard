<script lang="ts">
  import { coordinatesY } from "../lib/store";
  import { createFireMarker } from "../lib/utils";
  import  { showPopup } from "../lib/store";
  import  { popupText } from "../lib/store";
  import  { firePrediction } from "../lib/store";
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
    transform: translateY(${yPosition + 50}%) translateX(${coordinatesRotated ? 0 : -155}%);
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
      console.log('Success:', data); // Log the response data

      // Put firemarker with data
      const prediction = parseInt(data.prediction);
      const probability = parseFloat(data.probability);
      if (prediction === 1) {
        const fireMarker = createFireMarker(map, JSON.stringify(data.weather), probability, 30, 30);
        fireMarker.setLngLat([lon, lat]).addTo(map);;
        firePrediction.set(true)
      } else {
        firePrediction.set(false)
      }

      // Pop up text
      popupText.set(`Predicted at ${latInput}, ${longInput} with probability ${(probability * 100).toFixed(2)}%`);

      // Show the popup
      showPopup.set(true);
      showPopup.subscribe(value => {
        console.log('showPopup value:', value);
      });
    })
    .catch((error: Error) => {
      console.error('Error:', error); // Handle any errors
    });
    map.flyTo({
        center: [lon, lat],
        zoom: 12,
        speed: 0.9,
        curve: 1,
        easing(t) {
            return t;
        }
    });

  }
</script>

<body>
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

<div id="lat-text" class="text" style={combinedStyle}>
  Latitude:
  <input type="text" bind:value={latInput} class="text-field" />
</div>

<div id="long-text" class="text" style={combinedStyle}>
  Longitude:
  <input type="text" bind:value={longInput} class="text-field" />
</div>

<div id="submit-button" class="text" style={combinedStyleBttn} >
  <button
    class="button-30"
    on:click={() => predict(parseFloat(latInput), parseFloat(longInput))}
    >Predict</button
  >
</div>
</body>





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
    
  font-family: "Lilita One", sans-serif;
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
    
  font-family: "Lilita One", sans-serif;
    position: absolute;
    font-size: 25px;
    z-index: 10;
    font-family: "Lilita One", sans-serif;
    cursor: pointer;
    color: rgba(180, 159, 155, 0.895);
    transition: transform 0.4s ease;
    transform: translateX(-145%);
  }

  .text.show {
    transform: translateX(0);
  }

  #long-text {
    top: 313px;
    left: 97px;
    padding: 10px;
    border-radius: 5px;
  }

  #lat-text {
    top: 250px;
    left: 97px;
    padding: 10px;
    border-radius: 5px;
  }
  
</style>
