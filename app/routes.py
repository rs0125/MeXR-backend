"""API route handlers."""

from fastapi import APIRouter

from app.models import VRQueryRequest, VRQueryResponse
from app.knowledge_base import get_organ_info
from app.agent import create_agent
from app.session import session_manager

router = APIRouter()

# Initialize the agent once
agent_executor = create_agent()


@router.post("/medtech/query", response_model=VRQueryResponse)
async def process_vr_query(request: VRQueryRequest):
    """
    Process a query from the VR application.
    
    Args:
        request: VRQueryRequest containing session ID, context, and user query
        
    Returns:
        VRQueryResponse with display text, spoken response, and actions
    """
    print(f"Received request for session {request.sessionID}: {request.query}")
    print(f"Context (Held Object): {request.context.heldObject}")

    # Retrieve organ info from knowledge base
    organ_id = request.context.heldObject
    organ_info = get_organ_info(organ_id)

    if not organ_info:
        return VRQueryResponse(
            displayText=f"Error: Organ with ID '{organ_id}' not found.",
            spokenResponse="I'm sorry, I don't have information about that object.",
            actions=[]
        )

    # Construct the input for the LangChain agent
    input_prompt = f"""
    User Query: "{request.query}"
    Held Organ: {organ_info['displayName']} (ID: {organ_id})
    Correct Socket ID for this organ: {organ_info['socketID']}
    Function of this organ: {organ_info['function']}
    General description: {organ_info['description']}
    """
    
    # Retrieve chat history for the current session
    chat_history = session_manager.get_history(request.sessionID)

    # Invoke the agent
    result = await agent_executor.ainvoke({
        "input": input_prompt,
        "chat_history": chat_history
    })
    
    # Extract the final answer and tool outputs
    final_answer = result.get("output", "I'm sorry, I encountered an error.")
    tool_outputs = result.get("intermediate_steps", [])
    actions_list = [step[1] for step in tool_outputs]

    # Update chat history
    session_manager.update_history(request.sessionID, request.query, final_answer)
    
    # Format and return the response
    response_data = {
        "displayText": final_answer,
        "spokenResponse": final_answer,
        "actions": actions_list
    }
    
    print(f"Sending response: {response_data}")

    return VRQueryResponse(**response_data)


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "MeXR Backend"}
