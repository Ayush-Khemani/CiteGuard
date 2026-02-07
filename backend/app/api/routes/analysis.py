"""
API routes for text analysis - the core plagiarism prevention endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import logging

from app.services.similarity import get_similarity_service
from app.services.citation import CitationGenerator, CitationStyle
from app.services.paraphrasing import ParaphrasingService

logger = logging.getLogger(__name__)
router = APIRouter()


# Request/Response Models
class AnalyzeTextRequest(BaseModel):
    """Request to analyze text for similarity."""
    text: str = Field(..., min_length=10, max_length=100000)
    sources: Optional[List[Dict]] = Field(default=[], description="List of source texts to check against")
    threshold: Optional[float] = Field(default=0.85, ge=0.0, le=1.0)


class AnalyzeTextResponse(BaseModel):
    """Response from text analysis."""
    plagiarism_score: float = Field(..., ge=0.0, le=1.0, description="Plagiarism score 0-1")
    flagged_sections: int = Field(default=0, description="Number of flagged sections")
    recommendations: List[str] = Field(default=[], description="Recommendations to improve")
    total_matches: int = Field(default=0, description="Total matches found")
    sources_checked: int = Field(default=0, description="Number of sources checked")


class ParaphraseRequest(BaseModel):
    """Request to get paraphrasing suggestions."""
    text: str = Field(..., min_length=5, max_length=1000)
    context: Optional[str] = Field(default=None, max_length=2000)
    num_alternatives: int = Field(default=3, ge=1, le=5)


class ParaphraseResponse(BaseModel):
    """Paraphrasing suggestions response."""
    paraphrased_text: str = Field(..., description="Paraphrased version of text")
    style: str = Field(default="standard", description="Style used for paraphrasing")


class GenerateCitationRequest(BaseModel):
    """Request to generate citation."""
    title: str
    authors: List[str]
    year: Optional[int] = None
    publication_name: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    url: Optional[str] = None
    doi: Optional[str] = None
    source_type: str = "article"
    citation_style: str = "APA"


class CitationResponse(BaseModel):
    """Generated citation response."""
    formatted_citation: str = Field(..., description="Formatted citation string")
    style: str = Field(..., description="Citation style used")


# Endpoints
@router.post("/analyze", response_model=AnalyzeTextResponse)
async def analyze_text(request: AnalyzeTextRequest):
    """
    Analyze text for potential plagiarism.
    
    This is the core endpoint that checks text against sources
    and returns similarity scores and recommendations.
    """
    try:
        # Get similarity service
        similarity_service = get_similarity_service(threshold=request.threshold)
        
        # Perform analysis
        logger.info(f"Analyzing text of length {len(request.text)} chars")
        
        result = similarity_service.analyze_document(
            document_text=request.text,
            sources=request.sources or []
        )
        
        logger.info(f"Analysis complete: {result.get('total_matches', 0)} matches found")
        
        return AnalyzeTextResponse(**result)
    
    except Exception as e:
        logger.error(f"Error analyzing document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/paraphrase", response_model=ParaphraseResponse)
async def paraphrase(request: ParaphraseRequest):
    """
    Get paraphrasing suggestions for text.
    
    Returns paraphrased alternative for content
    while maintaining the original meaning.
    """
    try:
        service = ParaphrasingService()
        
        # Use the style if provided, otherwise use context
        style = request.context or "standard"
        paraphrased = service.paraphrase(request.text, style)
        
        return ParaphraseResponse(
            paraphrased_text=paraphrased,
            style=style
        )
    
    except Exception as e:
        logger.error(f"Error in paraphrasing: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/citation", response_model=CitationResponse)
async def generate_citation(request: GenerateCitationRequest):
    """
    Generate a properly formatted citation.
    
    Supports multiple citation styles: APA, MLA, Chicago, Harvard, IEEE
    """
    try:
        citation_gen = CitationGenerator()
        
        # Convert string style to enum
        try:
            style = CitationStyle[request.citation_style.upper()]
        except KeyError:
            style = CitationStyle.APA
        
        result = citation_gen.generate_citation(
            metadata={
                "title": request.title,
                "authors": request.authors,
                "year": request.year,
                "publication_name": request.publication_name,
                "source_type": request.source_type,
                "url": request.url,
                "doi": request.doi,
            },
            style=style
        )
        
        return CitationResponse(
            formatted_citation=result.get("full", result.get("formatted", "No citation generated")),
            style=request.citation_style
        )
    
    except Exception as e:
        logger.error(f"Error generating citation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/health")
async def health():
    """Health check for analysis service."""
    return {
        "status": "healthy",
        "service": "analysis",
        "features": {
            "plagiarism_detection": "ready",
            "citation_generation": "ready",
            "paraphrasing": "pending_llm_integration"
        }
    }
