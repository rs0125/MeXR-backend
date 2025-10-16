"""LangChain agent setup and execution."""

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.config import LLM_MODEL, LLM_TEMPERATURE
from app.tools import get_all_tools


def create_agent() -> AgentExecutor:
    """
    Create and configure the LangChain agent.
    
    Returns:
        Configured AgentExecutor instance
    """
    # Get all available tools
    tools = get_all_tools()
    
    # Initialize the OpenAI model
    llm = ChatOpenAI(model=LLM_MODEL, temperature=LLM_TEMPERATURE)
    
    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are an expert anatomy AI assistant for a medical training VR simulation.
        Your role is to answer user questions about human organs and to trigger helpful actions in the VR scene.

        You will receive the user's spoken question and the ID of the organ they are currently holding.

        Your task is to:
        1.  Provide a clear and concise answer to the user's question. This answer will be used for both display text and text-to-speech in the VR app.
        2.  If the question is about location (e.g., "where does this go?"), you MUST use the `highlight_object` tool to highlight the correct anatomical socket for the held organ.
        3.  You can use other tools, like `play_sound`, to provide additional feedback.
        4.  Formulate a final response that includes the text answer and a list of all tool-generated actions.
        """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Create the agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor
