/**
 * Main App component with routing.
 */
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './views/HomePage';
import LockerDetailPage from './views/LockerDetailPage';
import LockerDashboardPage from './views/LockerDashboardPage';
import TransactionLedgerPage from './views/TransactionLedgerPage';
import './styles/App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/locker/:id" element={<LockerDetailPage />} />
          <Route path="/locker/:id/dashboard" element={<LockerDashboardPage />} />
          <Route path="/locker/:id/transactions" element={<TransactionLedgerPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

