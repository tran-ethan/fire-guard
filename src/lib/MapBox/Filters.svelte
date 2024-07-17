<script>
    let rotated = false;
    let dateChecked = false;
    let startDate = '';
    let endDate = '';
    function toggleRotation() {
        rotated = !rotated;

        const checkboxContainer = document.querySelector('.checkbox-container');
        if (checkboxContainer) {  
            if (rotated) {
                checkboxContainer.classList.add('show');
            } else {
                checkboxContainer.classList.remove('show');
            }
        } 
    }
   
    function byDateChecked() {
        dateChecked = !dateChecked;
    }
    function byProvinceChecked() {
        
      }

</script>

<div id="filters" class="filters" on:click={toggleRotation}>
  Filters&nbsp;<span id="last-char" class:rotated={rotated}>&gt;</span>
</div>

<div class="checkbox-container {rotated ? 'show' : ''}">
  <label class="custom-checkbox">
    <input type="checkbox" name="filter" value="date" on:change={byDateChecked}> 
    <span class="custom-checkmark"></span>
    By Date
  </label>
  {#if dateChecked}
  <div class="by-date-label">
    <input type="text" bind:value={startDate} placeholder="" class="text-field">
    to
    <input type="text" bind:value={endDate} placeholder="" class="text-field">
</div>
    {/if}
  <label class="custom-checkbox">
    <input type="checkbox" name="filter" value="province" on:change={byProvinceChecked}> 
    <span class="custom-checkmark"></span>
    By Province
  </label>
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
  top: 100px;
  left: 97px;
  padding: 10px;
  border-radius: 5px;
  font-family: "Lilita One", sans-serif;
  font-size: 30px;
  font-style: normal;
  z-index: 10;
  cursor: pointer;
  color: rgba(180, 159, 155, 0.895); 
  display: flex;
  align-items: center; 
}
.filters:hover {
  top: 90px;
  left: 87px;
  color: rgba(202, 120, 104, 0.895); 
  font-size: 40px; 
}
 .checkbox-container {
    position: absolute;
  font-family: "Lilita One", sans-serif;
  font-size: 25px;
  font-style: normal;
  z-index: 10;
  left: 83px;
    top:160px;
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
        transition: background-color 0.2s ease, border-color 0.2s ease;
    }

    .custom-checkbox input:checked + .custom-checkmark {
      
      content: "";
   
   background-color: white;
        /* content: ' ';
        background-color: rgba(180, 159, 155, 0.895);
        border-color: rgba(180, 159, 155, 0.895); */
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
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
</style>