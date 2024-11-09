import React, { useState, useEffect } from "react";
import io from "socket.io-client";

const socket = io("http://localhost:5000"); // Ensure this matches your backend address

function InputText() {
    const [text, setText] = useState("");
    const [texts, setTexts] = useState([]);
    const [connectedClients, setConnectedClients] = useState([]);

    useEffect(() => {
        // Listen for connected clients updates
        socket.on("connected_clients", (data) => {
            setConnectedClients(data.clients);
        });

        // Clean up on component unmount
        return () => socket.off("connected_clients");
    }, []);

    useEffect(() => {
        // Fetch initial texts from the backend
        fetch("http://localhost:5000/texts")
            .then((response) => response.json())
            .then((data) => setTexts(data));

        // Listen for real-time updates from the server
        socket.on("new_text", (newText) => {
            setTexts((prevTexts) => [...prevTexts, newText]);
        });

        // Cleanup WebSocket connection when component unmounts
        return () => socket.off("new_text");
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch("http://localhost:5000/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });
        setText("");  // Clear input after submission
    };

    return (
        <div>
            <h1>Text Submission</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Enter text here"
                />
                <button type="submit">Enter</button>
            </form>

            <h3>Connected Clients:</h3>
            <ul>
                {connectedClients.map((client, index) => (
                    <li key={index}>{client}</li>
                ))}
            </ul>            

            <h2>Live Updates</h2>
            <ul>
                {texts.map((item) => (
                    <li key={item.id}>
                        <strong>{item.timestamp}</strong>: {item.text}
                    </li>
                ))}
            </ul>            

        </div>
    );
}

export default InputText;