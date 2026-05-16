"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { getPatent, getDockets, getPriorArts } from "@/lib/api";
import { Patent, DocketEvent, PriorArt } from "@/types";
import AiCopilotPanel from "@/components/patent/AiCopilotPanel";
import AddDocketForm from "@/components/docket/AddDocketForm";
import AddPriorArtForm from "@/components/patent/AddPriorArtForm";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { ArrowLeft, Pencil } from "lucide-react";

const statusColors: Record<string, string> = {
  drafted: "bg-gray-500",
  filed: "bg-blue-500",
  prosecution: "bg-yellow-500",
  issued: "bg-green-500",
  abandoned: "bg-red-500",
  lapsed: "bg-purple-500",
};

export default function PatentDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const [patent, setPatent] = useState<Patent | null>(null);
  const [dockets, setDockets] = useState<DocketEvent[]>([]);
  const [priorArts, setPriorArts] = useState<PriorArt[]>([]);
  const [loading, setLoading] = useState(true);

  async function loadDockets() {
    try {
      const d = await getDockets({ patent_id: id });
      setDockets(d.items);
    } catch (e) {
      console.error(e);
    }
  }

  async function loadPriorArts() {
    try {
      const pa = await getPriorArts({ patent_id: id });
      setPriorArts(pa.items);
    } catch (e) {
      console.error(e);
    }
  }

  useEffect(() => {
    async function load() {
      try {
        const [p, d, pa] = await Promise.all([
          getPatent(id),
          getDockets({ patent_id: id }),
          getPriorArts({ patent_id: id }),
        ]);
        setPatent(p);
        setDockets(d.items);
        setPriorArts(pa.items);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    if (id) load();
  }, [id]);

  if (loading) return <div className="p-8 text-sm text-gray-500">Loading...</div>;
  if (!patent) return <div className="p-8 text-sm text-gray-500">Patent not found</div>;

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
          <div className="flex-1">
            <h1 className="text-2xl font-bold tracking-tight">{patent.title}</h1>
            <p className="text-sm text-gray-500">{patent.patent_number}</p>
          </div>
          <Badge className={`${statusColors[patent.status]} text-white`}>{patent.status}</Badge>
          <Button variant="outline" size="sm">
            <Link href={`/patents/${id}/edit`} className="flex items-center gap-1">
              <Pencil className="h-3 w-3" />
              Edit
            </Link>
          </Button>
        </div>

        <Tabs defaultValue="overview">
          <TabsList>
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="claims">Claims</TabsTrigger>
            <TabsTrigger value="docket">Docket</TabsTrigger>
            <TabsTrigger value="prior-art">Prior Art</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-4 mt-4">
            <Card>
              <CardHeader>
                <CardTitle>Patent Information</CardTitle>
              </CardHeader>
              <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium text-gray-500">Applicant</span>
                  <p>{patent.applicant}</p>
                </div>
                <div>
                  <span className="font-medium text-gray-500">Jurisdiction</span>
                  <p>{patent.jurisdiction}</p>
                </div>
                <div>
                  <span className="font-medium text-gray-500">Filing Date</span>
                  <p>{new Date(patent.filing_date).toLocaleDateString()}</p>
                </div>
                <div>
                  <span className="font-medium text-gray-500">Issue Date</span>
                  <p>{patent.issue_date ? new Date(patent.issue_date).toLocaleDateString() : "—"}</p>
                </div>
                <div>
                  <span className="font-medium text-gray-500">Technology Category</span>
                  <p>{patent.technology_category || "—"}</p>
                </div>
                <div>
                  <span className="font-medium text-gray-500">Inventors</span>
                  <p>{patent.inventors?.join(", ") || "—"}</p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Abstract</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-700 leading-relaxed">{patent.abstract}</p>
              </CardContent>
            </Card>
            {patent.description && (
              <Card>
                <CardHeader>
                  <CardTitle>Description</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">{patent.description}</p>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          <TabsContent value="claims" className="mt-4">
            <Card>
              <CardHeader>
                <CardTitle>Claims</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {patent.claims.length === 0 ? (
                  <div className="text-sm text-gray-500">No claims recorded.</div>
                ) : (
                  patent.claims.map((claim, i) => (
                    <div key={i} className="text-sm text-gray-700 leading-relaxed border-l-2 border-blue-200 pl-3">
                      {claim}
                    </div>
                  ))
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="docket" className="mt-4">
            <AddDocketForm patentId={id} onCreated={loadDockets} />
            <Card className="mt-4">
              <CardHeader className="flex items-center justify-between">
                <CardTitle>Docket Events</CardTitle>
              </CardHeader>
              <CardContent>
                {dockets.length === 0 ? (
                  <div className="text-sm text-gray-500">No docket events.</div>
                ) : (
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Type</TableHead>
                        <TableHead>Description</TableHead>
                        <TableHead>Due Date</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead>Assignee</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {dockets.map((d) => (
                        <TableRow key={d.id}>
                          <TableCell className="capitalize">{d.event_type.replace("_", " ")}</TableCell>
                          <TableCell>{d.description}</TableCell>
                          <TableCell>{new Date(d.due_date).toLocaleDateString()}</TableCell>
                          <TableCell>
                            <Badge variant={d.status === "completed" ? "secondary" : d.status === "overdue" ? "destructive" : "default"}>
                              {d.status}
                            </Badge>
                          </TableCell>
                          <TableCell>{d.assignee || "—"}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="prior-art" className="mt-4">
            <AddPriorArtForm patentId={id} onCreated={loadPriorArts} />
            <Card className="mt-4">
              <CardHeader className="flex items-center justify-between">
                <CardTitle>Prior Art</CardTitle>
              </CardHeader>
              <CardContent>
                {priorArts.length === 0 ? (
                  <div className="text-sm text-gray-500">No prior art recorded.</div>
                ) : (
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Source Patent</TableHead>
                        <TableHead>Title</TableHead>
                        <TableHead>Relevance</TableHead>
                        <TableHead>Notes</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {priorArts.map((pa) => (
                        <TableRow key={pa.id}>
                          <TableCell className="font-medium">{pa.source_patent_number}</TableCell>
                          <TableCell>{pa.source_title}</TableCell>
                          <TableCell>
                            <Badge variant={pa.relevance_score > 0.8 ? "destructive" : pa.relevance_score > 0.5 ? "secondary" : "outline"}>
                              {Math.round(pa.relevance_score * 100)}%
                            </Badge>
                          </TableCell>
                          <TableCell className="max-w-xs truncate">{pa.analysis_notes || "—"}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
        <AiCopilotPanel patentId={patent.id} description={patent.description || patent.abstract} />
      </div>
    </main>
  );
}
