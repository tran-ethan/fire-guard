<script lang="ts">
  import flatpickr from "flatpickr";
  import "flatpickr/dist/flatpickr.min.css";
  import { filtersRotated } from "../lib/store";
  import { coordinatesY } from "../lib/store";
    import { onMount } from "svelte";
  

  let coordinatesRotated = false;
  let dateChecked = false;
  let startDate = "";
  let endDate = "";
  let newYValue = coordinatesY;


  function toggleFiltersRotation() {
    filtersRotated.update((value) => !value);

    if ($filtersRotated && !dateChecked) {
      coordinatesY.update((currentY) => 150);
      console.log($coordinatesY);
    } else if ($filtersRotated && dateChecked) {
      coordinatesY.update((currentY) => 230);
    }else {
      coordinatesY.update((currentY) => 3);
    }
  }

  function byDateChecked() {
    dateChecked = !dateChecked;
    
    if (dateChecked) {
      coordinatesY.update((currentY) => currentY + 80);
    } else {
      coordinatesY.update((currentY) => currentY - 80);
    }
  }
  function initializeFlatpickrStrt() {
    flatpickr("#start-date", { dateFormat: "d/m/Y" });
  }
  function initializeFlatpickrEnd() {
    flatpickr("#end-date", { dateFormat: "d/m/Y" });
  }
 

  onMount(() => {
    flatpickr("#start-date", { dateFormat: "d/m/Y" });
    flatpickr("#end-date", { dateFormat: "d/m/Y" });
  });
</script>

<div id="filters" class="filters" on:click={toggleFiltersRotation}>
  Filters&nbsp;<span id="last-char" class:rotated={$filtersRotated}>&gt;</span>
</div>

<div class="checkbox-container {$filtersRotated ? 'show' : ''}">
  <label class="custom-checkbox">
    <input
      type="checkbox"
      name="filter"
      value="date"
      on:change={byDateChecked}
    />
    <span class="custom-checkmark"></span>
    By Date
  </label>
  {#if dateChecked}
    <div class="by-date-label">
      <input
        type="text"
        bind:value={startDate}
        id="start-date"
        placeholder="Start Date"
        class="text-field"
        readonly
        on:click={initializeFlatpickrStrt()}
      />
      to
      <input
        type="text"
        bind:value={endDate}
        id="end-date"
        placeholder="End Date"
        class="text-field"
        readonly
        on:click={initializeFlatpickrEnd()}
      />
    </div>
  {/if}
  
</div>

<style>
  #last-char {
    /*display: inline-block;*/
    transition: transform 0.3s ease;
  }

  #last-char.rotated {
    transform: rotate(90deg);
  }

  .filters {
    position: absolute;
    top: 17.2%;
    left: 6.5%;
    padding: 10px;
    border-radius: 5px;
    font-size: 30px;
    font-style: normal;
    z-index: 10;
    cursor: pointer;
    color: rgba(180, 159, 155, 0.895);
    display: flex;
    align-items: center;
    transition: font-size 0.1s ease;
  }
  .filters:hover {
    color: rgba(202, 120, 104, 0.895);
    font-size: 40px;
  }
  .checkbox-container {
    position: absolute;
    font-family: "Lilita One", sans-serif;
    font-size: 25px;
    font-style: normal;
    z-index: 10;
    left: 77px;
    top: 24.3%;
    color: rgba(180, 159, 155, 0.895);
    transform: translateX(-170%);
    transition: transform 0.3s ease;
  }

  .custom-checkbox input {
    position: absolute;
    opacity: 0;
  }

  .custom-checkmark {
    height: 20px;
    width: 20px;
    background-color: transparent;
    border: 4px solid rgba(180, 159, 155, 0.895);
    border-radius: 50%;
    display: inline-block;
    margin-right: 10px;
    transition:
      background-color 0.2s ease,
      border-color 0.2s ease;
  }

  .custom-checkbox input:checked + .custom-checkmark {
    content: "";

    background-color: white;
  }

  .checkbox-container.show {
    flex-direction: column;
    transform: translateX(0);
  }

  .checkbox-container label {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }

  .checkbox-container input[type="checkbox"] {
    margin-right: 10px;
  }
  .checkbox-container label:hover {
    color: rgba(212, 155, 144, 0.895);
  }
  .text-field {
    margin: 0 10px;
    padding: 5px 10px;
    width: 120px;
    font-size: 18px;
    border: 1px solid rgba(180, 159, 155, 0.895);
    border-radius: 4px;
    outline: none;
    background-color: transparent;
    transition:
      border-color 0.2s ease,
      box-shadow 0.2s ease;
  }
  
  .flatpickr-calendar {
    z-index: 99;
  }
</style>