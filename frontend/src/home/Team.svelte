<style>
    #team{
        margin-top: 400%;
    margin-left: 34%;
    position:absolute;
    font-size: 60px;
    color: #af201b;
    line-height: 1.25;
    }
    .rectangle {
    width: 30%;   /* Width of the rectangle */
    height: 600px;  /* Height of the rectangle */
    background-color: #cc97974c;  /* Background color of the rectangle */
    position: absolute;
    border-width: 6px;
    border-color: #7d090948;
        }
    #rectangle-ethan{
margin-top: 471%;
    margin-left: 15%;
    
        }
        #rectangle-gab{
margin-top: 471%;
    margin-left: 55%;
        }
        #rectangle-anais{
margin-top: 591%;
    margin-left: 15%;
        }
        #rectangle-parsa{
    margin-top: 591%;
    margin-left: 55%;
        }
  .ethan-img{
    width: 10%;
    margin-top: 430%;
    margin-left: 25%;
    position: absolute;
  }
  .gab-img{
    width: 11%;
    margin-top: 430%;
    margin-left: 65%;
    position: absolute;
  }
  .anais-img{
    width: 13%;
    margin-top: 550%;
    margin-left: 23.5%;
    position: absolute;
  }
  .parsa-img{
    width: 10%;
    margin-top: 550%;
    margin-left: 65%;
    position: absolute;
  }

  
  .frame {
            width: 230px;            /* Set the width of the image */
            height: 230px;           /* Set the height of the image */
            border-radius: 50%;      
            overflow: hidden;        
            border: 2px solid #601515; 
    position: absolute; /* Optional: add a border around the circle */

        }
        .frame img {

            width: 100%;  /* Ensure the image covers the entire circle */
            height: 100%; /* Maintain the aspect ratio */
            object-fit: cover;  /* Scale the image to cover the circle */
        }
        


  #ethan-frame {
    margin-top: 460%;
    margin-left: 22.2%;
        }

        #gab-frame {
            margin-top: 460%;
    margin-left: 62.2%;

        }
        #anais-frame {
    margin-top: 581%;
    margin-left: 22.2%;
        }
        #parsa-frame {
    margin-top: 581%;
    margin-left: 62.2%;
        }

    .name{
        font-size: 50px;
        position: absolute;
        color: #601515;
    }
    #ethan-name{
        margin-top: 482%;
        margin-left: 22.4%;
    }
    #gab-name{
        margin-top: 482%;
        margin-left: 58%;
    }
    #anais-name{
        margin-top: 603%;
        margin-left: 20.4%;
    }
    #parsa-name{
        margin-top: 603%;
        margin-left: 59.5%;
    }
        
        

</style>

<div id="team">
    Our Awesome Team
</div>

<div class="rectangle" id="rectangle-ethan"></div>
<div class="rectangle" id="rectangle-gab"></div>

<div class="rectangle" id="rectangle-anais"></div>

<div class="rectangle" id="rectangle-parsa"></div>

<img src="Ethan.png" class="ethan-img" alt="Ethan">
<img src="Gabriel.png" class="gab-img" alt="Gabriel">
<img src="Anais.png" class="anais-img" alt="Anais">
<img src="Parsa.png" class="parsa-img" alt="Parsa">

<div class="frame" id = "ethan-frame">
    <!-- svelte-ignore a11y-img-redundant-alt -->
    <img src="et.jpg" alt="Circular Framed Image">
</div>
<div class="frame" id= "gab-frame">
    <!-- svelte-ignore a11y-img-redundant-alt -->
    <img src="gab.jpg" alt="Circular Framed Image">
</div>

<div class="frame" id= "anais-frame">
    <!-- svelte-ignore a11y-img-redundant-alt -->
    <img src="an.JPG" alt="Circular Framed Image">
</div>

<div class="frame" id= "parsa-frame">
    <!-- svelte-ignore a11y-img-redundant-alt -->
    <img src="par.jpg" alt="Circular Framed Image">
</div>

<div class="name" id="ethan-name">
    Ethan Tran
</div>
<div class="name" id="gab-name">
    Gabriel Saberian
</div>
<div class="name" id="anais-name">
    Anaïs Perron
</div>
<div class="name" id="parsa-name">
    Parsa Jafarian
</div>