// src/components/EntitiesDisplay.js
import React from 'react';
import { Chip, Tooltip } from '@mui/material';

function EntitiesDisplay({ entities }) {
  return (
    <div>
      {entities.map((entity, index) => (
        <Tooltip key={index} title={`Type: ${entity[1]}`}>
          <Chip
            label={entity[0]}
            variant="outlined"
            style={{ margin: '4px' }}
          />
        </Tooltip>
      ))}
    </div>
  );
}

export default EntitiesDisplay;
