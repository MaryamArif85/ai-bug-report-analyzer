from langgraph.graph import StateGraph, END
from typing import TypedDict
from nodes import bug_analysis_node, severity_detection_node, root_cause_node, format_report_node

class BugState(TypedDict):
    user_input: str
    analysis: str
    severity: str
    root_cause: str
    formatted_output: str

def build_graph():
    g = StateGraph(BugState)
    g.add_node("analysis", bug_analysis_node)
    g.add_node("severity", severity_detection_node)
    g.add_node("root_cause", root_cause_node)
    g.add_node("format", format_report_node)

    g.set_entry_point("analysis")
    g.add_edge("analysis", "severity")
    g.add_edge("severity", "root_cause")
    g.add_edge("root_cause", "format")
    g.add_edge("format", END)
    return g.compile()