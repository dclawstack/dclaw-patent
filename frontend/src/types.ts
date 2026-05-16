export interface Patent {
  id: string;
  patent_number: string;
  title: string;
  abstract: string;
  claims: string[];
  description?: string;
  filing_date: string;
  issue_date?: string;
  status: "drafted" | "filed" | "prosecution" | "issued" | "abandoned" | "lapsed";
  applicant: string;
  inventors?: string[];
  technology_category?: string;
  jurisdiction: string;
  extra_metadata?: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface PatentList {
  items: Patent[];
  total: number;
  limit: number;
  offset: number;
}

export interface DocketEvent {
  id: string;
  patent_id: string;
  event_type: "filing" | "response_due" | "maintenance_fee" | "prosecution_update" | "custom";
  due_date: string;
  description: string;
  status: "pending" | "completed" | "overdue";
  assignee?: string;
  created_at: string;
  updated_at: string;
}

export interface DocketAlerts {
  urgent: DocketEvent[];
  upcoming: DocketEvent[];
}

export interface PriorArt {
  id: string;
  patent_id: string;
  source_patent_number: string;
  source_title: string;
  relevance_score: number;
  claim_mapping?: Record<string, unknown>;
  analysis_notes?: string;
  created_at: string;
  updated_at: string;
}

export interface PriorArtList {
  items: PriorArt[];
  total: number;
  limit: number;
  offset: number;
}

export interface PatentSearchResult {
  id?: string;
  patent_number?: string;
  title?: string;
  abstract?: string;
  status?: string;
  jurisdiction?: string;
  relevance_score?: number;
  distance?: number;
  source: string;
  date?: string;
}

export interface PatentSearchResponse {
  query: string;
  results: PatentSearchResult[];
  total: number;
}

export interface DraftedClaim {
  claim_number: number;
  claim_text: string;
}

export interface DraftClaimsResponse {
  claims: DraftedClaim[];
  notes: string;
}

export interface ExaminerPrediction {
  patent_id: string;
  allowance_probability: number;
  confidence: number;
  suggested_amendments: string[];
  factors: string[];
}
