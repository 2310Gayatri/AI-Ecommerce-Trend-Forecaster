import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { TrendingUp, TrendingDown, MessageSquare, Activity, AlertCircle, FileText, Download, Zap, Search, Layers, Target } from 'lucide-react';
import AnimatedNumber from '../components/AnimatedNumber';

export default function Overview({ data }) {
  const [selectedBrand, setSelectedBrand] = useState('overall');
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    if (!data) return;

    if (selectedBrand === 'overall') {
      const forecast = data.forecast?.['30_day'] || [];
      const formatted = forecast.map((val, idx) => ({
        day: `Day ${idx + 1}`,
        sentiment: val,
      }));
      setChartData(formatted);
    } else {
      const brandForecast = data.forecast?.brand_forecast?.brand_forecasts?.find(f => f.brand === selectedBrand);
      if (brandForecast) {
        const forecast = brandForecast.forecasts['30_day'] || [];
        const formatted = forecast.map((val, idx) => ({
          day: `Day ${idx + 1}`,
          sentiment: val,
        }));
        setChartData(formatted);
      } else {
        setChartData([]);
      }
    }
  }, [data, selectedBrand]);

  if (!data) return <div className="p-8 animated-enter text-center">Loading Market Intelligence...</div>;

  // Helper to render narrative with clickable source links
  const renderNarrativeWithLinks = (text) => {
    if (!text) return null;
    
    // Match [Source X] or Source X
    const partRegex = /(\[?Source\s+\d+\]?)/gi;
    const parts = text.split(partRegex);
    
    return parts.map((part, i) => {
      const match = part.match(/Source\s+(\d+)/i);
      if (match) {
        const sourceId = parseInt(match[1]);
        const source = data.consumer_insights?.sources?.find(s => s.source_id === sourceId);
        
        return (
          <a 
            key={i}
            href={source?.url || '#'} 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-blue-400 font-bold hover:underline cursor-pointer mx-1"
            title={source?.content ? `View Source: ${source.content.substring(0, 100)}...` : 'View Source'}
          >
            {part}
          </a>
        );
      }
      return part;
    });
  };

  const handleExportCSV = () => {
    const { market_overview, brand_insights, consumer_insights, forecast, sentiment_change, alerts, topic_insights } = data;
    
    // Helper to escape CSV values
    const esc = (val) => `"${String(val).replace(/"/g, '""')}"`;

    const rows = [
      ['AI Ecommerce Trend Forecaster - Detailed Report'],
      [`Generated: ${new Date().toLocaleString()}`],
      [''],
      ['SECTION 1: MARKET OVERVIEW'],
      ['Trend Direction', market_overview?.trend_direction || 'N/A'],
      ['Trend Slope', market_overview?.trend_slope || '0'],
      ['Current Sentiment Score', market_overview?.current_sentiment || '0'],
      ['Volatility Index', market_overview?.volatility || '0'],
      [''],
      ['SECTION 2: AI MARKET NARRATIVE'],
      ['Direction', sentiment_change?.direction || 'N/A'],
      ['Explanation', esc(sentiment_change?.explanation || 'No narrative generated.')],
      [''],
      ['SECTION 3: BRAND PERFORMANCE'],
      ['Brand', 'Consumer Sentiment', 'Direction', 'Forecast Slope', 'Alert Count']
    ];

    const allBrandsSet = new Set();
    brand_insights?.brand_direction?.forEach(b => allBrandsSet.add(b.brand));
    consumer_insights?.brand_sentiment?.forEach(b => allBrandsSet.add(b.brand));
    forecast?.brand_forecast?.brand_forecasts?.forEach(b => allBrandsSet.add(b.brand));

    const sortedBrands = Array.from(allBrandsSet).sort();

    sortedBrands.forEach(brand => {
      const direction = brand_insights?.brand_direction?.find(d => d.brand === brand)?.direction || 'N/A';
      const sentimentData = consumer_insights?.brand_sentiment?.find(s => s.brand === brand);
      const sentiment = sentimentData ? sentimentData.final_consumer_sentiment.toFixed(4) : 'N/A';
      const forecastInfo = forecast?.brand_forecast?.brand_forecasts?.find(f => f.brand === brand);
      const slope = forecastInfo?.trend_slope !== undefined ? forecastInfo.trend_slope.toFixed(4) : 'N/A';
      const alertCount = (alerts || []).filter(a => a.brand.toLowerCase() === brand.toLowerCase()).length;

      rows.push([brand.toUpperCase(), sentiment, direction, slope, alertCount]);
    });

    rows.push(['']);
    rows.push(['SECTION 4: TOPIC INSIGHTS']);
    rows.push(['Fastest Rising Topic', topic_insights?.fastest_rising_topic || 'N/A']);
    rows.push(['Fastest Declining Topic', topic_insights?.fastest_declining_topic || 'N/A']);
    rows.push(['Top Keywords', esc(topic_insights?.top_topics?.join(', ') || 'N/A')]);

    const csvContent = rows.map(e => e.join(",")).join("\n");
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `market_detailed_report_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleDownloadPDF = () => {
    // This file is copied to public/ by vite.config.js
    // Adding a timestamp to bust the browser cache
    const pdfUrl = `/market_report.pdf?t=${new Date().getTime()}`;
    const a = document.createElement('a');
    a.href = pdfUrl;
    a.download = `Market_AI_Analysis_Report_${new Date().toISOString().split('T')[0]}.pdf`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const { market_overview, brand_insights } = data;
  const isPos = market_overview?.trend_slope > 0;

  return (
    <div className="animated-enter">
      <div className="page-header">
        <div>
          <h1 className="page-title">Market Overview</h1>
          <p className="text-secondary mt-1">Real-time analysis of ecommerce trends and consumer sentiment.</p>
        </div>
        <div className="page-actions">
          <select 
            className="glass-select"
            value={selectedBrand}
            onChange={e => setSelectedBrand(e.target.value)}
          >
            <option value="overall">All Brands (Market)</option>
            {brand_insights?.top_brands?.map(b => (
              <option key={b.brand} value={b.brand}>{b.brand.toUpperCase()}</option>
            ))}
          </select>
          <div className="flex gap-2">
            <button className="glass-btn flex items-center gap-2" onClick={handleExportCSV}>
              <Download size={16} /> Export CSV
            </button>
            <button className="glass-btn primary flex items-center gap-2" onClick={handleDownloadPDF}>
              <FileText size={16} /> Download PDF
            </button>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="glass-panel stat-card">
          <div className="stat-header">
            <span>Market Trend</span>
            <div className="stat-icon icon-blue">
              <Activity size={20} />
            </div>
          </div>
          <div className="stat-value">{market_overview?.trend_direction || 'Stable'}</div>
          <div className="stat-footer">
            <span className={isPos ? 'trend-up' : 'trend-down'}>
              <AnimatedNumber
                value={(market_overview?.trend_slope || 0) * 100}
                formatted={`${(market_overview?.trend_slope || 0) > 0 ? '+' : ''}${((market_overview?.trend_slope || 0) * 100).toFixed(1)}%`}
              />
            </span>
            <span className="text-secondary ml-1">slope intensity</span>
          </div>
        </div>

        <div className="glass-panel stat-card">
          <div className="stat-header">
            <span>Avg Consumer Sentiment</span>
            <div className="stat-icon icon-purple">
              <MessageSquare size={20} />
            </div>
          </div>
          <div className="stat-value">
            <AnimatedNumber
              value={market_overview?.current_sentiment || 0}
              formatted={(market_overview?.current_sentiment || 0).toFixed(3)}
            />
          </div>
          <div className="stat-footer">
            <span className="text-secondary">AI-calculated score from FinBERT</span>
          </div>
        </div>

        <div className="glass-panel stat-card">
          <div className="stat-header">
            <span>Market Volatility</span>
            <div className="stat-icon icon-red">
              <AlertCircle size={20} />
            </div>
          </div>
          <div className="stat-value">
            <AnimatedNumber
              value={market_overview?.volatility || 0}
              formatted={(market_overview?.volatility || 0).toFixed(2)}
            />
          </div>
          <div className="stat-footer text-secondary">
            Stability rating
          </div>
        </div>
        
        <div className="glass-panel stat-card">
          <div className="stat-header">
            <span>Top Performing Brand</span>
            <div className="stat-icon icon-green">
              <TrendingUp size={20} />
            </div>
          </div>
          <div className="stat-value capitalize">{brand_insights?.top_positive_brand || 'None'}</div>
          <div className="stat-footer text-secondary">
            Highest overall final consumer sentiment
          </div>
        </div>
      </div>

      {/* 30-Day Forward Sentiment Forecast (Existing) */}
      <div className="charts-grid" style={{ gridTemplateColumns: '1fr' }}>
        <div className="glass-panel chart-card" style={{ marginBottom: '1.5rem' }}>
          <h3 className="chart-card-title">30-Day Forward Sentiment Forecast</h3>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="day" stroke="#94a3b8" tick={{ fill: '#94a3b8' }} tickLine={false} axisLine={false} />
                <YAxis stroke="#94a3b8" tick={{ fill: '#94a3b8' }} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'rgba(20, 20, 30, 0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', color: '#fff' }}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="sentiment" 
                  name="Sentiment Score"
                  stroke="#8b5cf6" 
                  strokeWidth={3} 
                  dot={false}
                  activeDot={{ r: 6, fill: '#8b5cf6', stroke: '#14141e', strokeWidth: 2 }} 
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* New: Recent Insights & Alerts Preview */}
      <div className="glass-panel p-6 shadow-lg">
        <h3 className="chart-card-title flex items-center gap-2 mb-4">
          <AlertCircle className="text-warning" size={20} />
          Market Signals & Insights
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
          <div className="flex flex-col gap-3">
             <h4 className="text-xs font-bold text-secondary uppercase tracking-wider mb-1">Recent Alerts</h4>
             {(data.alerts || []).slice(0, 3).map((alert, i) => (
                <div key={i} className="glass-panel p-3 text-sm flex items-center gap-3" style={{ background: 'rgba(255,255,255,0.02)', borderLeft: `3px solid ${alert.severity === 'HIGH' ? '#ef4444' : '#3b82f6'}` }}>
                   <div style={{ fontWeight: 600, color: alert.severity === 'HIGH' ? '#ef4444' : '#3b82f6', textTransform: 'uppercase', fontSize: '10px', width: '45px' }}>{alert.severity}</div>
                   <div className="text-text-primary flex-1">{alert.message}</div>
                </div>
             ))}
             {(data.alerts || []).length === 0 && <div className="text-secondary text-sm italic">No active alerts.</div>}
          </div>
          <div className="flex flex-col gap-3">
              <h4 className="text-xs font-bold text-secondary uppercase tracking-wider mb-1">Latest Narrative</h4>
              {data.sentiment_change?.explanation ? (
                <div className="text-sm text-secondary leading-relaxed bg-blue-500/5 p-4 rounded-lg border border-blue-500/10" style={{ maxHeight: '120px', overflow: 'hidden', display: '-webkit-box', WebkitLineClamp: 4, WebkitBoxOrient: 'vertical' }}>
                  {renderNarrativeWithLinks(data.sentiment_change.explanation)}
                </div>
              ) : (
                <div className="text-sm text-secondary italic opacity-50">
                  {renderNarrativeWithLinks(data.consumer_insights?.consumer_ai_insight)}
                </div>
              )}
          </div>
        </div>
      </div>
    </div>
  );
}
