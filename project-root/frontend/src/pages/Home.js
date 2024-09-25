// src/pages/Home.js
import React, { useState } from 'react';
import { Container } from '@mui/material';
import UploadForm from '../components/UploadForm';
import ResultsDisplay from '../components/ResultsDisplay';

function Home() {
  const [results, setResults] = useState(null);

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <UploadForm setResults={setResults} />
      {results && <ResultsDisplay results={results} />}
    </Container>
  );
}

export default Home;
