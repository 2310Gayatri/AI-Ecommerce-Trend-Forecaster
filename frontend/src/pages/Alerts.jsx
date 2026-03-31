import { useState } from 'react';
import { Search, AlertTriangle, AlertCircle, Info, ExternalLink } from 'lucide-react';

export default function Alerts({ data }) {
  const [search, setSearch] = useState('');
  
  if (!data) return <div className="p-8 animated-enter">Loading...</div>;

  const insightsArray = data.consumer_insights?.consumer_ai_insight || [];
  // The structure is ["LLM response skipped...", [ { source_id: 1, content: "..." }, ... ]]
  const comments = Array.isArray(insightsArray) && insightsArray.length > 1 && Array.isArray(insightsArray[1]) 
    ? insightsArray[1] 
    : [];
    
  // Simple search filter
  const filteredComments = comments.filter(c => c.content.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="animated-enter">
      <div className="page-header">
        <div>
          <h1 className="page-title">Insights & Alerts</h1>
          <p className="text-secondary mt-1">AI-generated signals and extracted consumer commentary.</p>
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        
        {/* Alerts Column */}
        <div className="flex flex-col gap-4">
          <div className="glass-panel p-6 h-full">
            <h3 className="chart-card-title flex items-center gap-2 mb-6">
              <AlertTriangle className="text-warning" size={20} />
              Recent Market Signals
            </h3>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {data.brand_insights?.brand_direction?.filter(b => b.direction === 'Falling').slice(0, 1).map((b, i) => (
                <div key={i} className="glass-panel p-5" style={{ background: 'rgba(239, 68, 68, 0.05)', borderLeft: '4px solid #ef4444' }}>
                  <div className="font-semibold capitalize text-danger mb-2 text-lg">{b.brand} Momentum Dropping</div>
                  <div className="text-secondary text-sm leading-relaxed">FinBERT analysis detects increased negative sentiment vectors causing a downward trajectory.</div>
                </div>
              ))}
              
              {(!data.brand_insights?.brand_direction || data.brand_insights.brand_direction.filter(b => b.direction === 'Falling').length === 0) && (
                <div className="glass-panel p-5" style={{ background: 'rgba(59, 130, 246, 0.05)', borderLeft: '4px solid #3b82f6' }}>
                    <div className="font-semibold capitalize text-accent-blue mb-2 text-lg">Topic Breakout: {data.topic_insights?.fastest_rising_topic}</div>
                    <div className="text-secondary text-sm leading-relaxed">This topic has gained massive engagement across social and news channels recently.</div>
                </div>
              )}
            </div>
          </div>
        </div>
        
        {/* Insights / RAG Q&A Column */}
        <div className="glass-panel p-6" style={{ display: 'flex', flexDirection: 'column' }}>
          <div className="flex justify-between items-center mb-6">
            <h3 className="chart-card-title mb-0 flex items-center gap-2">
              <Info className="text-accent-purple" size={20} />
              Consumer Commentary Extractor
            </h3>
            
            <div className="relative">
              <div style={{ position: 'relative' }}>
                <Search size={18} style={{ position: 'absolute', top: '10px', left: '12px', color: '#94a3b8' }} />
                <input 
                  type="text" 
                  className="glass-btn pl-10" 
                  placeholder="Search comments..." 
                  style={{ paddingLeft: '2.5rem', width: '250px', textAlign: 'left' }}
                  value={search}
                  onChange={e => setSearch(e.target.value)}
                />
              </div>
            </div>
          </div>
          
          <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem', paddingRight: '1rem' }}>
            {filteredComments.map((comment, idx) => {
              // Parse out simple info if structured like "\nBrand: meesho\nTopic: funding\nSentiment: neutral\nNews: ..."
              const lines = comment.content.split('\n').filter(Boolean);
              
              return (
                <div key={idx} className="glass-panel" style={{ padding: '1.5rem', background: 'rgba(20, 20, 30, 0.4)', display: 'flex', flexDirection: 'column', gap: '0.75rem', borderLeft: '3px solid #6366f1' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.25rem' }}>
                    <div style={{ display: 'flex', gap: '0.5rem' }}>
                       <span className="text-xs px-2 py-1 rounded bg-blue-500/20 text-blue-400 capitalize inline-block" style={{ background: 'rgba(99, 102, 241, 0.15)', color: '#818cf8', padding: '0.25rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 'bold' }}>Source {comment.source_id}</span>
                    </div>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    {lines.map((line, lIdx) => {
                      const colonIndex = line.indexOf(':');
                      if (colonIndex > -1) {
                        const key = line.substring(0, colonIndex).trim();
                        const value = line.substring(colonIndex + 1).trim();
                        
                        let valueClassName = "text-text-primary";
                        let valueBadge = null;
                        
                        // Special styling for Sentiment and specific keys
                        if (key.toLowerCase().includes('sentiment')) {
                          if (value.toLowerCase().includes('positive')) {
                            valueClassName = "text-success font-medium";
                            valueBadge = <span style={{display: 'inline-block', width: '8px', height: '8px', borderRadius: '50%', background: '#10b981', marginRight: '6px'}}></span>;
                          } else if (value.toLowerCase().includes('negative')) {
                            valueClassName = "text-danger font-medium";
                            valueBadge = <span style={{display: 'inline-block', width: '8px', height: '8px', borderRadius: '50%', background: '#ef4444', marginRight: '6px'}}></span>;
                          } else {
                            valueClassName = "text-warning font-medium";
                            valueBadge = <span style={{display: 'inline-block', width: '8px', height: '8px', borderRadius: '50%', background: '#f59e0b', marginRight: '6px'}}></span>;
                          }
                        } else if (key.toLowerCase().includes('brand')) {
                          valueClassName = "text-accent-blue font-semibold capitalize";
                        }
                        
                        return (
                          <div key={lIdx} style={{ fontSize: '0.875rem', lineHeight: '1.6', display: 'flex', alignItems: 'flex-start' }}>
                            <span style={{ fontWeight: 600, color: '#94a3b8', width: '85px', flexShrink: 0 }}>{key}</span>
                            <span className={valueClassName} style={{ flex: 1, display: 'flex', alignItems: 'center' }}>
                              {valueBadge}{value}
                            </span>
                          </div>
                        );
                      }
                      
                      // Fallback for lines without colon
                      return (
                        <div key={lIdx} className="text-text-primary text-sm leading-relaxed whitespace-pre-line mt-1">
                          {line}
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
            
            {filteredComments.length === 0 && (
              <div className="text-center p-8 text-secondary">
                No matching commentary found for "{search}"
              </div>
            )}
          </div>
        </div>
        
      </div>
    </div>
  );
}
