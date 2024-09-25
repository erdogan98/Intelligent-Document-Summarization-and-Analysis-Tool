// src/theme.js
import { createTheme } from '@mui/material/styles';

const theme = (mode) =>
  createTheme({
    palette: {
      mode: mode,
      primary: {
        main: '#1976d2',
      },
      secondary: {
        main: '#ff4081',
      },
    },
  });

export default theme;
