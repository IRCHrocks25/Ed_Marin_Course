# Creator PDF Upload Interface - User Guide

## Overview

The PDF upload interface is now available in the Creator Dashboard, allowing you to upload PDF files and automatically generate structured lesson content using AI.

## Accessing the Feature

1. Go to **Creator Dashboard**: `/creator/`
2. Select a course
3. Click **"Upload PDF Lessons"** button (blue button next to "Add New Lesson")
4. Or navigate directly to: `/creator/courses/<course_slug>/upload-pdf/`

## How to Use

### Step 1: Select Course & Module

- **Course**: Automatically set to the current course
- **Module Name**: Enter the module name (e.g., "Module 1", "Introduction", "Fundamentals")
  - If the module doesn't exist, it will be created automatically
  - If it exists, lessons will be added to that module

### Step 2: Upload PDF Files

- Click the upload area or drag and drop PDF files
- **Multiple files supported**: Upload multiple PDFs at once
- Each PDF will become a separate lesson (unless splitting is enabled)

### Step 3: Configure Processing Options

- **Use AI Generation** (checked by default):
  - ✅ Enabled: AI generates titles, descriptions, content blocks, outcomes, and coach actions
  - ❌ Disabled: Basic text extraction only (no AI processing)

- **Split Large PDFs** (optional):
  - Enter number of pages per lesson (e.g., 10 = split every 10 pages)
  - Leave empty or 0 to process each PDF as one complete lesson

### Step 4: Process

Click **"Process PDFs & Generate Lessons"** button

## What Happens

1. **PDF Text Extraction**: Text is extracted from each PDF
2. **AI Processing** (if enabled):
   - Generates engaging lesson title
   - Creates short summary (1-2 sentences)
   - Creates full description (2-3 paragraphs)
   - Structures content into Editor.js blocks (headers, paragraphs, lists, quotes)
   - Generates learning outcomes (3-5 bullet points)
   - Suggests AI coach actions
3. **Lesson Creation**: Lessons are created with all generated content
4. **Redirect**: You're redirected to the course lessons page to review

## Review & Edit

After processing:

1. Go to the course lessons page
2. Review generated lessons
3. Click **"Edit"** on any lesson to:
   - Review AI-generated content
   - Make adjustments
   - Approve and finalize

## Tips

- **One PDF per Lesson**: Works best for accurate AI generation
- **Descriptive Filenames**: PDF filenames become suggested titles
- **Review Before Approving**: Always review AI-generated content
- **Edit Anytime**: You can edit lessons after creation
- **Batch Processing**: Upload multiple PDFs at once for efficiency

## Troubleshooting

### "Required packages not installed"
- Install: `pip install PyPDF2 pdfplumber openai`

### "AI generation not available"
- Check `OPENAI_API_KEY` environment variable is set
- Verify you have OpenAI API credits
- System will fall back to basic text extraction

### "Error processing PDF"
- Check PDF file is not corrupted
- Ensure PDF contains extractable text (not just images)
- Try processing one PDF at a time

## File Size Limits

- No hard limit, but very large PDFs may take longer to process
- Recommended: Keep PDFs under 50MB for best performance
- For very large PDFs, use the "Split by Pages" option

## Next Steps After Upload

1. **Review Lessons**: Check generated content
2. **Add Videos**: Add video URLs if needed
3. **Generate Quizzes**: Create quizzes from lesson content
4. **Train Chatbots**: Train AI chatbots on lesson content
5. **Publish**: Make lessons available to students

