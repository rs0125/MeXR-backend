"""Custom LangChain tools for VR scene manipulation."""

from typing import Dict, Any
from langchain_core.tools import tool


@tool
def highlight_object(target_id: str, color: str = "#00FF00", duration: int = 5, pattern: str = "pulse") -> Dict[str, Any]:
    """
    Creates a command to highlight a specific object or socket in the VR scene.
    Use this to visually guide the user's attention, for example, to show where an organ should be placed.
    The target_id should be the unique identifier of the object to highlight.
    
    Args:
        target_id: The unique identifier of the object to highlight
        color: Hex color code for the highlight (default: green)
        duration: Duration of the highlight in seconds
        pattern: Highlight pattern (e.g., "pulse", "steady")
        
    Returns:
        Dictionary containing the highlight command structure
    """
    return {
        "command": "highlight",
        "targetID": target_id,
        "options": {"color": color, "duration": duration, "pattern": pattern}
    }


@tool
def play_sound(sound_id: str) -> Dict[str, Any]:
    """
    Creates a command to play a specific sound effect in the VR scene.
    Use this to provide auditory feedback, such as 'positive_feedback_chime' for a correct action.
    
    Args:
        sound_id: The identifier of the sound to play
        
    Returns:
        Dictionary containing the play sound command structure
    """
    return {
        "command": "playSound",
        "targetID": sound_id
    }


def get_all_tools():
    """
    Get a list of all available tools.
    
    Returns:
        List of tool functions
    """
    return [highlight_object, play_sound]
