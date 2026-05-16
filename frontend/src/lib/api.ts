import { Patent, PatentList, DocketEvent, DocketAlerts, PriorArt, PriorArtList, PatentSearchResponse, PatentSearchResult, DraftClaimsResponse, ExaminerPrediction } from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function fetchJson<T>(path: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path}`;
  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });
  if (!response.ok) {
    const error = await response.text();
    throw new ApiError(`API error ${response.status}: ${error}`, response.status);
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return response.json();
}

export async function getHealth() {
  return fetchJson<{ status: string }>("/health/");
}

// Patents
export async function getPatents(params?: { status?: string; jurisdiction?: string; technology_category?: string; limit?: number; offset?: number }): Promise<PatentList> {
  const search = new URLSearchParams();
  if (params?.status) search.set("status", params.status);
  if (params?.jurisdiction) search.set("jurisdiction", params.jurisdiction);
  if (params?.technology_category) search.set("technology_category", params.technology_category);
  if (params?.limit) search.set("limit", String(params.limit));
  if (params?.offset) search.set("offset", String(params.offset));
  return fetchJson<PatentList>(`/api/v1/patents?${search.toString()}`);
}

export async function getPatent(id: string): Promise<Patent> {
  return fetchJson<Patent>(`/api/v1/patents/${id}`);
}

export async function createPatent(data: Omit<Patent, "id" | "created_at" | "updated_at">): Promise<Patent> {
  return fetchJson<Patent>("/api/v1/patents", { method: "POST", body: JSON.stringify(data) });
}

export async function updatePatent(id: string, data: Partial<Omit<Patent, "id" | "created_at" | "updated_at">>): Promise<Patent> {
  return fetchJson<Patent>(`/api/v1/patents/${id}`, { method: "PUT", body: JSON.stringify(data) });
}

export async function deletePatent(id: string): Promise<void> {
  return fetchJson<void>(`/api/v1/patents/${id}`, { method: "DELETE" });
}

// Dockets
export async function getDockets(params?: { patent_id?: string; limit?: number; offset?: number }): Promise<{ items: DocketEvent[]; total: number; limit: number; offset: number }> {
  const search = new URLSearchParams();
  if (params?.patent_id) search.set("patent_id", params.patent_id);
  if (params?.limit) search.set("limit", String(params.limit));
  if (params?.offset) search.set("offset", String(params.offset));
  return fetchJson(`/api/v1/dockets?${search.toString()}`);
}

export async function getDocketAlerts(days = 30): Promise<DocketAlerts> {
  return fetchJson<DocketAlerts>(`/api/v1/dockets/alerts/summary?days=${days}`);
}

export async function createDocket(data: Omit<DocketEvent, "id" | "created_at" | "updated_at">): Promise<DocketEvent> {
  return fetchJson<DocketEvent>("/api/v1/dockets", { method: "POST", body: JSON.stringify(data) });
}

export async function updateDocket(id: string, data: Partial<Omit<DocketEvent, "id" | "created_at" | "updated_at">>): Promise<DocketEvent> {
  return fetchJson<DocketEvent>(`/api/v1/dockets/${id}`, { method: "PUT", body: JSON.stringify(data) });
}

export async function deleteDocket(id: string): Promise<void> {
  return fetchJson<void>(`/api/v1/dockets/${id}`, { method: "DELETE" });
}

// Prior Art
export async function getPriorArts(params?: { patent_id?: string; limit?: number; offset?: number }): Promise<PriorArtList> {
  const search = new URLSearchParams();
  if (params?.patent_id) search.set("patent_id", params.patent_id);
  if (params?.limit) search.set("limit", String(params.limit));
  if (params?.offset) search.set("offset", String(params.offset));
  return fetchJson<PriorArtList>(`/api/v1/prior-art?${search.toString()}`);
}

export async function createPriorArt(data: Omit<PriorArt, "id" | "created_at" | "updated_at">): Promise<PriorArt> {
  return fetchJson<PriorArt>("/api/v1/prior-art", { method: "POST", body: JSON.stringify(data) });
}

export async function updatePriorArt(id: string, data: Partial<Omit<PriorArt, "id" | "created_at" | "updated_at">>): Promise<PriorArt> {
  return fetchJson<PriorArt>(`/api/v1/prior-art/${id}`, { method: "PUT", body: JSON.stringify(data) });
}

export async function deletePriorArt(id: string): Promise<void> {
  return fetchJson<void>(`/api/v1/prior-art/${id}`, { method: "DELETE" });
}

// AI
export async function aiPatentSearch(query: string, limit = 20): Promise<PatentSearchResponse> {
  return fetchJson<PatentSearchResponse>("/api/v1/ai/patent-search", {
    method: "POST",
    body: JSON.stringify({ query, limit }),
  });
}

export async function aiSimilarPatents(patentId: string): Promise<{ patent_id: string; results: PatentSearchResult[] }> {
  return fetchJson(`/api/v1/ai/similar-patents/${patentId}`, { method: "POST" });
}

export async function aiDraftClaims(description: string, numClaims = 5): Promise<DraftClaimsResponse> {
  return fetchJson<DraftClaimsResponse>("/api/v1/ai/draft-claims", {
    method: "POST",
    body: JSON.stringify({ invention_description: description, num_claims: numClaims }),
  });
}

export async function aiExaminerPrediction(patentId: string): Promise<ExaminerPrediction> {
  return fetchJson<ExaminerPrediction>(`/api/v1/ai/examiner-prediction/${patentId}`, { method: "POST" });
}

export { ApiError };
