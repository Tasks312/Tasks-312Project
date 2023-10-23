function welcome() {
    document.addEventListener("keypress", function (event) {
        if (event.code === "Enter") {
            sendChat();
        }
    });
    document.getElementById("paragraph").innerHTML += "<br/>It's a pleasure to have you!!!"
    document.getElementById("post-history").focus();
}

function postHTML(postJSON) {
    const username = postJSON.username;
    const post = postJSON.message;
    const postId = postJSON.id;
    // will change later to like/dislike button
   // let messageHTML = "<br><button onclick='deleteMessage(\"" + messageId + "\")'>X</button> ";
    let postHTML = "<span id='message_" + postId + "'><b>" + username + "</b>: " + post + "</span>";
    return postHTML;
}

function addPostTo(postJSON) {
    const postHistory = document.getElementById("post-history");
    postHistory.innerHTML += postHTML(postJSON);
    postHistory.scrollIntoView(false);
    postHistory.scrollTop = postHistory.scrollHeight - postHistory.clientHeight;
}

function updateChat() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            clearPost();
            const posts = JSON.parse(this.response);
            for (const each of posts) {
                addPostTo(each);
            }
        }
    }
    request.open("GET", "/post-history");
    request.send();
}


function clearPost() {
   const postMessages = document.getElementById("post");
    postMessages.innerHTML = "";
}