import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import time

# Import modular enterprise-grade components
from scenarios import SCENARIOS
from core_engine import Coordinate, LogisticsConvoy, CombatSimEngine

# ==============================================================================
# BATTLE-THEATER GEOSPATIAL LOGISTICS & STRATEGIC SUPPLY LINE SIMULATOR (v4.0 Enterprise)
# Presentation & Tactical User Interface Orchestrator
# ==============================================================================

# Set page configuration with a premium tactical look
st.set_page_config(
    page_title="TACTICAL OPERATIONAL COMMAND HUD — AIMH v4.0",
    page_icon="🎖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Tactical combat HUD Glassmorphism Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600;800&display=swap');
    
    /* Cybernetic Combat Theme */
    .main {
        background-color: #050811;
        background-image: 
            radial-gradient(rgba(18, 24, 38, 0.9) 0%, rgba(5, 8, 17, 1) 100%),
            linear-gradient(rgba(18, 30, 49, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(18, 30, 49, 0.05) 1px, transparent 1px);
        background-size: 100% 100%, 30px 30px, 30px 30px;
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Glowing card frames with border transitions */
    .tactical-card {
        background: rgba(10, 15, 30, 0.75);
        border: 1px solid rgba(133, 117, 78, 0.2);
        border-radius: 8px;
        padding: 24px;
        margin-bottom: 24px;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        box-shadow: 0 0 25px rgba(0, 0, 0, 0.6), inset 0 0 15px rgba(133, 117, 78, 0.05);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
    }
    .tactical-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 100%; height: 2px;
        background: linear-gradient(90deg, transparent, #85754E, transparent);
        transform: translateX(-100%);
        transition: transform 0.6s;
    }
    .tactical-card:hover::before {
        transform: translateX(100%);
    }
    .tactical-card:hover {
        border-color: rgba(133, 117, 78, 0.4);
        box-shadow: 0 0 35px rgba(133, 117, 78, 0.15), inset 0 0 20px rgba(133, 117, 78, 0.1);
    }
    
    /* Header HUD */
    .hud-header {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(133, 117, 78, 0.35);
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 25px;
        box-shadow: 0 0 30px rgba(0, 0, 0, 0.7), 0 0 15px rgba(133, 117, 78, 0.1);
        position: relative;
    }
    .hud-header::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0; height: 1px;
        background: linear-gradient(90deg, #1b365d, #85754E, #1b365d);
    }
    .hud-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        color: #F8FAFC !important;
        font-size: 2.5rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 0;
        text-shadow: 0 0 15px rgba(133,117,78,0.4);
    }
    .hud-subtitle {
        color: #85754E;
        font-family: 'Share Tech Mono', monospace;
        font-size: 1rem;
        letter-spacing: 3px;
        margin-top: 5px;
        text-transform: uppercase;
        font-weight: 700;
    }
    
    .tactical-title {
        color: #85754E;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.25rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 20px;
        border-bottom: 1px solid rgba(133, 117, 78, 0.25);
        padding-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Metrics Displays */
    .metric-box {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 6px;
        padding: 18px;
        text-align: center;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    }
    .metric-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.1rem;
        font-weight: 700;
        color: #F8FAFC;
        letter-spacing: -1px;
    }
    .metric-value.amber { color: #D97706; text-shadow: 0 0 10px rgba(217,119,6,0.3); }
    .metric-value.cyan { color: #06B6D4; text-shadow: 0 0 10px rgba(6,182,212,0.3); }
    .metric-value.green { color: #10B981; text-shadow: 0 0 10px rgba(16,185,129,0.3); }
    .metric-value.rose { color: #F43F5E; text-shadow: 0 0 10px rgba(244,63,94,0.3); }
    
    .metric-label {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.75rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 5px;
    }
    
    /* Sidebar adjustments */
    .stSidebar {
        background-color: #070B14 !important;
        border-right: 1px solid rgba(133, 117, 78, 0.2);
    }
    
    /* Glowing buttons */
    .stButton>button {
        background: linear-gradient(135deg, #85754E 0%, #63532C 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 6px !important;
        padding: 12px 28px !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        box-shadow: 0 0 15px rgba(133, 117, 78, 0.3) !important;
        transition: all 0.3s !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #A89566 0%, #85754E 100%) !important;
        box-shadow: 0 0 25px rgba(133, 117, 78, 0.6) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Status Badge styling */
    .hud-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 100px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: 1px solid;
    }
    .hud-badge.green { background: rgba(22,163,74,0.1); color: #4ADE80; border-color: #22C55E; }
    .hud-badge.amber { background: rgba(217,119,6,0.1); color: #FBBF24; border-color: #F59E0B; }
    .hud-badge.red { background: rgba(220,38,38,0.1); color: #FCA5A5; border-color: #EF4444; }

    /* Tactical progress bars */
    .progress-bar-bg {
        background-color: #1E293B;
        border-radius: 4px;
        height: 6px;
        width: 100%;
        overflow: hidden;
        margin-top: 8px;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease-out;
    }
    
    </style>
    """, unsafe_allow_html=True)

# Sidebar wargaming panel
st.sidebar.markdown("<div class='tactical-title'>🕹️ Tactical Wargaming setup</div>", unsafe_allow_html=True)
selected_scen_name = st.sidebar.selectbox("Select Combat Scenario", list(SCENARIOS.keys()))
scenario = SCENARIOS[selected_scen_name]

# Visual scenario introduction
st.markdown(f"""
<div class="tactical-card">
    <h3 style="color:#85754E !important; margin-bottom:5px; font-family:'Orbitron',sans-serif;">{scenario['title']}</h3>
    <p style="color:#E2E8F0; font-size:0.95rem; line-height:1.6;">{scenario['intro']}</p>
    <p style="color:#64748B; font-size:0.75rem; margin-top:8px; font-family:'Share Tech Mono', monospace;">HISTORICAL REFERENCE FILE: AIMH/OPS-LOG-{selected_scen_name.split()[1]}-1948</p>
</div>
""", unsafe_allow_html=True)

# Fleet controls in sidebar
st.sidebar.markdown("<div class='tactical-title'>🚛 Fleet Configuration</div>", unsafe_allow_html=True)
vehicle_type = st.sidebar.selectbox("Transport Platform", ["Heavy Logistics Vehicle (HLV)", "4x4 Utility Truck", "Tracked APC Carrier", "High-Altitude Pack Animal"])
convoy_size = st.sidebar.slider("Fleet Convoy Size (Vehicles)", 5, 100, 25)
payload_val = st.sidebar.slider("Payload per Vehicle (Tons)", 1.0, 15.0, 4.5)

st.sidebar.markdown("<div class='tactical-title'>🛡️ Force Protection Elements</div>", unsafe_allow_html=True)
escorts_active = st.sidebar.checkbox("Deploy Armed Escort Units", value=True)
mine_sweepers = st.sidebar.checkbox("Deploy Anti-Mine Engineers", value=False)
air_cover = st.sidebar.checkbox("Secure Tactical Air Support", value=False)

st.sidebar.markdown("<div class='tactical-title'>⚠️ Ambient Hazards</div>", unsafe_allow_html=True)
weather = st.sidebar.selectbox("Tactical Weather Conditions", ["Clear & Dry", "Heavy Snow / Alpine Winter", "Severe Heat & Sandstorms", "Monsoon / Landslides", "High-Altitude Blizzard"])
ambush_threat = st.sidebar.select_slider("Ambush Threat Potential", ["LOW", "MEDIUM", "HIGH", "CRITICAL"])

# Initialize enterprise-grade objects
convoy = LogisticsConvoy(vehicle_type, convoy_size, payload_val)
weather_speed = convoy.calculate_actual_speed(weather, scenario["peak_elev"])

# Panel Setup
col_map_hud, col_ops_hud = st.columns([1.1, 1])

# GIS Combat Map Panel
with col_map_hud:
    st.markdown("<div class='tactical-card'>", unsafe_allow_html=True)
    st.markdown("<div class='tactical-title'>🗺️ HIGH-RESOLUTION BATTLE-THEATER GIS HUD</div>", unsafe_allow_html=True)
    
    # Calculate map center
    nodes_data = scenario["nodes"]
    lats = [data["lat"] for data in nodes_data.values()]
    lons = [data["lon"] for data in nodes_data.values()]
    m_center = [np.mean(lats), np.mean(lons)]
    
    # Initialize Leaflet Map
    m = folium.Map(location=m_center, zoom_start=8, tiles="CartoDB dark_matter")
    
    # Draw Hazard / Contested Circular Zone
    folium.Circle(
        location=scenario["hazard_center"],
        radius=scenario["hazard_radius"],
        color="#DC2626",
        fill=True,
        fill_color="#DC2626",
        fill_opacity=0.15,
        tooltip=f"HIGH HAZARD: {scenario['hazard_desc']}"
    ).add_to(m)
    
    # Render nodes with custom tactical icons
    for name, data in nodes_data.items():
        node_color = "red" if data["type"] == "FDL" else ("blue" if data["type"] == "FOB" else "darkblue")
        folium.Marker(
            location=[data["lat"], data["lon"]],
            popup=f"<b>{name}</b><br>{data['desc']}",
            tooltip=name,
            icon=folium.Icon(color=node_color, icon="flag", prefix="glyphicon")
        ).add_to(m)
        
    # Draw high-fidelity supply path
    folium.PolyLine(
        scenario["path_coords"],
        color="#85754E",
        weight=6,
        opacity=0.85,
        tooltip="Active Operational Supply Line"
    ).add_to(m)
    
    # Streamlit Folium render
    st_folium(m, width=640, height=380, key="operational_center_gis")
    
    # Nodes listing
    st.markdown("<p style='font-size:0.75rem;color:#85754E;font-weight:bold;margin-top:10px;font-family:\"Share Tech Mono\", monospace;'>THEATER NODAL CONNECTIONS & COORDINATES</p>", unsafe_allow_html=True)
    df_nodes = pd.DataFrame.from_dict(nodes_data, orient='index')
    st.dataframe(df_nodes[['lat', 'lon', 'desc']], use_container_width=True, height=125)
    st.markdown("</div>", unsafe_allow_html=True)

# Operations Intelligence HUD
with col_ops_hud:
    st.markdown("<div class='tactical-card'>", unsafe_allow_html=True)
    st.markdown("<div class='tactical-title'>📊 OPERATIONS CONVOY TELEMETRY</div>", unsafe_allow_html=True)
    
    # Calculate path distances along all geographic segments
    path_points = scenario["path_coords"]
    total_raw_distance = 0
    for i in range(len(path_points) - 1):
        lat1, lon1 = path_points[i]
        lat2, lon2 = path_points[i+1]
        
        # Haversine formula
        R = 6371.0
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))
        total_raw_distance += R * c
        
    actual_line_dist = total_raw_distance * scenario["road_winding"]
    transit_duration = actual_line_dist / weather_speed
    
    # Display HUD Stats
    col_hud1, col_hud2 = st.columns(2)
    with col_hud1:
        st.markdown(f"""
        <div class="metric-box" style="margin-bottom:15px;">
            <div class="metric-value cyan">{convoy.total_payload:.1f} T</div>
            <div class="metric-label">Active Convoy Payload</div>
        </div>
        <div class="metric-box">
            <div class="metric-value amber">{weather_speed:.1f} km/h</div>
            <div class="metric-label">Estimated Transit Velocity</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_hud2:
        st.markdown(f"""
        <div class="metric-box" style="margin-bottom:15px;">
            <div class="metric-value highlight" style="color:#85754E;">{actual_line_dist:.1f} km</div>
            <div class="metric-label">Total Supply Line Length</div>
        </div>
        <div class="metric-box">
            <div class="metric-value rose">{transit_duration:.2f} Hrs</div>
            <div class="metric-label">Estimated Convoy ETA</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ADVANCED WARGAMING INTERACTIVE SECTION
    st.markdown("<div class='tactical-card'>", unsafe_allow_html=True)
    st.markdown("<div class='tactical-title'>⚡ HYPER-COMMAND MONTE CARLO COMBAT SIMULATOR</div>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.8rem;color:#94A3B8;'>Perform a high-fidelity 100-run operations wargaming simulation that rolls real-time combat ambush hazards, high-altitude fuel leaks, and route blockages dynamically mitigated by your deployed escorts.</p>", unsafe_allow_html=True)
    
    if st.button("⚡ EXECUTE BATTLE-THEATER CONVOY WARGAME"):
        progress_bar = st.progress(0)
        
        # Initialize combat simulation engine
        sim_engine = CombatSimEngine(
            ambush_threat=ambush_threat,
            peak_altitude=scenario["peak_elev"],
            escorts=escorts_active,
            mine_sweepers=mine_sweepers,
            air_support=air_cover
        )
        
        # Run wargame
        results = sim_engine.run_monte_carlo(convoy, actual_line_dist, weather_speed, iterations=100)
        
        # Animate progress bar
        for run in range(100):
            if run % 20 == 0:
                progress_bar.progress(run + 20)
                time.sleep(0.05)
                
        # Final progress bar completion
        progress_bar.progress(100)
        time.sleep(0.05)
        progress_bar.empty()
        
        success_runs = results["success_rate"]
        
        # Display simulated metrics
        col_sim1, col_sim2, col_sim3 = st.columns(3)
        with col_sim1:
            badge_type = "green" if success_runs > 80 else ("amber" if success_runs > 50 else "red")
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value green"><span class="hud-badge {badge_type}" style="font-size:1.35rem;padding:4px 10px;">{success_runs}%</span></div>
                <div class="metric-label">Sim Success Rate</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_sim2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value cyan">{results["yield_rate"]:.1f}%</div>
                <div class="metric-label">Supply Yield Rate</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_sim3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value rose">{results["avg_duration"]:.2f} Hrs</div>
                <div class="metric-label">Simulated Avg ETA</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Display Tactical Command Logs
        st.markdown("<p style='font-size:0.75rem;color:#85754E;font-weight:bold;margin-top:12px;font-family:\"Share Tech Mono\", monospace;'>TACTICAL COMMAND CENTER WARGAMER SIM LOGS</p>", unsafe_allow_html=True)
        st.info(f"Combat Runs Evaluated: 100. **DEFENSE MATRIX INTERCEPTIONS:** Detected {results['combat_aborts']} convoy ambushes causing supply line rupture. **ALPINES HAZARDS:** Evaluated {results['alpine_aborts']} landslide or weather closures. **FUEL EXHAUSTION:** Scored {results['fuel_aborts']} fuel exhaustion breakdowns.")
    else:
        st.warning("Hyper-Command Wargamer is in STANDBY. Click the button above to run the 100-run simulation.")
    st.markdown("</div>", unsafe_allow_html=True)

# SECTION III: Altitude Risk Evaluation & Resource Allocation
st.markdown("<div class='tactical-title'>III. Alpine Elevation Profile & Tactical Packing Matrix</div>", unsafe_allow_html=True)
col_bottom_chart, col_bottom_form = st.columns([2, 1])

with col_bottom_chart:
    st.markdown("<div class='tactical-card'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.9rem;color:#F8FAFC;font-weight:bold;margin-bottom:10px;'>Elevation profile climb along supply route (Meters)</p>", unsafe_allow_html=True)
    
    # Generate realistic mountains pass elevation step climb
    grid_steps = 30
    dist_arr = np.linspace(0, actual_line_dist, grid_steps)
    base_h = scenario["base_elev"]
    peak_h = scenario["peak_elev"]
    
    # Alpine elevation profile parabola climb
    heights = []
    for idx in range(grid_steps):
        prog = idx / (grid_steps - 1)
        h = base_h + (peak_h - base_h) * (3 * prog**2 - 2 * prog**3) + np.random.normal(0, 80)
        h = min(h, peak_h)
        heights.append(h)
        
    df_elev = pd.DataFrame({
        'Distance (km)': dist_arr,
        'Elevation (Meters)': heights
    })
    
    # High-altitude climb area chart
    st.area_chart(df_elev, x='Distance (km)', y='Elevation (Meters)', use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_bottom_form:
    st.markdown("<div class='tactical-card' style='height:360px;'>", unsafe_allow_html=True)
    st.markdown("<div class='tactical-title'>📦 Logistics Resource Packing</div>", unsafe_allow_html=True)
    
    # Slider representing resource weight packing
    fuel_load = st.slider("Convoy Fuel Reserves (%)", 10, 100, 50, step=5)
    ammo_load = st.slider("Ammunition Stocks (%)", 10, 100, 70, step=5)
    rations_load = st.slider("Infantry Rations / Supplies (%)", 10, 100, 40, step=5)
    
    # Calculate packing values in tons
    weight_fuel = (convoy.total_payload * fuel_load) / 300
    weight_ammo = (convoy.total_payload * ammo_load) / 300
    weight_rations = (convoy.total_payload * rations_load) / 300
    total_packed = weight_fuel + weight_ammo + weight_rations
    
    # Show loading status bar
    capacity_pct = (total_packed / convoy.total_payload) * 100
    bar_color = "#10B981" if capacity_pct <= 80 else ("#F59E0B" if capacity_pct <= 100 else "#EF4444")
    
    st.markdown("<p style='font-size:0.8rem;color:#85754E;font-weight:bold;'>TACTICAL CARGO DOCK SHEET</p>", unsafe_allow_html=True)
    st.caption(f"⛽ **Fuel Payload:** {weight_fuel:.1f} Tons")
    st.caption(f"💥 **Ammunition Stocks:** {weight_ammo:.1f} Tons")
    st.caption(f"🥩 **Operational Rations:** {weight_rations:.1f} Tons")
    
    st.markdown(f"""
    <div style='margin-top:15px;'>
        <p style='font-size:0.75rem;color:#94A3B8;text-transform:uppercase;'>Convoy Cargo Utilization: <b>{capacity_pct:.1f}%</b></p>
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width: {min(capacity_pct, 100):.1f}%; background-color: {bar_color};"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center;color:#64748B;font-size:0.75rem;font-family:\"Orbitron\",sans-serif;'>DESIGNED AND DEVELOPED AS A STATE-OF-THE-ART DIGITAL HUMANITIES DEMO FOR THE <b>ARMY INSTITUTE OF MILITARY HISTORY (AIMH)</b> BY LOKESH KUMAR (SINDH AGRICULTURE UNIVERSITY, TANDO JAM).</p>", unsafe_allow_html=True)
