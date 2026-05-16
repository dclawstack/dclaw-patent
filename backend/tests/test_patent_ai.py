"""Tests for patent AI services."""

import pytest
from app.services.patent_ai import PatentCopilot, ClaimDraftingAssistant, PatentQualityScorer


class TestPatentCopilot:
    """Test patent copilot functionality."""

    def test_search_similar_patents(self):
        """Test semantic patent search."""
        results = PatentCopilot.search_similar_patents("quantum computing", limit=5)
        assert isinstance(results, list)
        assert len(results) <= 5
        if results:
            assert "id" in results[0]
            assert "title" in results[0]
            assert "relevance_score" in results[0]

    def test_summarize_claims_empty(self):
        """Test summarizing empty claims."""
        result = PatentCopilot.summarize_claims("")
        assert isinstance(result, str)

    def test_summarize_claims_with_content(self):
        """Test summarizing actual claims."""
        claims = """1. A method for quantum error correction comprising:
        - applying a stabilizer code
        - measuring syndrome data
        - performing a correction operation"""
        result = PatentCopilot.summarize_claims(claims)
        assert isinstance(result, str)
        assert len(result) > 0


class TestClaimDraftingAssistant:
    """Test AI claim drafting."""

    def test_draft_claims_from_disclosure_empty(self):
        """Test drafting from empty disclosure."""
        results = ClaimDraftingAssistant.draft_claims_from_disclosure("")
        assert isinstance(results, list)
        assert len(results) > 0

    def test_draft_abstract_from_description_empty(self):
        """Test abstract generation from empty description."""
        result = ClaimDraftingAssistant.draft_abstract_from_description("")
        assert isinstance(result, str)

    def test_draft_abstract_with_content(self):
        """Test abstract generation with content."""
        description = """A system and method for machine learning model compression
        that reduces model size by 80% while maintaining accuracy through
        knowledge distillation and quantization."""
        result = ClaimDraftingAssistant.draft_abstract_from_description(description)
        assert isinstance(result, str)
        assert len(result) > 20


class TestPatentQualityScorer:
    """Test patent quality scoring."""

    def test_score_claims(self):
        """Test claim quality scoring."""
        claims = "1. A method comprising step A and step B."
        scores = PatentQualityScorer.score_claims("test-id", claims)
        assert "clarity" in scores
        assert "scope" in scores
        assert "validity" in scores
        assert "enforceability" in scores
        assert "overall_score" in scores
        # All scores should be 0-5
        for key in ["clarity", "scope", "validity", "enforceability", "overall_score"]:
            assert 0 <= scores[key] <= 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
