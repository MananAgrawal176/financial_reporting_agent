# state.py
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # The full message history - drives the ReAct loop
    # add_messages is a reducer: appends new messages rather than overwriting
    messages: Annotated[list[BaseMessage], add_messages]
    
    # The ticker being researched
    ticker: str
    
    # Structured research outputs (populated by tools)
    financials: dict
    news_sentiment: dict
    technical_indicators: dict
    analyst_ratings: dict
    
    # Final output
    investment_brief: str