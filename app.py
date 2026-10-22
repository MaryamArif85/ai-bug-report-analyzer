import streamlit as st, json
from graph import build_graph

st.set_page_config(page_title="AI Bug Report Analyzer", layout="centered")
st.markdown("""
<style>
.stApp{background:#0A0A0A; color:#fff;}
.block-container{max-width:1100px !important;}
h1{font-size:56px !important; font-weight:900 !important; line-height:0.85 !important;}

/* Fix textarea */
textarea {
    background:#FFF !important;
    color:#000 !important;
    font-size:17px !important;
    -webkit-text-fill-color:#000 !important;
}

/* Fix buttons - black text on white */
div[data-testid="column"] button {
    background:#FFF !important;
    color:#000 !important;
    border:1px solid #333 !important;
    font-weight:700 !important;
    font-size:13px !important;
}
div[data-testid="column"] button p {
    color:#000 !important;
    font-size:13px !important;
}

.report-box{border:2px solid #FF1E1E; background:#141414; padding:24px; font-size:18px !important;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1>4-STEP<br>BUG<br>ANALYZER <span style="color:#FF1E1E;">AGENT</span></h1>', unsafe_allow_html=True)
st.markdown('<hr style="border:2px solid #FF1E1E;">', unsafe_allow_html=True)

if "bug_input" not in st.session_state:
    st.session_state.bug_input = "User list empty after delete - map error"

def set_bug(text):
    st.session_state.bug_input = text

c1,c2,c3 = st.columns(3)
with c1:
    st.button("🔴 Login Crash", use_container_width=True, on_click=set_bug, args=("App crashes on login - POST /api/login returns 500 Internal Server Error, page freezes",))
with c2:
    st.button("🟡 UI Glitch - Low", use_container_width=True, on_click=set_bug, args=("On mobile, the submit button is overlapping with footer text on checkout page",))
with c3:
    st.button("🟠 Data Bug - High", use_container_width=True, on_click=set_bug, args=("User list empty after delete - map error - TypeError: Cannot read properties of undefined reading 'map'",))

st.markdown("### PASTE BUG DESCRIPTION:")
st.text_area("", key="bug_input", height=130, label_visibility="collapsed")

run = st.button("🚀 GENERATE BUG REPORT", type="primary", use_container_width=True)

def safe_json(s):
    try: return json.loads(s.replace("```json","").replace("```","").strip())
    except: return {"raw": s}

if run:
    with st.spinner("Running 4 nodes..."):
        g = build_graph()
        res = g.invoke({"user_input": st.session_state.bug_input, "analysis": "", "severity": "", "root_cause": "", "formatted_output": ""})
    
    st.markdown('<hr style="border:2px solid #FF1E1E; margin-top:30px;">', unsafe_allow_html=True)
    
    colA, colB = st.columns(2)
    with colA:
        st.markdown("## 01 Analysis")
        st.json(safe_json(res['analysis']))
        st.markdown("## 02 Severity")
        st.json(safe_json(res['severity']))
    with colB:
        st.markdown("## 03 Root Cause")
        st.json(safe_json(res['root_cause']))
        st.markdown("## 04 Final Report")
        st.markdown(f'<div class="report-box">{res["formatted_output"]}</div>', unsafe_allow_html=True)