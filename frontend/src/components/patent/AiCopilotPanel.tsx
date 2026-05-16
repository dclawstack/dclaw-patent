"use client";

import { useState } from "react";
import { aiSimilarPatents, aiDraftClaims, aiExaminerPrediction } from "@/lib/api";
import { PatentSearchResult, DraftedClaim, ExaminerPrediction } from "@/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function AiCopilotPanel({ patentId, description }: { patentId: string; description?: string }) {
  const [similar, setSimilar] = useState<PatentSearchResult[]>([]);
  const [claims, setClaims] = useState<DraftedClaim[]>([]);
  const [prediction, setPrediction] = useState<ExaminerPrediction | null>(null);
  const [loadingSimilar, setLoadingSimilar] = useState(false);
  const [loadingClaims, setLoadingClaims] = useState(false);
  const [loadingPrediction, setLoadingPrediction] = useState(false);

  async function loadSimilar() {
    setLoadingSimilar(true);
    try {
      const res = await aiSimilarPatents(patentId);
      setSimilar(res.results);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingSimilar(false);
    }
  }

  async function loadClaims() {
    setLoadingClaims(true);
    try {
      const res = await aiDraftClaims(description || "A novel method for data processing", 5);
      setClaims(res.claims);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingClaims(false);
    }
  }

  async function loadPrediction() {
    setLoadingPrediction(true);
    try {
      const res = await aiExaminerPrediction(patentId);
      setPrediction(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingPrediction(false);
    }
  }

  return (
    <Card className="border-blue-200">
      <CardHeader>
        <CardTitle className="text-blue-700 flex items-center gap-2">
          AI Copilot
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="similar">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="similar">Similar</TabsTrigger>
            <TabsTrigger value="draft">Draft Claims</TabsTrigger>
            <TabsTrigger value="prediction">Prediction</TabsTrigger>
          </TabsList>

          <TabsContent value="similar" className="space-y-3 mt-3">
            <Button size="sm" onClick={loadSimilar} disabled={loadingSimilar}>
              {loadingSimilar ? "Searching..." : "Find Similar Patents"}
            </Button>
            {similar.length === 0 && !loadingSimilar && (
              <div className="text-xs text-gray-500">Click to search for semantically similar patents in your portfolio.</div>
            )}
            <div className="space-y-2">
              {similar.map((s) => (
                <div key={s.id || s.patent_number} className="text-sm border rounded-md p-2">
                  <div className="font-medium">{s.title || s.patent_number}</div>
                  <div className="flex items-center gap-2 mt-1">
                    <Badge variant="outline">{s.jurisdiction}</Badge>
                    {s.relevance_score !== undefined && (
                      <Badge className="bg-blue-500 text-white">{Math.round(s.relevance_score * 100)}% match</Badge>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="draft" className="space-y-3 mt-3">
            <Button size="sm" onClick={loadClaims} disabled={loadingClaims}>
              {loadingClaims ? "Drafting..." : "Generate Claims"}
            </Button>
            {claims.length === 0 && !loadingClaims && (
              <div className="text-xs text-gray-500">AI will suggest claim language based on the invention description.</div>
            )}
            <div className="space-y-2">
              {claims.map((c) => (
                <div key={c.claim_number} className="text-sm border-l-2 border-blue-300 pl-3 py-1">
                  <span className="font-semibold">Claim {c.claim_number}.</span> {c.claim_text}
                </div>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="prediction" className="space-y-3 mt-3">
            <Button size="sm" onClick={loadPrediction} disabled={loadingPrediction}>
              {loadingPrediction ? "Analyzing..." : "Predict Outcome"}
            </Button>
            {prediction && (
              <div className="space-y-3 text-sm">
                <div className="flex items-center gap-3">
                  <span className="text-gray-500">Allowance Probability</span>
                  <Badge className={prediction.allowance_probability > 0.7 ? "bg-green-500 text-white" : prediction.allowance_probability > 0.5 ? "bg-yellow-500 text-white" : "bg-red-500 text-white"}>
                    {Math.round(prediction.allowance_probability * 100)}%
                  </Badge>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-gray-500">Confidence</span>
                  <Badge variant="outline">{Math.round(prediction.confidence * 100)}%</Badge>
                </div>
                <div>
                  <div className="font-medium text-gray-700 mb-1">Suggested Amendments</div>
                  <ul className="list-disc pl-4 space-y-1 text-gray-600">
                    {prediction.suggested_amendments.map((a, i) => (
                      <li key={i}>{a}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <div className="font-medium text-gray-700 mb-1">Factors</div>
                  <ul className="list-disc pl-4 space-y-1 text-gray-600">
                    {prediction.factors.map((f, i) => (
                      <li key={i}>{f}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
            {!prediction && !loadingPrediction && (
              <div className="text-xs text-gray-500">Predict allowance likelihood based on claim patterns and technology area.</div>
            )}
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}
