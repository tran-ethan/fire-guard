<script>
    let rotated = false;

    function toggleRotation() {
        rotated = !rotated;
    }
</script>

<div id="filters" class="filters" on:click={toggleRotation}>
    Filters&nbsp;<span id="last-char" class:rotated={rotated}>&gt;</span>
</div>

<style>
    
    #last-char {
  display: inline-block;
  transition: transform 0.3s ease;
}

#last-char.rotated {
  transform: rotate(90deg);
}
.filters {
  position: absolute;
  top: 100px;
  left: 97px;
  margin: 0;
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
</style>