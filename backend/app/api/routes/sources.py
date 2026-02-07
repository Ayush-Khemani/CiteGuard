from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl

router = APIRouter(prefix="/api/v1/sources", tags=["sources"])

# Request/Response Models
class SourceCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    url: HttpUrl
    authors: Optional[List[str]] = None
    publication_year: Optional[int] = Field(None, ge=1900, le=2100)
    source_type: str = Field("article", pattern="book|article|journal|website|thesis")
    abstract: Optional[str] = None
    citations: Optional[int] = Field(None, ge=0)
    tags: Optional[List[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Deep Learning for NLP",
                "url": "https://example.com/paper",
                "authors": ["John Doe", "Jane Smith"],
                "publication_year": 2024,
                "source_type": "article",
                "abstract": "This paper discusses...",
                "citations": 42,
                "tags": ["AI", "NLP", "machine-learning"]
            }
        }

class SourceUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    url: Optional[HttpUrl] = None
    authors: Optional[List[str]] = None
    publication_year: Optional[int] = Field(None, ge=1900, le=2100)
    source_type: Optional[str] = None
    abstract: Optional[str] = None
    citations: Optional[int] = Field(None, ge=0)
    tags: Optional[List[str]] = None

class SourceResponse(BaseModel):
    id: int
    title: str
    url: str
    authors: Optional[List[str]]
    publication_year: Optional[int]
    source_type: str
    abstract: Optional[str]
    citations: Optional[int]
    tags: Optional[List[str]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SourceSearchParams(BaseModel):
    query: str
    source_type: Optional[str] = None
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    min_citations: Optional[int] = None

# Endpoints
@router.get("/", response_model=List[SourceResponse])
async def list_sources(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    source_type: Optional[str] = None
):
    """List all sources in library with optional filtering"""
    # TODO: Implement database query with pagination and filtering
    return []

@router.post("/", response_model=SourceResponse, status_code=201)
async def create_source(source: SourceCreate):
    """Add a new source to the library"""
    # TODO: Implement database save with duplicate checking
    return SourceResponse(
        id=1,
        title=source.title,
        url=str(source.url),
        authors=source.authors,
        publication_year=source.publication_year,
        source_type=source.source_type,
        abstract=source.abstract,
        citations=source.citations,
        tags=source.tags,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@router.get("/{source_id}", response_model=SourceResponse)
async def get_source(source_id: int):
    """Get a single source by ID"""
    # TODO: Implement database fetch
    raise HTTPException(status_code=404, detail="Source not found")

@router.put("/{source_id}", response_model=SourceResponse)
async def update_source(source_id: int, source: SourceUpdate):
    """Update source metadata"""
    # TODO: Implement database update
    raise HTTPException(status_code=404, detail="Source not found")

@router.delete("/{source_id}", status_code=204)
async def delete_source(source_id: int):
    """Remove a source from the library"""
    # TODO: Implement database delete
    raise HTTPException(status_code=404, detail="Source not found")

@router.post("/search", response_model=List[SourceResponse])
async def search_sources(
    query: str = Query(..., min_length=1),
    source_type: Optional[str] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    min_citations: Optional[int] = Query(None, ge=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """Search sources by title, authors, keywords, or filters"""
    # TODO: Implement full-text search with filters
    return []

@router.post("/{source_id}/cite")
async def get_source_citations(source_id: int, format: str = Query("apa", pattern="apa|mla|chicago|harvard|ieee")):
    """Get formatted citations for a source"""
    # TODO: Implement citation generation using citation service
    raise HTTPException(status_code=404, detail="Source not found")

@router.get("/trending", response_model=List[SourceResponse])
async def get_trending_sources(limit: int = Query(10, ge=1, le=50)):
    """Get trending sources based on usage"""
    # TODO: Implement trending algorithm
    return []
