# MeXR Backend

A FastAPI backend for VR medical training simulation that uses LangChain and OpenAI to process user queries and return structured JSON responses with actions for the VR client.

## Features

-  **AI-Powered Anatomy Assistant**: Uses GPT-4 to answer medical questions
-  **Interactive VR Commands**: Highlights objects and plays sounds in VR
-  **Session Management**: Maintains conversation history per user session
-  **Modular Architecture**: Clean separation of concerns with well-organized modules
-  **Anatomy Knowledge Base**: Pre-loaded information about human organs
-  **FastAPI Framework**: Fast, modern, and async-ready API

## Project Structure

```
MeXR-backend/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration and environment variables
│   ├── models.py            # Pydantic models for request/response validation
│   ├── knowledge_base.py    # Anatomy knowledge database
│   ├── tools.py             # LangChain tools for VR interactions
│   ├── agent.py             # LangChain agent setup
│   ├── session.py           # Session and chat history management
│   └── routes.py            # API route handlers
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Prerequisites

- Python 3.8+
- OpenAI API key

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rs0125/MeXR-backend.git
   cd MeXR-backend
   ```

2. **Create a virtual environment** (recommended)
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
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

## Running the Application

### Development Mode

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:
- **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### `POST /medtech/query`

Process a query from the VR application.

**Request Body:**
```json
{
  "sessionID": "user_session_xyz123",
  "context": {
    "heldObject": "heart"
  },
  "query": "Where does this go?"
}
```

**Response:**
```json
{
  "displayText": "The heart should be placed in the chest cavity...",
  "spokenResponse": "The heart should be placed in the chest cavity...",
  "actions": [
    {
      "command": "highlight",
      "targetID": "socket_heart",
      "options": {
        "color": "#00FF00",
        "duration": 5,
        "pattern": "pulse"
      }
    }
  ]
}
```

### `GET /health`

Health check endpoint to verify the service is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "MeXR Backend"
}
```

## Architecture Overview

### Configuration (`app/config.py`)
Loads environment variables and manages application configuration settings.

### Knowledge Base (`app/knowledge_base.py`)
Contains anatomical information about organs including:
- Display names
- Socket IDs for VR placement
- Descriptions
- Functions

### Tools (`app/tools.py`)
LangChain tools that the AI agent can use:
- `highlight_object`: Highlights objects in VR scene
- `play_sound`: Plays audio feedback

### Agent (`app/agent.py`)
Sets up the LangChain agent with:
- OpenAI GPT-4 model
- Custom tools
- System prompt for medical expertise

### Session Management (`app/session.py`)
Manages conversation history for each user session, maintaining context across multiple queries.

### API Routes (`app/routes.py`)
Handles incoming requests, processes them through the agent, and returns formatted responses.

## Supported Organs

The current knowledge base includes:
- Heart
- Liver
- Stomach
- Left Lung
- Right Lung

To add more organs, edit `app/knowledge_base.py` and add entries to the `ANATOMY_KNOWLEDGE` dictionary.

## Development

### Adding New Tools

1. Add a new tool function in `app/tools.py`:
   ```python
   @tool
   def your_new_tool(param: str) -> Dict[str, Any]:
       """Tool description for the AI."""
       return {"command": "yourCommand", "targetID": param}
   ```

2. Add it to the `get_all_tools()` function

### Adding New Organs

Edit `app/knowledge_base.py` and add to `ANATOMY_KNOWLEDGE`:
```python
"organ_id": {
    "displayName": "Organ Name",
    "socketID": "socket_organ_id",
    "description": "Description...",
    "function": "Function..."
}
```

### Customizing the Agent

Modify the system prompt in `app/agent.py` to change the AI's behavior and personality.

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |

## Security Notes

-  Never commit your `.env` file to version control
-  Keep your OpenAI API key secure
-  The `.gitignore` file is configured to exclude `.env` automatically

## Troubleshooting

**Issue: "OPENAI_API_KEY not found" error**
- Make sure you've created a `.env` file in the project root
- Verify the API key is correctly set in `.env`
- Restart the application after adding the key

**Issue: Import errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're in the correct virtual environment

**Issue: Port already in use**
- Change the port: `uvicorn main:app --port 8001`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

See LICENSE file for details.

