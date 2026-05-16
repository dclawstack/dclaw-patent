"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getPatents, getDocketAlerts } from "@/lib/api";
import { Patent, DocketEvent } from "@/types";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { AlertTriangle, Calendar, FileText, Globe, Clock, Search, Shield } from "lucide-react";

const statusColors: Record<string, string> = {
  drafted: "bg-gray-500",
  filed: "bg-blue-500",
  prosecution: "bg-yellow-500",
  issued: "bg-green-500",
  abandoned: "bg-red-500",
  lapsed: "bg-purple-500",
};

export default function PortfolioDashboard() {
  const [patents, setPatents] = useState<Patent[]>([]);
  const [total, setTotal] = useState(0);
  const [urgent, setUrgent] = useState<DocketEvent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [patentData, alerts] = await Promise.all([
          getPatents({ limit: 50 }),
          getDocketAlerts(30),
        ]);
        setPatents(patentData.items);
        setTotal(patentData.total);
        setUrgent(alerts.urgent);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const statusCounts = patents.reduce((acc, p) => {
    acc[p.status] = (acc[p.status] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const jurisdictionCounts = patents.reduce((acc, p) => {
    acc[p.jurisdiction] = (acc[p.jurisdiction] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-gray-900">Patent Portfolio</h1>
            <p className="text-sm text-gray-500 mt-1">Manage your intellectual property estate</p>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">
              <Link href="/search" className="flex items-center gap-1">
                <Search className="h-4 w-4" />
                Search
              </Link>
            </Button>
            <Button variant="outline" size="sm">
              <Link href="/competitors" className="flex items-center gap-1">
                <Shield className="h-4 w-4" />
                Competitors
              </Link>
            </Button>
            <Button size="sm">
              <Link href="/patents/new">Add Patent</Link>
            </Button>
          </div>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Total Patents</CardTitle>
              <FileText className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{total}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Filed / Pending</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{(statusCounts.filed || 0) + (statusCounts.prosecution || 0)}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Issued</CardTitle>
              <Globe className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{statusCounts.issued || 0}</div>
            </CardContent>
          </Card>
          <Card className={urgent.length > 0 ? "border-red-200 bg-red-50" : ""}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Urgent Deadlines</CardTitle>
              <AlertTriangle className="h-4 w-4 text-red-500" />
            </CardHeader>
            <CardContent>
              <div className={`text-2xl font-bold ${urgent.length > 0 ? "text-red-600" : ""}`}>{urgent.length}</div>
            </CardContent>
          </Card>
        </div>

        {/* Status Distribution */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle>Patents</CardTitle>
              <CardDescription>All patents in your portfolio</CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="text-sm text-gray-500">Loading...</div>
              ) : patents.length === 0 ? (
                <div className="text-sm text-gray-500">No patents yet. Add your first patent to get started.</div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Number</TableHead>
                      <TableHead>Title</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Jurisdiction</TableHead>
                      <TableHead>Filing Date</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {patents.map((patent) => (
                      <TableRow key={patent.id}>
                        <TableCell className="font-medium">
                          <Link href={`/patents/${patent.id}`} className="hover:underline">
                            {patent.patent_number}
                          </Link>
                        </TableCell>
                        <TableCell>{patent.title}</TableCell>
                        <TableCell>
                          <Badge className={`${statusColors[patent.status]} text-white`}>{patent.status}</Badge>
                        </TableCell>
                        <TableCell>{patent.jurisdiction}</TableCell>
                        <TableCell>{new Date(patent.filing_date).toLocaleDateString()}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Jurisdictions</CardTitle>
              <CardDescription>Geographic coverage</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {Object.entries(jurisdictionCounts).map(([jur, count]) => (
                  <div key={jur} className="flex items-center justify-between">
                    <span className="text-sm">{jur}</span>
                    <Badge variant="outline">{count}</Badge>
                  </div>
                ))}
                {Object.keys(jurisdictionCounts).length === 0 && (
                  <div className="text-sm text-gray-500">No data</div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Docket Alerts */}
        {urgent.length > 0 && (
          <Card className="border-red-200">
            <CardHeader>
              <CardTitle className="text-red-600 flex items-center gap-2">
                <AlertTriangle className="h-5 w-5" />
                Overdue Deadlines
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Event</TableHead>
                    <TableHead>Due Date</TableHead>
                    <TableHead>Assignee</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {urgent.map((event) => (
                    <TableRow key={event.id}>
                      <TableCell>{event.description}</TableCell>
                      <TableCell className="text-red-600">{new Date(event.due_date).toLocaleDateString()}</TableCell>
                      <TableCell>{event.assignee || "—"}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        )}
      </div>
    </main>
  );
}
