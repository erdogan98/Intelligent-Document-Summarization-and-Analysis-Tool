import { useState } from 'react';
import axios from 'axios';
import { Button, TextField } from '@mui/material';

function UploadForm({ setResults }) {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://localhost:8000/process', formData);
      setResults(response.data);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <TextField type="file" onChange={handleFileChange} fullWidth />
      <Button type="submit" variant="contained" color="primary">
        Upload and Process
      </Button>
    </form>
  );
}

export default UploadForm;
