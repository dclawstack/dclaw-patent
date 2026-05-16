"""Patent AI services (copilot, claim drafting, analysis)."""

import os
import json
from typing import Optional
from anthropic import Anthropic

api_key = os.getenv("ANTHROPIC_API_KEY", "")
client = Anthropic(api_key=api_key) if api_key else None


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

        if not client:
            return "Claude API not configured. Please set ANTHROPIC_API_KEY."

        try:
            message = client.messages.create(
                model="claude-opus-4-7",
                max_tokens=500,
                messages=[
                    {
                        "role": "user",
                        "content": f"""You are an expert patent attorney. Summarize these patent claims in 2-3 clear, concise sentences:

{claims_text}

Focus on: What the invention does, its key innovation, and practical application.""",
                    }
                ],
            )
            return message.content[0].text
        except Exception as e:
            return f"Error summarizing claims: {str(e)}"


class ClaimDraftingAssistant:
    """AI-powered claim drafting from invention disclosure."""

    @staticmethod
    def draft_claims_from_disclosure(disclosure_text: str, num_variants: int = 3) -> list[str]:
        """Generate claim variants from invention disclosure."""
        if not disclosure_text:
            return ["No disclosure provided."]

        if not client:
            return ["Claude API not configured. Please set ANTHROPIC_API_KEY."]

        try:
            prompt = f"""You are an expert patent claim drafter specializing in technical innovations.
Based on this invention disclosure, generate {num_variants} different claim variants, each with an independent claim followed by 2-3 dependent claims.

INVENTION DISCLOSURE:
{disclosure_text}

REQUIREMENTS FOR EACH VARIANT:
- Independent claim should be broad but specific to the invention
- Use proper patent claim language (method, apparatus, system, etc.)
- Dependent claims add limitations and specific features
- Claims should cover different aspects (method, apparatus, system, computer-readable medium)
- Ensure claims are novel and non-obvious based on the disclosure
- Each variant should provide different claim scope

FORMAT OUTPUT AS:
VARIANT 1:
1. [Independent claim]
2. The method of claim 1, wherein...
3. The method of claim 1, wherein...

VARIANT 2:
[etc.]

Be specific to the disclosure provided. Use technical terms from the disclosure."""

            message = client.messages.create(
                model="claude-opus-4-7",
                max_tokens=3000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text

            # Parse variants by splitting on "VARIANT N"
            variants = []
            parts = response_text.split("VARIANT ")
            for i, part in enumerate(parts):
                if i == 0:
                    continue
                variant = part.strip()
                if variant:
                    variants.append(f"VARIANT {variant}")

            return variants if variants else [response_text]
        except Exception as e:
            return [f"Error drafting claims: {str(e)}"]

    @staticmethod
    def draft_abstract_from_description(description: str) -> str:
        """Generate patent abstract from description."""
        if not description:
            return "No description provided."

        if not client:
            return "Claude API not configured. Please set ANTHROPIC_API_KEY."

        try:
            message = client.messages.create(
                model="claude-opus-4-7",
                max_tokens=250,
                temperature=0.5,
                messages=[
                    {
                        "role": "user",
                        "content": f"""You are an expert patent attorney. Write a concise, professional patent abstract (100-150 words) from this description:

DESCRIPTION:
{description}

The abstract must:
1. Clearly state what the invention is (the technical solution)
2. Identify the technical problem it solves
3. Highlight the key innovation or improvement
4. Use clear, professional patent language
5. Be suitable for USPTO filing

Abstract:""",
                    }
                ],
            )
            return message.content[0].text.strip()
        except Exception as e:
            return f"Error drafting abstract: {str(e)}"


class PatentQualityScorer:
    """Score patent quality and enforceability."""

    @staticmethod
    def score_claims(patent_id: str, claims_text: str) -> dict:
        """Score claims on multiple dimensions."""
        if not claims_text:
            return {
                "clarity": 0,
                "scope": 0,
                "validity": 0,
                "enforceability": 0,
                "novelty": 0,
                "overall_score": 0,
                "feedback": "No claims to score.",
            }

        if not client:
            return {
                "clarity": 3.0,
                "scope": 3.0,
                "validity": 3.0,
                "enforceability": 3.0,
                "novelty": 3.0,
                "overall_score": 3.0,
                "feedback": "Claude API not available. Placeholder scoring.",
            }

        try:
            prompt = f"""You are an expert patent attorney and claim analyst. Score these patent claims on 5 dimensions (1-5 scale).

CLAIMS TO SCORE:
{claims_text}

SCORING DIMENSIONS:
1. CLARITY (1-5): Are claims written clearly and unambiguously?
2. SCOPE (1-5): Do independent claims have appropriate breadth?
3. VALIDITY (1-5): Will these survive USPTO examination?
4. ENFORCEABILITY (1-5): Will courts enforce these claims?
5. NOVELTY (1-5): How novel are these claims?

Respond in JSON format only:
{{
  "clarity": <score>,
  "scope": <score>,
  "validity": <score>,
  "enforceability": <score>,
  "novelty": <score>,
  "feedback": "<2-3 sentence improvement suggestion>"
}}"""

            message = client.messages.create(
                model="claude-opus-4-7",
                max_tokens=500,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text

            # Parse JSON response
            try:
                # Try to extract JSON from response
                import re
                json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
                if json_match:
                    scores = json.loads(json_match.group())
                else:
                    scores = json.loads(response_text)

                # Calculate overall score
                overall = (
                    scores.get("clarity", 3)
                    + scores.get("scope", 3)
                    + scores.get("validity", 3)
                    + scores.get("enforceability", 3)
                    + scores.get("novelty", 3)
                ) / 5

                return {
                    "clarity": scores.get("clarity", 3),
                    "scope": scores.get("scope", 3),
                    "validity": scores.get("validity", 3),
                    "enforceability": scores.get("enforceability", 3),
                    "novelty": scores.get("novelty", 3),
                    "overall_score": round(overall, 2),
                    "feedback": scores.get("feedback", "See individual scores above."),
                }
            except json.JSONDecodeError:
                return {
                    "clarity": 3.5,
                    "scope": 3.5,
                    "validity": 3.5,
                    "enforceability": 3.5,
                    "novelty": 3.5,
                    "overall_score": 3.5,
                    "feedback": "Scoring completed but parsing failed. Review response.",
                }
        except Exception as e:
            return {
                "clarity": 0,
                "scope": 0,
                "validity": 0,
                "enforceability": 0,
                "novelty": 0,
                "overall_score": 0,
                "feedback": f"Error scoring claims: {str(e)}",
            }
