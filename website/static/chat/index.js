function send_message() {
	text = $("#message_holder").val();
	if (text.replace(" ", "") != "") {
		$("#message_holder").val("");
		$("#message_holder").focus();
		socket.emit("send", { message: text, reciever: sendee });	
	}
}
$("#send_message").click(function (e) {
	send_message();
});

$("#message_holder").keydown(function (event) {
	if (event.which == 13) {
		send_message();
	}
});
