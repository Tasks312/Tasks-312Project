function likePost(post_id){
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
        }
    }
    request.open("POST", "/like-post/" + post_id);
    request.send();
}

function unlikePost(post_id){
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
        }
    }
    request.open("POST", "/unlike-post/" + post_id);
    request.send();
}


function postHTML(postJSON) {
    const username = postJSON.username;
    const title = postJSON.title;
    const description = postJSON.description;
    const post_id = postJSON.post_id;

    let postHTML = "<div class='post'>";
    postHTML += "<p><b><u>User:</u></b> " + username + " <b><u> Title: </u></b> " + title + "</p>"
    postHTML += "<p><b>Description: </b>" + description + "</p>"
    postHTML += "<br><button onclick='likePost(\"" + post_id + "\")'>Like</button> ";
    postHTML += "<br><button onclick='unlikePost(\"" + post_id + "\")'>Unlike</button> ";
    postHTML += "</div>";
    return postHTML;
}

function clearPostHistory() {
    const postHistory = document.getElementById("post-history");
    postHistory.innerHTML = "";
}

function addPostTo(postJSON) {
    const postHistory = document.getElementById("post-history");
    postHistory.innerHTML += postHTML(postJSON);
}

function updatePostHistory() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            clearPostHistory();
            const posts = JSON.parse(this.response);
            for (const each of posts) {
                addPostTo(each);
            }
        }
    }
    request.open("GET", "/post-history");
    request.send();
}

function welcome() {
    updatePostHistory();
    setInterval(updatePostHistory, 2000);
}