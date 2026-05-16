"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getDockets, getDocketAlerts } from "@/lib/api";
import { DocketEvent } from "@/types";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { ArrowLeft, AlertTriangle, Calendar, CheckCircle, Clock } from "lucide-react";

export default function DocketPage() {
  const [events, setEvents] = useState<DocketEvent[]>([]);
  const [urgent, setUrgent] = useState<DocketEvent[]>([]);
  const [upcoming, setUpcoming] = useState<DocketEvent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [all, alerts] = await Promise.all([
          getDockets({ limit: 100 }),
          getDocketAlerts(30),
        ]);
        setEvents(all.items);
        setUrgent(alerts.urgent);
        setUpcoming(alerts.upcoming);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const today = new Date();

  function eventBadge(event: DocketEvent) {
    const due = new Date(event.due_date);
    const diff = Math.ceil((due.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
    if (event.status === "completed") return <Badge variant="secondary"><CheckCircle className="h-3 w-3 mr-1" />Completed</Badge>;
    if (diff < 0) return <Badge variant="destructive"><AlertTriangle className="h-3 w-3 mr-1" />Overdue</Badge>;
    if (diff <= 7) return <Badge className="bg-yellow-500 text-white"><Clock className="h-3 w-3 mr-1" />{diff}d left</Badge>;
    return <Badge variant="outline"><Calendar className="h-3 w-3 mr-1" />{diff}d left</Badge>;
  }

  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto space-y-6">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm">
            <Link href="/" className="flex items-center">
              <ArrowLeft className="h-4 w-4 mr-1" />
              Back
            </Link>
          </Button>
          <h1 className="text-2xl font-bold tracking-tight">Docket Calendar</h1>
        </div>

        {/* Alerts */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card className={urgent.length > 0 ? "border-red-200" : ""}>
            <CardHeader>
              <CardTitle className="text-red-600 flex items-center gap-2">
                <AlertTriangle className="h-5 w-5" />
                Overdue ({urgent.length})
              </CardTitle>
            </CardHeader>
            <CardContent>
              {urgent.length === 0 ? (
                <div className="text-sm text-gray-500">No overdue events. Great job!</div>
              ) : (
                <div className="space-y-2">
                  {urgent.map((e) => (
                    <div key={e.id} className="flex items-center justify-between text-sm">
                      <span className="font-medium">{e.description}</span>
                      <span className="text-red-600">{new Date(e.due_date).toLocaleDateString()}</span>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Clock className="h-5 w-5" />
                Upcoming 30 Days ({upcoming.length})
              </CardTitle>
            </CardHeader>
            <CardContent>
              {upcoming.length === 0 ? (
                <div className="text-sm text-gray-500">No upcoming deadlines.</div>
              ) : (
                <div className="space-y-2">
                  {upcoming.map((e) => (
                    <div key={e.id} className="flex items-center justify-between text-sm">
                      <span className="font-medium">{e.description}</span>
                      <span className="text-gray-600">{new Date(e.due_date).toLocaleDateString()}</span>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Full list */}
        <Card>
          <CardHeader>
            <CardTitle>All Docket Events</CardTitle>
            <CardDescription>Complete deadline tracker</CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-sm text-gray-500">Loading...</div>
            ) : events.length === 0 ? (
              <div className="text-sm text-gray-500">No docket events yet.</div>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Type</TableHead>
                    <TableHead>Description</TableHead>
                    <TableHead>Due Date</TableHead>
                    <TableHead>Urgency</TableHead>
                    <TableHead>Assignee</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {events.map((e) => (
                    <TableRow key={e.id}>
                      <TableCell className="capitalize">{e.event_type.replace("_", " ")}</TableCell>
                      <TableCell>{e.description}</TableCell>
                      <TableCell>{new Date(e.due_date).toLocaleDateString()}</TableCell>
                      <TableCell>{eventBadge(e)}</TableCell>
                      <TableCell>{e.assignee || "—"}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </CardContent>
        </Card>
      </div>
    </main>
  );
}
