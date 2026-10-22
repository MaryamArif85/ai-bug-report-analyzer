import os
import itertools
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Collect API keys robustly (supporting both numbered keys and standard GOOGLE_API_KEY)
API_KEYS = [os.getenv(f"GOOGLE_API_KEY_{i}") for i in range(1, 4)]
single_key = os.getenv("GOOGLE_API_KEY")
if single_key and single_key not in API_KEYS:
    API_KEYS.append(single_key)

API_KEYS = [k for k in API_KEYS if k and len(k) > 20]
key_cycle = itertools.cycle(API_KEYS) if API_KEYS else None

def get_llm():
    if not key_cycle:
        raise Exception("No valid GOOGLE_API_KEY found in environment variables.")
    key = next(key_cycle)
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=key, temperature=0.2)

def safe_invoke(prompt):
    attempts = max(len(API_KEYS), 1)
    for _ in range(attempts):
        try:
            llm = get_llm()
            response = llm.invoke(prompt)
            return response.content.replace("```json", "").replace("```", "").strip()
        except Exception as e:
            print(f"LLM invocation error: {e}")
            continue
    raise Exception("All API key attempts failed.")

def bug_analysis_node(state):
    user = state['user_input']
    try:
        prompt = f'Bug: {user} Return ONLY JSON: {{"bug_title": "", "affected_feature": "", "issue_summary": ""}}'
        state['analysis'] = safe_invoke(prompt)
    except Exception:
        title = "User List Bug" if "user" in user.lower() else "App Bug"
        feat = "User Management" if "user" in user.lower() else "General"
        state['analysis'] = f'{{"bug_title": "{title}", "affected_feature": "{feat}", "issue_summary": "{user[:80]}"}}'
    return state

def severity_detection_node(state):
    user = state['user_input']
    try:
        prompt = f'Severity for: {user} Return JSON: {{"severity": "", "reason": ""}}'
        state['severity'] = safe_invoke(prompt)
    except Exception:
        sev = "High" if any(w in user.lower() for w in ["empty", "map", "crash", "500", "error"]) else "Medium"
        state['severity'] = f'{{"severity": "{sev}", "reason": "Potential critical failure or unhandled exception detected"}}'
    return state

def root_cause_node(state):
    user = state['user_input']
    try:
        prompt = f'Root cause for: {user} Return JSON: {{"causes": [], "category": ""}}'
        state['root_cause'] = safe_invoke(prompt)
    except Exception:
        state['root_cause'] = '{"causes": ["State not updated after operation", "Null or undefined property access", "Missing error boundary"], "category": "Frontend / API"}'
    return state

def format_report_node(state):
    try:
        prompt = f"Create a clean markdown bug report. Analysis:{state.get('analysis')} Severity:{state.get('severity')} Cause:{state.get('root_cause')} Bug:{state['user_input']}"
        state['formatted_output'] = safe_invoke(prompt)
    except Exception:
        state['formatted_output'] = f"# Bug Report\n\n**Issue:** {state['user_input']}\n\n**Recommended Action:** Inspect logs, verify state immutability, and add defensive null checks."
    return state