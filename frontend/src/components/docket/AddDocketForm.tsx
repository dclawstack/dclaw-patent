"use client";

import { useState } from "react";
import { createDocket } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

export default function AddDocketForm({ patentId, onCreated }: { patentId: string; onCreated: () => void }) {
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    const form = new FormData(e.currentTarget);
    const data = {
      patent_id: patentId,
      event_type: form.get("event_type") as string,
      due_date: new Date(form.get("due_date") as string).toISOString(),
      description: form.get("description") as string,
      status: "pending",
      assignee: (form.get("assignee") as string) || undefined,
    };
    try {
      await createDocket(data as any);
      onCreated();
      setOpen(false);
      (e.target as HTMLFormElement).reset();
    } catch (err) {
      console.error(err);
      alert("Failed to create docket event");
    } finally {
      setLoading(false);
    }
  }

  if (!open) {
    return (
      <Button size="sm" variant="outline" onClick={() => setOpen(true)}>
        + Add Docket Event
      </Button>
    );
  }

  return (
    <Card className="border-blue-200">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm">Add Docket Event</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-3">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="space-y-1">
              <Label htmlFor="event_type" className="text-xs">Event Type</Label>
              <select
                id="event_type"
                name="event_type"
                required
                className="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              >
                <option value="filing">Filing</option>
                <option value="response_due">Response Due</option>
                <option value="maintenance_fee">Maintenance Fee</option>
                <option value="prosecution_update">Prosecution Update</option>
                <option value="custom">Custom</option>
              </select>
            </div>
            <div className="space-y-1">
              <Label htmlFor="due_date" className="text-xs">Due Date</Label>
              <Input id="due_date" name="due_date" type="date" required />
            </div>
          </div>
          <div className="space-y-1">
            <Label htmlFor="description" className="text-xs">Description</Label>
            <Textarea id="description" name="description" required placeholder="e.g. Office action response due" />
          </div>
          <div className="space-y-1">
            <Label htmlFor="assignee" className="text-xs">Assignee</Label>
            <Input id="assignee" name="assignee" placeholder="Responsible person or firm" />
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
