import React, { useState, useEffect } from 'react';
import { DataTable } from './DataTable';
import { RecordDrawer } from './RecordDrawer';
import { NormalizedRecord } from '../types';

const API_BASE = 'https://terrasync-backend-nsul.onrender.com/api';

export const Dashboard: React.FC = () => {
  const [records, setRecords] = useState<NormalizedRecord[]>([]);
  const [selectedRecord, setSelectedRecord] = useState<NormalizedRecord | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchRecords = async () => {
    try {
      const res = await fetch(`${API_BASE}/records/`);
      const data = await res.json();
      setRecords(data);
    } catch (err) {
      console.error('Failed to fetch records:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecords();
  }, []);

  const handleAction = async (id: string, action: 'APPROVED' | 'REJECTED') => {
    try {
      const response = await fetch(`${API_BASE}/records/${id}/`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: action })
      });
      
      if (response.ok) {
        // Optimistic update
        setRecords(prev => prev.map(r => r.id === id ? { ...r, status: action } : r));
        // Refresh to ensure we have the latest audit-linked state
        fetchRecords();
      } else {
        console.error('Failed to update record status');
      }
    } catch (err) {
      console.error('Error performing action:', err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center text-white">
        <div className="w-12 h-12 border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin mb-4" />
        <p className="text-gray-400 font-medium tracking-widest animate-pulse">SYNCHRONIZING ESG DATA...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white font-sans selection:bg-blue-500/30 relative">
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-blue-900/10 blur-[120px] rounded-full mix-blend-screen" />
        <div className="absolute bottom-[-10%] right-[-5%] w-[40%] h-[50%] bg-emerald-900/10 blur-[100px] rounded-full mix-blend-screen" />
      </div>

      <div className="relative z-10 p-8 max-w-7xl mx-auto space-y-8">
        <header className="flex flex-col gap-2 border-b border-white/10 pb-6">
          <h1 className="text-3xl font-light tracking-tight text-gray-100">
            TerraSync <span className="font-semibold text-blue-400">Analyst Review</span>
          </h1>
          <p className="text-gray-400 text-sm">Enterprise ESG Data Normalization & Audit Platform</p>
        </header>

        <main>
          <DataTable records={records} onRowClick={setSelectedRecord} />
        </main>
      </div>

      <RecordDrawer 
        record={selectedRecord} 
        onClose={() => setSelectedRecord(null)} 
        onAction={handleAction} 
      />
    </div>
  );
};