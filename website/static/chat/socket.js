var socket;

function messageScrollIntoView(){
	const chat = $("#chat").children()
	chat[chat.length-1].scrollIntoView();
}

function msg_text(msg, is_sender) {
	const sent = is_sender ? "right" : "left";
	const opp_sent = is_sender ? "left" : "right";
	const style = is_sender ? " style='text-align: right;'" : "";
	return `<div class="chat-message-${sent} pb-4">
                <div class="flex-shrink-1 card-front rounded py-2 px-3">
					<div ${style}>
					</div>
					${msg.msg}
					<div class="text-muted small text-nowrap mt-2" style='text-align: ${opp_sent};'>
						${msg.t}
					</div>
	            </div>
            </div>`;
}
$(document).ready(function () {
	const abbr = document.getElementById("abbr");
	socket = io("http://" + document.domain + ":" + location.port + "/chat");
	socket.on("connect", function () {
		socket.emit("online", sendee);
		abbr.innerHTML = ""
	});
	socket.on("get_messages", function (msgs) {
		$("#chat").empty();
		msgs.forEach(function (msg) {
			const is_sender = msg.is_s;
			const name = msg.is_s ? "You" : msg.s;
			if (msg.msg) $("#chat").prepend(msg_text(msg, is_sender, name));
		});
		messageScrollIntoView();
		$("#message_holder").focus();
	});
	socket.on("new_message", function (msg) {
		const is_sender = msg.s_id == current_user;
		$("#chat").append(msg_text(msg, is_sender));
		messageScrollIntoView();
	});
	socket.on('disconnect', function(){
		abbr.innerHTML = "Connecting ..."
	});
});
