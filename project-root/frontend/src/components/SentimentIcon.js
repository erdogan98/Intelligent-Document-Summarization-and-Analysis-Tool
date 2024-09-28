import React from 'react';
import {
  SentimentVerySatisfied,
  SentimentNeutral,
  SentimentDissatisfied,
  SentimentVeryDissatisfied,
} from '@mui/icons-material';

function SentimentIcon({ label }) {
  switch (label) {
    case 'POSITIVE':
      return <SentimentVerySatisfied style={{ color: 'green' }} />;
    case 'NEGATIVE':
      return <SentimentVeryDissatisfied style={{ color: 'red' }} />;
    case 'NEUTRAL':
      return <SentimentNeutral style={{ color: 'gray' }} />;
    case 'MIXED':
      return <SentimentNeutral style={{ color: 'orange' }} />;
    default:
      return <SentimentNeutral style={{ color: 'gray' }} />;
  }
}

export default SentimentIcon;
