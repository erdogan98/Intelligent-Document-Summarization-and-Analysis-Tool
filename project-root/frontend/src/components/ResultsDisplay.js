import React from 'react';
import { Card, CardContent, Typography, Grid } from '@mui/material';
import { motion } from 'framer-motion';

// Define animation variants for consistent motion settings
const containerVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      staggerChildren: 0.2,
      duration: 0.5,
    },
  },
};

const cardVariants = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: {
      duration: 0.5,
    },
  },
};

function ResultsDisplay({ results }) {
  const { summary, entities, sentiment } = results;

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <Grid container spacing={2}>
        {/* Summary Card */}
        <Grid item xs={12}>
          <motion.div variants={cardVariants}>
            <Card variant="outlined" sx={{ backgroundColor: '#f9f9f9' }}>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Summary
                </Typography>
                <Typography variant="body1">{summary}</Typography>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Entities Card */}
        <Grid item xs={12}>
          <motion.div variants={cardVariants}>
            <Card variant="outlined" sx={{ backgroundColor: '#f1f1f1' }}>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Entities
                </Typography>
                {entities.length > 0 ? (
                  entities.map((entity, index) => (
                    <Typography key={index} variant="body2">
                      <strong>{entity[0]}</strong>: {entity[1]}
                    </Typography>
                  ))
                ) : (
                  <Typography variant="body2">No entities found.</Typography>
                )}
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Sentiment Analysis Card */}
        <Grid item xs={12}>
          <motion.div variants={cardVariants}>
            <Card variant="outlined" sx={{ backgroundColor: '#e9e9e9' }}>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Sentiment Analysis
                </Typography>
                <Typography variant="body2" color="success.main">
                  Positive: {sentiment.pos}
                </Typography>
                <Typography variant="body2" color="warning.main">
                  Neutral: {sentiment.neu}
                </Typography>
                <Typography variant="body2" color="error.main">
                  Negative: {sentiment.neg}
                </Typography>
                <Typography variant="body2">
                  Compound: {sentiment.compound}
                </Typography>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>
      </Grid>
    </motion.div>
  );
}

export default ResultsDisplay;
