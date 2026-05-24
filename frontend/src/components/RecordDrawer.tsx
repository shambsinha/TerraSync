import React from 'react';
import { NormalizedRecord } from '../types';

interface RecordDrawerProps {
  record: NormalizedRecord | null;
  onClose: () => void;
  onAction: (id: string, action: 'APPROVED' | 'REJECTED') => void;
}

export const RecordDrawer: React.FC<RecordDrawerProps> = ({ record, onClose, onAction }) => {
  if (!record) return null;

  return (
    <>
      <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 transition-opacity" onClick={onClose} />
      <div className="fixed right-0 top-0 bottom-0 w-full max-w-3xl bg-gray-900/95 backdrop-blur-xl border-l border-white/10 z-50 overflow-y-auto shadow-2xl flex flex-col transform transition-transform duration-300">
        <div className="p-6 border-b border-white/10 flex justify-between items-center bg-white/5 sticky top-0 z-10 backdrop-blur-md">
          <h2 className="text-xl font-semibold text-white tracking-wide">
            Review Record <span className="text-gray-500 text-sm font-mono ml-2">{record.id}</span>
          </h2>
          <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors text-3xl leading-none">&times;</button>
        </div>
        
        <div className="flex-1 p-6 flex flex-col md:flex-row gap-8">
          {/* Normalized Record Details */}
          <div className="flex-1 space-y-6">
            <h3 className="text-lg font-medium text-gray-200 border-b border-white/10 pb-2">Normalized Output</h3>
            
            <div className="space-y-5">
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wider">Status</p>
                <p className="text-sm text-white font-medium mt-1">{record.status}</p>
              </div>
              
              {record.status === 'FLAGGED' && (
                <div className="bg-red-500/10 border border-red-500/20 p-4 rounded-lg">
                  <p className="text-xs text-red-400 uppercase tracking-wider font-semibold">Suspicion Reason</p>
                  <p className="text-sm text-red-200 mt-1 leading-relaxed">{record.suspicion_reason}</p>
                </div>
              )}
              
              <div className="grid grid-cols-2 gap-6 bg-white/5 p-4 rounded-lg border border-white/5">
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wider">Scope</p>
                  <p className="text-sm text-white font-medium mt-1">{record.scope_category}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wider">Source Type</p>
                  <p className="text-sm text-white font-medium mt-1">{record.emission_source}</p>
                </div>
                <div className="col-span-2 border-t border-white/10 pt-4 mt-2">
                  <p className="text-xs text-gray-500 uppercase tracking-wider">Standardized Value</p>
                  <p className="text-2xl text-emerald-400 font-light mt-1 font-mono">
                    {record.standardized_value !== null ? Number(record.standardized_value).toFixed(4) : 'N/A'}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Raw Payload Details */}
          <div className="flex-1 space-y-6">
            <h3 className="text-lg font-medium text-gray-200 border-b border-white/10 pb-2">Raw Data Ledger</h3>
            
            {record.raw_payload ? (
              <div className="space-y-5">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="text-xs text-gray-500 uppercase tracking-wider">Source System</p>
                    <p className="text-sm text-white font-medium mt-1">{record.raw_payload.source_identifier}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-gray-500 uppercase tracking-wider">Ingested At</p>
                    <p className="text-sm text-gray-300 mt-1 font-mono">{new Date(record.raw_payload.received_at).toLocaleDateString()}</p>
                  </div>
                </div>
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Untampered JSON Payload</p>
                  <pre className="bg-black/60 border border-white/10 rounded-lg p-4 text-xs font-mono text-green-400/90 overflow-x-auto shadow-inner h-64 overflow-y-auto">
                    {JSON.stringify(record.raw_payload.payload, null, 2)}
                  </pre>
                </div>
              </div>
            ) : (
              <p className="text-sm text-gray-500 italic bg-white/5 p-4 rounded-lg">Raw payload not available or missing.</p>
            )}
          </div>
        </div>

        {/* Actions Footer */}
        {record.status === 'APPROVED' ? (
          <div className="p-6 border-t border-white/10 bg-emerald-500/5 flex justify-center items-center backdrop-blur-xl">
            <div className="flex items-center gap-2 text-emerald-400/80 bg-emerald-500/10 px-4 py-2 rounded-full border border-emerald-500/20">
              <span className="text-lg">🔒</span>
              <span className="text-xs font-semibold uppercase tracking-widest">Locked for Audit</span>
            </div>
          </div>
        ) : (record.status === 'PENDING' || record.status === 'FLAGGED') && (
          <div className="p-6 border-t border-white/10 bg-black/40 flex gap-4 justify-end backdrop-blur-xl">
            <button 
              onClick={() => { onAction(record.id, 'REJECTED'); onClose(); }}
              className="px-6 py-2.5 rounded-lg font-medium text-sm text-red-400 bg-red-500/10 border border-red-500/20 hover:bg-red-500/20 transition-all focus:ring-2 focus:ring-red-500 outline-none"
            >
              Reject Data
            </button>
            <button 
              onClick={() => { onAction(record.id, 'APPROVED'); onClose(); }}
              className="px-6 py-2.5 rounded-lg font-medium text-sm text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 hover:bg-emerald-500/20 transition-all shadow-[0_0_15px_rgba(16,185,129,0.1)] focus:ring-2 focus:ring-emerald-500 outline-none"
            >
              Approve & Normalize
            </button>
          </div>
        )}
      </div>
    </>
  );
};