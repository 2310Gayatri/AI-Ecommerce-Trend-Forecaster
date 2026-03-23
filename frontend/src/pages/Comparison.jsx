import { useState, useMemo, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export default function Comparison({ data }) {
  const [brandA, setBrandA] = useState('');
  const [brandB, setBrandB] = useState('');
  
  const allBrands = useMemo(() => {
    if (!data?.forecast?.brand_forecast?.brand_forecasts) return [];
    return data.forecast.brand_forecast.brand_forecasts
      .filter(b => b.forecasts && b.forecasts['30_day'] && b.forecasts['30_day'].length > 0)
      .map(b => b.brand)
      .sort();
  }, [data]);

  useEffect(() => {
    if (allBrands.length >= 2 && !brandA && !brandB) {
      setBrandA(allBrands[0]);
      setBrandB(allBrands[1]);
    } else if (allBrands.length === 1 && !brandA && !brandB) {
      setBrandA(allBrands[0]);
      setBrandB(allBrands[0]);
    }
  }, [allBrands, brandA, brandB]);

  const comparisonData = useMemo(() => {
    if (!data) return [];
    const forecastA = data.forecast?.brand_forecast?.brand_forecasts?.find(f => f.brand === brandA)?.forecasts['30_day'] || [];
    const forecastB = data.forecast?.brand_forecast?.brand_forecasts?.find(f => f.brand === brandB)?.forecasts['30_day'] || [];
    
    const length = Math.max(forecastA.length, forecastB.length);
    const result = [];
    
    for (let i = 0; i < length; i++) {
        result.push({
            day: `Day ${i + 1}`,
            [brandA]: forecastA[i] !== undefined ? forecastA[i] : null,
            [brandB]: forecastB[i] !== undefined ? forecastB[i] : null,
        });
    }
    return result;
  }, [data, brandA, brandB]);
  
  if (!data) return <div className="p-8 animated-enter">Loading...</div>;

  return (
    <div className="animated-enter">
      <div className="page-header">
        <div>
          <h1 className="page-title">Brand Comparison</h1>
          <p className="text-secondary mt-1">Cross-reference 30-day forecast sentiment trends between competitors.</p>
        </div>
        <div className="page-actions" style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <span className="text-secondary">Compare:</span>
            <select className="glass-select capitalize" value={brandA} onChange={e => setBrandA(e.target.value)}>
                {allBrands.map(b => (
                    <option key={b} value={b}>{b}</option>
                ))}
            </select>
            <span className="text-secondary">vs</span>
            <select className="glass-select capitalize" value={brandB} onChange={e => setBrandB(e.target.value)}>
                {allBrands.map(b => (
                    <option key={b} value={b}>{b}</option>
                ))}
            </select>
        </div>
      </div>

      <div className="glass-panel chart-card" style={{ height: '500px' }}>
          <h3 className="chart-card-title capitalize">{brandA} vs {brandB} Forecast Sentiment</h3>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={comparisonData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="day" stroke="#94a3b8" tick={{ fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <YAxis stroke="#94a3b8" tick={{ fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'rgba(20, 20, 30, 0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} 
                />
                <Legend iconType="circle" />
                <Line 
                  type="monotone" 
                  dataKey={brandA} 
                  stroke="#3b82f6" 
                  strokeWidth={3} 
                  dot={false}
                  activeDot={{ r: 6 }}
                />
                <Line 
                  type="monotone" 
                  dataKey={brandB} 
                  stroke="#ec4899" 
                  strokeWidth={3} 
                  dot={false}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
      </div>
    </div>
  );
}
