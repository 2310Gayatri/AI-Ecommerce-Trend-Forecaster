import { NavLink } from 'react-router-dom';
import { Home, BarChart2, TrendingUp, Bell, ExternalLink, Zap, FileText } from 'lucide-react';

export default function Sidebar({ data }) {
  const sources = data?.consumer_insights?.sources || [];

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <TrendingUp size={24} />
        <span>Market Forecaster</span>
      </div>
      
      <nav className="flex-1">
        <NavLink to="/" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <Home size={20} />
          <span>Overview</span>
        </NavLink>
        
        <NavLink to="/topics" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <BarChart2 size={20} />
          <span>Topics & Trends</span>
        </NavLink>
        
        <NavLink to="/comparison" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <TrendingUp size={20} />
          <span>Brand Comparison</span>
        </NavLink>
        
        <NavLink to="/alerts" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <Bell size={20} />
          <span>Insights & Alerts</span>
        </NavLink>
        
        <NavLink to="/sources" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <FileText size={20} />
          <span>Research Sources & Reference</span>
        </NavLink>
      </nav>
    </aside>
  );
}
