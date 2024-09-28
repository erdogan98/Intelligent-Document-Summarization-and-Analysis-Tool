import React from 'react';
import { AppBar, Toolbar, Typography, IconButton } from '@mui/material';
import { WbSunny, Brightness2 } from '@mui/icons-material';
import { Link } from 'react-router-dom';

function Navbar({ toggleTheme, mode }) {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          component={Link}
          to="/"
          style={{ flexGrow: 1, textDecoration: 'none', color: 'inherit' }}
        >
          Document Summarizer
        </Typography>
        <IconButton color="inherit" onClick={toggleTheme}>
          {mode === 'light' ? <Brightness2 /> : <WbSunny />}
        </IconButton>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
