<script lang="ts">
    import { get } from "svelte/store";
  import { coordinatesY } from "../lib/store";
  import { showPopup } from "../lib/store";
  import { createFireMarker } from "../lib/utils";

  let coordinatesRotated = false;
  let longInput = "";
  let latInput = "";
  let isHovered = false;
  export let map: mapboxgl.Map;

 

  function toggleCoordinatesRotation() {
    coordinatesRotated = !coordinatesRotated;
  }

  function onMouseEnter() {
    isHovered = true;
  }

  function onMouseLeave() {
    isHovered = false;
  }
  function handleBttnClick(){
    
    showPopup.set(true);
    showPopup.subscribe(value => {
    console.log('showPopup value:', value);
  });
    predict(parseFloat(latInput), parseFloat(longInput));
    
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
      console.log('Success:', data); // Handle the response data
      const fields = data.weather.split(",");
      const latValue = parseFloat(fields[0].split(':')[1]);
      const fireMarker = createFireMarker(30, 30, undefined, data.weather, lon , lat, map);
      fireMarker.setLngLat([lon, lat]).addTo(map);
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
  on:click={toggleCoordinatesRotation}
  on:mouseenter={onMouseEnter}
  on:mouseleave={onMouseLeave}
>
  Coordinates&nbsp;<span id="last-char" class:rotated={coordinatesRotated}
    >&gt;</span>
</div>

<div id="lat-text" class="text">
  Latitude:
  <input type="text" bind:value={latInput} class="text-field" />
</div>

<div id="long-text" class="text">
  Longitude:
  <input type="text" bind:value={longInput} class="text-field" />
</div>



<div id="submit-button" class="text">
  <button
    class="button-30"
    on:click= {handleBttnClick}
  
    >Predict</button
  >
</div>
</body>


<style>
body {
  position: relative;
  display: flex;
  flex-direction: column; /* or row depending on your layout */
  justify-content: flex-start; /* Aligns items to the top (or left if flex-direction is row) */
  align-items: flex-start; /* Aligns items to the left */
  top: 100px;
    left: 96.5px;
}
  #last-char {
    transition: transform 0.3s ease;
  }

  #last-char.rotated {
    transform: rotate(90deg);
  }

  .coordinates {
    position: absolute;
    color: rgba(189, 144, 144, 0.842);
    
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
  .coordinates:hover{
    padding: 10px;
    font-size: 35px;
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
  #lat-text {
    padding: 10px;
    border-radius: 5px;
  }
  #long-text {
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
