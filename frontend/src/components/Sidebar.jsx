import { NavLink } from 'react-router-dom';
import { Home, BarChart2, TrendingUp, Bell } from 'lucide-react';

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <TrendingUp size={24} />
        <span>Market Forecaster</span>
      </div>
      
      <nav>
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
      </nav>
    </aside>
  );
}
