import React, { useState, useMemo } from 'react';
import { NormalizedRecord } from '../types';

interface DataTableProps {
  records: NormalizedRecord[];
  onRowClick: (record: NormalizedRecord) => void;
}

export const DataTable: React.FC<DataTableProps> = ({ records, onRowClick }) => {
  const [filterStatus, setFilterStatus] = useState<string>('ALL');
  const [filterScope, setFilterScope] = useState<string>('ALL');
  const [sortOrder, setSortOrder] = useState<'ASC' | 'DESC'>('DESC');

  const filteredAndSortedRecords = useMemo(() => {
    return records
      .filter(r => {
        const matchStatus = filterStatus === 'ALL' || r.status === filterStatus;
        const matchScope = filterScope === 'ALL' || r.scope_category === filterScope;
        return matchStatus && matchScope;
      })
      .sort((a, b) => {
        const valA = Number(a.standardized_value || 0);
        const valB = Number(b.standardized_value || 0);
        return sortOrder === 'ASC' ? valA - valB : valB - valA;
      });
  }, [records, filterStatus, filterScope, sortOrder]);

  const getStatusColor = (status: string) => {
    switch(status) {
      case 'APPROVED': return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/50';
      case 'REJECTED': return 'bg-gray-500/20 text-gray-400 border-gray-500/50';
      case 'FLAGGED': return 'bg-red-500/20 text-red-400 border-red-500/50';
      case 'PENDING': default: return 'bg-amber-500/20 text-amber-400 border-amber-500/50';
    }
  };

  return (
    <div className="w-full bg-white/5 backdrop-blur-md rounded-xl border border-white/10 overflow-hidden shadow-2xl">
      <div className="p-4 border-b border-white/10 flex gap-4">
        <select 
          className="bg-gray-800/50 text-white border border-white/10 rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500 transition-all cursor-pointer"
          value={filterStatus} 
          onChange={e => setFilterStatus(e.target.value)}
        >
          <option value="ALL">All Statuses</option>
          <option value="PENDING">Pending</option>
          <option value="FLAGGED">Flagged</option>
          <option value="APPROVED">Approved</option>
          <option value="REJECTED">Rejected</option>
        </select>
        <select 
          className="bg-gray-800/50 text-white border border-white/10 rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500 transition-all cursor-pointer"
          value={filterScope} 
          onChange={e => setFilterScope(e.target.value)}
        >
          <option value="ALL">All Scopes</option>
          <option value="SCOPE_1">Scope 1</option>
          <option value="SCOPE_2">Scope 2</option>
          <option value="SCOPE_3">Scope 3</option>
        </select>
        <select 
          className="bg-gray-800/50 text-white border border-white/10 rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500 transition-all cursor-pointer"
          value={sortOrder} 
          onChange={e => setSortOrder(e.target.value as 'ASC' | 'DESC')}
        >
          <option value="DESC">Value (High to Low)</option>
          <option value="ASC">Value (Low to High)</option>
        </select>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-gray-300">
          <thead className="bg-white/5 text-gray-400 font-medium">
            <tr>
              <th className="px-6 py-4 whitespace-nowrap">Record ID</th>
              <th className="px-6 py-4">Scope</th>
              <th className="px-6 py-4">Source</th>
              <th className="px-6 py-4">Standardized Val</th>
              <th className="px-6 py-4">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {filteredAndSortedRecords.map(record => (
              <tr 
                key={record.id} 
                onClick={() => onRowClick(record)}
                className="hover:bg-white/5 cursor-pointer transition-colors duration-200"
              >
                <td className="px-6 py-4 font-mono text-xs text-gray-500">{record.id.substring(0,8)}...</td>
                <td className="px-6 py-4 whitespace-nowrap">{record.scope_category}</td>
                <td className="px-6 py-4">{record.emission_source}</td>
                <td className="px-6 py-4 font-mono">{record.standardized_value !== null ? Number(record.standardized_value).toFixed(2) : 'N/A'}</td>
                <td className="px-6 py-4">
                  <span className={`px-2.5 py-1 rounded-full text-xs font-semibold border ${getStatusColor(record.status)}`}>
                    {record.status}
                  </span>
                </td>
              </tr>
            ))}
            {filteredAndSortedRecords.length === 0 && (
              <tr>
                <td colSpan={5} className="px-6 py-12 text-center text-gray-500">No records found matching filters.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};