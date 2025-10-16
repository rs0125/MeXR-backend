"""Session management for chat history."""

from typing import Dict, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from app.config import MAX_CHAT_HISTORY


class SessionManager:
    """Manages chat history for user sessions."""
    
    def __init__(self):
        self._chat_history_store: Dict[str, List[BaseMessage]] = {}
    
    def get_history(self, session_id: str) -> List[BaseMessage]:
        """
        Retrieve chat history for a session.
        
        Args:
            session_id: The unique session identifier
            
        Returns:
            List of chat messages
        """
        return self._chat_history_store.get(session_id, [])
    
    def update_history(self, session_id: str, query: str, response: str) -> None:
        """
        Update chat history with new interaction.
        
        Args:
            session_id: The unique session identifier
            query: The user's query
            response: The AI's response
        """
        history = self._chat_history_store.get(session_id, [])
        history.extend([
            HumanMessage(content=query),
            AIMessage(content=response)
        ])
        # Keep only the most recent messages
        self._chat_history_store[session_id] = history[-MAX_CHAT_HISTORY:]
    
    def clear_history(self, session_id: str) -> None:
        """
        Clear chat history for a session.
        
        Args:
            session_id: The unique session identifier
        """
        if session_id in self._chat_history_store:
            del self._chat_history_store[session_id]


# Global session manager instance
session_manager = SessionManager()
