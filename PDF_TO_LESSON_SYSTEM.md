# PDF to Lesson Content Generation System

## Overview

This system allows you to upload PDF documents, extract their content, split them into lessons, and use AI to automatically generate structured lesson content including titles, descriptions, content blocks, and outcomes.

## Architecture

### 1. PDF Upload & Processing Flow

```
PDF Upload → Text Extraction → Chunking/Splitting → AI Content Generation → Lesson Creation
```

### 2. Folder Structure Recommendation

**Option A: One PDF per Lesson (Recommended)**
```
courses/
  ├── positive_psychology/
  │   ├── module1/
  │   │   ├── lesson1_introduction.pdf
  │   │   ├── lesson2_fundamentals.pdf
  │   │   └── lesson3_applications.pdf
  │   └── module2/
  │       ├── lesson1_advanced.pdf
  │       └── lesson2_practices.pdf
```

**Option B: One PDF per Module (with splitting)**
```
courses/
  ├── positive_psychology/
  │   ├── module1_complete.pdf  (will be split into lessons)
  │   └── module2_complete.pdf
```

**Recommendation: Option A (One PDF per Lesson)**
- ✅ Easier to manage
- ✅ Better control over lesson boundaries
- ✅ More accurate AI content generation
- ✅ Easier to update individual lessons
- ✅ Better for chunking (no arbitrary splits)

## Components

### 1. PDF Text Extraction
- Uses `PyPDF2` or `pdfplumber` for text extraction
- Handles multi-page PDFs
- Preserves structure (headings, paragraphs, lists)

### 2. Content Chunking (if needed)
- Split large PDFs into logical sections
- Use page breaks, headings, or fixed page counts
- Each chunk becomes a lesson

### 3. AI Content Generation
- Takes extracted PDF text
- Generates:
  - Clean lesson title
  - Short summary
  - Full description
  - Structured content blocks (Editor.js format)
  - Learning outcomes
  - AI coach actions

### 4. Lesson Creation
- Creates Course (if doesn't exist)
- Creates Module (if doesn't exist)
- Creates Lessons with all generated content

## Usage

### Method 1: Management Command (Recommended)

```bash
# Process a single PDF file
python manage.py process_pdf_to_lesson \
    --course positive_psychology \
    --module "Module 1" \
    --pdf-path "courses/positive_psychology/module1/lesson1.pdf" \
    --lesson-title "Introduction to Positive Psychology"

# Process entire folder
python manage.py process_pdf_to_lesson \
    --course positive_psychology \
    --module "Module 1" \
    --folder-path "courses/positive_psychology/module1/"

# Process with auto-splitting (for large PDFs)
python manage.py process_pdf_to_lesson \
    --course positive_psychology \
    --module "Module 1" \
    --pdf-path "courses/positive_psychology/module1_complete.pdf" \
    --split-by-pages 10  # Split every 10 pages
```

### Method 2: Admin Interface (Future)

- Upload PDF through admin panel
- Select course and module
- Auto-generate lessons

## PDF Processing Strategy

### For Single Lesson PDFs (Recommended)

1. **Extract all text** from PDF
2. **Send to AI** with prompt:
   - "Extract key concepts from this PDF"
   - "Generate lesson structure"
   - "Create content blocks"
3. **Create lesson** with generated content

### For Module PDFs (with splitting)

1. **Extract text** from entire PDF
2. **Split by pages** (e.g., every 10 pages) or by headings
3. **For each chunk**:
   - Send to AI for content generation
   - Create lesson

## AI Prompt Structure

```
You are an expert course content creator. Given the following PDF content, 
create a structured lesson with:

1. A clear, engaging lesson title
2. A short summary (1-2 sentences)
3. A full description (2-3 paragraphs)
4. Structured content blocks (Editor.js format):
   - Headers (H2, H3)
   - Paragraphs
   - Lists (bulleted, numbered)
   - Quotes (if applicable)
5. Learning outcomes (3-5 bullet points)
6. AI coach action suggestions

PDF Content:
[Extracted text here]

Course: [course_name]
Module: [module_name]
```

## File Structure

```
myApp/
  ├── management/
  │   └── commands/
  │       └── process_pdf_to_lesson.py  # Main processing command
  ├── utils/
  │   ├── pdf_extractor.py              # PDF text extraction
  │   └── ai_content_generator.py      # AI content generation
```

## Dependencies

```python
# Add to requirements.txt
PyPDF2>=3.0.0
pdfplumber>=0.10.0
openai>=1.0.0  # or your AI provider
```

## Benefits of This Approach

1. **Scalable**: Process hundreds of PDFs quickly
2. **Consistent**: AI ensures consistent formatting
3. **Fast**: Automated content generation
4. **Flexible**: Works with any PDF structure
5. **Maintainable**: Easy to update individual lessons

## Workflow Example

1. **Prepare PDFs**: Organize PDFs by course/module/lesson
2. **Run Command**: Execute management command
3. **Review**: Check generated lessons in admin
4. **Refine**: Edit any lessons that need adjustment
5. **Publish**: Make lessons available to students

## Future Enhancements

- [ ] Batch processing for multiple courses
- [ ] PDF upload via admin interface
- [ ] Preview before creating lessons
- [ ] Support for images/diagrams in PDFs
- [ ] Automatic quiz generation from PDF content
- [ ] Vectorization for search/retrieval

