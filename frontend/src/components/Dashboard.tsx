"use client";

import { useState } from "react";
import { Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface PatentSearch {
  id: string;
  description: string;
  similar_patents_count: number;
  novelty_score: number;
  filing_recommendation: string;
  created_at: string
}

export default function Dashboard() {
  const [description, setDescription] = useState("");
  const [patentSearch, setPatentSearch] = useState<PatentSearch | null>(null);
  const [extraData, setExtraData] = useState<any>(null);
const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    if (!description) return;
    setLoading(true);
    try {
      const res = await fetch("/searches", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
        description: description,
        }),
      });
      const data = await res.json();
      setPatentSearch(data);
      const extraRes = await fetch(`/searches/${search_id}/citations`);
      const extraData = await extraRes.json();
      setExtraData(extraData);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <div className="flex items-center gap-3">
        <Search className="w-8 h-8" style={{ color: "#9333EA" }} />
        <div>
          <h1 className="text-2xl font-bold">DClaw Patent</h1>
          <p className="text-sm text-slate-500">Patent search and analysis</p>
        </div>
        <Badge className="ml-auto" style={{ backgroundColor: "#9333EA" }}>Legal</Badge>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Search Patents</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Invention description</label>
              <Input value={description} onChange={(e) => setDescription(e.target.value)} placeholder="e.g. A novel battery cooling system" />
            </div>

          </div>
          <Button onClick={handleSubmit} disabled={loading || !description}>
            {loading ? "Processing..." : "Search Patents"}
          </Button>
        </CardContent>
      </Card>

      {patentSearch && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

          <Card>
            <CardHeader>
              <CardTitle>Search Results</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm">
              <p><strong>ID:</strong> {search.id}</p>
              <p><strong>Similar Patents:</strong> {search.similar_patents_count}</p>
              <p><strong>Novelty Score:</strong> {search.novelty_score + '/100'}</p>
              <p><strong>Filing Recommendation:</strong> {search.filing_recommendation}</p>
              <p><strong>Created:</strong> {new Date(search.created_at).toLocaleString()}</p>
            </CardContent>
          </Card>
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle>Citations</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {extraData?.map((rec: any, i: number) => (
                  <div key={i} className="flex items-center justify-between p-2 bg-slate-50 rounded">
                    <span className="text-sm">{rec.title}</span>
                    <Badge variant="secondary">{rec.patent_id}</Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
