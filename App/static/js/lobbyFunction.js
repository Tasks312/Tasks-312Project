d
function lobbyHTML(lobbyJSON) {
    const lobby_title = lobbyJSON.lobby_title;
    const lobby_description = lobbyJSON.lobby_description;
    const lobby_id = lobbyJSON.lobby_id;
    const users = lobbyJSON.users
    const lobby_image = lobbyJSON.lobby_image

    // Card Style
    let lobbyItemHtml = '<div class="card">' +
        '<div class="leftImage"> <img src="' + lobby_image +'" alt= Lobby Image"> </div>'+
        '<div class="container"> <h3><b> Title: </b>' + lobby_title + '</h3>' +
        '<p><b> Description: </b>' + lobby_description +'</p>'+
        '<p> Players in lobby: '+ users +'</p>' +
        '<button class="join-button" onclick="joinLobby(\'' + lobby_id + '\')">Join</button>' + '</div> </div>';
    
    // let lobbyItemHtml =  '<div class="lobby-item">' +
    //     '<h3><b>Lobby Title:</b> ' + lobby_title + '</h3>' +
    //     '<p><b>Description:</b> ' + lobby_description + '</p>' +
    //     '<p>Number of players in lobby: '+ users +'</p>' +
    //     '<button class="join-button" onclick="joinLobby(\'' + lobby_id + '\')">Join</button>' +
    //     '</div>';
    return lobbyItemHtml;
}

function joinLobby(lobby_id) {

    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 301) {
            console.log(this.response);
            window.location.href = "/game"
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

            if (lobbys.redirect !== undefined) {
                window.location.href = "/game"
            }
            else {
                for (const each of lobbys) {
                    addLobbyToList(each);
                }
            }
           
        }
    }
    request.open("GET", "/lobby-list");
    request.send();
}

function welcome() {
    updateLobbyList();
    
    setInterval(updateLobbyList, 2000);
}