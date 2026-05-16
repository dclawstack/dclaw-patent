"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getCompetitors, createCompetitor, deleteCompetitor, getCompetitorFilings } from "@/lib/api";
import { CompetitorWatch, PatentSearchResult } from "@/types";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ArrowLeft, Trash2, Search, Globe } from "lucide-react";

export default function CompetitorsPage() {
  const [watches, setWatches] = useState<CompetitorWatch[]>([]);
  const [loading, setLoading] = useState(true);
  const [newCompany, setNewCompany] = useState("");
  const [newKeywords, setNewKeywords] = useState("");
  const [adding, setAdding] = useState(false);
  const [scanningId, setScanningId] = useState<string | null>(null);
  const [scanResults, setScanResults] = useState<Record<string, PatentSearchResult[]>>({});

  async function load() {
    try {
      const data = await getCompetitors({ limit: 50 });
      setWatches(data.items);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    if (!newCompany.trim()) return;
    setAdding(true);
    try {
      await createCompetitor({
        company_name: newCompany.trim(),
        technology_keywords: newKeywords.split(",").map((s) => s.trim()).filter(Boolean),
      });
      setNewCompany("");
      setNewKeywords("");
      load();
    } catch (err) {
      console.error(err);
      alert("Failed to add competitor");
    } finally {
      setAdding(false);
    }
  }

  async function handleDelete(id: string) {
    if (!confirm("Remove this competitor from watch list?")) return;
    try {
      await deleteCompetitor(id);
      load();
    } catch (err) {
      console.error(err);
    }
  }

  async function handleScan(id: string) {
    setScanningId(id);
    try {
      const res = await getCompetitorFilings(id);
      setScanResults((prev) => ({ ...prev, [id]: res.results }));
    } catch (err) {
      console.error(err);
    } finally {
      setScanningId(null);
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-5xl mx-auto space-y-6">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm">
            <Link href="/" className="flex items-center">
              <ArrowLeft className="h-4 w-4 mr-1" />
              Back
            </Link>
          </Button>
          <h1 className="text-2xl font-bold tracking-tight">Competitive Intelligence</h1>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Add Competitor to Watch List</CardTitle>
            <CardDescription>Monitor patent filings by company and technology area</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleAdd} className="flex flex-col md:flex-row gap-3">
              <div className="flex-1 space-y-1">
                <Label htmlFor="company" className="text-xs">Company Name</Label>
                <Input
                  id="company"
                  value={newCompany}
                  onChange={(e) => setNewCompany(e.target.value)}
                  placeholder="e.g. IBM, Google, Microsoft"
                  required
                />
              </div>
              <div className="flex-[2] space-y-1">
                <Label htmlFor="keywords" className="text-xs">Technology Keywords (comma separated)</Label>
                <Input
                  id="keywords"
                  value={newKeywords}
                  onChange={(e) => setNewKeywords(e.target.value)}
                  placeholder="quantum computing, neural networks, battery"
                />
              </div>
              <div className="flex items-end">
                <Button type="submit" disabled={adding} className="w-full md:w-auto">
                  {adding ? "Adding..." : "Add to Watch"}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>

        {loading ? (
          <div className="text-sm text-gray-500">Loading...</div>
        ) : watches.length === 0 ? (
          <div className="text-sm text-gray-500">No competitors on watch list yet.</div>
        ) : (
          <div className="space-y-4">
            {watches.map((w) => (
              <Card key={w.id}>
                <CardHeader className="pb-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <Globe className="h-5 w-5 text-blue-500" />
                      <CardTitle className="text-base">{w.company_name}</CardTitle>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button size="sm" variant="outline" onClick={() => handleScan(w.id)} disabled={scanningId === w.id}>
                        <Search className="h-3 w-3 mr-1" />
                        {scanningId === w.id ? "Scanning..." : "Scan Filings"}
                      </Button>
                      <Button size="sm" variant="ghost" className="text-red-500" onClick={() => handleDelete(w.id)}>
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-2 mt-1">
                    {w.technology_keywords?.map((kw) => (
                      <Badge key={kw} variant="secondary">{kw}</Badge>
                    ))}
                  </div>
                </CardHeader>
                {scanResults[w.id] && (
                  <CardContent>
                    <div className="text-sm font-medium text-gray-700 mb-2">
                      Recent Filings ({scanResults[w.id].length} found)
                    </div>
                    <div className="space-y-2">
                      {scanResults[w.id].map((r, i) => (
                        <div key={i} className="text-sm border rounded-md p-2">
                          <div className="font-medium">{r.title || r.patent_number}</div>
                          <div className="flex items-center gap-2 mt-1 text-xs text-gray-500">
                            <span>{r.patent_number}</span>
                            <span>{r.date}</span>
                            <Badge variant="outline">{r.source}</Badge>
                          </div>
                          {r.abstract && (
                            <p className="text-xs text-gray-600 mt-1 line-clamp-2">{r.abstract}</p>
                          )}
                        </div>
                      ))}
                    </div>
                  </CardContent>
                )}
              </Card>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
