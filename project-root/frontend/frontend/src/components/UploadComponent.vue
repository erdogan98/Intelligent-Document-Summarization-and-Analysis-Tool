<template>
  <div>
    <input type="file" @change="onFileChange" />
    <button @click="uploadFile">Upload</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFile: null,
    };
  },
  methods: {
    onFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    uploadFile() {
      const formData = new FormData();
      formData.append('file', this.selectedFile);

      axios.post('http://localhost:8000/process', formData)
        .then(response => {
          // Handle the response data
          this.$emit('results', response.data);
        })
        .catch(error => {
          console.error(error);
        });
    },
  },
};
</script>
