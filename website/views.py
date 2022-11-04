from flask import Blueprint, render_template, redirect, url_for, json
from flask_login import login_required, current_user
from .models import Message, User, Chat
from . import db, emit, socketio, join_room
from .hash import h


views = Blueprint('views', __name__)

@views.route('/chat/<username>', methods=['GET', 'POST'])
@login_required
def chat(username):
    user = User.query.filter_by(username=username).first()
    if user:
        chat = Chat.query.filter_by(id="".join(sorted([str(user.id), str(current_user.id)]))).first()
        if not chat:
            new_chat = Chat(id="".join(sorted([str(user.id), str(current_user.id)])))
            db.session.add(new_chat)
            db.session.commit()
        return render_template('chat-app.html', user=user, sendee=user.id)
    else:
        return "Not found"

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    return render_template('search.html')

@socketio.on('search', namespace='/search')
@login_required
def search_user(data):
    users = db.session.query(User).filter(User.username.ilike(data+'%')).all()
    users_arr = []
    for i in users:
        if i == current_user:
            continue
        users_dict = {}
        users_dict["u"] = i.username
        users_dict["i"] = i.id
        users_arr.append(users_dict)
    emit("users", users_arr)

@socketio.on('connect', namespace='/search')
@login_required
def search_connected():
    users = User.query.order_by(User.username).all()
    users_arr = []
    for i in users:
        if i == current_user:
            continue
        users_dict = {}
        users_dict["u"] = i.username
        users_dict["i"] = i.id
        users_arr.append(users_dict)
    emit("users", users_arr)
    
@socketio.on('online', namespace='/chat')
@login_required
def isonline(sender):
    messages = []
    get_chat = Message.query.filter_by(chat_id="".join(sorted([str(sender), str(current_user.id)]))).order_by(Message.id.desc()).limit(30).all()
    for i in get_chat:
        messages.append({"msg": i.data, "t": str(i.date.time())[0:5], "is_s": i.sender==current_user.id})
    join_room("".join(sorted([str(sender), str(current_user.id)])))
    if len(messages) > 0:
        emit('get_messages', messages)

def create_message(text, reciever):
    new_message = Message(sender=current_user.id, reciever=reciever, chat_id="".join(sorted([str(reciever), str(current_user.id)])))
    new_message.data = text
    db.session.add(new_message)
    db.session.commit()
    return new_message

@socketio.on('send', namespace='/chat')
@login_required
def send(data):
    new_message = create_message(data['message'], data["reciever"])
    emit('new_message', {'msg': new_message.data, 't': str(new_message.date.time())[0:5], 's_id': new_message.sender}, room="".join(sorted([str(data["reciever"]), str(current_user.id)])))
