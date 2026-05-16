"use client";

import { useState } from "react";
import Link from "next/link";
import { aiPatentSearch } from "@/lib/api";
import { PatentSearchResult } from "@/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Search } from "lucide-react";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<PatentSearchResult[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await aiPatentSearch(query, 20);
      setResults(res.results);
      setTotal(res.total);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto space-y-6">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm">
            <Link href="/" className="flex items-center">
              <ArrowLeft className="h-4 w-4 mr-1" />
              Back
            </Link>
          </Button>
          <h1 className="text-2xl font-bold tracking-tight">Patent Search</h1>
        </div>

        <Card>
          <CardContent className="pt-6">
            <form onSubmit={handleSearch} className="flex gap-3">
              <Input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search patents by title, abstract, or natural language..."
                className="flex-1"
              />
              <Button type="submit" disabled={loading}>
                <Search className="h-4 w-4 mr-1" />
                {loading ? "Searching..." : "Search"}
              </Button>
            </form>
          </CardContent>
        </Card>

        {results.length > 0 && (
          <div className="space-y-3">
            <div className="text-sm text-gray-500">{total} results found</div>
            {results.map((r, i) => (
              <Card key={i}>
                <CardHeader className="pb-2">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-base">
                      {r.id ? (
                        <Link href={`/patents/${r.id}`} className="hover:underline">
                          {r.title || r.patent_number}
                        </Link>
                      ) : (
                        r.title || r.patent_number
                      )}
                    </CardTitle>
                    <div className="flex items-center gap-2">
                      {r.source && <Badge variant="outline">{r.source}</Badge>}
                      {r.relevance_score !== undefined && (
                        <Badge className="bg-blue-500 text-white">{Math.round(r.relevance_score * 100)}%</Badge>
                      )}
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  {r.abstract && (
                    <p className="text-sm text-gray-600 line-clamp-3">{r.abstract}</p>
                  )}
                  <div className="flex items-center gap-3 mt-2 text-xs text-gray-500">
                    {r.patent_number && <span>{r.patent_number}</span>}
                    {r.jurisdiction && <span>{r.jurisdiction}</span>}
                    {r.status && <span>{r.status}</span>}
                    {r.date && <span>{r.date}</span>}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
