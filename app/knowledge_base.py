"""Knowledge base containing anatomy information for the VR simulation."""

from typing import Dict, Any, Optional

ANATOMY_KNOWLEDGE = {
    "heart": {
        "displayName": "Heart",
        "socketID": "socket_heart",
        "description": "The heart is a muscular organ that pumps blood through the circulatory system by contraction and relaxation.",
        "function": "Its primary function is to pump oxygenated blood to the body and deoxygenated blood to the lungs."
    },
    "liver": {
        "displayName": "Liver",
        "socketID": "socket_liver",
        "description": "The liver is a large, meaty organ that sits on the right side of the belly, weighing about 3 pounds.",
        "function": "It filters the blood from the digestive tract, detoxifies chemicals, metabolizes drugs, and makes proteins important for blood clotting."
    },
    "stomach": {
        "displayName": "Stomach",
        "socketID": "socket_stomach",
        "description": "The stomach is a J-shaped organ that digests food. It produces enzymes and acids.",
        "function": "It secretes acid and enzymes that digest food, breaking it down before it moves to the small intestine."
    },
    "left_lung": {
        "displayName": "Left Lung",
        "socketID": "socket_left_lung",
        "description": "The left lung is one of the two lungs, located in the chest. It is slightly smaller than the right lung to make room for the heart.",
        "function": "Its main function is the process of gas exchange called respiration (or breathing)."
    },
    "right_lung": {
        "displayName": "Right Lung",
        "socketID": "socket_right_lung",
        "description": "The right lung is one of the two lungs, located in the chest. It is divided into three lobes.",
        "function": "Its main function is the process of gas exchange called respiration (or breathing)."
    }
}


def get_organ_info(organ_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve organ information from the knowledge base.
    
    Args:
        organ_id: The unique identifier for the organ
        
    Returns:
        Dictionary containing organ information, or None if not found
    """
    return ANATOMY_KNOWLEDGE.get(organ_id)


def get_all_organs() -> Dict[str, Dict[str, Any]]:
    """
    Get all organs in the knowledge base.
    
    Returns:
        Dictionary of all organs and their information
    """
    return ANATOMY_KNOWLEDGE
