from flask import Flask, request, jsonify
from flask_cors import CORS #allows react to make requests to this backend python code
from flask_socketio import SocketIO, emit, join_room, leave_room
from pymongo import MongoClient
from datetime import datetime
import uuid
import threading


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

#for mongoDB connection
client = MongoClient("mongodb+srv://arteaga215:admin@first-cluster.mu9ti.mongodb.net/")  #replace with MongoDB URI
db = client["TextsDB"]
collection = db["texts"]

# Custom room name to track connected clients
connected_clients_room = "connected_clients"
connected_clients = []

# Function to watch MongoDB changes (similar to previous example)
def watch_changes():
    with client.watch() as stream:
        for change in stream:
            if change["operationType"] in ["insert", "delete", "update"]:
                texts = list(collection.find({}, {'_id': 0}))
                socketio.emit("update_texts", texts)

# Start the Change Stream listener in a background thread
#threading.Thread(target=watch_changes, daemon=True).start()

# Track when a client connects
@socketio.on("connect")
def handle_connect():
    join_room(connected_clients_room)
    connected_clients.append(request.sid)  # Add client session ID to the list
    print(f"Client connected: {request.sid}")
    
    # Emit current client list to all clients
    emit("connected_clients", {"clients": connected_clients}, broadcast=True)

# Track when a client disconnects
@socketio.on("disconnect")
def handle_disconnect():
    leave_room(connected_clients_room)
    connected_clients.remove(request.sid)  # Remove client session ID from the list
    print(f"Client disconnected: {request.sid}")
    
    # Emit updated client list to all clients
    emit("connected_clients", {"clients": connected_clients}, broadcast=True)


@app.route('/submit', methods=['POST'])
def submit_text():
    data = request.json
    text = data.get("text", "")
    entry = {
        "id": str(uuid.uuid4()),
        "text": text,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    result = collection.insert_one(entry)
    entry["_id"] = str(result.inserted_id)
    socketio.emit('new_text', entry) #emits to all connected clients
    return 'success', 204

@app.route('/texts', methods=['GET'])
def get_texts():
    texts = list(collection.find({}, {'_id': 0}))
    return jsonify(texts)

if __name__ == '__main__':
    socketio.run(app, debug=True)