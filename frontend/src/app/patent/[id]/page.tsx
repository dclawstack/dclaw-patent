'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface Patent {
  id: string;
  title: string;
  abstract: string;
  claims: string;
  status: string;
  filing_date: string;
  assignee: string;
}

interface Docket {
  id: string;
  event_type: string;
  due_date: string;
  status: string;
}

export default function PatentDetailPage() {
  const params = useParams();
  const patentId = params.id as string;
  const [patent, setPatent] = useState<Patent | null>(null);
  const [dockets, setDockets] = useState<Docket[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // TODO: Fetch patent detail from API
    setLoading(false);
  }, [patentId]);

  if (loading) return <div>Loading...</div>;
  if (!patent) return <div>Patent not found</div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">{patent.title}</h1>
        <div className="flex gap-4 text-sm text-gray-600">
          <span>Status: <strong>{patent.status}</strong></span>
          <span>Filed: <strong>{patent.filing_date}</strong></span>
          <span>Assignee: <strong>{patent.assignee}</strong></span>
        </div>
      </div>

      <Tabs defaultValue="claims" className="w-full">
        <TabsList>
          <TabsTrigger value="claims">Claims</TabsTrigger>
          <TabsTrigger value="abstract">Abstract</TabsTrigger>
          <TabsTrigger value="dockets">Dockets</TabsTrigger>
          <TabsTrigger value="comments">Comments</TabsTrigger>
        </TabsList>

        <TabsContent value="claims">
          <Card>
            <CardHeader>
              <CardTitle>Patent Claims</CardTitle>
            </CardHeader>
            <CardContent>
              <pre className="bg-gray-50 p-4 rounded-lg whitespace-pre-wrap font-mono text-sm">
                {patent.claims || 'No claims recorded yet'}
              </pre>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="abstract">
          <Card>
            <CardHeader>
              <CardTitle>Abstract</CardTitle>
            </CardHeader>
            <CardContent>
              <p>{patent.abstract || 'No abstract available'}</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="dockets">
          <Card>
            <CardHeader>
              <CardTitle>Docket Events</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {dockets.map((docket) => (
                  <div key={docket.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <p className="font-medium">{docket.event_type}</p>
                      <p className="text-sm text-gray-600">Due: {docket.due_date}</p>
                    </div>
                    <span className={`px-2 py-1 rounded-full text-sm ${
                      docket.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                      docket.status === 'completed' ? 'bg-green-100 text-green-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {docket.status}
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="comments">
          <Card>
            <CardHeader>
              <CardTitle>Comments & Collaboration</CardTitle>
            </CardHeader>
            <CardContent>
              {/* TODO: Implement comments section */}
              <p className="text-gray-500">Comments feature coming soon</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* AI Copilot Panel */}
      <Card className="border-blue-200 bg-blue-50">
        <CardHeader>
          <CardTitle className="text-lg">AI Patent Copilot</CardTitle>
        </CardHeader>
        <CardContent>
          <Button variant="outline">Find Similar Patents</Button>
          <p className="text-sm text-gray-600 mt-2">
            Powered by semantic search and patent embeddings
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
