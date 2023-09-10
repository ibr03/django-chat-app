// chatapp/templates/chatapp/chat.js
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const message = data['message'];

    // Handle the received message (e.g., display it in the chat interface)
};

chatSocket.onclose = function (e) {
    // Handle WebSocket closure (e.g., reconnection logic)
};
