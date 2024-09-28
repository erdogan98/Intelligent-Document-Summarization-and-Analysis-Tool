import React from 'react';
import { Chip, Tooltip, Stack } from '@mui/material';

function EntitiesDisplay({ entities }) {
  // Categorize entities by their types
  const categorizedEntities = entities.reduce((acc, [text, label]) => {
    if (!acc[label]) acc[label] = [];
    acc[label].push(text);
    return acc;
  }, {});

  return (
    <Stack direction="row" flexWrap="wrap">
      {Object.entries(categorizedEntities).map(([label, texts], idx) => (
        <div key={idx} style={{ margin: '4px' }}>
          <strong>{label}: </strong>
          {texts.map((text, index) => (
            <Tooltip key={index} title={`Type: ${label}`}>
              <Chip
                label={text}
                variant="outlined"
                style={{ margin: '2px' }}
              />
            </Tooltip>
          ))}
        </div>
      ))}
    </Stack>
  );
}

export default EntitiesDisplay;
