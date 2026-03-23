import { useState, useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function Topics({ data }) {
  if (!data) return <div className="p-8 animated-enter">Loading...</div>;

  const { topic_insights, consumer_insights } = data;

  const distributionData = useMemo(() => {
    if (!consumer_insights?.sentiment_distribution) return [];
    return [
      { name: 'Positive', value: consumer_insights.sentiment_distribution.positive, color: '#10b981' },
      { name: 'Neutral', value: consumer_insights.sentiment_distribution.neutral, color: '#e2e8f0' },
      { name: 'Negative', value: consumer_insights.sentiment_distribution.negative, color: '#ef4444' }
    ];
  }, [consumer_insights]);

  // For demonstration, map the top_topics strings to some mock volume data since it isn't in JSON directly.
  const topicsData = useMemo(() => {
    if (!topic_insights?.top_topics) return [];
    const counts = [120, 85, 45, 30, 20];
    return topic_insights.top_topics.map((t, i) => ({
      topic: t,
      volume: counts[i] || 10
    }));
  }, [topic_insights]);

  return (
    <div className="animated-enter">
      <div className="page-header">
        <div>
          <h1 className="page-title">Market Topics & Sentiments</h1>
          <p className="text-secondary mt-1">LLM extracted discussion points across news & consumer data.</p>
        </div>
      </div>

      <div className="charts-grid" style={{ gridTemplateColumns: '2fr 1fr' }}>
        {/* Main Topics Bar Chart */}
        <div className="glass-panel chart-card">
          <h3 className="chart-card-title">Top Extract Topics by Volume</h3>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={topicsData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="topic" stroke="#94a3b8" tick={{ fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <YAxis stroke="#94a3b8" tick={{ fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <Tooltip 
                  cursor={{ fill: 'rgba(255,255,255,0.05)' }} 
                  contentStyle={{ backgroundColor: 'rgba(20, 20, 30, 0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} 
                />
                <Bar dataKey="volume" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Sentiment Distribution Pie/Bar */}
        <div className="glass-panel chart-card">
          <h3 className="chart-card-title">Sentiment Distribution</h3>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={distributionData} layout="vertical" margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" horizontal={false} />
                <XAxis type="number" stroke="#94a3b8" tick={{ fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <YAxis dataKey="name" type="category" stroke="#94a3b8" tick={{ fill: '#94a3b8' }} axisLine={false} tickLine={false} width={70} />
                <Tooltip 
                  cursor={{ fill: 'rgba(255,255,255,0.05)' }} 
                  contentStyle={{ backgroundColor: 'rgba(20, 20, 30, 0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} 
                />
                <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                  {distributionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Featured Trends Section */}
      <h3 className="chart-card-title mt-8 mb-4">Topic Momentum Highlights</h3>
      <div className="stats-grid" style={{ gridTemplateColumns: '1fr 1fr' }}>
        <div className="glass-panel stat-card border-green-500/30">
          <div className="stat-header">
            <span>Fastest Rising Topic</span>
            <span className="text-success text-lg">↑</span>
          </div>
          <div className="stat-value capitalize">{topic_insights?.fastest_rising_topic}</div>
        </div>

        <div className="glass-panel stat-card border-red-500/30">
          <div className="stat-header">
            <span>Fastest Declining Topic</span>
            <span className="text-danger text-lg">↓</span>
          </div>
          <div className="stat-value capitalize text-text-secondary">{topic_insights?.fastest_declining_topic}</div>
        </div>
      </div>
    </div>
  );
}
