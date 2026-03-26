import { useState } from 'react';
import { Search, AlertTriangle, AlertCircle, Info, TrendingUp, TrendingDown, Zap, FileText } from 'lucide-react';

export default function Alerts({ data }) {
  const [search, setSearch] = useState('');
  
  if (!data) return <div className="p-8 animated-enter text-center">Loading Market Signals...</div>;

  const alerts = data.alerts || [];
  const sentimentChange = data.sentiment_change || {};
  const consumerAiInsight = data.consumer_insights?.consumer_ai_insight;

  // Search filter for alerts
  const filteredAlerts = alerts.filter(a => 
    a.message.toLowerCase().includes(search.toLowerCase()) || 
    a.brand.toLowerCase().includes(search.toLowerCase())
  );

  const getSeverityColor = (severity) => {
    switch (severity?.toUpperCase()) {
      case 'HIGH': return '#ef4444';
      case 'MEDIUM': return '#f59e0b';
      case 'LOW': return '#3b82f6';
      default: return '#10b981';
    }
  };

  const getAlertIcon = (type) => {
    switch (type) {
      case 'TREND_SPIKE': return <TrendingUp size={18} />;
      case 'TREND_DROP': return <TrendingDown size={18} />;
      case 'LOW_SENTIMENT': return <AlertCircle size={18} />;
      default: return <Zap size={18} />;
    }
  };

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
            className="text-accent-purple font-bold hover:underline cursor-pointer mx-1"
            title={source?.content ? `View Source: ${source.content.substring(0, 100)}...` : 'View Source'}
          >
            {part}
          </a>
        );
      }
      return part;
    });
  };

  return (
    <div className="animated-enter">
      <div className="page-header">
        <div>
          <h1 className="page-title">Insights & Alerts</h1>
          <p className="text-secondary mt-1">AI-generated market signals and narrative analysis.</p>
        </div>
        <div className="relative">
          <div style={{ position: 'relative' }}>
            <Search size={18} style={{ position: 'absolute', top: '10px', left: '12px', color: '#94a3b8' }} />
            <input 
              type="text" 
              className="glass-btn pl-10" 
              placeholder="Search signals..." 
              style={{ paddingLeft: '2.5rem', width: '250px', textAlign: 'left' }}
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        
        {/* Market Signals Column */}
        <div className="flex flex-col gap-4">
          <div className="glass-panel p-6 h-full">
            <h3 className="chart-card-title flex items-center gap-2 mb-6">
              <AlertTriangle className="text-warning" size={20} />
              Real-time Market Signals
            </h3>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {filteredAlerts.length > 0 ? (
                filteredAlerts.map((alert, i) => (
                  <div key={i} className="glass-panel p-5" style={{ 
                    background: `rgba(${alert.severity === 'HIGH' ? '239, 68, 68' : '59, 130, 246'}, 0.05)`, 
                    borderLeft: `4px solid ${getSeverityColor(alert.severity)}`,
                    transition: 'transform 0.2s ease'
                  }}>
                    <div className="flex justify-between items-start mb-2">
                       <div className="flex items-center gap-2 font-semibold capitalize text-lg" style={{ color: getSeverityColor(alert.severity) }}>
                         {getAlertIcon(alert.type)}
                         {alert.brand}
                       </div>
                       <span className="text-xs px-2 py-1 rounded-full" style={{ 
                         background: 'rgba(255,255,255,0.05)', 
                         color: '#94a3b8',
                         border: '1px solid rgba(255,255,255,0.1)'
                       }}>
                         {alert.severity}
                       </span>
                    </div>
                    <div className="text-text-primary text-sm leading-relaxed mb-3">{alert.message}</div>
                    <div className="text-xs text-secondary mt-2 opacity-60">
                      {new Date(alert.timestamp).toLocaleTimeString()} • AI Identified
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center p-8 text-secondary glass-panel">
                  No active high-severity signals detected.
                </div>
              )}
            </div>
          </div>
        </div>
        
        {/* Market Narrative Column */}
        <div className="flex flex-col gap-4">
          <div className="glass-panel p-6" style={{ flex: 1 }}>
            <h3 className="chart-card-title mb-6 flex items-center gap-2">
              <Info className="text-accent-purple" size={20} />
              AI Market Narrative
            </h3>
            
            {sentimentChange.explanation ? (
              <div className="flex flex-col gap-6">
                <div className="glass-panel p-5" style={{ background: 'rgba(139, 92, 246, 0.05)', borderLeft: '4px solid #8b5cf6' }}>
                  <div className="font-semibold text-accent-purple mb-3 text-lg flex items-center gap-2">
                    <Zap size={18} />
                    Market Sentiment {sentimentChange.direction}
                  </div>
                  <div className="text-text-primary text-sm leading-relaxed whitespace-pre-line mb-4">
                    {renderNarrativeWithLinks(sentimentChange.explanation)}
                  </div>
                </div>

                {data.risk_signals && (
                  <div className="glass-panel p-5" style={{ background: 'rgba(239, 68, 68, 0.03)', borderLeft: '4px solid #ef4444', marginTop: '-0.5rem' }}>
                    <div className="font-semibold text-danger mb-2 text-md flex items-center gap-2">
                      <AlertCircle size={16} />
                      Strategic Risk Analysis
                    </div>
                    <div className="text-secondary text-sm leading-relaxed whitespace-pre-line italic">
                      {renderNarrativeWithLinks(data.risk_signals)}
                    </div>
                  </div>
                )}

                {sentimentChange.top_reasons && (
                  <div className="flex flex-col gap-3">
                    <h4 className="text-sm font-bold text-secondary uppercase tracking-wider">Key Drivers</h4>
                    {sentimentChange.top_reasons.slice(1).map((reason, idx) => (
                      <div key={idx} className="glass-panel p-4 text-sm text-secondary leading-relaxed" style={{ background: 'rgba(255,255,255,0.02)' }}>
                        {reason}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center p-8 text-secondary">
                {consumerAiInsight || "Waiting for latest AI narrative generation..."}
              </div>
            )}
          </div>
        </div>
        
      </div>
    </div>
  );
}
