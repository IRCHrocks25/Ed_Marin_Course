# Webhook-Based Content Generation System

## Overview

This system allows you to generate course content, modules, and lessons via a webhook. The webhook accepts course and module parameters for metadata filtering, and returns content under the `Response` field.

## Endpoint

**URL:** `/api/generate-course-content/`  
**Method:** `POST`  
**Authentication:** Staff member required  
**Default Webhook:** `https://katalyst-crm2.fly.dev/webhook/d90c3bb9-89f7-4658-86ba-f5406662b2b3`

## Request Format

```json
{
    "course": "positive_psychology",
    "module": "Module1",
    "webhook_url": "https://your-webhook-url.com/webhook/..." // Optional
}
```

### Course Types

The following course types are supported:
- `positive_psychology` - Positive Psychology
- `nlp` - NLP
- `nutrition` - Nutrition
- `naturopathy` - Naturopathy
- `hypnotherapy` - Hypnotherapy
- `ayurveda` - Ayurveda
- `art_therapy` - Art Therapy
- `aroma_therapy` - Aroma Therapy

### Module Format

Module names can be any string (e.g., "Module1", "Module2", "Introduction", etc.)

## Webhook Payload Sent

The system sends the following payload to your webhook:

```json
{
    "course": "positive_psychology",
    "module": "Module1",
    "metadata": {
        "course": "positive_psychology",
        "module": "Module1"
    }
}
```

## Expected Webhook Response

Your webhook should return a JSON response with content under the `Response` field:

```json
{
    "Response": {
        "course": {
            "name": "Positive Psychology",
            "description": "Full course description here...",
            "short_description": "Short description for course cards"
        },
        "module": {
            "name": "Module1",
            "description": "Module description here...",
            "order": 1
        },
        "lessons": [
            {
                "title": "Introduction to Positive Psychology",
                "description": "Lesson description here...",
                "order": 1,
                "lesson_type": "video"
            },
            {
                "title": "Understanding Happiness",
                "description": "Another lesson description...",
                "order": 2,
                "lesson_type": "video"
            }
        ]
    }
}
```

### Response Field Structure

- **course** (object):
  - `name` (string): Course name
  - `description` (string): Full course description
  - `short_description` (string): Short description (max 300 chars)

- **module** (object):
  - `name` (string): Module name
  - `description` (string): Module description
  - `order` (integer): Display order

- **lessons** (array):
  - `title` (string, required): Lesson title
  - `description` (string): Lesson description
  - `order` (integer): Display order
  - `lesson_type` (string): "video", "live", or "replay" (default: "video")

## API Response

### Success Response

```json
{
    "success": true,
    "message": "Content generated successfully",
    "result": {
        "course_created": true,
        "course_updated": false,
        "module_created": true,
        "module_updated": false,
        "lessons_created": 2,
        "lessons_updated": 0,
        "errors": []
    }
}
```

### Error Response

```json
{
    "success": false,
    "error": "Error message here"
}
```

## Example Usage

### Using cURL

```bash
curl -X POST http://your-domain.com/api/generate-course-content/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: your-csrf-token" \
  -d '{
    "course": "positive_psychology",
    "module": "Module1"
  }'
```

### Using Python

```python
import requests

url = "http://your-domain.com/api/generate-course-content/"
headers = {
    "Content-Type": "application/json",
    "X-CSRFToken": "your-csrf-token"
}
data = {
    "course": "positive_psychology",
    "module": "Module1"
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

## Behavior

1. **Course Creation/Update**: 
   - If a course with the same slug exists, it will be updated
   - Otherwise, a new course will be created

2. **Module Creation/Update**:
   - If a module with the same name exists in the course, it will be updated
   - Otherwise, a new module will be created

3. **Lesson Creation/Update**:
   - If a lesson with the same slug exists in the course/module, it will be updated
   - Otherwise, a new lesson will be created

## Notes

- The `Response` field can contain either a JSON object (as shown above) or a JSON string that will be parsed
- If `Response` contains only a string, it will be treated as a course description
- Course slugs are automatically generated from course names
- Lesson slugs are automatically generated from lesson titles
- All operations are idempotent - running the same request multiple times will update existing records rather than creating duplicates

