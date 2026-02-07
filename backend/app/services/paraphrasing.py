"""
Paraphrasing service with local and LLM-based options.
Provides text rewriting without requiring API keys by default.
"""
import os
import re
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class SimpleParaphraser:
    """
    Local paraphrasing using synonym replacement and restructuring.
    Works completely offline without API keys.
    """
    
    # Comprehensive synonym mapping for aggressive paraphrasing
    SYNONYM_MAP = {
        # Common verbs
        "is": "remains",
        "are": "exist as",
        "was": "proved to be",
        "were": "turned out to be",
        "important": "vital",
        "big": "substantial",
        "small": "minimal",
        "good": "beneficial",
        "bad": "detrimental",
        "help": "facilitate",
        "use": "leverage",
        "make": "generate",
        "get": "acquire",
        "go": "advance",
        "think": "consider",
        "know": "comprehend",
        "way": "approach",
        "thing": "item",
        "time": "duration",
        "people": "individuals",
        "work": "function",
        "can": "is able to",
        "very": "extremely",
        "really": "actually",
        "quite": "rather",
        "just": "merely",
        "also": "furthermore",
        "because": "since",
        "before": "ahead of",
        "after": "subsequent to",
        "need": "must have",
        "show": "demonstrate",
        "say": "state",
        "tell": "communicate",
        "give": "bestow",
        "take": "seize",
        "seem": "appear",
        "let": "permit",
        "put": "position",
        "have": "possess",
        "do": "execute",
        "see": "observe",
        "come": "arrive",
        "made": "created",
        "being": "existing",
        "becomes": "transforms into",
        "become": "transform into",
        "came": "arrived",
        "comes": "arrives",
        "making": "producing",
        "made": "produced",
        "takes": "requires",
        "took": "required",
        "given": "provided",
        "gives": "contributes",
        "gave": "contributed",
        "having": "possessing",
        "has": "contains",
        "had": "contained",
        "doing": "executing",
        "did": "executed",
        "done": "completed",
        "seeing": "observing",
        "seen": "observed",
        "saw": "observed",
    }
    
    def paraphrase(self, text: str, style: str = "standard") -> str:
        """Paraphrase text using local methods."""
        if not text or len(text.strip()) < 5:
            return text
        
        try:
            if style == "academic":
                return self._academicize(text)
            elif style == "formal":
                return self._formalize(text)
            elif style == "casual":
                return self._casualize(text)
            elif style == "simple":
                return self._simplify(text)
            else:
                return self._standard(text)
        except Exception as e:
            logger.error(f"Paraphrasing error: {e}")
            return text
    
    def _standard(self, text: str) -> str:
        """Apply aggressive synonym replacement and restructuring."""
        result = text
        
        # First pass: replace high-frequency words
        for word, synonym in self.SYNONYM_MAP.items():
            pattern = r'\b' + re.escape(word) + r'\b'
            result = re.sub(pattern, synonym, result, flags=re.IGNORECASE)
        
        # Second pass: apply text restructuring
        sentences = re.split(r'(?<=[.!?])\s+', result)
        restructured = []
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Reverse some sentences for variety (if more than 1 clause)
            if ',' in sentence and i % 2 == 0:
                parts = sentence.split(',', 1)
                if len(parts) == 2:
                    sentence = parts[1].strip() + ', ' + parts[0].strip()
            
            restructured.append(sentence)
        
        return ' '.join(restructured)
    
    def _academicize(self, text: str) -> str:
        """Make text more academic and scholarly."""
        result = text
        
        # Remove contractions aggressively
        contractions = {
            r"\bdon't\b": "do not",
            r"\bdoesn't\b": "does not",
            r"\bdidn't\b": "did not",
            r"\bcan't\b": "cannot",
            r"\bcouldn't\b": "could not",
            r"\bwon't\b": "will not",
            r"\bwouldn't\b": "would not",
            r"\bisn't\b": "is not",
            r"\baren't\b": "are not",
            r"\bI'm\b": "I am",
            r"\byou're\b": "you are",
            r"\bhe's\b": "he is",
            r"\bshe's\b": "she is",
            r"\bit's\b": "it is",
            r"\bwe're\b": "we are",
            r"\bthey're\b": "they are",
        }
        
        for contraction, formal in contractions.items():
            result = re.sub(contraction, formal, result, flags=re.IGNORECASE)
        
        # Replace casual words with academic equivalents
        casual_academic = {
            r"\bkinda\b": "somewhat",
            r"\bsorta\b": "rather",
            r"\blots? of\b": "numerous",
            r"\bstuff\b": "material",
            r"\bthing\b": "concept",
            r"\bguy\b": "individual",
            r"\nguys\b": "individuals",
            r"\bwanna\b": "want to",
            r"\bgonna\b": "going to",
        }
        
        for casual, academic in casual_academic.items():
            result = re.sub(casual, academic, result, flags=re.IGNORECASE)
        
        # Apply synonym replacement
        for word, synonym in list(self.SYNONYM_MAP.items())[:20]:
            pattern = r'\b' + re.escape(word) + r'\b'
            result = re.sub(pattern, synonym, result, flags=re.IGNORECASE)
        
        return result
    
    def _formalize(self, text: str) -> str:
        """Make text formal and professional."""
        result = text
        
        # Comprehensive contraction removal
        contractions = {
            r"\bdon't\b": "do not",
            r"\bdoesn't\b": "does not", 
            r"\bdidn't\b": "did not",
            r"\bcan't\b": "cannot",
            r"\bcouldn't\b": "could not",
            r"\bwon't\b": "will not",
            r"\bwouldn't\b": "would not",
            r"\bshouldn't\b": "should not",
            r"\bhasn't\b": "has not",
            r"\bhaven't\b": "have not",
            r"\bhadn't\b": "had not",
            r"\bisn't\b": "is not",
            r"\baren't\b": "are not",
            r"\bwasn't\b": "was not",
            r"\bweren't\b": "were not",
            r"\bI'm\b": "I am",
            r"\byou're\b": "you are",
            r"\bhe's\b": "he is",
            r"\bshe's\b": "she is",
            r"\bit's\b": "it is",
            r"\bwe're\b": "we are",
            r"\bthey're\b": "they are",
        }
        
        for contraction, formal in contractions.items():
            result = re.sub(contraction, formal, result, flags=re.IGNORECASE)
        
        # Apply synonym replacement with formality
        for word, synonym in self.SYNONYM_MAP.items():
            pattern = r'\b' + re.escape(word) + r'\b'
            result = re.sub(pattern, synonym, result, flags=re.IGNORECASE)
        
        # Add formality markers
        result = re.sub(r'\bbtw\b', 'by the way', result, flags=re.IGNORECASE)
        result = re.sub(r'\bretc\b', 'et cetera', result, flags=re.IGNORECASE)
        
        return result
    
    def _simplify(self, text: str) -> str:
        """Simplify text for easy reading - break into shorter sentences."""
        # First apply synonym replacements
        result = text
        for word, synonym in list(self.SYNONYM_MAP.items())[:15]:
            pattern = r'\b' + re.escape(word) + r'\b'
            result = re.sub(pattern, synonym, result, flags=re.IGNORECASE)
        
        # Split by periods, commas, and semicolons to break up long sentences
        sentences = re.split(r'[.;!?]+', result)
        simplified = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence or len(sentence) < 3:
                continue
            
            # Split further by commas to create even shorter sentences
            parts = sentence.split(',')
            for part in parts:
                part = part.strip()
                if part and len(part) > 5:
                    simplified.append(part)
        
        # Rejoin with simple connectors
        return '. '.join(simplified) + '.' if simplified else text
    
    def _casualize(self, text: str) -> str:
        """Make text casual and conversational."""
        result = text
        
        # Replace formal words with casual ones
        formal_to_casual = {
            r"\bobtain\b": "get",
            r"\butilize\b": "use",
            r"\bfacilitate\b": "help",
            r"\bmoreover\b": "plus",
            r"\bfurthermore\b": "also",
            r"\bsubsequently\b": "then",
            r"\bthereafter\b": "after that",
            r"\bnonetheless\b": "still",
            r"\bnotwithstanding\b": "despite",
            r"\bdemonstrate\b": "show",
            r"\nrequire\b": "need",
            r"\nacquire\b": "get",
            r"\bconsider\b": "think about",
        }
        
        for formal, casual in formal_to_casual.items():
            result = re.sub(formal, casual, result, flags=re.IGNORECASE)
        
        # Add conversational markers
        if len(result) > 50:
            # Add "you know" or similar markers periodically
            sentences = re.split(r'[.!?]+', result)
            if len(sentences) > 2:
                sentences[1] = "You know, " + sentences[1].strip()
            result = '. '.join(sentences)
        
        return result


class ParaphrasingService:
    """
    Generates paraphrasing suggestions using LLMs or local methods.
    Provides multiple alternatives with explanations.
    """
    
    def __init__(
        self,
        use_anthropic: bool = True,
        anthropic_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None
    ):
        """
        Initialize paraphrasing service.
        
        Args:
            use_anthropic: Use Claude (Anthropic) vs GPT (OpenAI)
            anthropic_api_key: Anthropic API key
            openai_api_key: OpenAI API key
        """
        self.local_paraphraser = SimpleParaphraser()
        self.use_anthropic = use_anthropic
        self.client = None
        self.model = None
        self.use_local = True
        
        # Lazy load LLM clients if API keys are available
        try:
            if use_anthropic and (anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")):
                from anthropic import Anthropic
                self.client = Anthropic(
                    api_key=anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
                )
                self.model = "claude-3-haiku-20240307"
                self.use_local = False
                logger.info("Anthropic loaded for paraphrasing")
        except ImportError:
            pass
        except Exception as e:
            logger.warning(f"Could not load Anthropic: {e}")
        
        try:
            if not self.client and (openai_api_key or os.getenv("OPENAI_API_KEY")):
                from openai import OpenAI
                self.client = OpenAI(
                    api_key=openai_api_key or os.getenv("OPENAI_API_KEY")
                )
                self.model = "gpt-4-turbo-preview"
                self.use_local = False
                logger.info("OpenAI loaded for paraphrasing")
        except ImportError:
            pass
        except Exception as e:
            logger.warning(f"Could not load OpenAI: {e}")
        
        if self.use_local:
            logger.info("Using local paraphraser (no API keys required)")
    
    def generate_paraphrases(
        self,
        text: str,
        context: Optional[str] = None,
        num_alternatives: int = 3
    ) -> List[Dict[str, str]]:
        """
        Generate paraphrasing suggestions for given text.
        
        Args:
            text: Original text to paraphrase
            context: Surrounding context for better understanding
            num_alternatives: Number of alternatives to generate
        
        Returns:
            List of dicts with 'paraphrase' and 'explanation'
        """
        # If no text, return empty
        if not text:
            return [{"paraphrase": "", "explanation": ""}]
        
        # Generate paraphrased text
        paraphrased = self.paraphrase(text, "standard")
        
        return [
            {
                "paraphrase": paraphrased,
                "explanation": f"Using {'LLM' if not self.use_local else 'local synonym replacement'} algorithm"
            }
        ]
    
    def paraphrase(self, text: str, style: str = "standard") -> str:
        """
        Paraphrase text using LLM or local method.
        
        Args:
            text: Text to paraphrase
            style: Style (standard, academic, formal, casual, simple)
        
        Returns:
            Paraphrased text
        """
        if not text or len(text.strip()) < 5:
            return text
        
        # Use local paraphraser by default
        if self.use_local:
            return self.local_paraphraser.paraphrase(text, style)
        
        # Try LLM if available
        try:
            if "claude" in (self.model or "").lower():
                return self._paraphrase_claude(text, style)
            elif "gpt" in (self.model or "").lower():
                return self._paraphrase_openai(text, style)
        except Exception as e:
            logger.error(f"LLM paraphrasing error: {e}, falling back to local")
            return self.local_paraphraser.paraphrase(text, style)
        
        return text
    
    def _paraphrase_claude(self, text: str, style: str) -> str:
        """Paraphrase using Claude."""
        try:
            prompt = f"Paraphrase the following text in a {style} style. Keep the same meaning but use different words and sentence structure. Only return the paraphrased text, nothing else.\n\nText: {text}"
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Claude paraphrasing failed: {e}")
            return text
    
    def _paraphrase_openai(self, text: str, style: str) -> str:
        """Paraphrase using OpenAI."""
        try:
            prompt = f"Paraphrase the following text in a {style} style. Keep the same meaning but use different words and sentence structure. Only return the paraphrased text, nothing else.\n\nText: {text}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI paraphrasing failed: {e}")
            return text
