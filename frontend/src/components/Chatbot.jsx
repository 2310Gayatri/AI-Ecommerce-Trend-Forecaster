import { useState, useRef, useEffect } from 'react';
import './Chatbot.css';

export default function Chatbot({ data }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { text: "Hi! I'm your Market Intelligence Bot. Ask me about trends, specific brands, or recent alerts!", isBot: true }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const getBotResponse = (userMessage) => {
    const lower = userMessage.toLowerCase();
    
    if (!data) return "I don't have access to the market engine data right now. Please wait for the dashboard to load.";

    // 1. Market Overview & Trends
    if (lower.includes('trend') || lower.includes('market') || lower.includes('overall')) {
      const direction = data.market_overview?.trend_direction || 'Stable';
      const sentiment = data.market_overview?.current_sentiment?.toFixed(3);
      const narrative = data.sentiment_change?.explanation ? `\n\nAI Narrative: ${data.sentiment_change.explanation.substring(0, 150)}...` : '';
      return `The overall market is currently ${direction} with a sentiment score of ${sentiment}.${narrative}`;
    }

    // 2. Specific Brand Queries
    const brands = data.brand_insights?.brand_direction?.map(b => b.brand.toLowerCase()) || [];
    const foundBrand = brands.find(b => lower.includes(b));
    
    if (foundBrand) {
      const directionInfo = data.brand_insights.brand_direction.find(b => b.brand.toLowerCase() === foundBrand);
      const forecastInfo = data.forecast?.brand_forecast?.brand_forecasts?.find(f => f.brand.toLowerCase() === foundBrand);
      const trendScore = data.brand_insights?.top_brands?.find(b => b.brand.toLowerCase() === foundBrand)?.final_trend_score;
      
      let response = `Analysis for **${foundBrand.toUpperCase()}**:\n`;
      response += `• Direction: ${directionInfo?.direction || 'N/A'}\n`;
      if (trendScore) response += `• Current Trend Score: ${trendScore.toFixed(3)}\n`;
      if (forecastInfo) response += `• Forecast: Predicted to be ${forecastInfo.trend_direction} over the next 30 days.`;
      
      return response;
    }

    // 3. Alerts & Signals
    if (lower.includes('alert') || lower.includes('warning') || lower.includes('signal') || lower.includes('risk')) {
      const alerts = data.alerts || [];
      if (alerts.length > 0) {
        const topAlert = alerts[0];
        return `⚠️ **Active Alert**: ${topAlert.message} (${topAlert.severity} priority for ${topAlert.brand}).\n\nStrategy: ${data.risk_signals ? data.risk_signals.substring(0, 200) + '...' : 'Monitor for further volatility.'}`;
      }
      return "Current market signals are stable. No high-severity alerts detected in the last cycle.";
    }

    // 4. Topics & Categories
    if (lower.includes('topic') || lower.includes('category') || lower.includes('news')) {
      const topTopics = data.topic_insights?.top_topics || [];
      const rising = data.topic_insights?.fastest_rising_topic;
      return `The hottest topics right now are: ${topTopics.join(', ')}.\n\n**${rising}** is the fastest growing topic in the current news cycle.`;
    }

    // 5. Forecast specific
    if (lower.includes('forecast') || lower.includes('future') || lower.includes('predict')) {
       const marketForecast = data.forecast?.['7_day'] || [];
       const direction = marketForecast[marketForecast.length - 1] > marketForecast[0] ? 'Upward' : 'Downward';
       return `My 7-day forecast suggests a general ${direction} movement for the overall market sentiment.`;
    }

    return "I can help with brand analysis, market trends, alerts, and hot topics. Try asking 'How is Flipkart doing?' or 'What are the current alerts?'";
  };

  const handleSend = (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isTyping) return;

    const userMessage = inputValue.trim();
    setMessages(prev => [...prev, { text: userMessage, isBot: false }]);
    setInputValue('');
    setIsTyping(true);

    // Simulate AI thinking
    setTimeout(() => {
      const botResponse = getBotResponse(userMessage);
      setMessages(prev => [...prev, { text: botResponse, isBot: true }]);
      setIsTyping(false);
    }, 800);
  };

  return (
    <>
      <button 
        className={`chatbot-toggle-btn ${isOpen ? 'open' : ''}`} 
        onClick={() => setIsOpen(!isOpen)}
        title="Market Assistant"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            {isOpen ? (
                <path d="M18 6L6 18M6 6l12 12" />
            ) : (
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
            )}
        </svg>
      </button>

      {isOpen && (
        <div className="chatbot-window glass-panel animated-enter">
          <div className="chatbot-header">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-success animate-pulse"></div>
              <h3 className="m-0 text-sm font-bold uppercase tracking-wider">Market Intelligence Hub</h3>
            </div>
            <button className="text-secondary hover:text-white" onClick={() => setIsOpen(false)}>
               <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 6L6 18M6 6l12 12"/></svg>
            </button>
          </div>
          <div className="chatbot-messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={`chatbot-message ${msg.isBot ? 'bot text-sm' : 'user text-sm'}`} style={{ whiteSpace: 'pre-line' }}>
                {msg.text}
              </div>
            ))}
            {isTyping && (
              <div className="chatbot-message bot text-secondary text-xs italic bg-transparent border-none">
                AI is analyzing dashboard data...
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <form className="chatbot-input-area" onSubmit={handleSend}>
            <input 
              type="text" 
              className="chatbot-input" 
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask about brands, trends, alerts..."
              autoFocus
            />
            <button type="submit" className="chatbot-send-btn flex items-center justify-center p-2 rounded-lg bg-accent-blue/10 hover:bg-accent-blue/20 transition-colors" disabled={!inputValue.trim() || isTyping}>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-accent-blue"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
            </button>
          </form>
        </div>
      )}
    </>
  );
}
