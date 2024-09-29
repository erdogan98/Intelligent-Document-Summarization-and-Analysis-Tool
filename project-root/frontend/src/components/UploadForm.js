import React, { useState } from 'react';
import axios from 'axios';
import { Button, TextField, Box, CircularProgress, Snackbar, Alert } from '@mui/material';

function UploadForm({ setResults }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);

    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/process', formData, {
        headers: {
          'Content-Type': 'aaplication/json',
        },
      });
      setResults(response.data);
      setSnackbar({ open: true, message: 'File processed successfully!', severity: 'success' });
    } catch (error) {
      console.error('Error uploading file:', error);
      setSnackbar({ open: true, message: 'Error processing file.', severity: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 4 }}>
      <TextField type="file" onChange={handleFileChange} fullWidth />
      <Button type="submit" variant="contained" color="primary" disabled={loading} sx={{ mt: 2 }}>
        Upload and Process
      </Button>
      {loading && <CircularProgress sx={{ mt: 2 }} />}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}

export default UploadForm;
