"""
Similarity detection service.
Detects plagiarism and similar content using embeddings.
"""
from typing import List, Dict, Optional
import logging
import os
from functools import lru_cache

logger = logging.getLogger(__name__)


class SimilarityService:
    """
    Service for detecting text similarity using embeddings.
    Uses sentence-transformers for semantic similarity detection.
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", threshold: float = 0.85):
        """
        Initialize similarity service.
        
        Args:
            model_name: HuggingFace model identifier
            threshold: Similarity threshold (0-1)
        """
        self.model_name = model_name
        self.threshold = threshold
        self.model = None
        
        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading similarity model: {model_name}")
            self.model = SentenceTransformer(model_name)
            logger.info("✓ Similarity model loaded successfully")
        except ImportError:
            logger.error("sentence-transformers not installed. Install with: pip install sentence-transformers")
        except Exception as e:
            logger.error(f"Failed to load similarity model: {e}")
    
    def analyze_document(self, document_text: str, sources: List[Dict] = None) -> Dict:
        """
        Analyze document for plagiarism by comparing against sources.
        
        Args:
            document_text: Text to analyze
            sources: List of source texts to compare against
        
        Returns:
            Dict with analysis results
        """
        if not document_text or not sources:
            return {
                "plagiarism_score": 0.0,
                "flagged_sections": 0,
                "recommendations": [
                    "No sources to compare against" if not sources else "Empty text provided"
                ],
                "total_matches": 0,
                "sources_checked": len(sources) if sources else 0
            }
        
        try:
            # Use ML model if available
            if self.model:
                return self._analyze_semantic(document_text, sources)
            else:
                # Fall back to simple word-overlap analysis
                return self._analyze_simple(document_text, sources)
                
        except Exception as e:
            logger.error(f"Error analyzing document: {e}")
            return {
                "plagiarism_score": 0.0,
                "flagged_sections": 0,
                "recommendations": [str(e)],
                "total_matches": 0,
                "sources_checked": len(sources) if sources else 0
            }
    
    def _analyze_semantic(self, document_text: str, sources: List[Dict]) -> Dict:
        """Analyze using semantic similarity with ML model."""
        try:
            from sklearn.metrics.pairwise import cosine_similarity
            import numpy as np
            
            # Get document and source embeddings
            doc_embedding = self.model.encode(document_text)
            source_texts = [s.get('content', '') for s in sources if s.get('content')]
            
            if not source_texts:
                return {
                    "plagiarism_score": 0.0,
                    "flagged_sections": 0,
                    "recommendations": ["No valid source content to compare"],
                    "total_matches": 0,
                    "sources_checked": 0
                }
            
            source_embeddings = self.model.encode(source_texts)
            
            # Calculate similarity scores
            similarities = cosine_similarity([doc_embedding], source_embeddings)[0]
            
            # Calculate overall plagiarism score
            max_similarity = float(np.max(similarities))
            avg_similarity = float(np.mean(similarities))
            plagiarism_score = (max_similarity + avg_similarity) / 2  # Average of max and mean
            plagiarism_score = min(plagiarism_score, 1.0)  # Cap at 1.0
            
            # Count high-similarity sections
            high_sim_count = sum(1 for s in similarities if s > 0.75)
            
            recommendations = []
            if plagiarism_score > 0.85:
                recommendations.append(f"⚠️ High similarity detected ({plagiarism_score*100:.1f}%) - Review content carefully")
            elif plagiarism_score > 0.7:
                recommendations.append(f"📋 Moderate similarity ({plagiarism_score*100:.1f}%) - Consider paraphrasing")
            else:
                recommendations.append("✓ Low plagiarism risk")
            
            return {
                "plagiarism_score": plagiarism_score,
                "flagged_sections": high_sim_count,
                "recommendations": recommendations,
                "total_matches": len([s for s in similarities if s > 0.5]),
                "sources_checked": len(sources)
            }
        except Exception as e:
            logger.error(f"Semantic analysis failed: {e}")
            return self._analyze_simple(document_text, sources)
    
    def _analyze_simple(self, document_text: str, sources: List[Dict]) -> Dict:
        """Simple word-overlap plagiarism analysis (no ML required)."""
        # Tokenize document
        doc_words = set(document_text.lower().split())
        doc_word_count = len(doc_words)
        
        if doc_word_count == 0:
            return {
                "plagiarism_score": 0.0,
                "flagged_sections": 0,
                "recommendations": ["Empty document provided"],
                "total_matches": 0,
                "sources_checked": 0
            }
        
        similarities = []
        matches_by_source = {}
        
        for source in sources:
            source_content = source.get('content', '')
            source_title = source.get('title', 'Unknown')
            
            if not source_content:
                continue
            
            # Tokenize source
            source_words = set(source_content.lower().split())
            
            # Calculate word overlap
            common_words = doc_words.intersection(source_words)
            similarity = len(common_words) / doc_word_count if doc_word_count > 0 else  0
            similarities.append(similarity)
            matches_by_source[source_title] = {
                "similarity": similarity,
                "matching_words": len(common_words)
            }
        
        if not similarities:
            return {
                "plagiarism_score": 0.0,
                "flagged_sections": 0,
                "recommendations": ["No sources provided"],
                "total_matches": 0,
                "sources_checked": 0
            }
        
        # Calculate plagiarism score
        max_similarity = max(similarities)
        avg_similarity = sum(similarities) / len(similarities)
        plagiarism_score = (max_similarity + avg_similarity) / 2
        
        # Count high-overlap sources
        high_overlap = sum(1 for s in similarities if s > 0.3)
        
        recommendations = []
        if plagiarism_score > 0.4:
            recommendations.append(f"⚠️ Significant word overlap ({plagiarism_score*100:.1f}%) detected")
            for title, data in matches_by_source.items():
                if data['similarity'] > 0.3:
                    recommendations.append(f"  • {title}: {data['matching_words']} matching words")
        else:
            recommendations.append("✓ Low similarity with stored documents")
        
        return {
            "plagiarism_score": plagiarism_score,
            "flagged_sections": high_overlap,
            "recommendations": recommendations,
            "total_matches": sum(1 for s in similarities if s > 0.15),
            "sources_checked": len(sources)
        }
    
    def get_embeddings(self, texts: List[str]) -> List:
        """
        Get embeddings for texts.
        
        Args:
            texts: List of texts to embed
        
        Returns:
            List of embedding vectors
        """
        if not self.model:
            logger.error("Model not loaded, cannot generate embeddings")
            return None
        
        try:
            embeddings = self.model.encode(texts)
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return None


# Global instance cache
_similarity_service = None


@lru_cache()
def get_similarity_service(threshold: float = 0.85) -> SimilarityService:
    """
    Get or create global similarity service instance.
    
    Args:
        threshold: Similarity threshold
    
    Returns:
        SimilarityService instance
    """
    global _similarity_service
    
    if _similarity_service is None:
        model_name = os.getenv("SIMILARITY_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        _similarity_service = SimilarityService(model_name=model_name, threshold=threshold)
    
    return _similarity_service
