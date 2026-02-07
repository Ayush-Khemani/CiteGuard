"""
Citation generation service supporting multiple citation styles.
Generates properly formatted citations from metadata.
"""
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass


class CitationStyle(str, Enum):
    """Supported citation styles."""
    APA = "APA"
    MLA = "MLA"
    CHICAGO = "Chicago"
    HARVARD = "Harvard"
    IEEE = "IEEE"


@dataclass
class SourceMetadata:
    """Metadata for a source to be cited."""
    title: str
    authors: List[str] = None  # ["First Last", "First Last"]
    year: Optional[int] = None
    publication_name: Optional[str] = None  # Journal, book publisher, website
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    url: Optional[str] = None
    doi: Optional[str] = None
    access_date: Optional[str] = None  # For websites
    source_type: str = "article"  # article, book, website, conference
    
    def __post_init__(self):
        if self.authors is None:
            self.authors = []


class CitationGenerator:
    """Generates citations in various academic formats."""
    
    def __init__(self):
        """Initialize citation generator."""
        pass
    
    def _format_authors_apa(self, authors: List[str]) -> str:
        """Format authors for APA style."""
        if not authors:
            return ""
        
        formatted = []
        for author in authors[:20]:  # APA limits to 20 authors
            parts = author.split()
            if len(parts) >= 2:
                # Last, F. M.
                last = parts[-1]
                initials = "".join([f"{p[0]}." for p in parts[:-1]])
                formatted.append(f"{last}, {initials}")
            else:
                formatted.append(author)
        
        if len(authors) == 1:
            return formatted[0]
        elif len(authors) == 2:
            return f"{formatted[0]}, & {formatted[1]}"
        else:
            # 3+ authors
            return ", ".join(formatted[:-1]) + f", & {formatted[-1]}"
    
    def _format_authors_mla(self, authors: List[str]) -> str:
        """Format authors for MLA style."""
        if not authors:
            return ""
        
        if len(authors) == 1:
            parts = authors[0].split()
            if len(parts) >= 2:
                return f"{parts[-1]}, {' '.join(parts[:-1])}"
            return authors[0]
        elif len(authors) == 2:
            first = authors[0]
            parts = first.split()
            first_formatted = f"{parts[-1]}, {' '.join(parts[:-1])}" if len(parts) >= 2 else first
            return f"{first_formatted}, and {authors[1]}"
        else:
            # 3+ authors: first author + "et al."
            parts = authors[0].split()
            first_formatted = f"{parts[-1]}, {' '.join(parts[:-1])}" if len(parts) >= 2 else authors[0]
            return f"{first_formatted}, et al."
    
    def generate_citation(
        self,
        metadata: Dict,
        style: CitationStyle = CitationStyle.APA
    ) -> Dict[str, str]:
        """
        Generate citation in specified style.
        
        Returns:
            Dict with 'full' (bibliography entry) and 'in_text' (in-text citation)
        """
        if style == CitationStyle.APA:
            return self._generate_apa(metadata)
        elif style == CitationStyle.MLA:
            return self._generate_mla(metadata)
        elif style == CitationStyle.CHICAGO:
            return self._generate_chicago(metadata)
        elif style == CitationStyle.HARVARD:
            return self._generate_harvard(metadata)
        elif style == CitationStyle.IEEE:
            return self._generate_ieee(metadata)
        else:
            return self._generate_apa(metadata)  # Default to APA
    
    def _generate_apa(self, metadata: Dict) -> Dict[str, str]:
        """Generate APA format citation."""
        authors = metadata.get("authors", [])
        title = metadata.get("title", "")
        year = metadata.get("year")
        pub_name = metadata.get("publication_name", "")
        url = metadata.get("url", "")
        
        author_str = self._format_authors_apa(authors) if authors else "Unknown"
        
        full = f"{author_str} ({year or 'n.d.'}). {title}. {pub_name}."
        if url:
            full += f" Retrieved from {url}"
        
        in_text = f"({author_str.split(',')[0]} {year or 'n.d.'})" if authors else "Unknown"
        
        return {
            "full": full,
            "in_text": in_text
        }
    
    def _generate_mla(self, metadata: Dict) -> Dict[str, str]:
        """Generate MLA format citation."""
        authors = metadata.get("authors", [])
        title = metadata.get("title", "")
        pub_name = metadata.get("publication_name", "")
        year = metadata.get("year")
        
        author_str = self._format_authors_mla(authors) if authors else "Unknown"
        
        full = f"{author_str}. \"{title}.\" {pub_name}, {year or 'n.d.'}."
        in_text = f"({author_str.split(',')[0] if ',' in author_str else author_str})"
        
        return {
            "full": full,
            "in_text": in_text
        }
    
    def _generate_chicago(self, metadata: Dict) -> Dict[str, str]:
        """Generate Chicago style citation."""
        authors = metadata.get("authors", [])
        title = metadata.get("title", "")
        pub_name = metadata.get("publication_name", "")
        year = metadata.get("year")
        
        author_str = ", ".join(authors) if authors else "Unknown"
        
        full = f"{author_str}. \"{title}.\" {pub_name} ({year or 'n.d.'})."
        in_text = f"({author_str.split(',')[0]} {year or 'n.d.'})"
        
        return {
            "full": full,
            "in_text": in_text
        }
    
    def _generate_harvard(self, metadata: Dict) -> Dict[str, str]:
        """Generate Harvard style citation."""
        authors = metadata.get("authors", [])
        title = metadata.get("title", "")
        pub_name = metadata.get("publication_name", "")
        year = metadata.get("year")
        
        author_str = ", ".join(authors) if authors else "Unknown"
        
        full = f"{author_str}, {year or 'n.d.d'}. {title}. {pub_name}."
        in_text = f"({author_str.split(',')[0]} {year or 'n.d.'})"
        
        return {
            "full": full,
            "in_text": in_text
        }
    
    def _generate_ieee(self, metadata: Dict) -> Dict[str, str]:
        """Generate IEEE style citation."""
        authors = metadata.get("authors", [])
        title = metadata.get("title", "")
        pub_name = metadata.get("publication_name", "")
        year = metadata.get("year")
        
        author_str = ", ".join(authors) if authors else "Unknown"
        
        full = f"[1] {author_str}, \"{title},\" {pub_name}, {year or 'n.d.'}."
        in_text = "[1]"
        
        return {
            "full": full,
            "in_text": in_text
        }
