import React, { useState } from 'react';
import axios from 'axios';
import { Button, TextField, Box, CircularProgress, Snackbar, Alert,Typography } from '@mui/material';

function TextInputForm({ setResults }) {
    const [inputText, setInputText] = useState('');
    const [loading, setLoading] = useState(false);
    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

    const handleChange = (event) => {
        setInputText(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!inputText.trim()) return;

        const payload = { text: inputText };

        setLoading(true);
        try {
            const response = await axios.post('http://localhost:8000/process_text', payload, {
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            setResults(response.data);
            setSnackbar({ open: true, message: 'Text processed successfully!', severity: 'success' });
        } catch (error) {
            console.error('Error processing text:', error);
            setSnackbar({ open: true, message: 'Error processing text.', severity: 'error' });
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 4 }}>
            <TextField
                label="Enter Text"
                multiline
                rows={6}
                value={inputText}
                onChange={handleChange}
                fullWidth
                variant="outlined"
            />

            {/* Character Count Display */}
            <Typography variant="body2" color="textSecondary" sx={{ mt: 1, textAlign: 'right' }}>
                Characters: {inputText.length}
            </Typography>

            <Button type="submit" variant="contained" color="secondary" disabled={loading} sx={{ mt: 2 }}>
                Submit Text
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

export default TextInputForm;
