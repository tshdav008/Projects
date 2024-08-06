//These are the about us displayed on page
const john1 = {id: 'john1',name:'Noah Davis', position: 'Financial Controller', review: '"Hello, I’m Noah Davis, the Financial Controller. I handle all financial aspects of the restaurant, from budgeting to financial planning. My analytical skills help us maintain a successful and sustainable business. Outside of work, I’m passionate about cooking and love trying out new recipes at home."'}; 
const john2 = {id: 'john2', name: 'Ethan Brown', position: 'Sous Chef', review: '"Hey, I’m Ethan Brown, the Sous Chef. I support our Executive Chef in the kitchen, ensuring that every dish meets our high standards of quality. With extensive experience in culinary arts, I’m dedicated to perfecting our menu and contributing to our restaurant’s success. In my free time, I enjoy visiting local farmers markets and experimenting with seasonal ingredients."'};
const john3 = {id: 'john3',name: 'Liam Carter', position: 'Operations Manager', review: '"Hi, I’m Liam Carter, the Operations Manager. My job is to oversee the day-to-day operations of the restaurant, ensuring that everything runs smoothly and efficiently. With a background in business management, I focus on optimizing our processes and enhancing the guest experience. In my downtime, I’m a sports enthusiast and enjoy playing soccer with friends."'};
const doe1 = {id: 'doe1',name: 'Olivia Martinez', position: 'Marketing Director', review: '"Hey there, I’m Olivia Martinez, the Marketing Director. I’m responsible for shaping our restaurant’s image and engaging with our community through various media channels. My background in digital media helps me connect with our guests effectively. When I’m not working, I’m passionate about photography and love capturing the beauty of everyday life."'};
const doe2 = {id: 'doe2',name: 'Sophia Lee', position: 'Guest Relations Manager', review: '"Hello, I’m Sophia Lee, the Guest Relations Manager. My role is to ensure that every guest who walks through our doors feels welcomed and valued. With over a decade of experience in hospitality, I strive to make each visit exceptional. Outside of work, I enjoy hiking and spending quality time outdoors with my loved ones."'};
const doe3 = {id: 'doe3',name: 'Emma Johnson', position: 'Executive Chef', review:'"Hi, I’m Emma Johnson, the Executive Chef here at Bella’s Bistro. With a background in culinary arts and a passion for crafting exquisite dishes, I lead our kitchen team in creating memorable dining experiences. I’ve worked in top-tier restaurants around the world and enjoy experimenting with innovative flavors. When I’m not in the kitchen, I love exploring new food cultures and spending time with my family."'};

arr1 = [doe1,john1,john2,doe2,john3,doe3]; //array containing the peoples about us
//console.log()

let pos = 3; //track postion in array

function display(){ //display about us on screen 
  document.querySelector('.js-image').innerHTML = `<img src = "Images/${arr1[pos].id}.jpeg">`;
  document.querySelector('.js-name').innerHTML = arr1[pos].name;
  document.querySelector('.js-position').innerHTML = arr1[pos].position;
  document.querySelector('.js-review').innerHTML = arr1[pos].review;
}


const leftButton = document.querySelector('.js-left-button'); //creating left Button element
leftButton.addEventListener('click', function (){
  console.log('left') 
  if(pos>0  && pos<= arr1.length){
    pos = pos - 1; //move to next review 
    console.log(pos);
    display(); //display review
  } 
  if(pos===0){
    display(); 
    pos = 5; //display review from start 
  }
  
});



const rightButton = document.querySelector('.js-right-button'); //creating right button element
rightButton.addEventListener('click', function (){
  console.log('right') 
  if(pos < arr1.length-1){
    pos = pos + 1; //move to next review 
    console.log(pos);
    display(); //display review
  }  
  //ADD IF POSTION IS EQUAL TO ARRAY LENTGHG
  if(pos >= arr1.length){ 
    console.log(pos);
    pos = 0; //display review from start 
    display();
  }
  

});