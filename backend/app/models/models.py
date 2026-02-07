"""
SQLAlchemy database models for CiteGuard.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()


class CitationStyle(str, enum.Enum):
    """Supported citation styles."""
    APA = "APA"
    MLA = "MLA"
    CHICAGO = "Chicago"
    HARVARD = "Harvard"
    IEEE = "IEEE"


class User(Base):
    """User model for authentication and preferences."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    
    # Preferences
    preferred_citation_style = Column(Enum(CitationStyle), default=CitationStyle.APA)
    similarity_threshold = Column(Float, default=0.85)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    sources = relationship("Source", back_populates="user", cascade="all, delete-orphan")


class Document(Base):
    """User documents being analyzed."""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Document info
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    word_count = Column(Integer, default=0)
    
    # Analysis results
    similarity_score = Column(Float, default=0.0)
    citation_health_score = Column(Float, default=0.0)  # 0-100
    flagged_sections = Column(JSON, default=list)  # List of problematic sections
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_analyzed = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="documents")
    citations = relationship("Citation", back_populates="document", cascade="all, delete-orphan")
    analysis_history = relationship("AnalysisHistory", back_populates="document", cascade="all, delete-orphan")


class Source(Base):
    """External sources for citation and similarity checking."""
    __tablename__ = "sources"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Source information
    title = Column(String, nullable=False)
    authors = Column(JSON, default=list)  # List of author names
    publication_year = Column(Integer)
    publication_name = Column(String)  # Journal, book, website name
    url = Column(String)
    doi = Column(String, unique=True, index=True)
    
    # Source type
    source_type = Column(String)  # "journal", "book", "website", "conference"
    
    # Full text for similarity checking (if available)
    full_text = Column(Text)
    abstract = Column(Text)
    
    # Embeddings for similarity (stored as JSON for simplicity)
    embeddings = Column(JSON)  # In production, use vector DB
    
    # Metadata
    added_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="sources")


class Citation(Base):
    """Generated citations for documents."""
    __tablename__ = "citations"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)
    
    # Citation info
    primary_citation = Column(Text, nullable=False)  # Full formatted citation
    in_text_citation = Column(Text, nullable=False)  # For in-text reference
    citation_style = Column(Enum(CitationStyle), default=CitationStyle.APA)
    
    # Position in document
    page_number = Column(Integer)
    text_snippet = Column(Text)  # Text being cited
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    document = relationship("Document", back_populates="citations")


class AnalysisHistory(Base):
    """Track analysis results over time."""
    __tablename__ = "analysis_history"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    
    # Analysis snapshot
    overall_score = Column(Float)  # 0-100 (100 = no plagiarism)
    total_matches = Column(Integer)
    analysis_data = Column(JSON)  # Full analysis results
    
    # Metadata
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    document = relationship("Document", back_populates="analysis_history")
