// src/components/SentimentChart.js
import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';

function SentimentChart({ sentiment }) {
  const data = [
    { name: 'Positive', value: sentiment.pos },
    { name: 'Neutral', value: sentiment.neu },
    { name: 'Negative', value: sentiment.neg },
  ];

  const COLORS = ['#00C49F', '#FFBB28', '#FF8042'];

  return (
    <PieChart width={300} height={250}>
      <Pie
        dataKey="value"
        data={data}
        cx="50%"
        cy="50%"
        outerRadius={80}
        label
      >
        {data.map((entry, index) => (
          <Cell key={`cell-${index}`} fill={COLORS[index]} />
        ))}
      </Pie>
      <Tooltip />
      <Legend />
    </PieChart>
  );
}

export default SentimentChart;
