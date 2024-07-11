let $ = jQuery;
let socket;

function initializeWebSocket() {
  socket = new WebSocket('ws://localhost:8000/message');

  socket.onopen = function (event) {
    console.log('WebSocket connection established.');
  };

  socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    const msgClass = data.isMe ? 'user-message' : 'other-message';
    const sender = data.isMe ? 'You' : data.username;
    const message = data.data;
    const messageElement = $('<li>').addClass('clearfix');
    messageElement.append($('<div>').addClass(msgClass).text(sender + ': ' + message));
    $('#messages').append(messageElement);
    $('#chat').scrollTop($('#chat')[0].scrollHeight);
  };


  socket.onerror = function (event) {
    console.error('WebSocket error. Please rejoin the chat.');
    showJoinModal();
  };

  socket.onclose = function (event) {
    if (event.code === 1000) {
      console.log('WebSocket closed normally.');
    } else {
      console.error('WebSocket closed with error code: ' + event.code + '. Please rejoin the chat.');
      showJoinModal();
    }
  };
}

function showJoinModal() {
  $('#username-form').show();
  $('#chat').hide();
  $('#message-input').hide();
  $('#usernameModal').modal('show');
}

$('#open-modal').click(function () {
  showJoinModal();
});

function joinChat() {
  $('#username-form').hide();
  $('#chat').show();
  $('#message-input').show();
  $('#usernameModal').modal('hide');
}

$('#join').click(function () {
  initializeWebSocket();
  joinChat()
});

$('#send').click(function () {
  sendMessage();
});

$('#message').keydown(function (event) {
  if (event.key === "Enter") {
    sendMessage();
  }
});

function sendMessage() {
  const message = $('#message').val();
  const username = $('#usernameInput').val();

  if (message && username) {
    socket.send(JSON.stringify({ "message": message, "username": username }));
    
    // MySQL API 엔드 포인트 호출하여 메세지 저장
    $.ajax({
      type: 'POST',
      url: '/chats/',
      contentType: 'application/json',
      data: JSON.stringify({ "room_idx": 1, "chatter": username, "chat": message}),
      success: function (response) {
          console.log('Chat message sent and saved to MySQL.');
      },
      error: function (error) {
          console.log('Error sending chat message to MySQL:', error);
      }
    });
    
    $('#message').val('');
  }
}