// src/pages/Home.js
import React, { useState } from 'react';
import { Container, Typography, Divider } from '@mui/material';
import UploadForm from '../components/UploadForm';
import TextInputForm from '../components/TextInputForm';
import ResultsDisplay from '../components/ResultsDisplay';

function Home() {
    const [results, setResults] = useState(null);

    return (
        <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
            <Typography variant="h4" gutterBottom>
                Intelligent Document Summarization and Analysis Tool
            </Typography>

            {/* File Upload Section */}
            <Typography variant="h6" gutterBottom>
                Upload a Document
            </Typography>
            <UploadForm setResults={setResults} />

            <Divider sx={{ my: 4 }} />

            {/* Direct Text Input Section */}
            <Typography variant="h6" gutterBottom>
                Enter Text Directly
            </Typography>
            <TextInputForm setResults={setResults} />

            {/* Display Results */}
            {results && <ResultsDisplay results={results} />}
        </Container>
    );
}

export default Home;
