import React from 'react';
import { Routes, Route } from 'react-router-dom';
import InputPage from './components/InputPage';
import ProgressPage from './components/ProgressPage';
import ResultsPage from './components/ResultsPage';

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<InputPage />} />
      <Route path="/progress/:jobId" element={<ProgressPage />} />
      <Route path="/results/:jobId" element={<ResultsPage />} />
    </Routes>
  );
};

export default App;