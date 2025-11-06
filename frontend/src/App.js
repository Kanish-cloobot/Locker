/**
 * Main App component with routing.
 */
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './views/HomePage';
import LockerDetailPage from './views/LockerDetailPage';
import TransactionLedgerPage from './views/TransactionLedgerPage';
import LockerDashboardPage from './views/LockerDashboardPage';
import './styles/App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/locker/:id" element={<LockerDetailPage />} />
          <Route path="/locker/:id/dashboard" element={<LockerDashboardPage />} />
          <Route path="/transactions" element={<TransactionLedgerPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

