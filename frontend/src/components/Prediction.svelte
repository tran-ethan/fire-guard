<script>
    import { showPopup } from "../lib/store";
    import { popupText } from "../lib/store";
    import { firePrediction } from "../lib/store";

    function closePopup() {
      showPopup.set(false);
    }
</script>

<style>
.popup-wrapper {
  position: absolute;
  top: 0%;
  left: 0%;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: opacity 0.3s ease, visibility 0.3s ease;
  opacity: 1;
  visibility: visible;
}
.popup-wrapper.hidden {
  opacity: 0;
  visibility: hidden;
}
.popup {
  margin: 70px auto;
  padding: 20px;
  background: #fff;
  border-radius: 5px;
  width: 30%;
  position: absolute;
  transition: all 1s ease-in-out;
  top: 72.9%;
    left: 3.5%;
    z-index: 100;
    text-align: center;
    transform: translateY(-20px); /* Start from above */
}
.popup.hidden {
  transform: translateY(20px); /* Move below */
  opacity: 0;
}


.popup h2 {
  margin-top: 0;
}
.popup .close {
  position: absolute;
  top: 0px;
  right: 10px;
  transition: all 200ms;
  font-size: 30px;
  font-weight: bold;
  text-decoration: none;
  color: #333;
}
.popup .close:hover {
  color: #06D85F;
}
.popup .content {
  max-height: 30%;
  overflow: auto;
}

@media screen and (max-width: 700px){
  .box{
    width: 70%;
    }
  .popup{
    width: 70%;
  }
}
</style>


{#if $showPopup}
<div class="popup-wrapper">
	<div class="popup">
    {#if $firePrediction}
    <span style="color: red;">
		  <h2>Wildfire</h2>
    </span>
    {:else}
      <span style="color: green;">
		  <h2>No wildfires</h2>
    </span>
    {/if}
		<a class="close" href="#" on:click|preventDefault={closePopup}>&times;</a>
		<div class="content">
			{$popupText}
		</div>
	</div>
</div>
{/if}