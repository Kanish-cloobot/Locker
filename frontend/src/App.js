/**
 * Main App component with routing.
 */
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './views/HomePage';
import LockerDetailPage from './views/LockerDetailPage';
import './styles/App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/locker/:id" element={<LockerDetailPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

