var board;
var totalRows = 6;
var totalColumns = 7;

var readyPlayer1 = false;
var readyPlayer2= false;

window.onload = function () {
    boardDisplay();
    checkReady();
};

function split() {
    return this.id.split("-");  
};

function boardDisplay() {

    for (let myRow = 0; myRow < totalRows; myRow++) {
        for (let column = 0; column < totalColumns; column++) {
            let chip = document.createElement("div");
            chip.id = myRow.toString();
            chip.id = chip.id + "-";
            chip.id = chip.id+ column.toString();
            chip.classList.add("chip");
            document.getElementById("board").append(chip);
        }
    }
};



function checkReady() {
    let Button1 = document.getElementById("ready-player1");
    let Button2 = document.getElementById("ready-player2");

    Button1.addEventListener("click", function () {
        readyPlayer1 = true;
        startCheck();
    });

    Button2.addEventListener("click", function () {
        readyPlayer2 = true;
        startCheck();
    });
};

function startCheck() {
    if (readyPlayer1 == true) {
        if(readyPlayer2 == true) {
            startGame();
    }
}
};

function startGame() {
    
};
