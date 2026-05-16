'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';

interface Docket {
  id: string;
  patent_id: string;
  event_type: string;
  due_date: string;
  jurisdiction: string;
  status: string;
  description?: string;
  auto_generated: boolean;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export default function DocketsPage() {
  const [dockets, setDockets] = useState<Docket[]>([]);
  const [filter, setFilter] = useState<'all' | 'overdue' | 'pending' | '30days'>('pending');
  const [jurisdiction, setJurisdiction] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState<'date' | 'urgency'>('date');

  useEffect(() => {
    fetchDockets();
  }, [filter, jurisdiction]);

  const fetchDockets = async () => {
    setLoading(true);
    try {
      let url = `${API_BASE}/dockets`;
      const params = new URLSearchParams();

      if (filter === 'overdue') {
        url = `${API_BASE}/dockets/overdue`;
      } else if (filter === '30days') {
        url = `${API_BASE}/dockets/upcoming?days_ahead=30`;
      } else if (filter === 'pending') {
        params.append('status', 'pending');
      }

      if (jurisdiction) {
        params.append('jurisdiction', jurisdiction);
      }

      const fullUrl = params.toString() ? `${url}?${params}` : url;
      const response = await fetch(fullUrl);
      if (!response.ok) throw new Error('Failed to fetch dockets');

      const data = await response.json();
      setDockets(Array.isArray(data) ? data : data.dockets || []);
    } catch (error) {
      console.error('Error fetching dockets:', error);
      setDockets([]);
    } finally {
      setLoading(false);
    }
  };

  const getDaysDue = (dueDate: string): number => {
    const due = new Date(dueDate);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    due.setHours(0, 0, 0, 0);
    return Math.floor((due.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
  };

  const getUrgencyColor = (days: number) => {
    if (days < 0) return 'border-red-500 bg-red-50';
    if (days < 14) return 'border-yellow-500 bg-yellow-50';
    if (days < 30) return 'border-blue-500 bg-blue-50';
    return 'border-gray-300 bg-white';
  };

  const getUrgencyBadgeColor = (days: number) => {
    if (days < 0) return 'bg-red-100 text-red-800';
    if (days < 14) return 'bg-yellow-100 text-yellow-800';
    if (days < 30) return 'bg-blue-100 text-blue-800';
    return 'bg-gray-100 text-gray-800';
  };

  const getUrgencyLabel = (days: number) => {
    if (days < 0) return `${Math.abs(days)} days overdue`;
    if (days === 0) return 'Due today';
    if (days === 1) return 'Due tomorrow';
    return `${days} days remaining`;
  };

  const handleMarkComplete = async (docketId: string) => {
    try {
      const response = await fetch(`${API_BASE}/dockets/${docketId}/mark-complete`, {
        method: 'POST',
      });
      if (response.ok) {
        setDockets(dockets.map(d => d.id === docketId ? { ...d, status: 'completed' } : d));
      }
    } catch (error) {
      console.error('Error marking docket complete:', error);
    }
  };

  const handleMarkPending = async (docketId: string) => {
    try {
      const response = await fetch(`${API_BASE}/dockets/${docketId}/mark-pending`, {
        method: 'POST',
      });
      if (response.ok) {
        setDockets(dockets.map(d => d.id === docketId ? { ...d, status: 'pending' } : d));
      }
    } catch (error) {
      console.error('Error marking docket pending:', error);
    }
  };

  const handleExportCSV = async () => {
    try {
      const params = new URLSearchParams();
      if (jurisdiction) params.append('jurisdiction', jurisdiction);
      const url = `${API_BASE}/dockets/export/csv${params.toString() ? '?' + params : ''}`;
      window.location.href = url;
    } catch (error) {
      console.error('Error exporting CSV:', error);
    }
  };

  const handleExportICal = async () => {
    try {
      const params = new URLSearchParams();
      if (jurisdiction) params.append('jurisdiction', jurisdiction);
      const url = `${API_BASE}/dockets/export/ical${params.toString() ? '?' + params : ''}`;
      window.location.href = url;
    } catch (error) {
      console.error('Error exporting iCal:', error);
    }
  };

  const sortedDockets = [...dockets].sort((a, b) => {
    if (sortBy === 'date') {
      return new Date(a.due_date).getTime() - new Date(b.due_date).getTime();
    } else {
      const daysA = getDaysDue(a.due_date);
      const daysB = getDaysDue(b.due_date);
      return daysA - daysB;
    }
  });

  const jurisdictions = Array.from(new Set(dockets.map(d => d.jurisdiction)));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Docket Calendar</h1>
        <div className="flex gap-2">
          <Button onClick={handleExportCSV} variant="outline" size="sm">📥 CSV</Button>
          <Button onClick={handleExportICal} variant="outline" size="sm">📅 iCal</Button>
        </div>
      </div>

      <div className="space-y-4">
        <div className="flex gap-2 flex-wrap">
          {['all', 'overdue', 'pending', '30days'].map((f) => (
            <Button
              key={f}
              variant={filter === f ? 'default' : 'outline'}
              onClick={() => setFilter(f as any)}
              size="sm"
            >
              {f === 'all' ? 'All' : f === 'overdue' ? '🔴 Overdue' : f === '30days' ? '📅 Next 30 Days' : '⏳ Pending'}
            </Button>
          ))}
        </div>

        <div className="flex gap-2 flex-wrap">
          <select
            className="px-3 py-2 border rounded-md text-sm"
            value={jurisdiction}
            onChange={(e) => setJurisdiction(e.target.value)}
          >
            <option value="">All Jurisdictions</option>
            {jurisdictions.map(j => (
              <option key={j} value={j}>{j}</option>
            ))}
          </select>

          <select
            className="px-3 py-2 border rounded-md text-sm"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as 'date' | 'urgency')}
          >
            <option value="date">Sort by Date</option>
            <option value="urgency">Sort by Urgency</option>
          </select>
        </div>
      </div>

      <div className="grid gap-3">
        {loading ? (
          <div className="text-center py-8">Loading dockets...</div>
        ) : sortedDockets.length === 0 ? (
          <div className="text-center py-8 text-gray-500">No dockets found</div>
        ) : (
          sortedDockets.map((docket) => {
            const daysDue = getDaysDue(docket.due_date);
            const isCompleted = docket.status === 'completed';

            return (
              <Card
                key={docket.id}
                className={`border-l-4 transition-opacity ${isCompleted ? 'opacity-60' : ''} ${getUrgencyColor(daysDue)}`}
              >
                <CardContent className="pt-6">
                  <div className="flex items-start gap-4">
                    <Checkbox
                      checked={isCompleted}
                      onCheckedChange={(checked) => {
                        if (checked) {
                          handleMarkComplete(docket.id);
                        } else {
                          handleMarkPending(docket.id);
                        }
                      }}
                      className="mt-1"
                    />

                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1">
                          <h3 className={`font-bold text-lg ${isCompleted ? 'line-through' : ''}`}>
                            {docket.event_type}
                          </h3>
                          {docket.description && (
                            <p className="text-sm text-gray-600 mt-1">{docket.description}</p>
                          )}
                          <div className="mt-2 flex gap-4 text-xs text-gray-600">
                            <span>Patent: {docket.patent_id.substring(0, 8)}</span>
                            <span>📍 {docket.jurisdiction}</span>
                            <span>📅 {new Date(docket.due_date).toLocaleDateString()}</span>
                            {docket.auto_generated && <span className="text-blue-600">🤖 Auto-generated</span>}
                          </div>
                        </div>

                        <div className="text-right flex-shrink-0">
                          <span className={`inline-block px-3 py-1 rounded-full font-medium text-sm ${getUrgencyBadgeColor(daysDue)}`}>
                            {getUrgencyLabel(daysDue)}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })
        )}
      </div>

      {sortedDockets.length > 0 && (
        <div className="text-sm text-gray-600 text-center py-4">
          {sortedDockets.length} docket{sortedDockets.length !== 1 ? 's' : ''} shown
          {jurisdiction && ` for ${jurisdiction}`}
        </div>
      )}
    </div>
  );
}
