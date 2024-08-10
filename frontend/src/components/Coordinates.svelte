<script lang="ts">
  import { onMount } from "svelte";
  import { filtersRotated } from "./store"; 
  import { coordinatesY } from "./store";

  let coordinatesRotated = false;
  let longInput = "";
  let latInput = "";
  let isHovered = false;
  
  let yPosition: number;
  $: yPosition = $coordinatesY; 

  $: coordinatesStyle = `
    transform: translateY(${yPosition}%);
    transition: transform 0.4s ease;
    
    
  `;

  $: hoverStyle = `
    font-size: ${isHovered ? '35px' : '30px'};
    transition: font-size 0.1s ease;
    color: ${isHovered ? 'rgba(202, 120, 104, 0.895)' : ''};
  `;

  // Combine them into a single transform property
  $: combinedStyle =  `transform: translateY(${yPosition + 20}%) translateX(${coordinatesRotated ? 0 : -135}%); transition: transform 0.4s ease;`;
  

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
  style={coordinatesStyle + (isHovered ? ` ${hoverStyle}` : '')} 
  on:click={toggleCoordinatesRotation}
  on:mouseenter={onMouseEnter}
  on:mouseleave={onMouseLeave}
>
  Coordinates&nbsp;<span id="last-char" class:rotated={coordinatesRotated}>&gt;</span>
</div>

<div id="long-text" class="text  " style={combinedStyle} > 
  Longitude:
  <input
    type="text"
    bind:value={longInput}
    class="text-field"
  />
</div>

<div id="lat-text" class="text" style={combinedStyle} > 
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
    font-size: 30px;
    border-radius: 5px;
    font-style: normal;
    z-index: 10;
    font-family: "Lilita One", sans-serif;
    cursor: pointer;
    color: rgba(180, 159, 155, 0.895);
    display: flex;
    align-items: center;
    transform: translateY(0);
    transition: transform 0.4s ease;
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
    transition: transform 0.3s ease;
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
  .text:hover{
    color: rgba(212, 155, 144, 0.895);
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