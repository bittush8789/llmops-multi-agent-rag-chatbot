from typing import TypedDict, List, Dict, Any, Annotated
import operator
from langchain_core.messages import SystemMessage
from backend.utils import get_llm
from backend.rag import retrieve_context

class GraphState(TypedDict):
    query: str
    context: str
    sources: Annotated[List[str], operator.add]
    next_agent: str
    draft_answer: str
    final_answer: str
    agents_used: Annotated[List[str], operator.add]
    is_valid: bool
    escalate: bool

def orchestrator_node(state: GraphState):
    query = state.get("query", "")
    llm = get_llm("llama-3.1-8b-instant")
    
    prompt = f"""You are the Orchestrator Agent for TechNova Solutions.
Analyze the following user query and decide which specialized agent should handle it.
Available Agents:
- "customer_support_agent": For billing, refunds, subscription, and general troubleshooting.
- "product_agent": For questions about NovaChat AI, NovaCloud, NovaAnalytics, NovaAutomation, NovaSecure, NovaCRM, NovaAssist.
- "hr_agent": For leave policy, WFH policy, benefits, and hiring process.
- "it_helpdesk_agent": For password reset, SSO, VPN, and access issues.
- "sales_agent": For pricing guidance, product comparison, enterprise plan suggestions, and upsells.
- "management_agent": For trends, common complaints, KPI summaries, and usage analytics.
- "escalation_agent": If the query is completely unrelated, offensive, or requests direct human contact.

Respond ONLY with the exact name of the agent.

Query: {query}"""

    response = llm.invoke([SystemMessage(content=prompt)])
    decision = response.content.strip().lower()
    
    valid_agents = [
        "customer_support_agent", "product_agent", "hr_agent", 
        "it_helpdesk_agent", "sales_agent", "management_agent", "escalation_agent"
    ]
    
    found_agent = "customer_support_agent" # Default
    for agent in valid_agents:
        if agent in decision:
            found_agent = agent
            break
            
    return {"next_agent": found_agent, "agents_used": ["orchestrator_agent"]}

def retriever_node(state: GraphState):
    query = state.get("query", "")
    context, sources = retrieve_context(query)
    return {"context": context, "sources": sources, "agents_used": ["retriever_agent"]}

def customer_support_agent_node(state: GraphState):
    llm = get_llm("llama-3.1-8b-instant")
    query = state.get("query", "")
    context = state.get("context", "")
    
    prompt = f"""You are the Customer Support Agent for TechNova Solutions.
Answer the user's query using ONLY the context provided.
Context:
{context}
Query: {query}"""

    response = llm.invoke([SystemMessage(content=prompt)])
    return {"draft_answer": response.content, "agents_used": ["customer_support_agent"]}

def product_agent_node(state: GraphState):
    llm = get_llm("llama-3.1-8b-instant")
    query = state.get("query", "")
    context = state.get("context", "")
    
    prompt = f"""You are the Product Agent for TechNova Solutions.
Answer the user's query using ONLY the context provided.
Context:
{context}
Query: {query}"""

    response = llm.invoke([SystemMessage(content=prompt)])
    return {"draft_answer": response.content, "agents_used": ["product_agent"]}

def hr_agent_node(state: GraphState):
    llm = get_llm("llama-3.1-8b-instant")
    query = state.get("query", "")
    context = state.get("context", "")
    
    prompt = f"""You are the HR Agent for TechNova Solutions.
Answer the user's query using ONLY the context provided.
Context:
{context}
Query: {query}"""

    response = llm.invoke([SystemMessage(content=prompt)])
    return {"draft_answer": response.content, "agents_used": ["hr_agent"]}

def it_helpdesk_agent_node(state: GraphState):
    llm = get_llm("llama-3.1-8b-instant")
    query = state.get("query", "")
    context = state.get("context", "")
    
    prompt = f"""You are the IT Helpdesk Agent for TechNova Solutions.
Answer the user's query using ONLY the context provided.
Context:
{context}
Query: {query}"""

    response = llm.invoke([SystemMessage(content=prompt)])
    return {"draft_answer": response.content, "agents_used": ["it_helpdesk_agent"]}

def sales_agent_node(state: GraphState):
    llm = get_llm("llama-3.1-8b-instant")
    query = state.get("query", "")
    context = state.get("context", "")
    
    prompt = f"""You are the Sales Agent for TechNova Solutions.
Answer the user's query using ONLY the context provided.
Context:
{context}
Query: {query}"""

    response = llm.invoke([SystemMessage(content=prompt)])
    return {"draft_answer": response.content, "agents_used": ["sales_agent"]}

def management_agent_node(state: GraphState):
    llm = get_llm("llama-3.1-8b-instant")
    query = state.get("query", "")
    context = state.get("context", "")
    
    prompt = f"""You are the Management Agent for TechNova Solutions.
Answer the user's query using ONLY the context provided.
Context:
{context}
Query: {query}"""

    response = llm.invoke([SystemMessage(content=prompt)])
    return {"draft_answer": response.content, "agents_used": ["management_agent"]}

def escalation_agent_node(state: GraphState):
    return {
        "draft_answer": "I am unable to assist with this request. Please contact our support team at support@technovasolutions.com.",
        "escalate": True,
        "agents_used": ["escalation_agent"]
    }

def validator_node(state: GraphState):
    llm = get_llm("llama-3.1-8b-instant")
    query = state.get("query", "")
    context = state.get("context", "")
    draft_answer = state.get("draft_answer", "")
    escalate = state.get("escalate", False)
    
    if escalate:
        return {"final_answer": draft_answer, "is_valid": True, "agents_used": ["validator_agent"]}
        
    prompt = f"""You are the Validator Agent.
Check if the Draft Answer is grounded in the Context.
Context: {context}
Query: {query}
Draft Answer: {draft_answer}
Respond ONLY with the verified answer. If not grounded, say "I couldn't find that information in our knowledge base." """

    response = llm.invoke([SystemMessage(content=prompt)])
    return {"final_answer": response.content, "is_valid": True, "agents_used": ["validator_agent"]}
