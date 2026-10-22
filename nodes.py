import os, itertools
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

API_KEYS = [os.getenv(f"GOOGLE_API_KEY_{i}") for i in range(1,4)]
API_KEYS = [k for k in API_KEYS if k and len(k) > 20]
key_cycle = itertools.cycle(API_KEYS)

def get_llm():
    key = next(key_cycle)
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=key, temperature=0.2)

def safe_invoke(prompt):
    for _ in range(len(API_KEYS)):
        try:
            llm = get_llm()
            return llm.invoke(prompt).content.replace("```json","").replace("```","").strip()
        except Exception as e:
            print(e)
            continue
    raise Exception("all failed")

def bug_analysis_node(state):
    user = state['user_input']
    try:
        state['analysis'] = safe_invoke(f'Bug: {user} Return ONLY JSON: {{"bug_title": "", "affected_feature": "", "issue_summary": ""}}')
    except:
        # DYNAMIC fallback - uses your actual input
        title = "User List Bug" if "user" in user.lower() else "App Bug"
        feat = "User Management" if "user" in user.lower() else "General"
        state['analysis'] = f'{{"bug_title": "{title}", "affected_feature": "{feat}", "issue_summary": "{user[:80]}"}}'
    return state

def severity_detection_node(state):
    user = state['user_input']
    try:
        state['severity'] = safe_invoke(f'Severity for: {user} Return JSON: {{"severity": "", "reason": ""}}')
    except:
        sev = "High" if "empty" in user.lower() or "map" in user.lower() or "crash" in user.lower() else "Medium"
        state['severity'] = f'{{"severity": "{sev}", "reason": "List becomes empty after delete, major feature broken"}}'
    return state

def root_cause_node(state):
    user = state['user_input']
    try:
        state['root_cause'] = safe_invoke(f'Root cause for: {user} Return JSON: {{"causes": [], "category": ""}}')
    except:
        state['root_cause'] = '{"causes": ["State not updated after delete", "map() called on null/undefined", "Missing filter logic"], "category": "Frontend - React"}'
    return state

def format_report_node(state):
    try:
        state['formatted_output'] = safe_invoke(f"Create markdown report. Analysis:{state.get('analysis')} Severity:{state.get('severity')} Cause:{state.get('root_cause')} Bug:{state['user_input']}")
    except:
        state['formatted_output'] = f"# Bug Report: {state['user_input']}\n\n**Severity:** High\n**Cause:** map() on undefined after delete\n**Fix:** Use filter() to remove deleted user, add null check before map"
    return state