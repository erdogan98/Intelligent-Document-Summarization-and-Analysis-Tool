import { useState } from 'react';
import UploadForm from '../components/UploadForm';
import ResultsDisplay from '../components/ResultsDisplay';
import Container from '@mui/material/Container';

function Home() {
  const [results, setResults] = useState(null);

  return (
    <Container maxWidth="md">
      <UploadForm setResults={setResults} />
      {results && <ResultsDisplay results={results} />}
    </Container>
  );
}

export default Home;
