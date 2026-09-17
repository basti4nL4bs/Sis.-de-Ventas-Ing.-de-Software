import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import VentaTerminal from './pages/VentaTerminal';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/terminal" />} />
        <Route path="/terminal" element={<VentaTerminal />} />
      </Routes>
    </BrowserRouter>
  );
}