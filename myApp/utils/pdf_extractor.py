"""
PDF Text Extraction Utility
Extracts text from PDF files for processing into lesson content.
"""
import os
import re
from typing import List, Dict, Optional


try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False


class PDFExtractor:
    """Extract text from PDF files"""
    
    def __init__(self, prefer_pdfplumber=True):
        """
        Initialize PDF extractor
        
        Args:
            prefer_pdfplumber: If True, use pdfplumber (better formatting), 
                             else use PyPDF2 (simpler)
        """
        if not PYPDF2_AVAILABLE and not PDFPLUMBER_AVAILABLE:
            raise ImportError(
                "Neither PyPDF2 nor pdfplumber is installed. "
                "Install one: pip install PyPDF2 pdfplumber"
            )
        
        self.prefer_pdfplumber = prefer_pdfplumber and PDFPLUMBER_AVAILABLE
        self.use_pdfplumber = self.prefer_pdfplumber and PDFPLUMBER_AVAILABLE
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract all text from a PDF file
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text as string
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if self.use_pdfplumber:
            return self._extract_with_pdfplumber(pdf_path)
        else:
            return self._extract_with_pypdf2(pdf_path)
    
    def _extract_with_pdfplumber(self, pdf_path: str) -> str:
        """Extract text using pdfplumber (better formatting)"""
        text_parts = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    text_parts.append(f"--- Page {page_num} ---\n{text}\n")
        
        return "\n".join(text_parts)
    
    def _extract_with_pypdf2(self, pdf_path: str) -> str:
        """Extract text using PyPDF2 (simpler, but less formatting)"""
        text_parts = []
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text:
                    text_parts.append(f"--- Page {page_num + 1} ---\n{text}\n")
        
        return "\n".join(text_parts)
    
    def extract_by_pages(self, pdf_path: str, pages_per_chunk: int = 10) -> List[Dict[str, any]]:
        """
        Extract text and split into chunks by page count
        
        Args:
            pdf_path: Path to PDF file
            pages_per_chunk: Number of pages per chunk
            
        Returns:
            List of dicts with 'text', 'start_page', 'end_page'
        """
        full_text = self.extract_text(pdf_path)
        
        # Split by page markers
        page_markers = re.finditer(r'--- Page (\d+) ---', full_text)
        pages = []
        current_page_start = 0
        
        for match in page_markers:
            if pages:
                pages[-1]['end'] = match.start()
            pages.append({
                'start': match.start(),
                'end': len(full_text),
                'page_num': int(match.group(1))
            })
        
        if not pages:
            # No page markers found, return entire text as one chunk
            return [{
                'text': full_text,
                'start_page': 1,
                'end_page': 1
            }]
        
        # Group pages into chunks
        chunks = []
        for i in range(0, len(pages), pages_per_chunk):
            chunk_pages = pages[i:i + pages_per_chunk]
            start_idx = chunk_pages[0]['start']
            end_idx = chunk_pages[-1]['end']
            
            chunks.append({
                'text': full_text[start_idx:end_idx].strip(),
                'start_page': chunk_pages[0]['page_num'],
                'end_page': chunk_pages[-1]['page_num']
            })
        
        return chunks
    
    def extract_by_headings(self, pdf_path: str, heading_pattern: str = r'^[A-Z][A-Z\s]{10,}$') -> List[Dict[str, any]]:
        """
        Extract text and split by headings
        
        Args:
            pdf_path: Path to PDF file
            heading_pattern: Regex pattern to identify headings
            
        Returns:
            List of dicts with 'text', 'heading', 'start_page', 'end_page'
        """
        full_text = self.extract_text(pdf_path)
        lines = full_text.split('\n')
        
        chunks = []
        current_chunk = []
        current_heading = "Introduction"
        
        for line in lines:
            if re.match(heading_pattern, line.strip()):
                # Save previous chunk
                if current_chunk:
                    chunks.append({
                        'text': '\n'.join(current_chunk).strip(),
                        'heading': current_heading
                    })
                # Start new chunk
                current_heading = line.strip()
                current_chunk = [line]
            else:
                current_chunk.append(line)
        
        # Add final chunk
        if current_chunk:
            chunks.append({
                'text': '\n'.join(current_chunk).strip(),
                'heading': current_heading
            })
        
        return chunks
    
    def get_page_count(self, pdf_path: str) -> int:
        """Get total number of pages in PDF"""
        if self.use_pdfplumber:
            with pdfplumber.open(pdf_path) as pdf:
                return len(pdf.pages)
        else:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return len(pdf_reader.pages)

