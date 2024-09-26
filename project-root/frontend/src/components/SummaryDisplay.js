import React from 'react';
import { Typography } from '@mui/material';

function SummaryDisplay({ summary }) {
  return (
    <Typography
      variant="body1"
      style={{ textAlign: 'justify', lineHeight: 1.6 }}
    >
      {summary}
    </Typography>
  );
}

export default SummaryDisplay;
