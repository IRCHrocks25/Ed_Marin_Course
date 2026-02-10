# PDF to Lesson Processing - Quick Start Guide

## Installation

### 1. Install Required Packages

Add to your `requirements.txt` or install directly:

```bash
pip install PyPDF2 pdfplumber openai
```

Or add to `requirements.txt`:
```
PyPDF2>=3.0.0
pdfplumber>=0.10.0
openai>=1.0.0
```

### 2. Set OpenAI API Key

```bash
# Windows
set OPENAI_API_KEY=your-api-key-here

# Linux/Mac
export OPENAI_API_KEY=your-api-key-here
```

Or add to your `.env` file:
```
OPENAI_API_KEY=your-api-key-here
```

## Folder Structure Recommendation

**Recommended: One PDF per Lesson**

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

## Usage Examples

### Example 1: Process Single PDF File

```bash
python manage.py process_pdf_to_lesson \
    --course positive_psychology \
    --module "Module 1" \
    --pdf-path "courses/positive_psychology/module1/lesson1.pdf" \
    --lesson-title "Introduction to Positive Psychology"
```

### Example 2: Process Entire Folder

```bash
python manage.py process_pdf_to_lesson \
    --course positive_psychology \
    --module "Module 1" \
    --folder-path "courses/positive_psychology/module1/"
```

This will process all PDF files in the folder, creating one lesson per PDF.

### Example 3: Split Large PDF into Multiple Lessons

If you have a large PDF (e.g., 50 pages) and want to split it into lessons of 10 pages each:

```bash
python manage.py process_pdf_to_lesson \
    --course positive_psychology \
    --module "Module 1" \
    --pdf-path "courses/positive_psychology/module1_complete.pdf" \
    --split-by-pages 10 \
    --lesson-title "Module 1 Content"
```

This will create:
- Lesson 1: Pages 1-10
- Lesson 2: Pages 11-20
- Lesson 3: Pages 21-30
- etc.

### Example 4: Dry Run (Preview Without Creating)

```bash
python manage.py process_pdf_to_lesson \
    --course positive_psychology \
    --module "Module 1" \
    --folder-path "courses/positive_psychology/module1/" \
    --dry-run
```

This shows what would be created without actually creating lessons.

### Example 5: Skip AI Generation (Basic Text Only)

```bash
python manage.py process_pdf_to_lesson \
    --course positive_psychology \
    --module "Module 1" \
    --pdf-path "courses/positive_psychology/module1/lesson1.pdf" \
    --skip-ai
```

This creates lessons with basic text extraction only (no AI-generated titles, descriptions, etc.).

## What Gets Generated

When using AI generation (default), each lesson will have:

1. **Title**: AI-generated engaging lesson title
2. **Short Summary**: 1-2 sentence summary
3. **Full Description**: 2-3 paragraph description
4. **Content Blocks**: Structured Editor.js content with:
   - Headers (H2, H3)
   - Paragraphs
   - Lists (bulleted, numbered)
   - Quotes
5. **Learning Outcomes**: 3-5 bullet points
6. **AI Coach Actions**: Suggested actions for the AI chatbot

## Workflow

1. **Prepare PDFs**: Organize PDFs by course/module/lesson
2. **Run Command**: Execute the management command
3. **Review**: Check generated lessons in Django admin
4. **Refine**: Edit any lessons that need adjustment
5. **Approve**: Set `ai_generation_status` to 'approved' to finalize

## Troubleshooting

### Error: "OpenAI API key not found"
- Make sure `OPENAI_API_KEY` environment variable is set
- Or pass `api_key` parameter to `AIContentGenerator`

### Error: "PDF file not found"
- Check the path is correct (relative to project root)
- Use forward slashes `/` even on Windows

### Error: "Neither PyPDF2 nor pdfplumber is installed"
- Install: `pip install PyPDF2 pdfplumber`

### AI Generation Fails
- Check your OpenAI API key is valid
- Check you have API credits
- The system will fall back to basic text extraction if AI fails

## Tips

1. **One PDF per Lesson**: This gives you the best control and most accurate AI generation
2. **Meaningful Filenames**: Use descriptive filenames (they become suggested titles)
3. **Review Before Approving**: Always review AI-generated content before marking as 'approved'
4. **Batch Processing**: Process entire folders at once for efficiency
5. **Dry Run First**: Use `--dry-run` to preview before processing

## Next Steps

After processing PDFs:

1. Review lessons in Django admin
2. Add video URLs if needed
3. Generate quizzes from lesson content
4. Train AI chatbots on lesson content
5. Publish lessons to students

