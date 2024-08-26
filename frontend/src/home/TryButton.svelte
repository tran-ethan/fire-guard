

<button class="button" on:click={() => (window.location.href = "/map")}>
Try it out now!
</button>

<style>
    .button{
      
  font-family: "Lilita One", sans-serif;
        position: fixed; 
    bottom: 40px;
    right: 40px; 
        background-color: #e3c3b9;
  border: 2px solid #422800;
  border-radius: 30px;
  box-shadow: #422800 4px 4px 0 0;
  color: #422800;
  cursor: pointer;
  display: inline-block;
  font-weight: 600;
  font-size: 24px; /* Increase font size */
  padding: 20px 36px; /* Increase padding (ensure both top-bottom and left-right values are set) */
  line-height: 60px; /* Adjust line height */
  text-align: center;
  text-decoration: none;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  z-index: 100;
    }
    .button:hover{
        background-color: #d2978d;
    }
    .button:active {
  box-shadow: #422800 2px 2px 0 0;
  transform: translate(2px, 2px);
}

@media (min-width: 768px) {
  .button {
    min-width: 120px;
    padding: 0 25px;
  }

  
}
</style>