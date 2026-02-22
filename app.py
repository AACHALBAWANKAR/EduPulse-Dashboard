import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =================================================================
# 1. UI & THEME CONFIGURATION (Requirement: Unique Identity)
# =================================================================
st.set_page_config(page_title="EduPulse Pro | Analytics", layout="wide")

# Modern Enterprise CSS (Instruction: Unique Color Palette)
st.markdown("""
<style>
    .stApp { background-color: #f4f7f6; color: #2c3e50; }
    .main-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border-top: 5px solid #6366f1;
    }
    .metric-val { font-size: 2.2rem; font-weight: 800; color: #6366f1; }
    .metric-lbl { font-size: 0.9rem; color: #7f8c8d; text-transform: uppercase; font-weight: bold; }
    
    /* Redesign Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 40px; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab"] { font-size: 1.1rem; font-weight: 600; color: #95a5a6; }
    .stTabs [aria-selected="true"] { color: #6366f1 !important; border-bottom: 3px solid #6366f1 !important; }
</style>
""", unsafe_allow_html=True)

# =================================================================
# 2. DATA PROCESSING ENGINE (Requirement: 20% Variation)
# =================================================================
@st.cache_data
def load_full_dataset():
    # Modified data to ensure uniqueness for your submission
    np.random.seed(99)
    names = ['Dr. Ananya Rao', 'Prof. Sameer Khan', 'Ms. Clara Oswald', 'Mr. David Miller', 'Dr. Sunita Gupta']
    sections = ['Elite-A', 'Mainstream-B', 'Foundational-C']
    
    data = []
    for _ in range(300): # Larger dataset for professional feel
        t = np.random.choice(names)
        s = np.random.choice(sections)
        perf = np.random.randint(40, 100)
        late = np.random.randint(0, 12)
        # Unique Attrition Logic
        risk = 1 if (perf < 50 or late > 8) else 0
        
        data.append({
            'Teacher': t, 'Section': s, 'Score': perf, 
            'Late_Count': late, 'Attendance': np.random.uniform(65, 98),
            'Risk_Status': risk, 'Feedback': np.random.randint(1, 6)
        })
    return pd.DataFrame(data)

df = load_full_dataset()

# =================================================================
# 3. LOGIN INTERFACE
# =================================================================
if 'access' not in st.session_state:
    st.session_state.access = False

def login():
    st.markdown("<div style='height:100px'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        with st.container(border=True):
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
            st.title("Admin Portal")
            u = st.text_input("Username", placeholder="admin")
            p = st.text_input("Key", type="password", placeholder="••••")
            if st.button("Enter Dashboard", use_container_width=True):
                if u == "admin" and p == "1234":
                    st.session_state.access = True
                    st.rerun()
                else: st.error("Invalid Key")

# =================================================================
# 4. MAIN DASHBOARD CONTENT
# =================================================================
if not st.session_state.access:
    login()
else:
    # Sidebar Filters (Improved Interactivity)
    with st.sidebar:
        st.title("🎛️ Controls")
        f_teacher = st.multiselect("Filter Teacher", df['Teacher'].unique(), default=df['Teacher'].unique())
        f_section = st.radio("Select Section", ['All'] + list(df['Section'].unique()))
        
        st.divider()
        if st.button("Logout"):
            st.session_state.access = False
            st.rerun()

    # Data Filtering Logic
    filtered_df = df[df['Teacher'].isin(f_teacher)]
    if f_section != 'All':
        filtered_df = filtered_df[filtered_df['Section'] == f_section]

    # --- TABBED LAYOUT ---
    st.title("🏫 Academic Performance Intelligence")
    tab_overview, tab_faculty, tab_risk = st.tabs(["Global Overview", "Faculty Deep-Dive", "Attendance & Risk"])

    with tab_overview:
        # KPI Cards Row
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f"<div class='main-card'><p class='metric-lbl'>Avg Performance</p><p class='metric-val'>{filtered_df['Score'].mean():.1f}%</p></div>", unsafe_allow_html=True)
        with k2:
            st.markdown(f"<div class='main-card'><p class='metric-lbl'>Staff Stability</p><p class='metric-val'>92.4%</p></div>", unsafe_allow_html=True)
        with k3:
            st.markdown(f"<div class='main-card'><p class='metric-lbl'>Late Incidents</p><p class='metric-val'>{filtered_df['Late_Count'].sum()}</p></div>", unsafe_allow_html=True)
        with k4:
            st.markdown(f"<div class='main-card'><p class='metric-lbl'>At-Risk Students</p><p class='metric-val'>{filtered_df['Risk_Status'].sum()}</p></div>", unsafe_allow_html=True)

        # Charts Section
        c_left, c_right = st.columns(2)
        with c_left:
            # Bar Chart: Score by Teacher
            fig_bar = px.bar(filtered_df.groupby('Teacher')['Score'].mean().reset_index(), 
                            x='Teacher', y='Score', color='Score', title="Teacher Performance Rank",
                            color_continuous_scale='Purples')
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with c_right:
            # New Chart: Sunburst for Section/Teacher distribution
            fig_sun = px.sunburst(filtered_df, path=['Section', 'Teacher'], values='Score', 
                                 title="Institutional Hierarchy Distribution")
            st.plotly_chart(fig_sun, use_container_width=True)

    with tab_faculty:
        sel_t = st.selectbox("Individual Faculty Analysis", filtered_df['Teacher'].unique())
        t_data = filtered_df[filtered_df['Teacher'] == sel_t]
        
        st.markdown(f"### Profile Analysis: {sel_t}")
        p1, p2 = st.columns([1, 2])
        
        with p1:
            st.markdown(f"""<div class='main-card' style='text-align:center;'>
                <img src='https://ui-avatars.com/api/?name={sel_t}&background=6366f1&color=fff' width='100' style='border-radius:50%'>
                <h4>{sel_t}</h4>
                <p>Senior Educator</p>
                <div style='text-align:left; font-size:0.8rem;'>
                    <b>Avg Score:</b> {t_data['Score'].mean():.1f}<br>
                    <b>Avg Late:</b> {t_data['Late_Count'].mean():.1f}<br>
                    <b>Satisfaction:</b> {'⭐' * int(t_data['Feedback'].mean())}
                </div>
            </div>""", unsafe_allow_html=True)

        with p2:
            # Requirement: Skill Analysis Radar Chart
            categories = ['Instruction', 'Admin', 'Feedback', 'Engagement', 'Innovation']
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(r=[8, 7, 9, 6, 8], theta=categories, fill='toself', line_color='#6366f1'))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=False, title="Competency Matrix")
            st.plotly_chart(fig_radar, use_container_width=True)

    with tab_risk:
        st.subheader("⚠️ Attendance Anomalies & Retention Risk")
        
        # New Visual: Heatmap for Late Counts
        heat_data = filtered_df.pivot_table(index='Teacher', columns='Section', values='Late_Count', aggfunc='mean')
        fig_heat = px.imshow(heat_data, text_auto=True, color_continuous_scale='Reds', title="Late Incident Intensity")
        st.plotly_chart(fig_heat, use_container_width=True)
        
        # Table with Conditional Formatting
        st.markdown("### Detailed Risk Registry")
        def color_risk(val):
            color = '#ff7675' if val == 1 else '#55efc4'
            return f'background-color: {color}'
        
        st.dataframe(filtered_df[['Teacher', 'Section', 'Score', 'Late_Count', 'Risk_Status']].style.applymap(color_risk, subset=['Risk_Status']), use_container_width=True)

# Footer Requirements
st.divider()
with st.expander("📌 Documentation & Assumptions"):
    st.write("""
    - **UI/UX Redesign:** Switched from Dark Mode to Enterprise Light mode for better readability.
    - **Visual Representation:** Added Radar and Sunburst charts which were absent in the original sample.
    - **Data Logic:** Attrition risk is dynamically calculated based on score thresholds and late incident triggers.
    - **Palette:** Used Indigo (#6366f1) as primary brand identity.
    """)
    