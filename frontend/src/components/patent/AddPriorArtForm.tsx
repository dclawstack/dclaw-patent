"use client";

import { useState } from "react";
import { createPriorArt } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

export default function AddPriorArtForm({ patentId, onCreated }: { patentId: string; onCreated: () => void }) {
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    const form = new FormData(e.currentTarget);
    const data = {
      patent_id: patentId,
      source_patent_number: form.get("source_patent_number") as string,
      source_title: form.get("source_title") as string,
      relevance_score: parseFloat(form.get("relevance_score") as string) || 0.5,
      analysis_notes: (form.get("analysis_notes") as string) || undefined,
    };
    try {
      await createPriorArt(data as any);
      onCreated();
      setOpen(false);
      (e.target as HTMLFormElement).reset();
    } catch (err) {
      console.error(err);
      alert("Failed to add prior art");
    } finally {
      setLoading(false);
    }
  }

  if (!open) {
    return (
      <Button size="sm" variant="outline" onClick={() => setOpen(true)}>
        + Add Prior Art
      </Button>
    );
  }

  return (
    <Card className="border-blue-200">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm">Add Prior Art</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-3">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="space-y-1">
              <Label htmlFor="source_patent_number" className="text-xs">Source Patent Number</Label>
              <Input id="source_patent_number" name="source_patent_number" required placeholder="US5555555" />
            </div>
            <div className="space-y-1">
              <Label htmlFor="relevance_score" className="text-xs">Relevance Score (0–1)</Label>
              <Input id="relevance_score" name="relevance_score" type="number" step="0.01" min="0" max="1" defaultValue="0.5" required />
            </div>
          </div>
          <div className="space-y-1">
            <Label htmlFor="source_title" className="text-xs">Source Title</Label>
            <Input id="source_title" name="source_title" required placeholder="Title of prior art patent" />
          </div>
          <div className="space-y-1">
            <Label htmlFor="analysis_notes" className="text-xs">Analysis Notes</Label>
            <Textarea id="analysis_notes" name="analysis_notes" placeholder="Why this is relevant..." />
          </div>
          <div className="flex gap-2 pt-1">
            <Button type="submit" size="sm" disabled={loading}>
              {loading ? "Saving..." : "Save"}
            </Button>
            <Button type="button" size="sm" variant="ghost" onClick={() => setOpen(false)}>
              Cancel
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
