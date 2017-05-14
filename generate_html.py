# -*- coding: utf-8 -*-
"""
Created on Thu May 11 16:21:21 2017

@author: danie
"""

# %% Imports 

import requests 
import os


# %% Download image url from dropbox 

def getImageUrl(filename):
    r = requests.get("https://amazing-sigma.herokuapp.com//images?filename={}".format(filename))
    return r.text
    

# %% HTML Head

html_head_1 = """\

<!DOCTYPE html>
<html lang="en">
<meta charset="UTF-8">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/> 
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://www.w3schools.com/lib/w3-theme-indigo.css">

<style>
body,h1 {font-family: "Raleway", sans-serif}
body, html {height: 100%}
.bgimg {
    background-color: MediumVioletRed;
    min-height: 100%;
    background-image: 
"""

html_background = """url("{back}");""".format(back=getImageUrl("finance.jpg"))
html_head_2 = """\

    background-position: center;
    background-size: cover;
}

"""

complete_html_head = html_head_1+html_background+html_head_2

# %% 
html_without_images = """\

</style>

<head>
  <title>The Amazing Sigma</title>
</head>

<!-- Links (sit on top) -->
<div class="w3-top">
  <div class="w3-bar w3-black w3-card-2"> 
    <div class="w3-col s3">
      <a href="#" class="w3-button w3-block w3-black">HOME</a>
    </div>
    <div class="w3-col s3">
      <a href="#about" class="w3-button w3-block w3-black">ABOUT ME</a>
    </div>
    <div class="w3-col s3">
      <a href="#menu" class="w3-button w3-block w3-black">MENU</a>
    </div>
    <div class="w3-col s3">
      <a href="#how to use me" class="w3-button w3-block w3-black">HOW TO USE ME</a>
    </div>
    <div class="w3-col s3">
      <a href="#examples" class="w3-button w3-block w3-black">EXAMPLES</a>
    </div>
    <div class="w3-col s3">
      <a href="#notes" class="w3-button w3-block w3-black">NOTES</a>
    </div>
    <div class="w3-col s3">
      <a href="#team" class="w3-button w3-block w3-black">TEAM</a>
    </div>
  </div>
</div>

<body>
<div class="bgimg w3-display-container w3-animate-opacity w3-text-darkpurple">

  <div class="w3-display-middle w3-center w3-padding-large">
    <span class="w3-text-white" style="font-size:95px">Sigma</span>
    <hr class="w3-border-black" style="margin:auto;width:85%">
    <p class="w3-large w3-center">Your personal finance assistant.</p>
  </div>
  
</div>

<!-- About me -->
<div class="w3-content w3-container w3-padding-64" id="about">
  <h3 class="w3-center">Would you like to meet me? Go ahead!</h3>
  <p class="w3-center"><em>Python at the tip of your fingers</em></p>
  <p>Sigma is an online chatbot as a personal finance assistant. You can ask her to valuate European, Binary and Barrier options. Furthermore, you can select any set of assets listed on the Mexican Stock Exchange and Sigma will help you to evaluate portfolio performance.
  </p>
  <p class="w3-large w3-center w3-padding-16">I can:</p>
 
  <h4>
  <UL type = circle align="justify">
   <LI>Valuate and graph different options<p>
   <LI>Create, simulate and graph a portfolio of your choice<p>
   <LI>Create, simulate and graph an optimal portfolio with assets of your choice<p>
   <LI>Evaluate a portfolio performance<p>
   <LI>Tell some jokes 
   </UL></h4>
  
<div class="w3-row-padding w3-center w3-margin-top">
<div class="w3-third">
  <div class="w3-card-2 w3-container" style="min-height:460px">
  <h3>Introduction</h3><br>
  <i class="fa fa-desktop w3-margin-bottom w3-text-theme" style="font-size:120px"></i>
  <p class="w3-text-grey" align="justify">In this site you are going to discover the easy way to get the experience of use SigmaBot like a tool for making good financial decisions, investment and hedges. 
  <p class="w3-text-grey" align="justify">You have two different choices, in the first one you can calculate the price of the premium of more than ten kind of different options. In the second one, you can simulate an optimum portfolio with the parameters of your election. 
  <p class="w3-text-grey" align="justify">Then you can use Markowitz and Sharpe theory to find the efficient curve, using the shares you most prefer. Finally, you can get the optimum portfolio within efficient frontier. You can access to the tool through talking to Sigma in the Messenger of Facebook. </p>
  </div>
</div>

<div class="w3-third">
  <div class="w3-card-2 w3-container" style="min-height:460px">
  <h3>General Objetive</h3><br>
  <i class="fa fa-css3 w3-margin-bottom w3-text-theme" style="font-size:120px"></i>
  <p class="w3-text-grey" align="justify">Provide the user the fastest assistance in the process of making optimal financial decisions.</p>
  </div>
</div>

<div class="w3-third">
  <div class="w3-card-2 w3-container" style="min-height:460px">
  <h3>Specific Objetives</h3><br>
  <i class="fa fa-diamond w3-margin-bottom w3-text-theme" style="font-size:120px"></i>
   <UL type = disk class="w3-text-grey" align="justify" >
   <LI>Help the user to formulate the cost of premiums for multiple types of financial options.
   <p>
   <LI>Being an easy assistance for creating portfolios with shares of the Mexican Stock Exchange.
   <p>
   <LI>Support the user to make appropriate financial decisions according to the different investing profiles. 
   </UL>
   

  </div>
</div>
</div>

</div>


<!-- Menu Container -->
<div class="w3-container" id="menu">
  <div class="w3-content" style="max-width:700px">
 
    <h5 class="w3-center w3-padding-48"><span class="w3-tag w3-wide">THE MENU</span></h5>
  
    <div class="w3-row w3-center w3-card-2 w3-padding">
      <a href="javascript:void(0)" onclick="openMenu(event, 'Options');" id="myLink">
        <div class="w3-col s6 tablink">Options</div>
      </a>
      <a href="javascript:void(0)" onclick="openMenu(event, 'Portfolios');">
        <div class="w3-col s6 tablink">Portfolios</div>
      </a>
    </div>

    <div id="Options" class="w3-container menu w3-padding-48 w3-card-2">
      <h5>European Options</h5>
      <p class="w3-text-grey" align="justify">An option that can only be exercised at its maturity.
	<p class="w3-text-grey" align="justify"> 
	There are two types of options: </p>
	<p class="w3-text-grey" align="justify">	
	A call option is an agreement that gives an investor the right, but not the obligation, to buy a stock, bond, commodity or other instrument at a specified price within a specific time period.
	<p class="w3-text-grey" align="justify">	
	A put option is an agreement that gives an investor the right, but not the obligation, to sell a stock, bond, commodity or other instrument at a specified price within a specific time period.</p><br>
        <p class="w3-text-grey" align="justify">
        The equations of picing finance options is given by the Black-Scholes equation. The valuation formula has this form: </p><br>
        <p class="w3-text-grey" align="center"> 
        <img align="center" src="{bseuropean}" border=0></p>

      <h5>Binary Options</h5>
      <p class="w3-text-grey" align="justify">The simplest kind of options. If a trader believes the market is rising, he would purchase a call. If the trader believes the market is falling, he would buy a put.</p><br>
      <p class="w3-text-grey" align="justify">
        The equations are given by: </p><br>
        <p align="center"> 
        <img align="center" src="{bsbinary}" border=0></p>


      <h5>Barrier Options</h5>
      <p class="w3-text-grey" align="justify">A type of option whose payoff depends on whether or not the underlying asset has reached or exceeded a predetermined price. A barrier option can be knock-out (deactivation) or knock-in (activation)</p><br>
      <p class="w3-text-grey" align="justify">There are eigth barrier options:</p><br>
      
      <b>Up and Out Option:</b>
      <p class="w3-text-grey" align="justify">A type of barrier option that becomes worthless if the price of the underlying asset increases beyond a specified price level (the "knock out" price). If the up-and-out option stays below the knock out price, then the holder may be entitled to a payout.</p> 
       <UL type = disk align="justify" >
       <LI>Call: is exercised just if the price at the maturity is between the strike and the barrier. 
       <p>
       <LI>Put: is exercised just if the price at the maturity is below the strike. 
       </UL>
      
       <b>Down and Out Option:</b>
      <p class="w3-text-grey" align="justify">A type of knock-out barrier option that ceases to exist when the price of the underlying security hits a specific barrier price level. If the price of the underlying does not reach the barrier level, the investor has the right to exercise their European call or put option at the exercise price specified in the contract.</p> 
       <UL type = disk align="justify" >
       <LI>Call: is exercised just if the price at the maturity is above the strike.
       <p>
       <LI>Put: is exercised just if the price at the maturity is between the strike and the barrier. 
       </UL>
       
        <b>Up and In Option:</b>
      <p class="w3-text-grey" align="justify">An option that can only be exercised when the price of the underlying asset reaches a set barrier level. This is a type of a knock-in barrier option.</p> 
       <UL type = disk align="justify" >
       <LI>Call: is exercised just if the price at the maturity is above the strike.
       <p>
       <LI>Put: is exercised just if the price at the maturity is below the strike.
       </UL>
       
        <b>Down and In Option:</b>
      <p class="w3-text-grey" align="justify">A form of barrier option that becomes activated only if the price of the underlying asset falls below a pre-determined barrier price level during the life of the option. In a down-and-in option, the barrier level is set at some level below the current spot or prevailing price of the underlying asset. If the asset price falls below the barrier level, it becomes activated and has value; if the asset price does not fall below the barrier level, the option expires worthless.</p> 
       <UL type = disk align="justify" >
       <LI>Call: is exercised just if the price at the maturity is above the strike.
       <p>
       <LI>Put: is exercised just if the price at the maturity is below the strike.
       </UL>
       
       <p class="w3-text-grey" align="justify">
          The Black Scholes equations of this options are given by: </p><br>
          <p align="center"> 
          <img align="center" src="{barrier}" width="680" height="800" border=0></p>
       <p class="w3-text-grey" align="justify">
          Where standard normal variables are given by: </p><br>
          <p align="center"> 
          <img align="center" src="{ds}" border=0></p>
      
     
    <div id="Portfolios" class="w3-container menu w3-padding-48 w3-card-2">
      <h5>Simulate arbitrary portfolio</h5>
      <p class="w3-text-grey" align="justify">Sigma is able to simulate your own portfolio with arbitrary assets listed in the Mexican Stock Exchange and with the weights you give her.</p><br>
    
      <h5>Simulate an efficient portfolio using Markowitz criterion</h5>
      <p class="w3-text-grey" align="justify">Sigma can also optimize your own portfolio with assets listed in the Mexican Stock Exchange using the Markowitz criterion.</p>
      <p class="w3-text-grey" align="justify">This criterion is based on an optimization problem, where it seeks to maximize the performance of a portfolio under a given risk, or minimize the risk of a given performance. </p>
      <p class="w3-text-grey" align="justify">Under the model: </p>
       <UL type = disk class="w3-text-grey" align="justify" >
       <LI>Portfolio return is the proportion-weighted combination of the constituent assets returns.<p>
       <LI>Portfolio volatility is a function of the correlations of the component assets, for all asset pairs.
       </UL>     
      <p class="w3-text-grey" align="justify">The problem of optimization with Markowitz is given by the equation: </p><br>
          <p align="center"> 
          <img align="center" src="{markoweq}" border=0></p>
      <p class="w3-text-grey" align="justify">Where &alpha; are constants to weight risk or performance, X are the weights that will be given to the stocks, &Sigma; is the covariance matrix and &mu; the returns vector.</p><br>
         
          
      <h5>Simulate an efficient portfolio using Sharpe criterion</h5>
      <p class="w3-text-grey" align="justify">On the other way, Sigma can optimize your own portfolio using the Sharpe criterion.
      <p class="w3-text-grey" align="justify">The Sharpe Ratio is a measure for calculating risk-adjusted return, and this ratio has become the industry standard for such calculations. The Sharpe ratio is the average return earned in excess of the risk-free rate per unit of volatility or total risk. </p><br>
      <p class="w3-text-grey" align="justify">The Sharpe Ratio and the problem of optimization with Sharpe is given by the equations: </p><br>
          <p align="center"> 
          <img align="center" src="{sharpe}" border=0></p>
      <p class="w3-text-grey" align="justify">Where rp is the portfolio's return, rf is the risk rate and &sigma p is the portfolio's volatility. X are the weights that will be given to the stocks, &Sigma; is the covariance matrix and &mu; the returns vector.</p><br>
            
      
            <h3><em>How were the simulations done?</em></h3>
      <p align="justify">Asset simulations were performed for the estimation of option premiums with Montecarlo and for the creation of portfolios. This was done in two ways: assuming normality and not doing so.
      <UL type = disk class="w3-text-grey" align="justify" >
       <LI>For the first method the Black Scholes solution equation was used, which is given by: <p>
           <p align="center"> 
           <img align="center" src="{bsequation}" border=0></p>
       <LI>For the second method, the kernel distribution estimate was used, which consists of the following:
           <p align="justify"> 
           Kernel density estimation (KDE) is a non-parametric way to estimate the probability density function of a random variable. Is a fundamental data smoothing problem where inferences about the population are made, based on a finite data sample. If you have (x1, x2, ... , xn) independent and identically distributed sample drawn from some distribution with an unknown density f then you can estimate the shape of this function following the equation:</p>
           <p align="center"> 
           <img align="center" src="{kerneleq}" border=0></p>
       </UL> 
               
             
    </div>  
    <img src="{investment}" style="width:100%;max-width:1000px;margin-top:32px;">
  </div>
</div>




<!-- How to use me -->
<div class="w3-container" id="how to use me">
  <div class="w3-content" style="max-width:700px">
 
    <h5 class="w3-center w3-padding-48"><span class="w3-tag w3-wide">HOW TO USE ME</span></h5>
  
  <!-- Left Column -->
    <div class="w3-third">
    
      <div class="w3-white w3-text-grey w3-card-4">
        <div class="w3-display-container">
          <img src="{sigma}" style="width:100%" alt="Avatar">
          <div class="w3-display-bottomleft w3-container w3-text-black">
          </div>
        </div>
        
      </div><br>

    <!-- End Left Column -->
    </div>

<!-- Right Column -->
    <div class="w3-twothird">
    
        <div class="w3-container">
        <h5 class="w3-opacity"><b>How to enter Sigma?</b></h5>
          <p align="justify">To access Sigma you must log in to Facebook and write "The Amazing Sigma" in the search engine. Once you enter the page, click on "send message" and a chat will open to be able to speak with Sigma.</p>
          <hr>
        </div>
 	 	
        <div class="w3-container">          
         <h5 class="w3-opacity"><b>How can I talk to Sigma?</b></h5>         
         <p align="justify">In order to talk to Sigma you must give the correct instructions of what you want to estimate. See below the commands.</p>
         
         <UL type = square class="w3-text-grey" align="justify" >
   <LI>To get the available stocks on the Mexican stock exchange you just have to write the word available. For example: available stocks<p>
   <LI>To get a description of a stock, the key-word to use is describe. For example: describe bimbo<p>
   <LI>To get a plot of a stock price, the key-word is plot, but you must be careful and do not write the words marko or covar. For example: plot alsea<p>
   <LI>To get a plot of the covariance of some stocks, you must write: plot, covar, of. For example: plot covar of alsea alfa gmexico cemex<p>
   <LI>To get a simulation of a stock price, you have to write the word simulate (if you want to assume normality). For example: simulate gmexico. If you want to simulate with KDE (without assuming normality) you have to write simulate using kde and you can specify the days and trajectories. For example: simulate GMEXICO for 50 days with 50 trajectories using kde<p>
   <LI>To get a plot of the efficient frontier of markowitz the key-words are: markowitz, plot, with. For example: create a markowitz plot with alsea alfa gmexico cemex<p>
   <LI>To get an efficient portfolio (one of the frontier), the key-words are percentile, port, efficient and using. For example: get percentile 10 portfolio from efficient frontier using alsea bimbo cemex gmexico. The lower the percentile, the lower the risk you decide to take. If you write the words Markowitz, port, efficient, using, for example: get markowitz efficient portfolio using alsea bimbo cemex gmexico; Sigma will estimate the optimal portfolio with the lowest risk.<p>
   <LI> To get a simulation of a portfolio you must write the next text: simulate portfolio given by (stocks) with weights (in decimals) and initial capital of (amount). For example: simulate portfolio given by alsea bimbo gmexico with weights 0.4 0.2 0.2 and initial capital of 10000<p>
   Note: The weights can be arbitrary, or write the obtained ones with the efficient portfolio.
   <LI> To get an optimal portfolio using Sharpe ratio, you have to write this: get sharpe optimal portfolio using (stocks). For examples: get sharpe optimal portfolio using alsea gmexico gruma herdez</p>
   <LI> To get the price of a European option you must write: calculate european option price for (stock) with maturity in (number of years) y, strike of (strike price). For example: calculate european option price for ALSEA stock with maturity in 1 y, strike of 50<p>
   <LI> To get the price of a Binary option you must write: calculate binary option (type) price for (stock) with maturity in (number of years) y, strike of (strike price). For example: calculate binary option (asset_or_nothing) price for ALSEA stock with maturity in 1 y, strike of 50<p>
   <LI> To get the price of a Barrier option you must write: calculate barrier option (type) price for (stock) with maturity in (number of years) y, strike of (strike price), barrier of (barrier price). For example: calculate barrier option (barrier_down_and_out) price for ALSEA stock with maturity in 1 y, strike of 50, barrier of 60<p>
   </UL>
              
         <hr>
        </div>
        
 	 	
       <div class="w3-container"> 
         <h5 class="w3-opacity"><b>What can I estimate with Sigma?</b></h5>         
         <p align="justify">Sigma can make valuations of different types of financial options and generate portfolios (arbitrary and optimal) under different criteria, as indicated by the user. Sigma can also calculate portfolio performance.</p>
          <hr>
        </div>

       <div class="w3-container"> 
         <h5 class="w3-opacity"><b>How does Sigma give me the results?</b></h5>         
         <p align="justify">Sigma gives you the results in form of text or image, depending on whether it is a value or a graph.</p>
          <hr>
        </div>
 
<!-- End Right Column -->
      </div>

  </div>
</div>


    <!-- Examples -->
    <div class="w3-content" id="examples">
    <h5 class="w3-center w3-padding-48"><span class="w3-tag w3-wide">EXAMPLES</span></h5>

<!-- First Photo Grid-->
  <div class="w3-row-padding w3-padding-16 w3-center" id="food">
    <div class="w3-quarter">
      <img src="{available}" style="width:100%" onclick="onClick(this)" class="w3-hover-opacity" alt="Available stocks">
      <h3>Available stocks</h3>
      <p align="justify">Sigma can show you randomly some available stocks on the BMV</p>
    </div>
    <div class="w3-quarter">
      <img src="{describe}" style="width:100%" onclick="onClick(this)" class="w3-hover-opacity" alt="Describe stock">
      <h3>Describes a stock</h3>
      <p align="justify">Sigma can give you a short description of a stock and a small analysis of their prices and returns as the current price, minimum, maximum, the last 10 prices, as well as daily and annual return and volatility.</p>
    </div>
    <div class="w3-quarter">
      <img src="{plotalsea}" style="width:100%" onclick="onClick(this)" class="w3-hover-opacity" alt="Price plot">
      <h3>Price plot</h3>
      <p align="justify">Sigma is able to show you a price graph (with 2 years of historical data)</p>
    </div>
    <div class="w3-quarter">
      <img src="{covar}" style="width:100%" onclick="onClick(this)" class="w3-hover-opacity" alt="Covariance">
      <h3>Covariance of stocks</h3>
      <p align="justify">Sigma provides you the covariance matrix with stocks you give her. The more intense the color, the more correlation there is.</p>
    </div>
  </div> 

  
  <!-- Second Photo Grid-->
  <div class="w3-row-padding w3-padding-16 w3-center">
    <div class="w3-quarter">
      <img src="{simstock}" style="width:100%" onclick="onClick(this)" class="w3-hover-opacity" alt="Simulation of a stock">
      <h3>Simulate a stock</h3>
      <p align="justify">
      Sigma provides you the simulation of a stock (assuming normality) with days and trajectories you give her. If you do not specify the parameters, Sigma does it with default parameters.</p>
    </div>
    <div class="w3-quarter">
      <img src="{simstockde}" style="width:100%" onclick="onClick(this)" class="w3-hover-opacity" alt="Markowitz">
      <h3>Simulate a stock using kde</h3>
      <p align="justify">Sigma provides you the simulation of a stock (without assuming normality) with days and trajectories you give her. If you do not specify the parameters, Sigma does it with default parameters.</p>
    </div>
    <div class="w3-quarter">
      <img src="{markow1}" style="width:100%" onclick="onClick(this)" class="w3-hover-opacity" alt="Markowitz">
      <h3>Efficient frontier of Markowitz</h3>
      <p align="justify">Sigma can create many optimal portfolios and show you the efficient frontier of Markowitz's theory</p>
    </div>
    <div class="w3-quarter">
      <img src="{effport}" style="width:100%" onclick="onClick(this)" class="w3-hover-opacity" alt="Efficient portfolio">
      <h3>Efficient portfolio with Markowitz</h3>
      <p align="justify">
      Sigma returns you the weights of an efficient portfolio (located on the frontier), formed by the assets that you say with the level of risk you specify  (percentile), ordered from lowest to highest risk.</p>
    </div>
  </div>
  
  
  <!-- Third Photo Grid-->
  <div class="w3-row-padding w3-padding-16 w3-center">
    <div class="w3-quarter">
      <img src="{sharpeport}" style="width:100%" onclick="onClick(this)" class="w3-hover-opacity" alt="Simulation of a stock">
      <h3>Efficient portfolio with Sharpe</h3>
      <p align="justify">Sigma returns you the weights of the portfolio that maximizes the sharpe ratio formed by the assets you say.</p>
    </div>
    <div class="w3-quarter">
      <img src="{simport}" style="width:100%" onclick="onClick(this)" class="w3-hover-opacity" alt="Simulation of a stock">
      <h3>Simulate an efficient portfolio</h3>
      <p align="justify">Sigma provides you the simulation of a portfolio (assuming normality and without assuming normality) with default days and trajectories. Also, Sigma show you the probability of generating returns at the end of the period.</p>
    </div>
    <div class="w3-quarter">
      <img src="{option1}" style="width:100%" onclick="onClick(this)" class="w3-hover-opacity" alt="Markowitz">
      <h3>European and Binary option price</h3>
      <p align="justify">Sigma shows you the option premium of a european and binary option (call and put) with Black Scholes method and Montecarlo simulation (assuming normality and not doing so).</p>
    </div>
    <div class="w3-quarter">
      <img src="{option3}" style="width:100%" onclick="onClick(this)" class="w3-hover-opacity" alt="Simulation of a stock">
      <h3>Barrier option price</h3>
      <p align="justify">Sigma shows you the option premium of a barrier option: down and out (call and put) with Black Scholes method and Montecarlo simulation (assuming normality and not doing so).</p>
    </div>
  </div>


</div>
</div>



<!-- Notes -->
<div class="w3-content" id="notes">
<h5 class="w3-center w3-padding-48"><span class="w3-tag w3-wide">NOTES</span></h5>
<div class="w3-container w3-card-2 w3-white w3-round w3-margin"><br>
        <img src="{recom}" alt="Avatar" class="w3-left w3-circle w3-margin-right" style="width:95px">
        <h4>Conclusions</h4><br>
        <p align="justify">Sigma is a financial tool that can be very useful because it is personalized, you can use it anytime, anywhere and make estimates that could become complicated quickly.</p>
        <p align="justify">Sigma can be used when you need to make decisions that require information at the moment, since with this chatbot you can estimate prices of financial options, asset simulations and efficient portfolios, as well as their probability of obtaining a return in a certain time.</p>
        <img src="{recom}" alt="Avatar" class="w3-left w3-circle w3-margin-right" style="width:95px">
        <h4>Recommendations</h4><br>
        <p align="justify">For future work, we recommend that the commands can be used using natural language and are not subject to certain syntax for its operation.</p>
        <p align="justify">On the other hand, it is recommended to use functional programming and vectorization to make the process more efficient.</p>
               
        <h4 class="w3-center"><em>Do you want to know how Sigma works?</em></h4><br>
        <p align="center"> 
          <img align="center" src="{diagram}" border=0></p> 
  
</div>
</div>



<!-- Team Container -->
<div class="w3-content w3-container w3-padding-64" id="team">
  <div class="w3-container w3-padding-64 w3-center" id="team">
<h2>OUR WORK TEAM</h2>
<p>Meet the team:</p>

<div class="w3-row"><br>

<div class="w3-third">
  <img src="{Danny}" alt="Boss" style="width:45%" class="w3-circle w3-hover-opacity">
  <h3>Daniela Guerra Alcal&aacute</h3>
  <p>Financial engineer</p>
</div>

<div class="w3-third">
  <img src="{Rodrigo}" alt="Boss" style="width:45%" class="w3-circle w3-hover-opacity">
  <h3>Rodrigo Hern&aacutendez Mota</h3>
  <p>Financial engineer</p>
</div>

<div class="w3-third">
  <img src="{Yolanda}" alt="Boss" style="width:45%" class="w3-circle w3-hover-opacity">
  <h3>Yolanda Rodr&iacuteguez Ca&ntilde;edo</h3>
  <p>Financial engineer</p>
</div>

</div>
</div>
</div>



<!-- Allow on click expansion -->
<div id="modal01" class="w3-modal w3-black" onclick="this.style.display='none'">
  <span class="w3-button w3-xxlarge w3-black w3-padding-large w3-display-topright" title="Close Modal Image">X</span>
  <div class="w3-modal-content w3-animate-zoom w3-center w3-transparent w3-padding-64">
    <img id="img01" class="w3-image">
    <p id="caption" class="w3-opacity w3-large"></p>
  </div>
</div>


"""

html_end = """\



<script>
function onClick(element) {
  document.getElementById("img01").src = element.src;
  document.getElementById("modal01").style.display = "block";
  var captionText = document.getElementById("caption");
  captionText.innerHTML = element.alt;
}
</script>



</body>

</html>

"""
# %% 

# %% 


def returnHTML():
    
    
    complete_html = complete_html_head+html_without_images.format(
                                                  
    Rodrigo=getImageUrl("Rodrigo.jpg"),
    Danny=getImageUrl("danny.jpg"),
    investment=getImageUrl("investment.jpg"),
    bsbinary=getImageUrl("bsbinary.png"),
    bseuropean=getImageUrl("bseuropean.png"),
    recom=getImageUrl("recom.png"),
    sigma=getImageUrl("sigma.jpg"),
    Yolanda=getImageUrl("Yolanda.jpg"),
    barrier=getImageUrl("barrier.png"),
    ds=getImageUrl("ds.png"),
    available=getImageUrl("available.PNG"),
    describe=getImageUrl("describe.PNG"),
    plotalsea=getImageUrl("plotalsea.PNG"),
    markow1=getImageUrl("markow1.PNG"),
    markoweq=getImageUrl("markoweq.PNG"),
    sharpe=getImageUrl("sharpe.PNG"),
    bsequation=getImageUrl("bsequation.PNG"),
    kerneleq=getImageUrl("kerneleq.png"),
    diagram=getImageUrl("diagram.PNG"),
    covar=getImageUrl("covar.PNG"),
    simstock=getImageUrl("simstock.PNG"),
    effport=getImageUrl("effport.PNG"),
    simstockde=getImageUrl("simstockde.PNG"),
    simport=getImageUrl("simport.PNG"),
    sharpeport=getImageUrl("sharpeport.PNG"),
    option1=getImageUrl("option1.PNG"),
    option3=getImageUrl("option3.PNG"))+html_end
    
    return complete_html
    
def generateHTML():
    html_file = open("index.html","w")
    html_file.write(returnHTML())
    html_file.close()



# %% 
#    https://github.com/mxquants/sigmaBot/blob/master/interact.py

# %% 



# %% 
