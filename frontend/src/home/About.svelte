
  
  <style>
    .soldier-img {
      width: 60%;
      position: absolute;
      margin-top: 110%;
      margin-left: 0%;
      opacity: 0.9;
      z-index: -20;
    }
    
    .loupe-img{
        width: 30%;
      position: absolute;
      margin-top:205%;
      margin-left: 57%;
      opacity: 0.88;
    }

    .hug-img{
        width: 35%;
      position: absolute;
      margin-top:320%;
      margin-left: 9%;
      opacity: 0.88;
    }

 
  .slogan{
    margin-top: 80%;
    margin-left: 60%;
    position:absolute;
    font-size: 60px;
    color: #a05454;
    line-height: 1.25;
  }
  .txt{
    position:absolute;
    font-size: 25px;
    color: #daa392;
    max-width: 570px;
  }
    
  #txt1{
    margin-top: 112%;
    margin-left: 58%;
    font-size: 22px;
    text-align: center;
    
  }
  #txt2{
    margin-top: 211%;
    margin-left: 8.5%;
    line-height: 2;
    
  }
  #txt3{
    margin-top:320%;
      margin-left: 53%;
      line-height: 2;
      text-align: right;
    max-width: 620px;
  }

  .sub{
    position:absolute;
    font-size: 50px;
    color: #c3695f;
    line-height: 1.25;
  }
  #sub1{
    margin-top: 170%;
    margin-left: 13%;
  }
  #sub2{
    margin-left: 63%;
    margin-top: 275%;
  }
  </style>



  <div class="slogan" id="about">
    Guarding the Nation <br>Before Fire Catches
  </div>
  <img src="soldiers.jpg" class="soldier-img" alt="Soldiers">
  <div class="txt" id="txt1">Wildfires pose a significant threat to both human life and property. By accurately predicting wildfires and strategically placing fire shelters, we can:
    <br>
    <br> - Enhance public safety and preparedness
    
    <br> - Reduce the loss of life and property
    
    <br> - Improve resource allocation for firefighting and emergency response teams
    </div>

    <div class="sub">
        
    </div>

    <div class="sub" id="sub1">How does it Work?</div>

    <div class="txt" id="txt2">
        &emsp;The app uses a Random Forest model, created with scikit-learn, to help predict wildfires. 
        By analyzing historical weather and location data, the model can estimate the likelihood of a 
        wildfire occurring in specific areas. It examines patterns from the past to determine whether 
        a particular location is at risk of a wildfire, providing valuable insights for early warning and prevention.
         This way, users can better prepare and make informed decisions to protect their communities from potential wildfires.
    </div>

    <img src="fireLoupe.png" class="loupe-img" alt="Loupe">

    <div class="sub" id="sub2">Target Audience</div>

    <div class="txt" id="txt3">
        &emsp;The app primarily serves residents in wildfire-prone areas, providing them with vital warnings and insights.
         It also benefits local and state government agencies by helping them make informed public safety decisions. Firefighting
          and emergency response teams in Canada can use the app to better plan and allocate resources.
        Secondary users include environmental researchers, who can study wildfire patterns, and insurance companies, which can 
        assess risks more effectively. Urban planners and developers in at-risk regions can also use the app to make safer planning 
        decisions.
    </div>

    <img src="hug.png" class="hug-img" alt="Hug">


  
