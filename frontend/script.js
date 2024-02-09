import { updateData } from "./server.js";

//Getting Buttons and canvas from html
let brush_value = document.getElementById("brush_value");
let slider = document.getElementById("brush_size");
let cleanBtn = document.getElementById("button");
let canvas = document.getElementById("canvas");
let color = document.getElementById("Color");
let ctx = canvas.getContext("2d");
let checkNumberBtn = document.getElementById("check-Number");
let brushSize = 1;
let paint = false;

//Variables for canvas properties
ctx.fillStyle = '#FFFFFF';
ctx.fillRect(0, 0, canvas.width, canvas.height);
ctx.lineWidth = 1;
ctx.strokeStyle = '#000000';
canvas.width = innerWidth / 3;
canvas.height = canvas.width;


//=====================================================================================================
//ALL THE FUNCTIONS
//=====================================================================================================

//Function to call all the functions on start
function executor() {
    clean();
    drawing();
    cleanData();
    checkNumberEvnt();
}

//TO LET USER DRAW ON THE CANVAS
function drawing() {

    //Function to start paint
    function startDraw() {
        paint = true;
        ctx.beginPath();
    }

    //Function to stop paint
    function endDraw() {
        paint = false;
    }

    //Main function for paint
    function draw(event) {
        if (!paint) return;

        ctx.lineWidth = brushSize;
        ctx.lineCap = 'round';
        ctx.lineCap = ''
        ctx.strokeStyle = color.value;
        ctx.lineTo(event.clientX - canvas.offsetLeft, event.pageY - 90);
        ctx.moveTo(event.pageX - canvas.offsetLeft, event.pageY - 90);
        ctx.stroke();
    }
    canvas.addEventListener("mousedown", startDraw);
    canvas.addEventListener("mouseup", endDraw);
    canvas.addEventListener("mousemove", draw);
}

//To clean the canvas
function clean(event) {
    ctx.fillStyle = '#FFFFFF';  // Set to white
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

// Response Function()
function response(value) {
    for (let i = 0; i <= 9; i++) {
        let activation = document.getElementById('c' + i)
        activation.style.backgroundColor = 'rgba(0,0,0,' + value["prediction"][i] + ')';
    }
    console.log(value["prediction"]);
    let number = document.getElementById('result');
    number.innerHTML = value["max"];
}

// Function to check number
function checkNumber(event) {

    let screenshot = canvas.toDataURL('image/png');

    updateData(screenshot, response);

}

// GET DATA
function getdata() {
    executor();
}

// =====================================================================================================
// Eevnt Listneres
// =====================================================================================================
function cleanData() {
    cleanBtn.addEventListener('click', clean);
}

function checkNumberEvnt() {
    checkNumberBtn.addEventListener('click', checkNumber);
}

slider.addEventListener("input", () => {
    brushSize = slider.value;
    brush_value.value = slider.value;
});

brush_value.addEventListener("change", () => {
    if (brush_value.value <= 50 && brush_value.value > 0) {
        slider.value = brush_value.value;
        brushSize = brush_value.value;
    }
    else {
        brush_value.value = brushSize;
    }
});
window.addEventListener("load", getdata());