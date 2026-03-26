import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import { RefreshCw, AlertCircle } from 'lucide-react';

export default function DashboardLayout({ data, lastUpdated, isError, isSyncing, onRefresh }) {
  const formatTime = (date) => {
    if (!date) return 'Just now';
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  };

  return (
    <div className="app-container">
      <Sidebar data={data} />
      <main className="main-content">
        {isError && (
          <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', color: '#fca5a5', padding: '0.75rem 1rem', borderRadius: '8px', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <AlertCircle size={18} />
            <span>Connection to AI pipeline lost. Retrying automatically...</span>
          </div>
        )}
        
        <header className="flex justify-between items-center mb-8 pb-4 border-b border-white/10" style={{ display: 'flex', justifyContent: 'flex-end', paddingBottom: '1rem', borderBottom: '1px solid rgba(255,255,255,0.05)', marginBottom: '2rem' }}>
          <div className="flex items-center gap-4" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            
             <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(255,255,255,0.03)', padding: '0.4rem 0.8rem', borderRadius: '20px', border: '1px solid rgba(255,255,255,0.05)' }}>
               {isSyncing ? (
                 <RefreshCw size={14} className="text-secondary" style={{ animation: 'spin 1s linear infinite' }} />
               ) : (
                 <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: isError ? '#ef4444' : '#10b981', boxShadow: isError ? '0 0 8px #ef4444' : '0 0 8px #10b981' }}></div>
               )}
               <span className="text-sm text-secondary" style={{ fontSize: '0.8rem', color: '#94a3b8' }}>
                 {isError ? 'Disconnected' : `Live • Updated: ${formatTime(lastUpdated)}`}
               </span>
             <button 
                onClick={onRefresh} 
                disabled={isSyncing}
                className="glass-btn flex items-center gap-2"
                style={{ height: '32px', fontSize: '0.8rem', padding: '0 1rem' }}
                title="Force Refresh Data"
              >
               <RefreshCw size={14} className={isSyncing ? "animate-spin" : ""} />
               <span>Refresh</span>
             </button>
             </div>
             
             <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>

             <div className="text-sm text-secondary" style={{ display: 'none' }}>Updated Today</div>
          </div>
        </header>
        <Outlet />
      </main>
    </div>
  );
}
