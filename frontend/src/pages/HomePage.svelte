<script>
  import TryButton from "../home/TryButton.svelte";
</script>


<div class="background">

  <header class="styled-header">
    <img src="logo.png" alt="Icon" class="icon" />
    <h1 class= "title">Fire Guard</h1>
  </header>

  
  <TryButton/>
</div>




<style>
  .title{
    font-size: 35px;
    color:  #af201b;
    
  }
   .background {
    background-image: url('homepage.jpeg');
    background-size: cover;
    background-position: center;
    height: 100vh; /* Full height */
    width: 100%; /* Full width */
    position: relative;
  }

  .styled-header {
    background-color: #e3c3b9; /* Same background color as the button */
    border: 2px solid #422800; /* Same border color as the button */
    box-shadow: #422800 1px 1px 0 0; /* Same shadow effect as the button */
    color: #422800; /* Text color similar to the button */
    font-weight: 600; /* Bold text */
    padding: 20px 0;
    display: flex; /* Enable flexbox */
    align-items: center; /* Center vertically */
    height: 70px; /* Set a fixed height */
    width: 100%; /* Ensure full width */
    user-select: none; /* Prevent text selection */
    -webkit-user-select: none; /* Prevent text selection in WebKit browsers */
    touch-action: manipulation; /* Ensures proper behavior on touch devices */
    position: relative; /* Adjust positioning as needed */
  }
  .icon{
    width: 3.5%;
  margin-right: 5px;
  }
</style>

