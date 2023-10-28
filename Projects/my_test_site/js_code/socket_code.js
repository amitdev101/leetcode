var socket = new WebSocket('ws://localhost:8000/ws/some_path/');

socket.onopen = (event) => {
  console.log('WebSocket connected from client:', event);
  sendMessage('Hello Server!');
};

socket.onmessage = (event) => {
  console.log('Received event from server:', event.data);
};

socket.onclose = (event) => {
  console.log('WebSocket closed:', event);
};

socket.onerror = (error) => {
  console.error('WebSocket error:', error);
};

function sendMessage(message) {
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(message);
    console.log('Message sent:', message);
  } else {
    console.error('WebSocket is not open. Ready state:', socket.readyState);
  }
}
