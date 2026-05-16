"""Patent AI services (copilot, claim drafting, analysis)."""

import os
from typing import Optional
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class PatentCopilot:
    """AI assistant for patent research and analysis."""

    @staticmethod
    def search_similar_patents(query: str, limit: int = 10) -> list[dict]:
        """Search patents semantically (embedding-based)."""
        # TODO: Implement embeddings search with pgvector
        # For now, return stub
        return [
            {
                "id": "stub-1",
                "title": f"Patent similar to: {query}",
                "relevance_score": 0.85,
                "abstract": "This is a placeholder patent matching your query.",
            }
        ]

    @staticmethod
    def summarize_claims(claims_text: str) -> str:
        """Summarize patent claims using AI."""
        if not claims_text:
            return "No claims to summarize."

        message = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize these patent claims in 2-3 sentences:\n\n{claims_text}",
                }
            ],
        )
        return message.content[0].text


class ClaimDraftingAssistant:
    """AI-powered claim drafting from invention disclosure."""

    @staticmethod
    def draft_claims_from_disclosure(disclosure_text: str, num_variants: int = 3) -> list[str]:
        """Generate claim variants from invention disclosure."""
        if not disclosure_text:
            return ["No disclosure provided."]

        prompt = f"""You are an expert patent claim drafter. Based on this invention disclosure,
generate {num_variants} different independent claims with 2-3 dependent claims each.

INVENTION DISCLOSURE:
{disclosure_text}

Requirements:
- Each independent claim should be progressively broader
- Use proper patent claim language
- Include method/apparatus variations
- Ensure claims are novel and non-obvious

Return only the claims, numbered clearly."""

        message = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )

        # Simple splitting by variant (in production, use better parsing)
        response_text = message.content[0].text
        variants = [response_text]  # Return full response for MVP

        return variants

    @staticmethod
    def draft_abstract_from_description(description: str) -> str:
        """Generate patent abstract from description."""
        if not description:
            return "No description provided."

        message = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=200,
            messages=[
                {
                    "role": "user",
                    "content": f"""Write a concise patent abstract (100-150 words) from this description:

{description}

Abstract should briefly describe:
1. What the invention is
2. The technical problem it solves
3. The key innovation""",
                }
            ],
        )
        return message.content[0].text


class PatentQualityScorer:
    """Score patent quality and enforceability."""

    @staticmethod
    def score_claims(patent_id: str, claims_text: str) -> dict:
        """Score claims on multiple dimensions."""
        # TODO: Implement LLM-based scoring
        return {
            "clarity": 4.2,
            "scope": 3.8,
            "validity": 4.0,
            "enforceability": 3.9,
            "novelty": 4.1,
            "overall_score": 4.0,
            "feedback": "Claims are well-structured. Consider broadening independent claims.",
        }
