<script lang="ts">
  import { coordinatesY } from "./store";

  let coordinatesRotated = false;
  let longInput = "";
  let latInput = "";
  let isHovered = false;

  let yPosition: number;
  $: yPosition = $coordinatesY;

  // Transform style based on yPosition and rotation
  $: coordinatesStyle = `
    transform: translateY(${yPosition}%);
    transition: transform 0.4s ease;
  `;

  // Hover style for font-size and color changes
  $: hoverStyle = `
    font-size: ${isHovered ? '35px' : '30px'};
    color: ${isHovered ? 'rgba(202, 120, 104, 0.895)' : 'rgba(180, 159, 155, 0.895)'};
    transition: font-size 0.3s ease, color 0.3s ease;
  `;

  // Combine transformations for text
  $: combinedStyle = `
    transform: translateY(${yPosition + 50}%) translateX(${coordinatesRotated ? 0 : -135}%);
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
</script>

<div 
  class="coordinates" 
  style={coordinatesStyle + hoverStyle}
  on:click={toggleCoordinatesRotation}
  on:mouseenter={onMouseEnter}
  on:mouseleave={onMouseLeave}
>
  Coordinates&nbsp;<span id="last-char" class:rotated={coordinatesRotated}>&gt;</span>
</div>

<div id="long-text" class="text" style={combinedStyle}> 
  Longitude:
  <input
    type="text"
    bind:value={longInput}
    class="text-field"
  />
</div>

<div id="lat-text" class="text" style={combinedStyle}> 
  Latitude:
  <input
    type="text"
    bind:value={latInput}
    class="text-field"
  />
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
    transition: transform 0.4s ease, font-size 0.3s ease, color 0.3s ease;
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
</style>