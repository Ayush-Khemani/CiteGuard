"""
AI-powered paraphrasing service.
Helps students rephrase text while maintaining meaning.
"""
from typing import List, Dict, Optional
import os
from anthropic import Anthropic
from openai import OpenAI


class ParaphrasingService:
    """
    Generates paraphrasing suggestions using LLMs.
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
        self.use_anthropic = use_anthropic
        
        if use_anthropic:
            self.client = Anthropic(
                api_key=anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
            )
            self.model = "claude-sonnet-4-20250514"
        else:
            self.client = OpenAI(
                api_key=openai_api_key or os.getenv("OPENAI_API_KEY")
            )
            self.model = "gpt-4-turbo-preview"
    
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
        prompt = self._build_prompt(text, context, num_alternatives)
        
        if self.use_anthropic:
            response = self._call_anthropic(prompt)
        else:
            response = self._call_openai(prompt)
        
        return self._parse_response(response)
    
    def _build_prompt(
        self,
        text: str,
        context: Optional[str],
        num_alternatives: int
    ) -> str:
        """Build the prompt for the LLM."""
        prompt = f"""You are an academic writing coach helping students paraphrase text to avoid plagiarism while maintaining meaning.

Original text to paraphrase:
"{text}"
"""
        
        if context:
            prompt += f"""
Context (for better understanding):
"{context}"
"""
        
        prompt += f"""
Please provide {num_alternatives} different paraphrased versions of the original text.

Requirements:
1. Maintain the original meaning and key information
2. Use different sentence structures and vocabulary
3. Keep it academic and clear
4. Avoid simply replacing words with synonyms
5. Make it sound natural, not robotic

For each paraphrase, also explain WHAT made the original problematic and HOW your version improves it.

Format your response as:

PARAPHRASE 1:
[Your paraphrased version]

EXPLANATION 1:
[Brief explanation of changes]

PARAPHRASE 2:
[Your paraphrased version]

EXPLANATION 2:
[Brief explanation of changes]

(continue for all {num_alternatives} versions)
"""
        
        return prompt
    
    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic Claude API."""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI GPT API."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an academic writing coach helping students paraphrase text properly."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
    
    def _parse_response(self, response: str) -> List[Dict[str, str]]:
        """Parse LLM response into structured format."""
        paraphrases = []
        
        # Split by paraphrase markers
        sections = response.split("PARAPHRASE ")
        
        for section in sections[1:]:  # Skip first empty section
            try:
                # Extract paraphrase
                paraphrase_part, explanation_part = section.split("EXPLANATION ")
                
                # Clean up
                paraphrase = paraphrase_part.split("\n", 1)[1].strip()
                explanation = explanation_part.split("\n", 1)[1].strip()
                
                # Remove next paraphrase marker if present
                if "PARAPHRASE" in explanation:
                    explanation = explanation.split("PARAPHRASE")[0].strip()
                
                paraphrases.append({
                    "paraphrase": paraphrase,
                    "explanation": explanation
                })
            except (ValueError, IndexError):
                continue
        
        return paraphrases
    
    def get_paraphrase_with_citation(
        self,
        text: str,
        source_title: str,
        citation_style: str = "APA"
    ) -> str:
        """
        Generate a paraphrase with proper citation.
        
        Useful when text is too similar to source and needs both
        paraphrasing and citation.
        """
        paraphrases = self.generate_paraphrases(text, num_alternatives=1)
        
        if not paraphrases:
            return text
        
        paraphrase = paraphrases[0]["paraphrase"]
        
        # Add citation placeholder
        paraphrase += " [CITATION NEEDED]"
        
        return paraphrase
    
    def batch_paraphrase(
        self,
        texts: List[str],
        context: Optional[str] = None
    ) -> Dict[str, List[Dict[str, str]]]:
        """
        Paraphrase multiple text segments efficiently.
        
        Useful for paraphrasing multiple flagged sections at once.
        """
        results = {}
        
        for i, text in enumerate(texts):
            try:
                paraphrases = self.generate_paraphrases(
                    text,
                    context=context,
                    num_alternatives=2  # Fewer for batch to save tokens
                )
                results[f"section_{i}"] = paraphrases
            except Exception as e:
                results[f"section_{i}"] = [
                    {
                        "paraphrase": text,
                        "explanation": f"Error generating paraphrase: {str(e)}"
                    }
                ]
        
        return results


# Example usage and testing
if __name__ == "__main__":
    # Test with mock text
    service = ParaphrasingService(use_anthropic=True)
    
    original = "Climate change is causing significant alterations to global weather patterns, leading to more frequent extreme weather events."
    
    print("Original text:")
    print(original)
    print("\nGenerating paraphrases...\n")
    
    paraphrases = service.generate_paraphrases(original)
    
    for i, p in enumerate(paraphrases, 1):
        print(f"--- Paraphrase {i} ---")
        print(p["paraphrase"])
        print(f"\nExplanation: {p['explanation']}")
        print()