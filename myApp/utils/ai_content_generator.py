"""
AI Content Generator for Lessons
Generates structured lesson content from PDF text using AI.
"""
import os
import json
import re
from typing import Dict, List, Optional


try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AIContentGenerator:
    """Generate lesson content from PDF text using AI"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI content generator
        
        Args:
            api_key: OpenAI API key (if None, reads from OPENAI_API_KEY env var)
        """
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI package not installed. Install with: pip install openai"
            )
        
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not provided. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.client = OpenAI(api_key=self.api_key)
    
    def generate_lesson_content(
        self,
        pdf_text: str,
        course_name: str,
        module_name: str,
        suggested_title: Optional[str] = None,
        model: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Generate complete lesson content from PDF text
        
        Args:
            pdf_text: Extracted text from PDF
            course_name: Name of the course
            module_name: Name of the module
            suggested_title: Optional suggested title for the lesson
            model: OpenAI model to use (auto-selects based on content size if None)
            
        Returns:
            Dict with lesson content:
            - clean_title: str
            - short_summary: str
            - full_description: str
            - content_blocks: List[Dict] (Editor.js format)
            - outcomes: List[str]
            - coach_actions: List[str]
        """
        # Determine content size and select appropriate model
        content_length = len(pdf_text)
        estimated_tokens = content_length // 4  # Rough estimate: 1 token ≈ 4 characters
        
        # Auto-select model based on content size
        max_output_tokens = 4000  # Default
        if model is None:
            if estimated_tokens > 100000:  # Very large (600+ pages)
                model = "gpt-4o"  # Use more powerful model
                max_output_tokens = 16000
            elif estimated_tokens > 50000:  # Large (200+ pages)
                model = "gpt-4o"
                max_output_tokens = 16000
            elif estimated_tokens > 20000:  # Medium (50+ pages)
                model = "gpt-4o-mini"
                max_output_tokens = 8000
            else:  # Small (20 pages or less)
                model = "gpt-4o-mini"
                max_output_tokens = 4000
        else:
            # If model is specified, set appropriate max_tokens
            if "gpt-4o" in model:
                max_output_tokens = 16000
            else:
                max_output_tokens = 8000
        
        # For very large PDFs, we'll process in chunks and combine
        if content_length > 200000:  # ~50k tokens
            return self._generate_large_pdf_content(
                pdf_text, course_name, module_name, suggested_title, model, max_output_tokens
            )
        
        prompt = f"""You are an expert course content creator. Given the following PDF content from a course module, create a COMPREHENSIVE and DETAILED structured lesson.

IMPORTANT: This PDF contains substantial content. Create a THOROUGH lesson that covers ALL major topics, concepts, and details from the PDF. Do not summarize - create detailed content blocks that students can learn from.

Requirements:
1. A clear, engaging lesson title (max 200 characters)
2. A short summary (1-2 sentences, max 300 characters)
3. A full description (3-5 paragraphs, comprehensive overview)
4. EXTENSIVE structured content blocks in Editor.js format:
   - Create MULTIPLE sections with H2 headers for major topics
   - Use H3 headers for subsections
   - Include DETAILED paragraphs explaining concepts thoroughly
   - Use lists (bulleted and numbered) to break down information
   - Use quotes for important concepts, definitions, or key takeaways
   - Cover ALL major topics from the PDF - be comprehensive, not brief
   - Aim for 20-50+ content blocks for large PDFs
   - Each section should be detailed enough for students to learn from
5. Learning outcomes (5-10 bullet points covering all major topics)
6. AI coach action suggestions (4-6 suggestions)

Course: {course_name}
Module: {module_name}
{f'Suggested Title: {suggested_title}' if suggested_title else ''}
PDF Length: {content_length} characters (~{estimated_tokens} tokens)

PDF Content:
{pdf_text}

Return the response as a JSON object with this exact structure:
{{
  "clean_title": "Lesson title here",
  "short_summary": "Brief summary here",
  "full_description": "Comprehensive full description here (3-5 paragraphs)",
  "content_blocks": [
    {{"type": "header", "data": {{"text": "Major Section Title", "level": 2}}}},
    {{"type": "paragraph", "data": {{"text": "Detailed paragraph explaining the concept thoroughly..."}}}},
    {{"type": "header", "data": {{"text": "Subsection", "level": 3}}}},
    {{"type": "paragraph", "data": {{"text": "More detailed explanation..."}}}},
    {{"type": "list", "data": {{"style": "unordered", "items": ["Detailed point 1", "Detailed point 2", "Detailed point 3"]}}}},
    {{"type": "quote", "data": {{"text": "Important concept or definition", "caption": "Source or context"}}}},
    {{"type": "paragraph", "data": {{"text": "Continue with comprehensive coverage..."}}}}
    // ... MANY more blocks covering all topics
  ],
  "outcomes": ["Comprehensive outcome 1", "Outcome 2", "Outcome 3", "Outcome 4", "Outcome 5", ...],
  "coach_actions": ["Action 1", "Action 2", "Action 3", "Action 4", ...]
}}

CRITICAL: Generate COMPREHENSIVE content blocks covering ALL major topics from the PDF. For large PDFs (50+ pages), generate 30-50+ content blocks. For very large PDFs (200+ pages), generate 50-100+ content blocks. Be thorough and detailed.

Only return valid JSON, no additional text or markdown formatting."""

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educational content creator specializing in comprehensive course content. Always return valid JSON only, no markdown formatting. Generate detailed, thorough content that covers all topics."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=max_output_tokens
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Clean up response (remove markdown code blocks if present)
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            if response_text.endswith('```'):
                response_text = response_text.rsplit('```', 1)[0].strip()
            
            # Parse JSON
            content_data = json.loads(response_text)
            
            # Validate and structure response
            return {
                'clean_title': content_data.get('clean_title', 'Untitled Lesson'),
                'short_summary': content_data.get('short_summary', ''),
                'full_description': content_data.get('full_description', ''),
                'content_blocks': content_data.get('content_blocks', []),
                'outcomes': content_data.get('outcomes', []),
                'coach_actions': content_data.get('coach_actions', [])
            }
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse AI response as JSON: {e}\nResponse: {response_text[:500]}")
        except Exception as e:
            raise Exception(f"Error generating content: {str(e)}")
    
    def _generate_large_pdf_content(
        self,
        pdf_text: str,
        course_name: str,
        module_name: str,
        suggested_title: Optional[str],
        model: str,
        max_output_tokens: int
    ) -> Dict[str, any]:
        """
        Generate content for very large PDFs by processing in chunks and combining
        
        Args:
            pdf_text: Full PDF text
            course_name: Course name
            module_name: Module name
            suggested_title: Suggested title
            model: Model to use
            max_output_tokens: Max output tokens
            
        Returns:
            Combined content dict
        """
        # Split PDF into logical chunks (by pages or sections)
        chunk_size = 100000  # ~25k tokens per chunk
        chunks = []
        
        for i in range(0, len(pdf_text), chunk_size):
            chunk = pdf_text[i:i + chunk_size]
            chunks.append(chunk)
        
        # Generate content for each chunk
        all_content_blocks = []
        title = suggested_title or "Untitled Lesson"
        summary_parts = []
        description_parts = []
        all_outcomes = set()
        all_coach_actions = set()
        
        for i, chunk in enumerate(chunks):
            chunk_prompt = f"""Extract and structure content from this section of a PDF (part {i+1} of {len(chunks)}):

PDF Section:
{chunk}

Create structured content blocks covering ALL topics in this section. Return JSON:
{{
  "content_blocks": [
    {{"type": "header", "data": {{"text": "Section Title", "level": 2}}}},
    {{"type": "paragraph", "data": {{"text": "Detailed content..."}}}},
    // ... many blocks
  ],
  "outcomes": ["Outcome 1", "Outcome 2"],
  "summary_note": "Brief note about this section"
}}

Only return JSON."""
            
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "Extract and structure PDF content. Return JSON only."},
                        {"role": "user", "content": chunk_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=max_output_tokens // len(chunks)  # Distribute tokens across chunks
                )
                
                response_text = response.choices[0].message.content.strip()
                if response_text.startswith('```'):
                    response_text = response_text.split('```')[1]
                    if response_text.startswith('json'):
                        response_text = response_text[4:]
                    response_text = response_text.strip()
                if response_text.endswith('```'):
                    response_text = response_text.rsplit('```', 1)[0].strip()
                
                chunk_data = json.loads(response_text)
                all_content_blocks.extend(chunk_data.get('content_blocks', []))
                all_outcomes.update(chunk_data.get('outcomes', []))
                summary_parts.append(chunk_data.get('summary_note', ''))
                
            except Exception as e:
                # If chunk processing fails, continue with other chunks
                print(f"Warning: Failed to process chunk {i+1}: {e}")
                continue
        
        # Generate final summary and description from all chunks
        final_prompt = f"""Create a comprehensive lesson summary and description from these section summaries:

Course: {course_name}
Module: {module_name}
Suggested Title: {suggested_title or 'Untitled'}

Section Summaries:
{chr(10).join(f'- {part}' for part in summary_parts if part)}

Return JSON:
{{
  "clean_title": "Comprehensive lesson title",
  "short_summary": "Brief summary",
  "full_description": "Comprehensive 3-5 paragraph description covering all sections"
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Create comprehensive lesson summaries. Return JSON only."},
                    {"role": "user", "content": final_prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            response_text = response.choices[0].message.content.strip()
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            if response_text.endswith('```'):
                response_text = response_text.rsplit('```', 1)[0].strip()
            
            final_data = json.loads(response_text)
            title = final_data.get('clean_title', title)
            summary = final_data.get('short_summary', '')
            description = final_data.get('full_description', '')
        except:
            # Fallback if final summary fails
            summary = f"Comprehensive lesson covering {len(chunks)} major sections"
            description = f"This lesson covers extensive material from the PDF, organized into {len(chunks)} major sections."
        
        return {
            'clean_title': title,
            'short_summary': summary,
            'full_description': description,
            'content_blocks': all_content_blocks,
            'outcomes': list(all_outcomes)[:15],  # Limit to top 15
            'coach_actions': [
                "Summarize key concepts from this lesson",
                "Create a study guide from this content",
                "Generate quiz questions from the material",
                "Break down complex topics into simpler explanations",
                "Create action items from the lesson content"
            ]
        }
    
    def convert_to_editorjs_format(self, content_blocks: List[Dict]) -> Dict:
        """
        Convert content blocks to Editor.js format
        
        Args:
            content_blocks: List of content block dicts
            
        Returns:
            Editor.js format dict
        """
        import uuid
        import time
        
        blocks = []
        for block in content_blocks:
            block_id = str(uuid.uuid4())
            blocks.append({
                "id": block_id,
                "type": block.get("type", "paragraph"),
                "data": block.get("data", {})
            })
        
        return {
            "time": int(time.time() * 1000),
            "blocks": blocks,
            "version": "2.28.2"
        }

