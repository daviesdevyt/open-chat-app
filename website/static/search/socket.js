var socket;

$(document).ready(function () {
	var chatTemp = document.querySelector("[chat-template]")
	var chatDiv = document.querySelector("#chats")
	
	function addChat(user){
		var newChat = chatTemp.content.cloneNode(true)
		newChat.querySelector("[uname]").innerHTML = user.u
		newChat.querySelector("a").setAttribute("href", `/chat/${user.u}`)
		newChat.querySelector("polkadot-web-identicon").setAttribute("address", CryptoJS.MD5(user.u).toString())
		chatDiv.append(newChat)
	}
	socket = io("http://" + document.domain + ":" + location.port + "/search");
	socket.on("connect", function () {
		console.log("Connected");
	});
	socket.on("users", function (users) {
		console.log(users)
		chatDiv.innerHTML = ""
		users.forEach(user => {
			addChat(user)
		});
	});
	socket.on('disconnect', function(){
		console.log("Connecting ...")
	});
	var search_bar = document.querySelector("#search_bar")
	search_bar.addEventListener("input", (e) => {
		socket.emit("search", search_bar.value)
	})
});
