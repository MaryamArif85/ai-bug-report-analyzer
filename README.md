# 4-STEP BUG ANALYZER AGENT

> AI Bug Report Analyzer | LangGraph 4 Nodes | Multi-Key Rotation

An autonomous AI agent that takes a raw bug description and automatically generates a structured bug report using 4 sequential nodes: Analysis, Severity Detection, Root Cause Analysis, and Final Report Formatting.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-4%20Nodes-orange)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![Gemini](https://img.shields.io/badge/LLM-Gemini%201.5%20Flash-yellow)

### 🚀 Live Demo
**Live Link:** `Coming Soon - Will be deployed on Streamlit Cloud`

---

### 🧠 Architecture - 4 Nodes
User Input → [01 Analysis] → [02 Severity] → [03 Root Cause] → [04 Final Report] → UI

| Node | Function | Output |
|---|---|---|
| 01 Analysis | `bug_analysis_node()` | bug_title, affected_feature, issue_summary |
| 02 Severity | `severity_detection_node()` | severity (Critical/High/Medium/Low), reason |
| 03 Root Cause | `root_cause_node()` | causes[], category |
| 04 Final Report | `format_report_node()` | Clean Markdown Report |

### ✨ Features
- 4-Step LangGraph Agent
- Multi-Key Rotation (3 Keys) - auto switch on quota/error
- Supports `AQ...` and `AIza...` Google keys (fixed `startswith` bug)
- All 4 nodes display at same time
- Example bugs: Login Crash, UI Glitch, Data Bug
- Dynamic fallback - matches user input


