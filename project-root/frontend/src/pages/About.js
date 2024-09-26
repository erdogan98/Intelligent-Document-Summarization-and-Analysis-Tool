import React from 'react';
import { Container, Typography } from '@mui/material';

function About() {
  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        About This App
      </Typography>
      <Typography variant="body1" paragraph>
        The Intelligent Document Summarization and Analysis Tool allows users to upload documents and receive automated summaries, entity recognition, and sentiment analysis. Built with modern technologies and advanced AI models, it showcases capabilities in full-stack development and machine learning integration.
      </Typography>
    </Container>
  );
}

export default About;
