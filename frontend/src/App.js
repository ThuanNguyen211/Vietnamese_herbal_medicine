import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import CatalogPage from './pages/CatalogPage';
import PlantDetailPage from './pages/PlantDetailPage';
import ChatbotPage from './pages/ChatbotPage';

function App() {
  return (
    <div className="app">
      <Navbar />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<CatalogPage />} />
          <Route path="/plant/:id" element={<PlantDetailPage />} />
          <Route path="/chatbot" element={<ChatbotPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
