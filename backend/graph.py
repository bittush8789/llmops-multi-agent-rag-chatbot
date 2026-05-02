from langgraph.graph import StateGraph, END
from backend.agents import (
    GraphState,
    orchestrator_node,
    retriever_node,
    customer_support_agent_node,
    product_agent_node,
    hr_agent_node,
    it_helpdesk_agent_node,
    sales_agent_node,
    management_agent_node,
    escalation_agent_node,
    validator_node
)

def route_after_orchestrator(state: GraphState):
    agent = state.get("next_agent", "customer_support_agent")
    if agent == "escalation_agent":
        return "escalation"
    return "retriever"

def route_after_retriever(state: GraphState):
    agent = state.get("next_agent", "customer_support_agent")
    if agent == "customer_support_agent":
        return "customer_support"
    elif agent == "product_agent":
        return "product"
    elif agent == "hr_agent":
        return "hr"
    elif agent == "it_helpdesk_agent":
        return "it_helpdesk"
    elif agent == "sales_agent":
        return "sales"
    elif agent == "management_agent":
        return "management"
    else:
        return "customer_support"

def build_graph():
    workflow = StateGraph(GraphState)
    
    workflow.add_node("orchestrator", orchestrator_node)
    workflow.add_node("retriever", retriever_node)
    workflow.add_node("customer_support", customer_support_agent_node)
    workflow.add_node("product", product_agent_node)
    workflow.add_node("hr", hr_agent_node)
    workflow.add_node("it_helpdesk", it_helpdesk_agent_node)
    workflow.add_node("sales", sales_agent_node)
    workflow.add_node("management", management_agent_node)
    workflow.add_node("escalation", escalation_agent_node)
    workflow.add_node("validator", validator_node)
    
    workflow.set_entry_point("orchestrator")
    
    workflow.add_conditional_edges(
        "orchestrator",
        route_after_orchestrator,
        {
            "escalation": "escalation",
            "retriever": "retriever"
        }
    )
    
    workflow.add_conditional_edges(
        "retriever",
        route_after_retriever,
        {
            "customer_support": "customer_support",
            "product": "product",
            "hr": "hr",
            "it_helpdesk": "it_helpdesk",
            "sales": "sales",
            "management": "management"
        }
    )
    
    workflow.add_edge("customer_support", "validator")
    workflow.add_edge("product", "validator")
    workflow.add_edge("hr", "validator")
    workflow.add_edge("it_helpdesk", "validator")
    workflow.add_edge("sales", "validator")
    workflow.add_edge("management", "validator")
    workflow.add_edge("escalation", "validator")
    
    workflow.add_edge("validator", END)
    
    return workflow.compile()

app_graph = build_graph()
