# SAWA - Scientific Argumentative Writing Assistant

A chatbot API designed to support students' preparation for scientific argumentative essays. SAWA follows a structured conversation flow that helps students develop their scientific argumentation skills through interactive feedback and guidance.

## Features

- **Structured Conversation Flow**: Implements the preferred logic where AI presents prompts, students respond, AI provides feedback, and offers options to continue discussion
- **AI-Powered Feedback**: Uses OpenAI GPT models to analyze student responses and provide detailed feedback on argument structure, evidence quality, scientific accuracy, and clarity
- **Comprehensive Analytics**: Tracks student progress, conversation history, and learning outcomes
- **Teacher Dashboard**: Allows teachers to create prompts, monitor student progress, and access system analytics
- **Secure Authentication**: JWT-based authentication system with role-based access control

## Conversation Flow

The chatbot follows this specific conversation pattern:

1. **AI presents the prompt** - Student receives a scientific argumentation prompt
2. **Student gives initial response** - Student submits their argument
3. **AI provides feedback** - Detailed analysis with scores and suggestions
4. **Continue question** - AI asks if student wants to discuss more
5. **Optional continuation** - If yes, continue the conversation; if no, archive the data

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with OAuth2
- **AI Integration**: OpenAI GPT-3.5-turbo
- **Migration**: Alembic
- **Documentation**: FastAPI automatic docs

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- OpenAI API key

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sawa-structure
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb sawa_db
   
   # Run migrations
   alembic upgrade head
   
   # Seed sample data
   python scripts/seed_data.py
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Chatbot
- `POST /api/chatbot/start` - Start new conversation
- `POST /api/chatbot/respond` - Submit student response
- `POST /api/chatbot/continue/{conversation_id}` - Continue conversation
- `GET /api/chatbot/history/{conversation_id}` - Get conversation history
- `GET /api/chatbot/conversations` - Get user's conversations

### Prompts
- `GET /api/prompts/` - Get all prompts (with filtering)
- `GET /api/prompts/{prompt_id}` - Get specific prompt
- `POST /api/prompts/` - Create new prompt (teachers only)
- `PUT /api/prompts/{prompt_id}` - Update prompt (teachers only)

### Analytics
- `GET /api/analytics/user/progress` - Get user progress
- `GET /api/analytics/user/feedback-history` - Get feedback history
- `GET /api/analytics/admin/overview` - Get system overview (admin)

## Database Schema

### Core Tables

- **users**: User accounts (students and teachers)
- **prompts**: Scientific argumentation prompts
- **conversations**: Chat sessions between users and AI
- **messages**: Individual messages in conversations
- **feedback_analyses**: Detailed feedback and scoring data

### Key Relationships

- Users can have multiple conversations
- Each conversation is based on a specific prompt
- Messages belong to conversations
- Feedback analyses are linked to messages and conversations

## Configuration

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/sawa_db

# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# JWT
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

## Usage Examples

### Starting a Conversation

```python
import requests

# Login
response = requests.post("http://localhost:8000/api/auth/login", 
                        data={"username": "student", "password": "student123"})
token = response.json()["access_token"]

headers = {"Authorization": f"Bearer {token}"}

# Start conversation
response = requests.post("http://localhost:8000/api/chatbot/start",
                        json={"prompt_id": 1},
                        headers=headers)
conversation = response.json()
```

### Submitting Student Response

```python
# Submit response
response = requests.post("http://localhost:8000/api/chatbot/respond",
                        json={
                            "conversation_id": conversation["conversation_id"],
                            "content": "Climate change is caused by greenhouse gases..."
                        },
                        headers=headers)
feedback = response.json()
```

## Development

### Running Tests

```bash
pytest
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Code Style

The project uses standard Python formatting. Run:

```bash
black .
isort .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact the development team or create an issue in the repository.
