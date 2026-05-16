'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

interface Patent {
  id: string;
  title: string;
  status: string;
  filing_date: string;
  expiration_date: string;
  assignee: string;
}

export default function PortfolioPage() {
  const [patents, setPatents] = useState<Patent[]>([]);
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // TODO: Fetch patents from API
    setLoading(false);
  }, [search, status]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Patent Portfolio</h1>
        <Button>+ Add Patent</Button>
      </div>

      <div className="flex gap-4">
        <Input
          placeholder="Search by title, assignee..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-1"
        />
        <select
          value={status || ''}
          onChange={(e) => setStatus(e.target.value || null)}
          className="px-3 py-2 border rounded-md"
        >
          <option value="">All Status</option>
          <option value="draft">Draft</option>
          <option value="filed">Filed</option>
          <option value="prosecution">Prosecution</option>
          <option value="issued">Issued</option>
          <option value="abandoned">Abandoned</option>
          <option value="expired">Expired</option>
        </select>
      </div>

      <div className="border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Title</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Filing Date</TableHead>
              <TableHead>Expiration</TableHead>
              <TableHead>Assignee</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={6} className="text-center py-8">
                  Loading...
                </TableCell>
              </TableRow>
            ) : patents.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} className="text-center py-8">
                  No patents found
                </TableCell>
              </TableRow>
            ) : (
              patents.map((patent) => (
                <TableRow key={patent.id}>
                  <TableCell className="font-medium">{patent.title}</TableCell>
                  <TableCell>
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                      {patent.status}
                    </span>
                  </TableCell>
                  <TableCell>{patent.filing_date}</TableCell>
                  <TableCell>{patent.expiration_date}</TableCell>
                  <TableCell>{patent.assignee}</TableCell>
                  <TableCell>
                    <Button variant="ghost" size="sm">
                      View
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
