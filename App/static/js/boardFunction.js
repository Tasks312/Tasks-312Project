var board;
var totalRows = 6;
var totalColumns = 7;




var currentPlayer; // stores the color of the current player

// if 1 player ==  RED
//if 2 player == Yellow 

const ws = false;
let socket = null;

window.onload = function () {
    boardDisplay();
    initWS();
    click_column();
    
};




function initWS() {
    // Establish a WebSocket connection with the server
    socket = new WebSocket('ws://' + window.location.host + '/websocket');

   
    socket.onmessage = function (ws_message) {
        const message = JSON.parse(ws_message.data);
        const messageType = message.messageType
     
        if(messageType === 'currentPlayer'){
            //whos tyrb is it red or yellow gets sent to client 
            currentPlayer = message.turn;

        }

        else if(message.messageType === 'placePiece'){

            // the row column to place piece gets sent to client as well as whether its red or yellow
            const row = message.row;
            const column = message.column;
            placePiece(row,column,currentPlayer);

        }


        else if(message.messageType === 'gameOver'){
            // server sends to client if a winner was decided on 
            const winner = message.winner;
            display_winner(winner,currentPlayer);
            
        }

        else{
            console.error('Invalid message Request received');
    }
}
};


function boardDisplay() {
        // displays the board 
    for (let myRow = 0; myRow < totalRows; myRow++) {
        for (let column = 0; column < totalColumns; column++) {
            let chip = document.createElement("div");

            chip.dataset.col = column;//data-col attribute to the column index

            chip.id = myRow.toString();
            chip.id = chip.id + "-";
            chip.id = chip.id+ column.toString();
            chip.classList.add("chip");
            document.getElementById("board").append(chip);
        }
    }
};

function placePiece(row,column,currentPlayer){
    //places the red or yellow piece in the correct row and column css has styling
    const chip = document.getElementById(row + "-" + column);
    if(currentPlayer === 'RED'){
        chip.classList.add('red-piece')
    }
    else{
        chip.classList.add('yellow-piece')
    }

};







function display_winner(currentPlayer){
    //gets the winner of the game and displays winner will be either red or yellow
    let the_id = document.getElementById("winner");
    let winner_statement = '<h1>${currentPlayer} is the winner!!!</h1>';
    the_id.innerHTML = winner_statement
}

function click_column(){

    // if a column is clicked this is triggered 
    
    let gameBoard = document.getElementById("board")
    gameBoard.addEventListener("click", function(event){
        getColumn(event);
    })
};

function getColumn(event){
    // get the clicked column
    const column = event.target.dataset.col;
    columnReq(column);

};



function columnReq(column){
    // sends using websockets int of the column that was clicked 

    if(ws){
        socket.send(JSON.stringify({'column': column}));
    }

    else{
        
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if ((this.readyState === 4)&&(this.status === 200 )){
                console.log('Column sent Successfully');
            }
            else{
                console.error('Column was not sent  successfully');
            }
        }


        const messageJSON = {"column": column};
        request.open("POST", "/column-position/" + column);
        request.send(JSON.stringify(messageJSON));



    }
        
    };