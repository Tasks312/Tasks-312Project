const ws = true;
let socket = null;

function initWS() {
    // Establish a WebSocket connection with the server
    socket = new WebSocket('ws://' + window.location.host + '/ws');

    // Called whenever data is received from the server over the WebSocket connection
    socket.onmessage = function (ws_message) {
        const message = JSON.parse(ws_message.data);
        const messageType = message.messageType
        if(messageType === 'lobby_update'){
            updateLobbyList();
        }
    }
}
function lobbyHTML(lobbyJSON) {
    const lobby_title = lobbyJSON.lobby_title;
    const lobby_description = lobbyJSON.lobby_description;
    const lobby_id = lobbyJSON.lobby_id;
    // For later implement a status label, Open or Full(When 2 players in)
    let lobbyItemHtml =  '<div class="lobby-item">' +
        '<h3><b>Lobby Title:</b> ' + lobby_title + '</h3>' +
        '<p><b>Description:</b> ' + lobby_description + '</p>' +
        '<button class="join-button" onclick="joinLobby(\'' + lobby_id + '\')">Join</button>' +
        '</div>';
    return lobbyItemHtml;
}

function joinLobby(lobby_id) {
    if (ws){
        socket.send(JSON.stringify({'messageType': 'join_lobby', 'lobby_id': lobby_id}));
    }
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
        }
    }
    request.open("POST", "/join-lobby/" + lobby_id);
    request.send();
}

function clearLobbyList() {
    const lobbyList = document.getElementById("lobby-list");
    lobbyList.innerHTML = "";
}

function addLobbyToList(lobbyJSON) {
    const lobbyList = document.getElementById("lobby-list");
    lobbyList.innerHTML += lobbyHTML(lobbyJSON);
}

function updateLobbyList() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            clearLobbyList();
            const lobbys = JSON.parse(this.response);
            for (const each of lobbys) {
                addLobbyToList(each);
            }
        }
    }
    request.open("GET", "/lobby-list");
    request.send();
}

function welcome() {
    updateLobbyList();
    setInterval(updateLobbyList, 2000);
    if (ws) {
        initWS();
    }
}