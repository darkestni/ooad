import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ChatPage from './pages/ChatPage';
import ProtectedRoute from './components/ProtectedRoute';

import 'antd/dist/reset.css';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [token, setToken] = useState(null);
  const [history, setHistory] = useState([]);

  const handleLogin = (tokenFromServer, historyFromServer) => {
    setToken(tokenFromServer);
    setHistory(historyFromServer || []);
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setToken(null);
    setHistory([]);
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />

        <Route
          path="/login"
          element={<LoginPage onLogin={handleLogin} />}
        />

        <Route path="/register" element={<RegisterPage />} />

        <Route
          path="/chat"
          element={
            <ProtectedRoute isLoggedIn={isLoggedIn}>
              <ChatPage
                token={token}
                history={history}
                onLogout={handleLogout}
              />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
