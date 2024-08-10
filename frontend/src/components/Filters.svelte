<script lang="ts">
  import flatpickr from "flatpickr";
  import "flatpickr/dist/flatpickr.min.css";
  import { filtersRotated } from "./store"; 
  import { coordinatesY } from "./store";
  import { get } from "svelte/store";
  
  

  
  let coordinatesRotated = false;
  let dateChecked = false;
  let provinceChecked = false;
  let startDate = "";
  let endDate = "";
  let provinceInput = "";
  let newYValue = coordinatesY;



  const filteredProvinces = [
    "Alberta",
    "British Columbia",
    "Manitoba",
    "New Brunswick",
    "Newfoundland and Labrador",
    "Northwest Territories",
    "Nova Scotia",
    "Nunavut",
    "Ontario",
    "Prince Edward Island",
    "Quebec",
    "Saskatchewan",
    "Yukon",
  ];

  function toggleFiltersRotation() {
    filtersRotated.update(value => !value);
  
    if($filtersRotated && !provinceChecked && !dateChecked){
      coordinatesY.update(currentY => 150);
      console.log($coordinatesY);
    }
    else if($filtersRotated && provinceChecked && dateChecked){
      coordinatesY.update(currentY => 400);
      console.log($coordinatesY);
    }

    else if($filtersRotated && dateChecked){
      coordinatesY.update(currentY => 230);
    }
    else if($filtersRotated && provinceChecked){
      coordinatesY.update(currentY => 320);
    }
    
    
    else{
      coordinatesY.update(currentY => 3);
    }
    
    }
  



  function byDateChecked() {
    dateChecked = !dateChecked;
    if (dateChecked) {
      initializeFlatpickr();
      coordinatesY.update(currentY => currentY + 80);
    }
    else{
      coordinatesY.update(currentY => currentY - 80);
    }
<<<<<<< HEAD:frontend/src/lib/MapBox/Filters.svelte
   
=======
>>>>>>> ae0735f1784bba2ab4ac95e5f6ad3f993b832f86:frontend/src/components/Filters.svelte
  }
  function initializeFlatpickr() {
    flatpickr("#start-date", { dateFormat: "d/m/Y" });
    flatpickr("#end-date", { dateFormat: "d/m/Y" });
  }
  function byProvinceChecked() {
    provinceChecked = !provinceChecked;

    if(provinceChecked){
      initializeFlatpickr();
      coordinatesY.update(currentY => currentY + 170);
    }
    else{
      coordinatesY.update(currentY => currentY - 170);
    }
    
  }

  function filterProvinces() {}
</script>

<div id="filters" class="filters" on:click={toggleFiltersRotation}>
  Filters&nbsp;<span id="last-char" class:rotated={$filtersRotated}>&gt;</span>
</div>



<div class="checkbox-container {($filtersRotated) ? 'show' : ''}">
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
        on:click={initializeFlatpickr}
      />
      to
      <input
        type="text"
        bind:value={endDate}
        id="end-date"
        placeholder="End Date"
        class="text-field"
      />
    </div>
  {/if}
  <label class="custom-checkbox">
    <input
      type="checkbox"
      name="filter"
      value="province"
      on:change={byProvinceChecked}
    />
    <span class="custom-checkmark"></span>
    By Province
  </label>
  {#if provinceChecked}
    <div class="by-province-dropdown">
      <input
        type="text"
        bind:value={provinceInput}
        on:click={filterProvinces}
        placeholder="Select Province"
        class="text-field"
        id="text-field-province"
        readonly
      />
      {#if filteredProvinces.length > 0}
        <ul class="province-list">
          {#each filteredProvinces as province}
            <li on:click={() => (provinceInput = province)}>{province}</li>
          {/each}
        </ul>
      {/if}
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
    font-family: "Lilita One", sans-serif;
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
  }
  .filters:hover {
     top: 16.35%;
     left: 5.83%;  
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
    transform: translateX(-160%);
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
  #text-field-province {
    width: 140px;
    margin-left: 0px;
  }

  .by-province-dropdown {
    position: relative;
    margin-top: 10px;
  }

  .province-list {
    list-style-type: none;
    padding: 0;
    margin: 0;
    position: left;
    width: 150px;
    background-color: transparent;
    border: 1px solid rgba(180, 159, 155, 0.895);
    border-radius: 4px;
    max-height: 75px;
    overflow-y: auto;
    z-index: 10;
  }

  .province-list li {
    padding: 10px;
    font-size: 18px;
  }

  .province-list li:hover {
    background-color: rgba(180, 159, 155, 0.2);
  }
  .flatpickr-calendar {
    z-index: 9999;
  }
  #text-field-province:focus + .dropdown-content {
    display: block;
  }
</style>
