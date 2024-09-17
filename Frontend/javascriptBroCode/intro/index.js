/* ===== How to accept user input ===== */

// Easy way with window prompt:
// let username = window.prompt("What's your name");
// console.log(username)


// Difficult way with html textbox:
// let username;
// document.getElementById("myButton").onclick = function() {
//     username = document.getElementById("myText").value;
//     console.log(username)
//     document.getElementById("myLabel").innerHTML = "Hello " + username;
// }

/* ===== Type conversion ===== */

// let age = window.prompt("How old are you?");

// console.log(typeof age);
// age = Number(age);
// console.log(typeof age);
// age += 1;

// console.log("Happy Birthday! You Are " + age , "years old")

// let x;
// let y;
// let z;

// x = Number("3.14");
// y = String(3.14)
// z = Boolean("pizza") // empty string give you false, any string is true

// console.log(x, typeof x);
// console.log(y, typeof y);
// console.log(z, typeof z);


/* ===== Constants ===== */

// let pi = 3.14159;
// let radius;
// let circumference;

// radius = window.prompt("Enter the radius of a circle");
// radius = Number(radius);

// circumference = 2 * pi * radius;

// console.log("The circumference is " + circumference);


/* ===== Math Built in Library===== */

// let x = 3.14;

// // Round
// x = Math.round(x)
// // Floor -- round number down
// x = Math.floor(x);
// // Ceil -- round up
// x = Math.ceil(x)
// // Raise to power
// x = Math.pow(x, 2) // x^2
// // Etc.
// console.log(x)

// let a;
// let b;
// let c;

// a = window.prompt("Enter side A");
// a = Number(a);

// b = window.prompt("Enter side B");
// b = Number(b);


// c = Math.sqrt((Math.pow(a, 2)) + (Math.pow(b, 2)));

// console.log("Side C: ", c);


// Counter program

// let count = 0

// document.getElementById("decreaseBtn").onclick = function () {
//     count-=1;
//     document.getElementById("countLabel").innerHTML = count
// }
// document.getElementById("resetBtn").onclick = function () {
//     count=0;
//     document.getElementById("countLabel").innerHTML = count
// }
// document.getElementById("increaseBtn").onclick = function () {
//     count+=1;
//     document.getElementById("countLabel").innerHTML = count
// }



/* ===== Game development stuff ===== */

// let x;
// let y;
// let z;

// document.getElementById("rollBtn").onclick = function() {
//     x = Math.floor(Math.random() * 6) + 1;
//     y = Math.floor(Math.random() * 6) + 1;
//     z = Math.floor(Math.random() * 6) + 1;

//     document.getElementById("xLabel").innerHTML = "Roll 1: " + x
//     document.getElementById("yLabel").innerHTML = "Roll 2: " + y
//     document.getElementById("zLabel").innerHTML = "Roll 3: " + z
// }



/* ===== Useful String Methods ===== */

// let userName = "Bro Code";

// console.log(userName.length)
// let firstLetter = userName.charAt(0);
// console.log(firstLetter)




/* ===== Method Chaining ===== */

// let userName = 'david';

// let letter = userName.charAt(0).toUpperCase();
// console.log(letter);



/* ===== If Statement ===== */

// let age = 65;

// if(age >= 65){
//     console.log("You are a senior citizen");
// }
// else if(age >= 18){
//     console.log("You are an adult");
// }
// else if(age < 0){
//     console.log("You haven't been born yet");
// }
// else{
//     console.log("You are a child");
// }

// let online = false;

// if(online){
//     console.log("You are online");
// }
// else{
//     console.log("You are offline");
// }




/* ===== Checking if checkbox is ticked ===== */
/* ===== .checked can be used with checkbox and radios and returns true false ===== */

// document.getElementById("myButton").onclick = function() {
//     const myCheckBox = document.getElementById("myCheckBox");
//     const visaBtn = document.getElementById("visaBtn");
//     const mastercardBtn = document.getElementById("mastercardBtn");
//     const paypalBtn = document.getElementById("paypalBtn");


//     if(myCheckBox.checked){
//         console.log("You are subscribed");
//     }
//     else{
//         console.log("You are not subscribed");
//     }

//     if(visaBtn.checked){
//         console.log("You are paying with Visa")
//     }
//     else if(mastercardBtn.checked){
//         console.log("You are paying with Mastercard");
//     }
//     else if(paypalBtn.checked){
//         console.log("You are paying with Paypal")
//     }
//     else{
//         console.log("You must select a payment type")
//     }
// }


/* ===== Switch statement good for lots of else if ===== */

// let grade = "D";

// switch(grade){
//     case "A":
//         console.log("You did great!")
//         break;
//     case "B":
//         console.log("You did good!")
//         break;
//     case "C":
//         console.log("You did okay!")
//         break;
//     case "D":
//         console.log("You passed....barely!")
//         break;
//     case "F":
//         console.log("You failed!")
//         break;
//     default:
//         console.log(grade, "is not a letter grade")
// }


// let grade_num = "59";

// switch(true){
//     case grade_num >= 90:
//         console.log("You did great!")
//         break;
//     case grade_num >= 80:
//         console.log("You did good!")
//         break;
//     case grade_num >= 70:
//         console.log("You did okay!")
//         break;
//     case grade_num >= 60:
//         console.log("You passed....barely!")
//         break;
//     case grade_num < 60:
//         console.log("You failed!")
//         break;
//     default:
//         console.log(grade_num, "is not a letter grade")
// }



/* ===== and or logical and (&&) or (||) not (!) ===== */

// let temp = 50;

// if(temp > 0 || temp < 30){
//     console.log("The weather is good");
// }
// else{
//     console.log("The weather is bad");
// }




/* ===== While loop can not start if condition is not true to start===== */

// let userName = "";

// while(userName == "" || userName == null){
//     userName = window.prompt("Enter your username");
// }

// console.log("Hello", userName);



/* ===== Do While loop do it at least once then check the condition ===== */

// let userName;

// do{
//     userName = window.prompt("Enter your username");
// }while(userName == "")

// console.log("Hello", userName);


/* ===== Template Literals ===== */

// let userName = "David";
// let items = 3;
// let total = 75;

// console.log(`Hello ${userName}`)
// console.log(`You have ${items} in your cart`)
// console.log(`Your total is $${total}`)



/* ===== Format Currency ===== */

// let myNum = 100;

// myNum = myNum.toLocaleString("en-US"); //US English
// myNum = myNum.toLocaleString("en-US", {style: "currency", currency: "USD"}); 
// myNum = myNum.toLocaleString(undefined, {style: "percent"})
// myNum = myNum.toLocaleString(undefined, {style: "unit", unit: "celsius"})
// console.log(myNum);


/* ===== Number Guessing Game ===== */

/* <body>
    <h1>Number Guessing Game</h1>
    <p>Pick a nunber between 1 and 10</p>
    <label>Enter a guess</label>

    <input type="text" id="guessField">
    <button type="submit" id="submitButton">Submit</button>
    <script src="index.js"></script>
</body>

const answer = Math.floor(Math.random() * 10 + 1)
let guesses = 0;

document.getElementById("submitButton").onclick = function () {

    let guess = document.getElementById("guessField").value;
    guesses+=1;

    if(guess == answer){
        alert(`${answer} is the number. It took you ${guesses} guesses`)
    }
    else if(guess < answer){
        alert(`Too Small!`)
    }
    else{
        alert("Too Large!")
    }
} */




/* ===== Callback - a function passed as an argument to another function ===== */

// Ensures a function is not going to run before a task is completed

// sum(2, 3, displayDOM);

// function sum(x, y, callBack){
//     let result = x + y;
//     callBack(result);
// }

// function displayConsole(output){
//     console.log(output);
// }

// function displayDOM(output){
//     document.getElementById("myLabel").innerHTML = output;
// }



/* ===== array.forEach() - executes a provided callback function once for each array element ===== */
// element, index, array are provided to us, dont need to use them
// need at least an element 

// let students = ["spongebob", "patrick", "squidward"];
// students.forEach(capitalize);
// students.forEach(print);

// function capitalize(element, index, array){
//     array[index] = element[0].toUpperCase() + element.substring(1);
// }

// function print(element){
//     console.log(element);
// }



/* ===== array.map() executes a provided callback function once for each array element AND creates a new array ===== */
// element, index, array are provided to us, dont need to use them
// need at least an element 

// let numbers = [1, 2, 3, 4, 5];
// let squares = numbers.map(square);

// squares.forEach(print);

// function square(element){
//     return Math.pow(element, 2);
// }

// function print(element){
//     console.log(element);
// }


/* ===== array.filter() creates a new array with all elements that pass the test provided by a function ===== */

// let ages = [18, 16, 21, 17, 19, 90];
// let adults = ages.filter(checkAge);

// adults.forEach(print);

// function checkAge(element){
//     return element >= 18;
// }

// function print(element){
//     console.log(element);
// }


/* ===== array.reduce() reduces an array to a single value ===== */

let prices = [5, 10, 15, 20, 25];
let total = prices.reduce(checkOut);

console.log(`The total is $${ total}`)

function checkOut(total, element){
    return total + element;
}