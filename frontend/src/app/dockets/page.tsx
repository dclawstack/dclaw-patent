'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface Docket {
  id: string;
  patent_title: string;
  event_type: string;
  due_date: string;
  jurisdiction: string;
  status: string;
  days_until_due: number;
}

export default function DocketsPage() {
  const [dockets, setDockets] = useState<Docket[]>([]);
  const [filter, setFilter] = useState<'all' | 'overdue' | 'pending' | '30days'>('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // TODO: Fetch dockets from API based on filter
    setLoading(false);
  }, [filter]);

  const getUrgencyColor = (days: number) => {
    if (days < 0) return 'bg-red-100 text-red-800';
    if (days < 30) return 'bg-yellow-100 text-yellow-800';
    return 'bg-green-100 text-green-800';
  };

  const getUrgencyLabel = (days: number) => {
    if (days < 0) return `${Math.abs(days)} days overdue`;
    if (days === 0) return 'Due today';
    return `${days} days remaining`;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Docket Calendar</h1>
        <Button>+ Add Event</Button>
      </div>

      <div className="flex gap-2">
        {['all', 'overdue', 'pending', '30days'].map((f) => (
          <Button
            key={f}
            variant={filter === f ? 'default' : 'outline'}
            onClick={() => setFilter(f as any)}
          >
            {f === 'all' ? 'All' : f === 'overdue' ? 'Overdue' : f === '30days' ? 'Next 30 Days' : 'Pending'}
          </Button>
        ))}
      </div>

      <div className="grid gap-4">
        {loading ? (
          <div className="text-center py-8">Loading...</div>
        ) : dockets.length === 0 ? (
          <div className="text-center py-8 text-gray-500">No dockets found</div>
        ) : (
          dockets.map((docket) => (
            <Card key={docket.id} className="border-l-4" style={{
              borderLeftColor: docket.status === 'completed' ? '#22c55e' : docket.days_until_due < 0 ? '#ef4444' : docket.days_until_due < 30 ? '#eab308' : '#3b82f6'
            }}>
              <CardContent className="pt-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-bold text-lg">{docket.event_type}</h3>
                    <p className="text-sm text-gray-600">{docket.patent_title}</p>
                    <div className="mt-2 flex gap-4 text-sm">
                      <span>📍 {docket.jurisdiction}</span>
                      <span>📅 {docket.due_date}</span>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className={`px-3 py-1 rounded-full font-medium ${getUrgencyColor(docket.days_until_due)}`}>
                      {getUrgencyLabel(docket.days_until_due)}
                    </span>
                    <div className="mt-2">
                      <Button variant="ghost" size="sm">Mark Done</Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
