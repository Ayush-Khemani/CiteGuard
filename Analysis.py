"""
API routes for text analysis - the core plagiarism prevention endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import logging

from app.services.similarity import get_similarity_service
from app.services.paraphrasing import ParaphrasingService
from app.services.citation import CitationGenerator, SourceMetadata, CitationStyle

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
    overall_score: float = Field(..., description="Health score 0-100 (100 = no issues)")
    flagged_sections: List[Dict]
    recommendations: List[Dict]
    total_matches: int
    sources_checked: int


class ParaphraseRequest(BaseModel):
    """Request to get paraphrasing suggestions."""
    text: str = Field(..., min_length=5, max_length=1000)
    context: Optional[str] = Field(default=None, max_length=2000)
    num_alternatives: int = Field(default=3, ge=1, le=5)


class ParaphraseResponse(BaseModel):
    """Paraphrasing suggestions response."""
    original_text: str
    suggestions: List[Dict[str, str]]


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
    citation_style: CitationStyle = CitationStyle.APA


class CitationResponse(BaseModel):
    """Generated citation response."""
    full_citation: str
    in_text_citation: str
    style: str


# Endpoints
@router.post("/analyze", response_model=AnalyzeTextResponse)
async def analyze_text(
    request: AnalyzeTextRequest,
    background_tasks: BackgroundTasks
):
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
        
        logger.info(f"Analysis complete: {result['total_matches']} matches found")
        
        # TODO: Save analysis to database in background
        # background_tasks.add_task(save_analysis, result)
        
        return AnalyzeTextResponse(**result)
    
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/paraphrase", response_model=ParaphraseResponse)
async def paraphrase_text(request: ParaphraseRequest):
    """
    Get AI-powered paraphrasing suggestions.
    
    Helps students rephrase text to reduce similarity while
    maintaining meaning.
    """
    try:
        # Initialize paraphrasing service
        paraphrasing_service = ParaphrasingService(use_anthropic=True)
        
        logger.info(f"Generating {request.num_alternatives} paraphrases")
        
        # Generate paraphrases
        suggestions = paraphrasing_service.generate_paraphrases(
            text=request.text,
            context=request.context,
            num_alternatives=request.num_alternatives
        )
        
        return ParaphraseResponse(
            original_text=request.text,
            suggestions=suggestions
        )
    
    except Exception as e:
        logger.error(f"Paraphrasing failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Paraphrasing failed: {str(e)}"
        )


@router.post("/citation/generate", response_model=CitationResponse)
async def generate_citation(request: GenerateCitationRequest):
    """
    Generate properly formatted citation.
    
    Takes source metadata and returns formatted citations
    in the requested style (APA, MLA, Chicago, etc.).
    """
    try:
        # Create metadata object
        metadata = SourceMetadata(
            title=request.title,
            authors=request.authors,
            year=request.year,
            publication_name=request.publication_name,
            volume=request.volume,
            issue=request.issue,
            pages=request.pages,
            url=request.url,
            doi=request.doi,
            source_type=request.source_type
        )
        
        # Generate citation
        citation_generator = CitationGenerator()
        citation = citation_generator.generate_citation(
            metadata,
            style=request.citation_style
        )
        
        return CitationResponse(
            full_citation=citation["full"],
            in_text_citation=citation["in_text"],
            style=request.citation_style.value
        )
    
    except Exception as e:
        logger.error(f"Citation generation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Citation generation failed: {str(e)}"
        )


@router.post("/citation/from-url")
async def generate_citation_from_url(url: str, style: CitationStyle = CitationStyle.APA):
    """
    Generate citation from URL.
    
    Attempts to extract metadata from URL and generate citation.
    Works with DOIs, arXiv, and some websites.
    """
    try:
        citation_generator = CitationGenerator()
        
        # Extract metadata from URL
        metadata = citation_generator.extract_metadata_from_url(url)
        
        if not metadata:
            raise HTTPException(
                status_code=400,
                detail="Could not extract metadata from URL"
            )
        
        # Generate citation
        citation = citation_generator.generate_citation(metadata, style)
        
        return {
            "citation": citation,
            "metadata": {
                "title": metadata.title,
                "authors": metadata.authors,
                "year": metadata.year,
                "url": metadata.url
            },
            "message": "Note: Metadata was auto-extracted and may need verification"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"URL citation generation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate citation from URL: {str(e)}"
        )


@router.get("/health")
async def analysis_health():
    """Health check for analysis service."""
    try:
        # Check if similarity model is loaded
        similarity_service = get_similarity_service()
        
        return {
            "status": "healthy",
            "similarity_model": similarity_service.model.get_sentence_embedding_dimension(),
            "threshold": similarity_service.threshold
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


# Batch endpoints for efficiency
@router.post("/analyze/batch")
async def analyze_batch(texts: List[str], sources: Optional[List[Dict]] = None):
    """
    Analyze multiple text segments at once.
    
    Useful for checking entire documents section by section.
    """
    try:
        similarity_service = get_similarity_service()
        
        results = []
        for i, text in enumerate(texts):
            result = similarity_service.analyze_document(
                document_text=text,
                sources=sources or []
            )
            result["section_index"] = i
            results.append(result)
        
        return {
            "total_sections": len(texts),
            "results": results
        }
    
    except Exception as e:
        logger.error(f"Batch analysis failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Batch analysis failed: {str(e)}"
        )