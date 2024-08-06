let count = 0;// counter variable 
const countElement = document.querySelector('.js-count'); //creating element of the count on screen

function countUp(){ //function that increases count
  count = count + 1; 
  document.querySelector('.js-count').innerHTML = `${count}`; //display count to screen
  countColor();
} 

function countDown(){ //function that decreases count
  count = count - 1; 
  document.querySelector('.js-count').innerHTML = `${count}`; //display count
  countColor();
}

function countColor(){ //function determines the color of the count
  if(count===0){ //Set count color Default(Black)
    countElement.classList.remove('countNegative'); 
    countElement.classList.remove('countPositive');
  }
  
  if(count>0){
    countElement.classList.add('countPositive'); //Change count color to green
    countElement.classList.remove('countNegative'); //Remove Red count color
  } 
  if(count<0){
    countElement.classList.add('countNegative') //Change count color to red
    countElement.classList.remove('countPositive'); //Remove Green count color

  }
}

let isIncreasing = true; //Tracks whether player has switched increase on or off
let isDecreasing = true; //Tracks whether player has switched decrease on or off
let intervalID; //ID of the interval  

const increaseButton = document.querySelector('.js-increase-button'); //increase button element
const decreaseButton = document.querySelector('.js-decrease-button'); //decrease button element
const resetButton = document.querySelector('.js-reset-button'); //reset button elelement

function increase(){ 

  if(isIncreasing == true){ //If player has pressed increase button once
    increaseButton.classList.add('buttonOn'); //Change button style when on
    isDecreasing = false;  //Make sure decreasing is off 
    decrease();
    intervalID = setInterval(function(){countUp()}, 1000); //run countUP every 1 second
    isIncreasing =false; //Next time user clicks increase button and calls increase() it will invoke else statement
    console.log('start increasing') 

  }  
  else{
    increaseButton.classList.remove('buttonOn'); //Change button style when off
    clearInterval(intervalID); //stop the setInterval() function 
    console.log('stop increasing');
    document.querySelector('.js-count').innerHTML = `${count}`; //display count to screen
    isIncreasing = true; //next time user clicks increase button count will start 
    isDecreasing = true; //Allow user to press decrease
  }
} 


function decrease(){
  if(isDecreasing == true){ 
    decreaseButton.classList.add('buttonOn'); //change button style when on
    isIncreasing = false;  //Make sure increasing is off 
    increase();
    intervalID = setInterval(function(){countDown()}, 1000); //Start decreasing
    isDecreasing = false; //next time decrease button is pressed decrease will stop 
    console.log('start decreasing');
  } 
  else{
    decreaseButton.classList.remove('buttonOn'); //change button style when off
    clearInterval(intervalID); //Stop decreasing 
    isDecreasing = true //next time press decrease button will start decreasing 
    isIncreasing = true; //next time user presses increase button will start increasing
    document.querySelector('.js-count').innerHTML = `${count}`; //display count 
    console.log('stop decreasing');
  }
} 

function reset(){ 
  resetButton.classList.add('buttonOn'); //change button style when pressed
  count = 0; //Reset count 
  console.log('Count reset');
  isDecreasing = false; //make sure decreasing is off
  decrease(); //invoke line above
  isIncreasing = false; //make sure increasing is off
  increase(); //invoke line above

  isDecreasing = true; //Back to default
  isIncreasing = true; //Back to default
  setTimeout(function(){resetButton.classList.remove('buttonOn')}, 150) //Change button style to default
  countColor() //Reset color of count
}

