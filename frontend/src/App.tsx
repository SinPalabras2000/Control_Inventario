import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from './components/layout';
import { Home, InventoryRegistration, InventoryQuery } from './pages';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/inventario" element={<InventoryRegistration />} />
          <Route path="/consulta-inventario" element={<InventoryQuery />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;