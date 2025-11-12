import React from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

// Coral Health Bar Chart
export const CoralHealthChart = () => {
  const data = [
    { name: 'Healthy', value: 65 },
    { name: 'Stressed', value: 20 },
    { name: 'Bleached', value: 15 }
  ];

  return (
    <ResponsiveContainer width="100%" height={180}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#0a2f4a" />
        <XAxis dataKey="name" stroke="#90e0ef" style={{ fontSize: '11px' }} />
        <YAxis stroke="#90e0ef" style={{ fontSize: '11px' }} />
        <Tooltip 
          contentStyle={{ 
            backgroundColor: '#061a2c', 
            border: 'none', 
            borderRadius: '8px',
            color: '#e3f6fc'
          }} 
        />
        <Bar dataKey="value" fill="#00b4d8" radius={[8, 8, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
};

// Risk Forecast Line Chart
export const RiskForecastChart = () => {
  const data = [
    { time: '00:00', risk: 20 },
    { time: '04:00', risk: 35 },
    { time: '08:00', risk: 45 },
    { time: '12:00', risk: 60 },
    { time: '16:00', risk: 55 },
    { time: '20:00', risk: 40 },
    { time: '24:00', risk: 30 }
  ];

  return (
    <ResponsiveContainer width="100%" height={180}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#0a2f4a" />
        <XAxis dataKey="time" stroke="#90e0ef" style={{ fontSize: '11px' }} />
        <YAxis stroke="#90e0ef" style={{ fontSize: '11px' }} />
        <Tooltip 
          contentStyle={{ 
            backgroundColor: '#061a2c', 
            border: 'none', 
            borderRadius: '8px',
            color: '#e3f6fc'
          }} 
        />
        <Line 
          type="monotone" 
          dataKey="risk" 
          stroke="#ff6b35" 
          strokeWidth={2.5} 
          dot={{ fill: '#ff6b35', r: 4 }}
          activeDot={{ r: 7 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

// MEHI Index Donut Chart
export const MEHIChart = () => {
  const data = [
    { name: 'Water Quality', value: 30, color: '#00b4d8' },
    { name: 'Biodiversity', value: 25, color: '#0077b6' },
    { name: 'Habitat Integrity', value: 20, color: '#023e8a' },
    { name: 'Pollution Load', value: 15, color: '#ff6b35' },
    { name: 'Climate Resilience', value: 10, color: '#ffd60a' }
  ];

  return (
    <ResponsiveContainer width="100%" height={180}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={45}
          outerRadius={70}
          paddingAngle={5}
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color} />
          ))}
        </Pie>
        <Tooltip 
          contentStyle={{ 
            backgroundColor: '#061a2c', 
            border: 'none', 
            borderRadius: '8px',
            color: '#e3f6fc'
          }} 
        />
      </PieChart>
    </ResponsiveContainer>
  );
};