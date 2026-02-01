import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show_farmer_dashboard():
    # Page Configuration for High-End Feel
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
        
        * {
            font-family: 'Outfit', sans-serif;
        }
        
        .main {
            background-color: #0e1117;
            color: #ffffff;
        }
        
        .stButton>button {
            border-radius: 12px;
            background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 114, 255, 0.3);
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 114, 255, 0.4);
        }
        
        /* Glassmorphism Cards */
        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: transform 0.3s ease;
        }
        
        .glass-card:hover {
            border: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(255, 255, 255, 0.05);
        }
        
        .stat-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #00c6ff;
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Custom sidebar */
        [data-testid="stSidebar"] {
            background-color: #0a0c10;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .header-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 2rem;
        }
        
        .badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .badge-green { background: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid #10b981; }
        .badge-yellow { background: rgba(245, 158, 11, 0.1); color: #f59e0b; border: 1px solid #f59e0b; }
        .badge-red { background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid #ef4444; }
        
        </style>
    """, unsafe_allow_html=True)

    # Sidebar Navigation
    with st.sidebar:
        st.image("https://img.icons8.com/clouds/200/farm.png", width=120)
        st.title("AgriTech AI")
        st.markdown("---")
        
        page = st.radio("Navigation", ["Dashboard", "AI Advisor"])
        
        st.markdown("---")
        st.subheader("Active Crop")
        active_crop = st.session_state.get('crop_type', 'Wheat')
        st.info(f"{active_crop} (Stage: Flowering)")
        
        st.markdown("---")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.page = "login"
            st.rerun()

    if page == "Dashboard":
        # Header
        st.markdown("""
            <div class='header-container'>
                <div>
                    <h1 style='margin:0;'>Farmer Dashboard</h1>
                    <p style='color:#94a3b8;'>Welcome back! Monitoring your {st.session_state.get('crop_type', 'crop')} in {st.session_state.get('soil_type', 'your')} soil.</p>
                </div>
                <div>
                    <span class='badge badge-green'>System Online</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Top Stats Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div class='glass-card'>
                    <p class='stat-label'>Soil Moisture</p>
                    <p class='stat-value'>42%</p>
                    <p style='color:#10b981; font-size:0.8rem;'>↑ 2% from yesterday</p>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
                <div class='glass-card'>
                    <p class='stat-label'>Avg Temp</p>
                    <p class='stat-value'>24°C</p>
                    <p style='color:#f59e0b; font-size:0.8rem;'>Stable</p>
                </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
                <div class='glass-card'>
                    <p class='stat-label'>Nutrient Level</p>
                    <p class='stat-value'>Good</p>
                    <p style='color:#10b981; font-size:0.8rem;'>pH {st.session_state.get('ph_level', 7.0)}</p>
                </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown("""
                <div class='glass-card'>
                    <p class='stat-label'>Risk Level</p>
                    <p class='stat-value' style='color:#ef4444;'>Low</p>
                    <p style='color:#94a3b8; font-size:0.8rem;'>No active threats</p>
                </div>
            """, unsafe_allow_html=True)

        # Main Content Area
        left_col, right_col = st.columns([1, 1]) # Make it more balanced or single column

        with left_col:
            st.markdown("### Next Best Actions")
            
            with st.container():
                st.markdown("""
                    <div class='glass-card'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <div>
                                <h4 style='margin:0; color:#00c6ff;'>Apply Nitrogen Fertilizer</h4>
                                <p style='margin:5px 0; font-size:0.9rem; color:#cbd5e1;'>Based on the current growth stage (Flowering) and recent soil test.</p>
                            </div>
                            <span class='badge badge-yellow'>Urgent</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                    <div class='glass-card'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <div>
                                <h4 style='margin:0; color:#00c6ff;'>Scheduled Irrigation</h4>
                                <p style='margin:5px 0; font-size:0.9rem; color:#cbd5e1;'>Upcoming heatwave detected. Early morning irrigation recommended.</p>
                            </div>
                            <span class='badge badge-green'>Scheduled</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        with right_col:
            st.markdown("### Crop Progress")
            # Sample chart
            chart_data = pd.DataFrame({
                'Day': range(1, 11),
                'Height (cm)': [5, 7, 10, 15, 22, 30, 45, 60, 75, 90],
                'Expected': [5, 8, 12, 18, 25, 35, 48, 62, 78, 95]
            })
            fig = px.line(chart_data, x='Day', y=['Height (cm)', 'Expected'], 
                          color_discrete_sequence=['#00c6ff', 'rgba(255,255,255,0.2)'])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                margin=dict(l=0, r=0, t=20, b=0),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, width='stretch')

        # Move Weather Alert to a more prominent position since AI Advisor is moved
        st.markdown("### ☁️ Weather Alert")
        st.warning("Upcoming rain expected in 48 hours. Postpone any pesticide application.")


    elif page == "AI Advisor":
        st.markdown(f"<h1 style='margin-bottom:0;'>🤖 AI Advisor</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#94a3b8;'>Expert guidance for your {active_crop} in {st.session_state.get('soil_type', 'your')} soil.</p>", unsafe_allow_html=True)
        
        # Full-page Chat Interface
        st.markdown(f"""
            <div class='glass-card' style='height: 600px; display: flex; flex-direction: column; margin-top: 20px;'>
                <div style='flex-grow: 1; overflow-y: auto; padding: 10px;'>
                    <div style='background: rgba(0, 198, 255, 0.1); padding: 15px; border-radius: 15px; margin-bottom: 15px; max-width: 80%; border: 1px solid rgba(0, 198, 255, 0.2);'>
                        <strong style='color:#00c6ff;'>AI Advisor:</strong> Hello! I am your AI Agronomist. 
                        I've analyzed your field data for <b>{active_crop}</b>. How can I help you today?
                    </div>
                    <div style='background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px; margin-bottom: 15px; margin-left: auto; max-width: 80%; text-align: right; border: 1px solid rgba(255, 255, 255, 0.1);'>
                        <strong>You:</strong> What is the current health status of my crops?
                    </div>
                    <div style='background: rgba(0, 198, 255, 0.1); padding: 15px; border-radius: 15px; margin-bottom: 15px; max-width: 80%; border: 1px solid rgba(0, 198, 255, 0.2);'>
                        <strong style='color:#00c6ff;'>AI Advisor:</strong> Overall health is good (85%). However, the soil pH of <b>{st.session_state.get('ph_level', 'unknown')}</b> is slightly outside the optimal range for {active_crop}. I recommend checking your fertilizer balance.
                    </div>
                </div>
                <div style='padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.05); display: flex; gap: 10px;'>
                    <input type='text' placeholder='Ask about irrigation, pests, or fertilizer...' style='flex-grow: 1; padding: 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); background: rgba(0,0,0,0.2); color: white;'>
                    <button style='background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%); color: white; border: none; padding: 10px 25px; border-radius: 10px; font-weight: 600; cursor: pointer;'>Send</button>
                </div>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_farmer_dashboard()