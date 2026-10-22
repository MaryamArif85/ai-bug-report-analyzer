import streamlit as st
import json
from graph import build_graph

st.set_page_config(
    page_title="AI Bug Report Analyzer",
    page_icon="🐛",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- WHITE & LAVENDER / LILAC THEME WITH LIVELY BORDERS ---
st.markdown("""
<style>
.stApp {
    background-color: #F8F7FC;
    color: #2D2640;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.block-container {
    max-width: 1000px !important;
    padding-top: 3rem;
    padding-bottom: 4rem;
}

h1 {
    font-size: 48px !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
    color: #1A1528;
    line-height: 1.1 !important;
}

h3, h4 {
    color: #4A3E73 !important;
    font-weight: 700 !important;
}

/* Quick Example Buttons */
div[data-testid="column"] button {
    background: #EDE8F5 !important;
    color: #5C4B99 !important;
    border: 1px solid #D5CCE8 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    transition: all 0.2s ease;
}

div[data-testid="column"] button:hover {
    background: #5C4B99 !important;
    color: #FFFFFF !important;
    border-color: #5C4B99 !important;
}

div[data-testid="column"] button p {
    color: inherit !important;
}

/* Text Area Styling with glowing border */
textarea {
    background: #FFFFFF !important;
    color: #1A1528 !important;
    border: 2px solid #C4B5FD !important;
    border-radius: 12px !important;
    font-size: 16px !important;
    padding: 12px !important;
    box-shadow: 0 2px 8px rgba(124, 102, 220, 0.08) !important;
}

textarea:focus {
    border-color: #7C66DC !important;
    box-shadow: 0 0 0 4px rgba(124, 102, 220, 0.2) !important;
}

/* Primary Action Button */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7C66DC 0%, #5C4B99 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    padding: 0.75rem 1.5rem !important;
    box-shadow: 0 4px 14px rgba(124, 102, 220, 0.35) !important;
    transition: transform 0.1s ease, box-shadow 0.2s ease;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(124, 102, 220, 0.45) !important;
}

/* Secondary / Clear Button Styling */
.stButton > button[kind="secondary"] {
    background: #FFFFFF !important;
    color: #5C4B99 !important;
    border: 2px solid #D5CCE8 !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    padding: 0.75rem 1.5rem !important;
    transition: all 0.2s ease;
}

.stButton > button[kind="secondary"]:hover {
    background: #F3EEFC !important;
    border-color: #7C66DC !important;
    color: #7C66DC !important;
}

/* Lively Cards with Accent Top Border & Hover Lift */
.card-box {
    background: #FFFFFF;
    border: 2px solid #E2D9F3;
    border-top: 5px solid #7C66DC;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 6px 20px rgba(124, 102, 220, 0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card-box:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 28px rgba(124, 102, 220, 0.16);
    border-color: #D5CCE8;
    border-top: 5px solid #7C66DC;
}

.report-box {
    background: #FAF8FD;
    border: 1px solid #E2D9F3;
    border-left: 5px solid #7C66DC;
    border-radius: 0 14px 14px 0;
    padding: 24px;
    font-size: 16px !important;
    color: #2D2640;
    line-height: 1.6;
}

hr {
    border: none;
    height: 2px;
    background: linear-gradient(to right, #7C66DC, #D5CCE8, transparent);
    margin: 30px 0;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown('<h1>MULTI-STEP<br>BUG ANALYZER <span style="color:#7C66DC;">AGENT</span></h1>', unsafe_allow_html=True)
st.markdown("<p style='color: #6E628F; font-size: 18px; margin-top: -10px;'>Powered by LangGraph & Gemini 1.5 Flash</p>", unsafe_allow_html=True)
st.markdown('<hr>', unsafe_allow_html=True)

# Initialize Session State
if "bug_input" not in st.session_state:
    st.session_state.bug_input = "User list empty after delete - map error - TypeError: Cannot read properties of undefined reading 'map'"

if "workflow_result" not in st.session_state:
    st.session_state.workflow_result = None

def update_input(text):
    st.session_state.bug_input = text

def clear_input():
    st.session_state.bug_input = ""
    st.session_state.workflow_result = None

# Quick Fill Examples
st.markdown("<p style='font-weight:600; color:#4A3E73; margin-bottom:8px;'>✨ Quick Test Presets:</p>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    st.button("🔴 Login Crash", use_container_width=True, on_click=update_input, args=("App crashes on login - POST /api/login returns 500 Internal Server Error, page freezes",))
with c2:
    st.button("🟡 UI Glitch", use_container_width=True, on_click=update_input, args=("On mobile, the submit button is overlapping with footer text on checkout page",))
with c3:
    st.button("🟠 Data Bug", use_container_width=True, on_click=update_input, args=("User list empty after delete - map error - TypeError: Cannot read properties of undefined reading 'map'",))

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 📝 PASTE BUG DESCRIPTION:")
bug_description = st.text_area("", key="bug_input", height=130, label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# Action Buttons Side-by-Side
col_btn1, col_btn2 = st.columns([3, 1])
with col_btn1:
    run = st.button("🚀 GENERATE STRUCTURED REPORT", type="primary", use_container_width=True)
with col_btn2:
    clear = st.button("🗑️ Clear", type="secondary", use_container_width=True, on_click=clear_input)

def safe_json(s):
    try:
        return json.loads(s)
    except:
        return {"raw_output": s}

if run:
    if not st.session_state.bug_input.strip():
        st.warning("Please enter a bug description first.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Step 1/4: Analyzing bug structure...")
        progress_bar.progress(25)
        
        status_text.text("Step 2/4: Determining severity level...")
        progress_bar.progress(50)
        
        status_text.text("Step 3/4: Isolating root cause...")
        progress_bar.progress(75)
        
        try:
            g = build_graph()
            st.session_state.workflow_result = g.invoke({
                "user_input": st.session_state.bug_input,
                "analysis": "",
                "severity": "",
                "root_cause": "",
                "formatted_output": ""
            })
            progress_bar.progress(100)
            status_text.empty()
            progress_bar.empty()
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"Error executing graph workflow: {e}")
            st.session_state.workflow_result = None

# Render Results
res = st.session_state.workflow_result
if res:
    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown("### 📊 Agent Workflow Results")
    
    colA, colB = st.columns(2, gap="medium")
    
    with colA:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("#### 01 Bug Analysis")
        st.json(safe_json(res['analysis']))
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("#### 02 Severity Assessment")
        st.json(safe_json(res['severity']))
        st.markdown('</div>', unsafe_allow_html=True)
        
    with colB:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("#### 03 Root Cause Diagnosis")
        st.json(safe_json(res['root_cause']))
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("#### 04 Executive Report")
        st.markdown(f'<div class="report-box">{res["formatted_output"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)