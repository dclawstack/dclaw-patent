"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { createPatent } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { ArrowLeft } from "lucide-react";

export default function NewPatentPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [claims, setClaims] = useState([""]);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    const form = new FormData(e.currentTarget);
    const data = {
      patent_number: form.get("patent_number") as string,
      title: form.get("title") as string,
      abstract: form.get("abstract") as string,
      claims: claims.filter((c) => c.trim() !== ""),
      description: form.get("description") as string,
      filing_date: new Date(form.get("filing_date") as string).toISOString(),
      issue_date: form.get("issue_date") ? new Date(form.get("issue_date") as string).toISOString() : undefined,
      status: (form.get("status") as string) || "filed",
      applicant: form.get("applicant") as string,
      inventors: (form.get("inventors") as string).split(",").map((s) => s.trim()).filter(Boolean),
      technology_category: form.get("technology_category") as string,
      jurisdiction: (form.get("jurisdiction") as string) || "US",
    };
    try {
      const created = await createPatent(data as any);
      router.push(`/patents/${created.id}`);
    } catch (err) {
      console.error(err);
      alert("Failed to create patent");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-3xl mx-auto space-y-6">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm">
            <Link href="/" className="flex items-center">
              <ArrowLeft className="h-4 w-4 mr-1" />
              Back
            </Link>
          </Button>
          <h1 className="text-2xl font-bold tracking-tight">Add New Patent</h1>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Patent Details</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="patent_number">Patent Number</Label>
                  <Input id="patent_number" name="patent_number" required placeholder="US1234567" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="title">Title</Label>
                  <Input id="title" name="title" required placeholder="Invention title" />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="abstract">Abstract</Label>
                <Textarea id="abstract" name="abstract" required placeholder="Brief summary of the invention" />
              </div>

              <div className="space-y-2">
                <Label>Claims</Label>
                {claims.map((claim, i) => (
                  <Textarea
                    key={i}
                    value={claim}
                    onChange={(e) => {
                      const next = [...claims];
                      next[i] = e.target.value;
                      setClaims(next);
                    }}
                    placeholder={`Claim ${i + 1}`}
                  />
                ))}
                <Button type="button" variant="outline" size="sm" onClick={() => setClaims([...claims, ""])}>
                  Add Claim
                </Button>
              </div>

              <div className="space-y-2">
                <Label htmlFor="description">Description</Label>
                <Textarea id="description" name="description" placeholder="Detailed description (optional)" />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="filing_date">Filing Date</Label>
                  <Input id="filing_date" name="filing_date" type="date" required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="issue_date">Issue Date</Label>
                  <Input id="issue_date" name="issue_date" type="date" />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="status">Status</Label>
                  <select id="status" name="status" defaultValue="filed" className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50">
                    <option value="drafted">Drafted</option>
                    <option value="filed">Filed</option>
                    <option value="prosecution">Prosecution</option>
                    <option value="issued">Issued</option>
                    <option value="abandoned">Abandoned</option>
                    <option value="lapsed">Lapsed</option>
                  </select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="jurisdiction">Jurisdiction</Label>
                  <select id="jurisdiction" name="jurisdiction" defaultValue="US" className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50">
                    <option value="US">US</option>
                    <option value="EU">EU</option>
                    <option value="JP">JP</option>
                    <option value="CN">CN</option>
                    <option value="KR">KR</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="applicant">Applicant</Label>
                  <Input id="applicant" name="applicant" required placeholder="Company or individual name" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="technology_category">Technology Category</Label>
                  <Input id="technology_category" name="technology_category" placeholder="e.g. quantum_computing" />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="inventors">Inventors (comma separated)</Label>
                <Input id="inventors" name="inventors" placeholder="Alice Smith, Bob Jones" />
              </div>

              <div className="pt-4 flex gap-3">
                <Button type="submit" disabled={loading}>
                  {loading ? "Saving..." : "Create Patent"}
                </Button>
                <Button variant="outline">
                  <Link href="/" className="flex items-center">Cancel</Link>
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </main>
  );
}
