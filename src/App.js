import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './home';
import Process from './process';

function App() {
    return (
        <Router>
            <div>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/process/:bookId/:telephoneNumber" element={<Process />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
