"""Pydantic models for API request and response validation."""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class VRQueryContext(BaseModel):
    """Context information about the current VR scene state."""
    heldObject: str = Field(
        ..., 
        description="The unique ID of the organ the user is holding.",
        example="heart"
    )


class VRQueryRequest(BaseModel):
    """Request model for VR query endpoint."""
    sessionID: str = Field(
        ..., 
        description="A unique identifier for the user session.",
        example="user_session_xyz123"
    )
    context: VRQueryContext
    query: str = Field(
        ..., 
        description="The user's spoken question.",
        example="Where does this go?"
    )


class Action(BaseModel):
    """Action to be performed in the VR scene."""
    command: str
    targetID: str
    options: Optional[Dict[str, Any]] = None


class VRQueryResponse(BaseModel):
    """Response model for VR query endpoint."""
    displayText: str
    spokenResponse: str
    actions: List[Action]
