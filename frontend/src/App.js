import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import InputText from "./InputText";

function App() {
    return (
        <Router>
            <Routes>
              
                <Route path="/" element={<InputText />} />

            </Routes>
        </Router>
    );
}

export default App;