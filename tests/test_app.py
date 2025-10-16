"""
Unit tests for MeXR Backend
Run with: pytest tests/test_app.py -v
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from langchain_core.messages import HumanMessage, AIMessage

from app.knowledge_base import get_organ_info, get_all_organs
from app.tools import highlight_object, play_sound, get_all_tools
from app.session import SessionManager
from app.models import VRQueryRequest, VRQueryContext, VRQueryResponse
from main import app


# Initialize test client
client = TestClient(app)


class TestKnowledgeBase:
    """Tests for the knowledge base module."""
    
    def test_get_organ_info_valid(self):
        """Test retrieving valid organ information."""
        organ = get_organ_info("heart")
        assert organ is not None
        assert organ["displayName"] == "Heart"
        assert organ["socketID"] == "socket_heart"
        assert "function" in organ
        assert "description" in organ
    
    def test_get_organ_info_invalid(self):
        """Test retrieving invalid organ returns None."""
        organ = get_organ_info("invalid_organ")
        assert organ is None
    
    def test_get_all_organs(self):
        """Test retrieving all organs."""
        organs = get_all_organs()
        assert len(organs) == 5
        assert "heart" in organs
        assert "liver" in organs
        assert "stomach" in organs
        assert "left_lung" in organs
        assert "right_lung" in organs


class TestTools:
    """Tests for LangChain tools."""
    
    def test_highlight_object_default_params(self):
        """Test highlight_object with default parameters."""
        result = highlight_object.invoke({"target_id": "socket_heart"})
        assert result["command"] == "highlight"
        assert result["targetID"] == "socket_heart"
        assert result["options"]["color"] == "#00FF00"
        assert result["options"]["duration"] == 5
        assert result["options"]["pattern"] == "pulse"
    
    def test_highlight_object_custom_params(self):
        """Test highlight_object with custom parameters."""
        result = highlight_object.invoke({
            "target_id": "socket_liver",
            "color": "#FF0000",
            "duration": 10,
            "pattern": "steady"
        })
        assert result["command"] == "highlight"
        assert result["targetID"] == "socket_liver"
        assert result["options"]["color"] == "#FF0000"
        assert result["options"]["duration"] == 10
        assert result["options"]["pattern"] == "steady"
    
    def test_play_sound(self):
        """Test play_sound tool."""
        result = play_sound.invoke({"sound_id": "positive_feedback_chime"})
        assert result["command"] == "playSound"
        assert result["targetID"] == "positive_feedback_chime"
    
    def test_get_all_tools(self):
        """Test getting all tools."""
        tools = get_all_tools()
        assert len(tools) == 2
        assert highlight_object in tools
        assert play_sound in tools


class TestSessionManager:
    """Tests for session management."""
    
    def test_new_session_empty_history(self):
        """Test that new session has empty history."""
        manager = SessionManager()
        history = manager.get_history("new_session")
        assert history == []
    
    def test_update_history(self):
        """Test updating session history."""
        manager = SessionManager()
        manager.update_history("session1", "What is this?", "This is a heart.")
        
        history = manager.get_history("session1")
        assert len(history) == 2
        assert isinstance(history[0], HumanMessage)
        assert history[0].content == "What is this?"
        assert isinstance(history[1], AIMessage)
        assert history[1].content == "This is a heart."
    
    def test_history_max_length(self):
        """Test that history is limited to MAX_CHAT_HISTORY."""
        manager = SessionManager()
        
        # Add 15 interactions (30 messages)
        for i in range(15):
            manager.update_history("session1", f"Question {i}", f"Answer {i}")
        
        history = manager.get_history("session1")
        # Should only keep last 10 messages (5 interactions)
        assert len(history) == 10
        # Check that we have the most recent messages
        assert "Question 14" in history[-2].content
        assert "Answer 14" in history[-1].content
    
    def test_clear_history(self):
        """Test clearing session history."""
        manager = SessionManager()
        manager.update_history("session1", "Question", "Answer")
        assert len(manager.get_history("session1")) == 2
        
        manager.clear_history("session1")
        assert len(manager.get_history("session1")) == 0
    
    def test_multiple_sessions(self):
        """Test that different sessions have separate histories."""
        manager = SessionManager()
        manager.update_history("session1", "Question 1", "Answer 1")
        manager.update_history("session2", "Question 2", "Answer 2")
        
        history1 = manager.get_history("session1")
        history2 = manager.get_history("session2")
        
        assert len(history1) == 2
        assert len(history2) == 2
        assert history1[0].content == "Question 1"
        assert history2[0].content == "Question 2"


class TestModels:
    """Tests for Pydantic models."""
    
    def test_vr_query_context_valid(self):
        """Test VRQueryContext model validation."""
        context = VRQueryContext(heldObject="heart")
        assert context.heldObject == "heart"
    
    def test_vr_query_request_valid(self):
        """Test VRQueryRequest model validation."""
        request = VRQueryRequest(
            sessionID="test_session",
            context=VRQueryContext(heldObject="heart"),
            query="Where does this go?"
        )
        assert request.sessionID == "test_session"
        assert request.context.heldObject == "heart"
        assert request.query == "Where does this go?"
    
    def test_vr_query_response_valid(self):
        """Test VRQueryResponse model validation."""
        response = VRQueryResponse(
            displayText="Test response",
            spokenResponse="Test response",
            actions=[]
        )
        assert response.displayText == "Test response"
        assert response.spokenResponse == "Test response"
        assert response.actions == []


class TestAPIEndpoints:
    """Tests for API endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct response."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "MeXR Backend is running" in data["message"]
        assert data["documentation"] == "/docs"
        assert data["health"] == "/health"
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "MeXR Backend"
    
    @pytest.mark.asyncio
    @patch('app.routes.agent_executor')
    async def test_query_endpoint_valid_organ(self, mock_agent):
        """Test query endpoint with valid organ."""
        # Mock the agent response
        mock_agent.ainvoke = AsyncMock(return_value={
            "output": "The heart goes in the chest cavity.",
            "intermediate_steps": [
                (None, {
                    "command": "highlight",
                    "targetID": "socket_heart",
                    "options": {"color": "#00FF00", "duration": 5, "pattern": "pulse"}
                })
            ]
        })
        
        request_data = {
            "sessionID": "test_session",
            "context": {"heldObject": "heart"},
            "query": "Where does this go?"
        }
        
        response = client.post("/medtech/query", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "displayText" in data
        assert "spokenResponse" in data
        assert "actions" in data
    
    def test_query_endpoint_invalid_organ(self):
        """Test query endpoint with invalid organ."""
        request_data = {
            "sessionID": "test_session",
            "context": {"heldObject": "invalid_organ"},
            "query": "What is this?"
        }
        
        response = client.post("/medtech/query", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "Error" in data["displayText"]
        assert "invalid_organ" in data["displayText"]
        assert data["actions"] == []
    
    def test_query_endpoint_missing_fields(self):
        """Test query endpoint with missing required fields."""
        request_data = {
            "sessionID": "test_session",
            # Missing context and query
        }
        
        response = client.post("/medtech/query", json=request_data)
        assert response.status_code == 422  # Validation error


class TestIntegration:
    """Integration tests for the full application flow."""
    
    @pytest.mark.asyncio
    @patch('app.routes.agent_executor')
    async def test_full_query_flow(self, mock_agent):
        """Test complete query flow from request to response."""
        # Mock the agent to return a complete response
        mock_agent.ainvoke = AsyncMock(return_value={
            "output": "The liver is located in the upper right abdomen. I'll highlight where it goes.",
            "intermediate_steps": [
                (None, {
                    "command": "highlight",
                    "targetID": "socket_liver",
                    "options": {"color": "#00FF00", "duration": 5, "pattern": "pulse"}
                }),
                (None, {
                    "command": "playSound",
                    "targetID": "positive_feedback"
                })
            ]
        })
        
        request_data = {
            "sessionID": "integration_test_session",
            "context": {"heldObject": "liver"},
            "query": "Where does the liver go?"
        }
        
        response = client.post("/medtech/query", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "displayText" in data
        assert "spokenResponse" in data
        assert "actions" in data
        
        # Verify actions are present
        assert len(data["actions"]) >= 1
        
        # Verify at least one action is a highlight command
        commands = [action["command"] for action in data["actions"]]
        assert "highlight" in commands or "playSound" in commands


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
