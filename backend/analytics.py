import json
import os
import time
from collections import defaultdict
from typing import List, Dict

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ANALYTICS_FILE = os.path.join(BASE_DIR, 'analytics_data.json')

from collections import defaultdict

def load_analytics():
    if os.path.exists(ANALYTICS_FILE):
        with open(ANALYTICS_FILE, 'r') as f:
            raw_data = json.load(f)
            # Re-wrap in defaultdict
            data = {
                "total_queries": raw_data.get("total_queries", 0),
                "agent_usage": defaultdict(int, raw_data.get("agent_usage", {})),
                "common_questions": defaultdict(int, raw_data.get("common_questions", {})),
                "failed_answers": raw_data.get("failed_answers", 0),
                "response_times": raw_data.get("response_times", []),
                "department_distribution": defaultdict(int, raw_data.get("department_distribution", {}))
            }
            return data
    return {
        "total_queries": 0,
        "agent_usage": defaultdict(int),
        "common_questions": defaultdict(int),
        "failed_answers": 0,
        "response_times": [],
        "department_distribution": defaultdict(int)
    }

def save_analytics(data):
    # Convert defaultdict to regular dict for JSON serialization
    serializable_data = {
        "total_queries": data["total_queries"],
        "agent_usage": dict(data["agent_usage"]),
        "common_questions": dict(data["common_questions"]),
        "failed_answers": data["failed_answers"],
        "response_times": data["response_times"],
        "department_distribution": dict(data["department_distribution"])
    }
    with open(ANALYTICS_FILE, 'w') as f:
        json.dump(serializable_data, f, indent=4)

def log_interaction(query: str, agents: List[str], response_time: float, success: bool, department: str = "unknown"):
    data = load_analytics()
    
    data["total_queries"] += 1
    for agent in agents:
        data["agent_usage"][agent] += 1
    
    data["common_questions"][query.lower()] += 1
    
    if not success:
        data["failed_answers"] += 1
        
    data["response_times"].append(response_time)
    # Keep only last 100 response times for average
    if len(data["response_times"]) > 100:
        data["response_times"] = data["response_times"][-100:]
        
    data["department_distribution"][department] += 1
    
    save_analytics(data)

def get_analytics_summary():
    data = load_analytics()
    avg_response_time = sum(data["response_times"]) / len(data["response_times"]) if data["response_times"] else 0
    
    return {
        "total_queries": data["total_queries"],
        "most_used_agent": max(data["agent_usage"], key=data["agent_usage"].get) if data["agent_usage"] else "None",
        "avg_response_time": round(avg_response_time, 2),
        "failure_rate": f"{(data['failed_answers'] / data['total_queries'] * 100):.2f}%" if data["total_queries"] > 0 else "0%",
        "top_department": max(data["department_distribution"], key=data["department_distribution"].get) if data["department_distribution"] else "None",
        "agent_usage_stats": dict(data["agent_usage"]),
        "dept_distribution": dict(data["department_distribution"])
    }
