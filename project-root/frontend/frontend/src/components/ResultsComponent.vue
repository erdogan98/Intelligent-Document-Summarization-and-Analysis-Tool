<template>
  <div>
    <h2>Summary</h2>
    <p>{{ summary }}</p>

    <h2>Entities</h2>
    <ul>
      <li v-for="(entity, index) in entities" :key="index">
        {{ entity[0] }} - {{ entity[1] }}
      </li>
    </ul>

    <h2>Sentiment Analysis</h2>
    <p>Positive: {{ sentiment.pos }}</p>
    <p>Neutral: {{ sentiment.neu }}</p>
    <p>Negative: {{ sentiment.neg }}</p>
    <p>Compound: {{ sentiment.compound }}</p>
  </div>
</template>

<script>
export default {
  props: ['summary', 'entities', 'sentiment'],
};
</script>
