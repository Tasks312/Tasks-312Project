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
    
};




function initWS() {
    // Establish a WebSocket connection with the server
    socket = new WebSocket('ws://' + window.location.host + '/websocket');

   
    socket.onmessage = function (ws_message) {
        const message = JSON.parse(ws_message.data);
        const messageType = message.messageType
     
        if(messageType === 'currentPlayer'){
            currentPlayer = message.turn;

        }

        else if(message.messageType === 'placePiece'){

            const row = message.row;
            const column = message.column;
            placePiece(row,column,currentPlayer);

        }


        else if(message.messageType === 'gameOver'){
            const winner = message.winner;
            display_winner(winner,currentPlayer);
            
        }

        else{
            console.error('Invalid message Request received');
    }
}
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


function placePiece(row,column,currentPlayer){
    const chip = document.getElementById(row + "-" + column);
    if(currentPlayer === 'RED'){
        chip.classList.add('red-piece')
    }
    else{
        chip.classList.add('yellow-piece')
    }

};






function insertPieceReq(column,lobbyID){
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4){
            
            if(this.status === 200 )
            {
                console.log('Piece was inserted successfully');
            }
            else{
                console.error('Piece could not be inserted successfully');
            }
        }
    }
};

function display_winner(currentPlayer){
    let the_id = document.getElementById("winner");
    let winner_statement = '<h1>${currentPlayer} is the winner!!!</h1>';
    the_id.innerHTML = winner_statement
};




function welcome() {
    insertPieceReq();
    setInterval(insertPieceReq, 2000);
};