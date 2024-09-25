<template>
  <div id="app">
    <upload-component @results="handleResults"></upload-component>
    <results-component
      v-if="results"
      :summary="results.summary"
      :entities="results.entities"
      :sentiment="results.sentiment"
    ></results-component>
  </div>
</template>

<script>
import UploadComponent from './components/UploadComponent.vue';
import ResultsComponent from './components/ResultsComponent.vue';

export default {
  components: {
    UploadComponent,
    ResultsComponent,
  },
  data() {
    return {
      results: null,
    };
  },
  methods: {
    handleResults(data) {
      this.results = data;
    },
  },
};
</script>
