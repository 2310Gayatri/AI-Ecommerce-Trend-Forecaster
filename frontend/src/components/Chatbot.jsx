import { useState, useRef, useEffect } from 'react';
import './Chatbot.css';

export default function Chatbot({ data }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { text: "Hi! Ask me anything about the market trends or specific brands.", isBot: true }
  ]);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMessage = inputValue.trim();
    setMessages(prev => [...prev, { text: userMessage, isBot: false }]);
    setInputValue('');

    // Basic bot logic
    setTimeout(() => {
      let botResponse = "I'm not sure about that. Try asking about a specific brand or trending topic!";
      const lower = userMessage.toLowerCase();
      
      if (!data) {
          botResponse = "I don't have enough data loaded right now.";
      } else if (lower.includes('trend') || lower.includes('market')) {
        botResponse = `The market is currently looking ${data.market_overview?.trend_direction || 'stable'} with a sentiment score of ${data.market_overview?.current_sentiment?.toFixed(2) || 'N/A'}.`;
      } else if (lower.includes('top brand') || lower.includes('best brand')) {
        botResponse = `The top positive brand right now is ${data.brand_insights?.top_positive_brand}, while the most volatile is ${data.brand_insights?.most_volatile_brand}.`;
      } else if (lower.includes('alert') || lower.includes('warning') || lower.includes('signal')) {
        const fallingBrands = data.brand_insights?.brand_direction?.filter(b => b.direction === 'Falling') || [];
        if (fallingBrands.length > 0) {
          botResponse = `Recent alert: ${fallingBrands[0].brand} Momentum Dropping. FinBERT analysis detects increased negative sentiment vectors causing a downward trajectory.`;
        } else {
          botResponse = `Recent alert: Topic Breakout for ${data.topic_insights?.fastest_rising_topic}. This topic has gained massive engagement recently.`;
        }
      } else {
          // Check if asked about a specific brand
          const brands = data.brand_insights?.top_brands?.map(b => b.brand) || [];
          const foundBrand = brands.find(b => lower.includes(b));
          
          // Setup RAG data (Consumer Commentary)
          const insightsArray = data.consumer_insights?.consumer_ai_insight || [];
          const comments = Array.isArray(insightsArray) && insightsArray.length > 1 && Array.isArray(insightsArray[1]) 
            ? insightsArray[1] 
            : [];
            
          // Get search terms
          const searchTerms = lower.split(/\s+/).filter(w => w.length > 3);
          
          if (foundBrand) {
              const brandData = data.brand_insights?.top_brands.find(b => b.brand === foundBrand);
              let response = `${foundBrand} currently has a trend score of ${brandData?.final_trend_score?.toFixed(2) || 'N/A'}.`;
              
              const brandRagMatches = comments.filter(c => c.content.toLowerCase().includes(foundBrand.toLowerCase()));
              if (brandRagMatches.length > 0) {
                  // Format RAG content slightly
                  const ragContent = brandRagMatches[0].content.split('\n').filter(line => !!line && !line.toLowerCase().includes('brand:')).join('\n');
                  response += `\n\nInsights from RAG data:\n${ragContent}`;
              }
              botResponse = response;
          } else {
              // Try to find any RAG match for user keywords
              const ragMatches = comments.filter(c => searchTerms.some(term => c.content.toLowerCase().includes(term)));
              if (ragMatches.length > 0) {
                  botResponse = `Here's what I found in the market RAG data:\n\n${ragMatches[0].content.trim()}`;
              }
          }
      }

      setMessages(prev => [...prev, { text: botResponse, isBot: true }]);
    }, 600);
  };

  return (
    <>
      <button 
        className={`chatbot-toggle-btn ${isOpen ? 'open' : ''}`} 
        onClick={() => setIsOpen(!isOpen)}
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
            <h3>Market Assistant</h3>
          </div>
          <div className="chatbot-messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={`chatbot-message ${msg.isBot ? 'bot' : 'user'}`}>
                {msg.text}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          <form className="chatbot-input-area" onSubmit={handleSend}>
            <input 
              type="text" 
              className="glass-select chatbot-input" 
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask a question..."
            />
            <button type="submit" className="glass-btn primary chatbot-send-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
            </button>
          </form>
        </div>
      )}
    </>
  );
}
