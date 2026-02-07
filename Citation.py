"""
Citation generation service supporting multiple citation styles.
Generates properly formatted citations from metadata.
"""
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
import re
from datetime import datetime


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
    authors: List[str]  # ["First Last", "First Last"]
    year: Optional[int] = None
    publication_name: Optional[str] = None  # Journal, book publisher, website
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    url: Optional[str] = None
    doi: Optional[str] = None
    access_date: Optional[str] = None  # For websites
    source_type: str = "article"  # article, book, website, conference


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
        metadata: SourceMetadata,
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
            raise ValueError(f"Unsupported citation style: {style}")
    
    def _generate_apa(self, m: SourceMetadata) -> Dict[str, str]:
        """Generate APA 7th edition citation."""
        authors = self._format_authors_apa(m.authors)
        year = m.year or "n.d."
        
        # In-text citation
        if len(m.authors) == 1:
            in_text = f"({m.authors[0].split()[-1]}, {year})"
        elif len(m.authors) == 2:
            in_text = f"({m.authors[0].split()[-1]} & {m.authors[1].split()[-1]}, {year})"
        else:
            in_text = f"({m.authors[0].split()[-1]} et al., {year})"
        
        # Full citation
        if m.source_type == "article":
            full = f"{authors} ({year}). {m.title}. "
            if m.publication_name:
                full += f"*{m.publication_name}*"
            if m.volume:
                full += f", *{m.volume}*"
            if m.issue:
                full += f"({m.issue})"
            if m.pages:
                full += f", {m.pages}"
            full += "."
            if m.doi:
                full += f" https://doi.org/{m.doi}"
        
        elif m.source_type == "book":
            full = f"{authors} ({year}). *{m.title}*. {m.publication_name or 'Publisher'}."
        
        elif m.source_type == "website":
            full = f"{authors} ({year}). *{m.title}*. {m.publication_name or 'Website name'}. "
            if m.url:
                full += m.url
        
        else:
            full = f"{authors} ({year}). {m.title}."
        
        return {"full": full, "in_text": in_text}
    
    def _generate_mla(self, m: SourceMetadata) -> Dict[str, str]:
        """Generate MLA 9th edition citation."""
        authors = self._format_authors_mla(m.authors)
        
        # In-text citation
        if m.authors:
            in_text = f"({m.authors[0].split()[-1]}"
            if m.pages:
                in_text += f" {m.pages}"
            in_text += ")"
        else:
            in_text = f"(\"{m.title[:20]}...\")"
        
        # Full citation
        full = ""
        if authors:
            full += f"{authors}. "
        full += f'"{m.title}." '
        
        if m.source_type == "article":
            if m.publication_name:
                full += f"*{m.publication_name}*, "
            if m.volume:
                full += f"vol. {m.volume}, "
            if m.issue:
                full += f"no. {m.issue}, "
            if m.year:
                full += f"{m.year}, "
            if m.pages:
                full += f"pp. {m.pages}."
        
        elif m.source_type == "book":
            full += f"*{m.publication_name or 'Publisher'}*, {m.year or 'n.d.'}."
        
        elif m.source_type == "website":
            if m.publication_name:
                full += f"*{m.publication_name}*, "
            if m.year:
                full += f"{m.year}, "
            if m.url:
                full += m.url
        
        return {"full": full, "in_text": in_text}
    
    def _generate_chicago(self, m: SourceMetadata) -> Dict[str, str]:
        """Generate Chicago (Notes-Bibliography) citation."""
        # This is simplified; Chicago has many variations
        authors = self._format_authors_apa(m.authors)  # Similar format
        
        # In-text (footnote number in practice)
        in_text = f"({m.authors[0].split()[-1] if m.authors else 'Source'} {m.year or 'n.d.'})"
        
        # Full citation
        full = f"{authors}. "
        if m.year:
            full += f"{m.year}. "
        full += f'"{m.title}." '
        if m.publication_name:
            full += f"*{m.publication_name}* "
        if m.volume:
            full += f"{m.volume} "
        if m.issue:
            full += f"({m.issue})"
        if m.pages:
            full += f": {m.pages}"
        full += "."
        
        return {"full": full, "in_text": in_text}
    
    def _generate_harvard(self, m: SourceMetadata) -> Dict[str, str]:
        """Generate Harvard citation style."""
        # Very similar to APA
        return self._generate_apa(m)
    
    def _generate_ieee(self, m: SourceMetadata) -> Dict[str, str]:
        """Generate IEEE citation style."""
        # IEEE uses numbered references
        authors = ", ".join([
            " ".join([p[0] + "." for p in author.split()[:-1]] + [author.split()[-1]])
            for author in m.authors[:6]  # IEEE limits to 6
        ])
        
        if len(m.authors) > 6:
            authors += ", et al."
        
        # In-text is just a number
        in_text = "[1]"  # Would be sequential in actual use
        
        # Full citation
        full = f"{authors}, "
        full += f'"{m.title}," '
        if m.publication_name:
            full += f"*{m.publication_name}*, "
        if m.volume:
            full += f"vol. {m.volume}, "
        if m.issue:
            full += f"no. {m.issue}, "
        if m.pages:
            full += f"pp. {m.pages}, "
        if m.year:
            full += f"{m.year}."
        
        return {"full": full, "in_text": in_text}
    
    def extract_metadata_from_url(self, url: str) -> Optional[SourceMetadata]:
        """
        Extract metadata from URL (simplified version).
        In production, use Crossref API, Google Books API, etc.
        """
        # Check for DOI
        doi_match = re.search(r'10\.\d{4,}/[^\s]+', url)
        if doi_match:
            # In production, query Crossref API with DOI
            return SourceMetadata(
                title="Article Title",
                authors=["Author Name"],
                doi=doi_match.group(),
                source_type="article"
            )
        
        # Check for arXiv
        if 'arxiv.org' in url:
            arxiv_id = re.search(r'(\d{4}\.\d{4,5})', url)
            if arxiv_id:
                # In production, query arXiv API
                return SourceMetadata(
                    title="Paper Title",
                    authors=["Author Name"],
                    source_type="article",
                    url=url
                )
        
        # Default to website
        return SourceMetadata(
            title="Web Page Title",
            authors=["Website Name"],
            source_type="website",
            url=url,
            access_date=datetime.now().strftime("%Y-%m-%d")
        )


# Example usage
if __name__ == "__main__":
    generator = CitationGenerator()
    
    # Example metadata
    metadata = SourceMetadata(
        title="The impact of AI on academic writing",
        authors=["John Smith", "Jane Doe", "Bob Johnson"],
        year=2024,
        publication_name="Journal of Educational Technology",
        volume="45",
        issue="2",
        pages="123-145",
        doi="10.1234/jet.2024.123",
        source_type="article"
    )
    
    # Generate citations
    for style in CitationStyle:
        citation = generator.generate_citation(metadata, style)
        print(f"\n{style.value}:")
        print(f"In-text: {citation['in_text']}")
        print(f"Full: {citation['full']}")