import React from 'react';
import { Box, Typography } from '@mui/material';

function Footer() {
  return (
    <Box component="footer" sx={{ p: 2, textAlign: 'center' }}>
      <Typography variant="body2" color="text.secondary">
        © {new Date().getFullYear()} Document Summarizer. All rights reserved.
      </Typography>
        Developed by Ed E. Kervanli
        <Typography variant="body3" color="text.thirdly">

        </Typography>
    </Box>
  );
}

export default Footer;
