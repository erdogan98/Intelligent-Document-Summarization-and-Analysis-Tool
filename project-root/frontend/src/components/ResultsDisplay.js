import React from 'react';
import { Grid, Typography, Button, Accordion, AccordionSummary, AccordionDetails } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import SummaryDisplay from './SummaryDisplay';
import EntitiesDisplay from './EntitiesDisplay';
import SentimentChart from './SentimentChart';
import { jsPDF } from 'jspdf';

function ResultsDisplay({ results }) {
  const { summary, entities, sentiment } = results;

  const handleDownload = () => {
    const doc = new jsPDF();
    doc.setFontSize(16);
    doc.text('Summary', 10, 10);
    doc.setFontSize(12);
    doc.text(summary, 10, 20);
    doc.save('analysis.pdf');
  };

  return (
    <Grid container spacing={2} sx={{ mt: 4 }}>
      <Grid item xs={12}>
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography variant="h6">Summary</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <SummaryDisplay summary={summary} />
          </AccordionDetails>
        </Accordion>
      </Grid>

      <Grid item xs={12} md={6}>
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography variant="h6">Entities</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <EntitiesDisplay entities={entities} />
          </AccordionDetails>
        </Accordion>
      </Grid>

      <Grid item xs={12} md={6}>
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography variant="h6">Sentiment Analysis</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <SentimentChart sentiment={sentiment} />
            <Typography variant="body2">Compound Score: {sentiment.compound}</Typography>
          </AccordionDetails>
        </Accordion>
      </Grid>

      <Grid item xs={12}>
        <Button variant="contained" onClick={handleDownload}>
          Download Results
        </Button>
      </Grid>
    </Grid>
  );
}

export default ResultsDisplay;
