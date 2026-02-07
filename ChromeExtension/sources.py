"""
Source management routes.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()


class Source(BaseModel):
    id: int
    title: str
    authors: List[str]
    url: str = None
    doi: str = None


@router.get("/", response_model=List[Source])
async def list_sources():
    """List user's saved sources."""
    # TODO: Implement database query
    return []


@router.post("/")
async def add_source(title: str, authors: List[str], url: str = None):
    """Add new source."""
    # TODO: Implement source creation
    return {"id": 1, "title": title}


@router.get("/{source_id}", response_model=Source)
async def get_source(source_id: int):
    """Get specific source."""
    # TODO: Implement database query
    raise HTTPException(status_code=404, detail="Source not found")


@router.delete("/{source_id}")
async def delete_source(source_id: int):
    """Delete source."""
    # TODO: Implement deletion
    return {"deleted": True}