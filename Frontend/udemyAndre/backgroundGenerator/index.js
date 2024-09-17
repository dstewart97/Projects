var css = document.querySelector("h3");
var left = document.getElementById("left");
var right = document.getElementById("right");
var body = document.querySelector("body");


function backgroundPainter() {
    body.style.background = 
    "linear-gradient(to right, " 
    + left.value 
    + ", " 
    + right.value 
    ;

    css.textContent = body.style.background + ";";
}

// Get user input on color selection
left.addEventListener("input", backgroundPainter);
right.addEventListener("input",backgroundPainter);

