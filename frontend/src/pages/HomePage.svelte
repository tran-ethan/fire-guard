<script lang="ts">
  import TryButton from "../home/TryButton.svelte";
  import About from "../home/About.svelte";

  /**
   * @param id html id of the element to scroll to
   */
  function scrollToElement(id: string) {
    const element = document.getElementById(id);
    if (!element) return;
    element.scrollIntoView({ behavior: "smooth" });
  }
</script>

<body>
  <div class="background">
    <header class="header">
      <img src="logo.png" alt="Icon" class="icon" />
      <h1 class="title">Fire Guard</h1>
      <h1 class="header-text">Home</h1>
      <h1 class="header-text" on:click={() => scrollToElement("about")}>About</h1>
      <h1 class="header-text">Collaboration</h1>
    </header>

    <div class="sub">
      <span id="sub1">Guard the Flames,</span><br />
      <span id="sub2">Shield the Future</span>
    </div>

    <div class="sub3">
      A machine learning model that analyzes weather patterns, vegetation types,
      and historical fire records to accurately predict wildfires' likelihood,
      location, and severity to strategically place fire shelters.
    </div>

    <img src="sword.png" class="sword" />
  </div>
  <About />
  <TryButton />
</body>

<style>
  body {
    overflow-x: hidden; /* Prevent horizontal scrolling */
    margin: 0; /* Remove default margin */
    padding: 0; /* Remove default padding */
    position: relative;
  }
  .title {
    font-size: 40px;
    color: #af201b;
  }

  .header-text {
    font-size: 35px;
    color: #791c15d4;
    margin-left: 15%;
  }
  .header-text:hover {
    text-decoration: underline;
  }

  .background {
    position: relative;
    height: 100vh;
    width: 100%;
  }

  .background::before {
    content: "";
    background-image: url("homepage.jpeg");
    background-size: contain; /* Ensures the entire image is visible without cropping */
    background-repeat: no-repeat; /* Prevents the image from repeating */
    background-position: center right; /* Positions the image to the right */
    /* opacity: 0.7; */
    position: absolute;
    top: 80px;
    right: -70px;
    bottom: 130px;
    width: 80%; /* Adjust the container width as needed */
    z-index: -1;
  }

  .header,
  .sub,
  .icon {
    z-index: 1;
  }

  .header {
    background-color: #e3c3b9;
    border-bottom: 0.5px solid #422800;
    box-shadow: #422800 1px 1px 0 0;
    color: #422800;
    font-weight: 600;
    padding: 20px 0;
    display: flex;
    align-items: center;
    height: 70px;
    width: 100%;
    top: 0; /* Align to the top of the viewport */
    left: 0; /* Ensure it stretches the full width */
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
    position: fixed;
  }

  .icon {
    width: 3.5%;
    margin-right: 7px;
    margin-left: 10px;
  }

  .sub {
    font-size: 60px;
    margin-left: 70px;
    margin-top: 160px;
    line-height: 1.25;
  }

  #sub1 {
    color: #a4645f;
    margin-bottom: 0;
  }

  #sub2 {
    color: #6f140d;
    margin-top: 0;
  }

  .sub3 {
    font-size: 25px;
    margin-top: 15px;
    color: rgb(179, 135, 126);
    margin-left: 70px;
    max-width: 550px;
    word-wrap: break-word;
    font-weight: 10;
  }
  .sword {
    width: 13%;
    transform: rotate(52deg);
    margin-top: 10%;
    margin-left: 45%;
    opacity: 0.85;
  }
</style>
