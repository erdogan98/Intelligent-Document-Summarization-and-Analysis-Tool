import React from 'react';
import { Grid, Card,Box, CardContent, Typography, Button } from '@mui/material';
import SummaryDisplay from './SummaryDisplay';
import EntitiesDisplay from './EntitiesDisplay';
import SentimentIcon from './SentimentIcon';

function ResultsDisplay({ results }) {
  const { summary, entities, sentiment } = results;

  return (
      <Grid container spacing={2} sx={{ mt: 4 }}>
        <Grid item xs={12}>
          {/* Summary Card */}
          <Card variant="outlined">
            <CardContent>
              <Typography variant="h5">Summary</Typography>
              <SummaryDisplay summary={summary} />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          {/* Entities Card */}
          <Card variant="outlined">
            <CardContent>
              <Typography variant="h5">Entities</Typography>
              <EntitiesDisplay entities={entities} />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          {/* Sentiment Analysis Card */}
          <Card variant="outlined">
            <CardContent>
              <Typography variant="h5">Sentiment Analysis</Typography>
              {sentiment.label === 'ERROR' ? (
                  <Typography variant="body1" color="error">
                    An error occurred during sentiment analysis.
                  </Typography>
              ) : (
                  <Box display="flex" alignItems="center">
                    <SentimentIcon label={sentiment.label} />
                    <Typography variant="body1" style={{ marginLeft: '8px' }}>
                      {sentiment.label} ({(sentiment.score * 100).toFixed(2)}%)
                    </Typography>
                  </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* ... any other components like download button ... */}
      </Grid>
  );
}

export default ResultsDisplay;
