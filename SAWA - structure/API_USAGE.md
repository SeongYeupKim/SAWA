# SAWA API Usage Guide

This guide provides detailed examples of how to use the SAWA API for scientific argumentative writing assistance.

## Authentication

All API endpoints (except registration and login) require authentication using JWT tokens.

### Register a New User

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "username": "student1",
    "password": "password123",
    "full_name": "John Student"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=student1&password=password123"
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

## Chatbot Conversation Flow

### 1. Start a New Conversation

```bash
curl -X POST "http://localhost:8000/api/chatbot/start" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt_id": 1
  }'
```

Response:
```json
{
  "message": "Write a scientific argument about the role of greenhouse gases in climate change...",
  "message_type": "ai_prompt",
  "conversation_id": 1,
  "next_step": "student_response",
  "should_continue": true
}
```

### 2. Submit Student Response

```bash
curl -X POST "http://localhost:8000/api/chatbot/respond" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": 1,
    "content": "Climate change is primarily caused by greenhouse gases such as carbon dioxide and methane. These gases trap heat in the Earth's atmosphere, creating a greenhouse effect. Human activities, particularly the burning of fossil fuels, have significantly increased the concentration of these gases. Scientific evidence from ice core samples and atmospheric measurements shows a clear correlation between rising CO2 levels and global temperature increases. Therefore, reducing greenhouse gas emissions is essential to mitigate climate change."
  }'
```

Response:
```json
{
  "message": "Excellent work! Your response demonstrates strong scientific argumentation skills.\n\n**Strengths:**\n• Clear thesis statement about greenhouse gases and climate change\n• Good use of scientific terminology\n• Strong evidence from ice core samples and atmospheric measurements\n• Logical conclusion connecting evidence to action\n\n**Areas for Improvement:**\n• Could include more specific data or statistics\n• Consider discussing the mechanism of the greenhouse effect in more detail\n\n**Specific Suggestions:**\n• Add specific CO2 concentration numbers (e.g., pre-industrial vs. current levels)\n• Explain how greenhouse gases physically trap heat\n• Include examples of specific human activities that contribute to emissions",
  "message_type": "ai_feedback",
  "conversation_id": 1,
  "next_step": "continue_question",
  "feedback": {
    "feedback_text": "...",
    "scores": {
      "argument_structure": 8.5,
      "evidence_quality": 7.0,
      "scientific_accuracy": 9.0,
      "clarity": 8.0,
      "overall": 8.1
    },
    "strengths": ["Clear thesis statement", "Good use of scientific terminology"],
    "areas_for_improvement": ["Could include more specific data"],
    "specific_suggestions": ["Add specific CO2 concentration numbers"]
  },
  "should_continue": true
}
```

### 3. Continue the Conversation

```bash
curl -X POST "http://localhost:8000/api/chatbot/continue/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '"Yes, I would like to discuss more about the greenhouse effect mechanism"'
```

Response:
```json
{
  "message": "Great! Let's explore the greenhouse effect mechanism in more detail. The greenhouse effect works like this: solar radiation enters Earth's atmosphere and warms the surface. The Earth then emits infrared radiation back toward space. Greenhouse gases in the atmosphere absorb some of this outgoing infrared radiation and re-emit it in all directions, including back toward Earth's surface. This process traps heat and warms the planet. What specific aspect of this mechanism would you like to explore further?",
  "message_type": "ai_feedback",
  "conversation_id": 1,
  "next_step": "continue_question",
  "should_continue": true
}
```

### 4. End the Conversation

```bash
curl -X POST "http://localhost:8000/api/chatbot/continue/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '"No, thank you. I think I have enough information now."'
```

Response:
```json
{
  "message": "Thank you for using SAWA! Your conversation has been archived.",
  "message_type": "ai_feedback",
  "conversation_id": 1,
  "next_step": "completed",
  "should_continue": false
}
```

## Managing Prompts

### Get All Available Prompts

```bash
curl -X GET "http://localhost:8000/api/prompts/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Filter Prompts

```bash
# Filter by category
curl -X GET "http://localhost:8000/api/prompts/?category=biology" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Filter by difficulty level
curl -X GET "http://localhost:8000/api/prompts/?difficulty_level=beginner" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Filter by subject area
curl -X GET "http://localhost:8000/api/prompts/?subject_area=chemistry" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Create New Prompt (Teachers Only)

```bash
curl -X POST "http://localhost:8000/api/prompts/" \
  -H "Authorization: Bearer TEACHER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "DNA Replication Process",
    "content": "Explain the process of DNA replication and its importance in cell division...",
    "category": "biology",
    "difficulty_level": "intermediate",
    "subject_area": "biology",
    "expected_elements": "[\"helicase\", \"polymerase\", \"base_pairing\", \"semi_conservative\"]"
  }'
```

## Analytics and Progress Tracking

### Get User Progress

```bash
curl -X GET "http://localhost:8000/api/analytics/user/progress" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Response:
```json
{
  "total_conversations": 5,
  "completed_conversations": 4,
  "completion_rate": 0.8,
  "average_scores": {
    "overall": 7.8,
    "argument_structure": 8.2,
    "evidence_quality": 7.5,
    "clarity": 7.9
  },
  "recent_activity": {
    "conversations_last_30_days": 3
  }
}
```

### Get Feedback History

```bash
curl -X GET "http://localhost:8000/api/analytics/user/feedback-history" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Conversation History

```bash
curl -X GET "http://localhost:8000/api/chatbot/history/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Error Handling

The API returns standard HTTP status codes:

- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

Error responses include a `detail` field with the error message:

```json
{
  "detail": "Prompt not found"
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse. If you exceed the rate limit, you'll receive a `429 Too Many Requests` response.

## WebSocket Support (Future Enhancement)

Future versions may include WebSocket support for real-time conversations:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chatbot');
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};
```

## SDK Examples

### Python SDK Example

```python
import requests

class SAWAClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.token = None
    
    def login(self, username, password):
        response = requests.post(f"{self.base_url}/api/auth/login", 
                               data={"username": username, "password": password})
        self.token = response.json()["access_token"]
        return self.token
    
    def start_conversation(self, prompt_id):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{self.base_url}/api/chatbot/start",
                               json={"prompt_id": prompt_id},
                               headers=headers)
        return response.json()
    
    def respond(self, conversation_id, content):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{self.base_url}/api/chatbot/respond",
                               json={"conversation_id": conversation_id, "content": content},
                               headers=headers)
        return response.json()

# Usage
client = SAWAClient()
client.login("student1", "password123")
conversation = client.start_conversation(1)
response = client.respond(conversation["conversation_id"], "My scientific argument...")
```

This completes the comprehensive SAWA chatbot API implementation following your preferred conversation flow!
