var board;
var totalRows = 6;
var totalColumns = 7;

var readyPlayer1 = false;
var readyPlayer2= false;


const ws = false;
let socket = null;

window.onload = function () {
    boardDisplay();
    
};




function initWS() {
    // Establish a WebSocket connection with the server
    socket = new WebSocket('ws://' + window.location.host + '/websocket');

   
    socket.onmessage = function (ws_message) {
        const message = JSON.parse(ws_message.data);
        const messageType = message.messageType
        if(messageType === 'chatMessage'){
            addMessageToChat(message);
        }else{
            // send message to WebRTC
            processMessageAsWebRTC(message, messageType);
        }
    }
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
}




function welcome() {
    insertPieceReq();
    setInterval(insertPieceReq, 2000);
}