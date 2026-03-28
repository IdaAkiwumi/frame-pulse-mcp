import streamlit as st
import sys
import os
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Connection state tracking
CONNECTION_STATUS = "unknown"
DEMO_MODE = False

try:
    from frame_pulse.system_client import get_thermal_status
    from frame_pulse.render_guard import find_render_processes, emergency_throttle
    test_status = get_thermal_status()
    if "DEMO" in test_status:
        DEMO_MODE = True
        CONNECTION_STATUS = "demo"
    else:
        CONNECTION_STATUS = "live"
except Exception as e:
    CONNECTION_STATUS = "offline"
    # Fallback functions for display
    def get_thermal_status():
        return "OFFLINE: Host system unavailable — See example data below"
    def find_render_processes():
        return []
    def emergency_throttle(pid=None):
        return "Throttle unavailable — Connect to live system"

st.set_page_config(
    page_title="Frame Pulse MCP | AI-Native Creative Workstation Telemetry",
    layout="wide",
    page_icon="🎬",
    initial_sidebar_state="expanded"
)

# SEO-Heavy Sidebar (Google-indexable via meta + visible text)
with st.sidebar:
    st.markdown("## 🎬 Frame Pulse MCP")
    st.markdown("""
    **AI-native telemetry for creative workstations.**
    
    Bridge Claude, Hermes, and Cursor with your 3D pipeline—monitor Blender, Unreal Engine, Houdini, and Maya in real-time.
    """)

    
    st.divider()
    
    st.markdown("### 🛠️ Tech Stack")
    st.markdown("""
    - Python 3.10+
    - Model Context Protocol (MCP)
    - FastMCP SDK
    - psutil
    - Streamlit
    - NVIDIA NVML (optional)
    """)
    
    st.divider()
    
    st.markdown("### 🎯 Keywords")
    st.caption("""
    MCP server, AI agent tools, creative workstation monitoring, 
    Blender telemetry, Unreal Engine monitoring, Houdini pipeline, 
    VFX infrastructure, game dev ops, render farm safety, 
    thermal throttling, AI safety layer, technical director tools,
    Python system monitoring, LLM tool integration
    """)
    
    st.divider()
    
    st.markdown("### 🔗 Connect")
    st.markdown("[📂 GitHub Repository](https://github.com/idaakiwumi/frame-pulse-mcp)")
    st.markdown("[💼 LinkedIn](https://www.linkedin.com/in/idaa11/)")
    st.markdown("[👩🏽‍💻 Developer Profile](https://github.com/idaakiwumi)")

# Main header with connection indicator
header_cols = st.columns([6, 1])
with header_cols[0]:
    st.title("🎬 Frame Pulse")
    st.caption("Hardware-aware mission control for creative workstations · Built by Ida Akiwumi")
with header_cols[1]:
    if CONNECTION_STATUS == "live":
        st.success("🟢 LIVE")
    elif CONNECTION_STATUS == "demo":
        st.warning("🟡 DEMO")
    else:
        st.error("🔴 OFFLINE")

# Connection-aware main display
left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("System Status")
    
    try:
        thermal = get_thermal_status()
        status = thermal.split(":")[0] if ":" in thermal else "OFFLINE"
        
        # Extract CPU if available
        cpu_val = 0.0
        if CONNECTION_STATUS in ["live", "demo"]:
            match = re.search(r'CPU\s+(\d+\.?\d*)%', thermal)
            cpu_val = float(match.group(1)) if match else 0.0
        
        # Metrics grid
        mcol1, mcol2 = st.columns(2)
        with mcol1:
            delta = "normal" if "SAFE" in status else "inverse" if "CAUTION" in status or "CRITICAL" in status else "off"
            st.metric("Status", status, delta_color=delta)
        with mcol2:
            if CONNECTION_STATUS in ["live", "demo"]:
                st.metric("CPU Load", f"{cpu_val:.1f}%")
            else:
                st.metric("CPU Load", "—")
        
        mcol3, mcol4 = st.columns(2)
        with mcol3:
            mode = "🟡 Demo Mode" if DEMO_MODE else "🟢 Live Connection" if CONNECTION_STATUS == "live" else "🔴 Host Offline"
            st.metric("Data Source", mode)
        with mcol4:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        
        # Status alerts
        if "CRITICAL" in status:
            st.error(f"🔥 {thermal}")
        elif "CAUTION" in status:
            st.warning(f"⚠️ {thermal}")
        elif "DEMO" in status:
            st.info(f"ℹ️ {thermal}")
        elif "OFFLINE" in status:
            st.info(f"⏸️ {thermal}")
        else:
            st.success(f"✅ {thermal}")

    except Exception as e:
        st.error(f"Connection failed: Host system may be sleeping or offline")

with right_col:
    st.subheader("🎨 Active Creative Apps")
    
    try:
        processes = find_render_processes()
        
        if not processes and CONNECTION_STATUS != "offline":
            st.info("No creative apps currently running — Start Blender, Unreal Engine, Houdini, or Maya to see live telemetry")
        elif not processes and CONNECTION_STATUS == "offline":
            st.info("""
            **Host system offline.** 
            
            When connected, this panel displays:
            - 🎨 Blender renders in progress
            - 🎮 Unreal Engine lighting builds  
            - 🎬 Houdini simulations
            - 🎥 After Effects compositions
            """)
        else:
            for p in processes:
                with st.container(border=True):
                    cols = st.columns([3, 1])
                    with cols[0]:
                        st.markdown(f"**{p['name']}**")
                        st.caption(f"PID `{p['pid']}` | CPU {p['cpu']:.1f}% | RAM {p['memory']:.1f}%")
                    with cols[1]:
                        if st.button("⏸️ Cool Down", key=f"throttle_{p['pid']}", use_container_width=True):
                            result = emergency_throttle(p['pid'])
                            st.toast(result)
                            st.rerun()
    except Exception as e:
        st.error(f"Unable to scan processes: {e}")

# What You See section — SEO-rich, always visible
st.divider()
st.subheader("📊 What You'll See Here")

what_cols = st.columns(3)

with what_cols[0]:
    st.markdown("**🟢 System Idle**")
    st.code("SAFE: CPU 12%, Temp 45°C\nReady for production", language="text")
    st.caption("Low load. Safe to start overnight renders or heavy simulations.")

with what_cols[1]:
    st.markdown("**🟡 Active Production**")
    st.code("CAUTION: CPU 78%, Temp 71°C\nQueue carefully", language="text")
    st.caption("Blender render or UE5 build in progress. Monitor closely.")

with what_cols[2]:
    st.markdown("**🔥 Thermal Risk**")
    st.code("CRITICAL: CPU 94%, Temp 89°C\nHALT immediately", language="text")
    st.caption("Emergency state. AI agent or human should throttle or pause jobs.")

# About this tool — keyword dense
st.divider()
st.subheader("🎯 About Frame Pulse MCP")

about_cols = st.columns([2, 1])

with about_cols[0]:
    st.markdown("""
    **Frame Pulse** is an open-source [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server 
    that bridges AI assistants (Claude, Hermes, Cursor) with real-time workstation telemetry.
    
    ### What It Does
    
    - **Monitors** CPU, memory, and thermal sensors via Python's `psutil`
    - **Detects** creative applications: Blender, Unreal Engine, Unity, Houdini, Maya, After Effects, Cinema 4D, Nuke, DaVinci Resolve
    - **Prevents** thermal crashes by throttling background processes before hardware limits
    - **Integrates** with Claude Desktop for natural language system queries
    
    ### Who Uses This
    
    - **Technical Directors** managing render farm nodes
    - **Solo creators** running overnight bakes on personal workstations  
    - **AI engineers** building agentic workflows for creative pipelines
    - **Educators** teaching AI-assisted content creation
    
    ### Live vs. Demo Mode
    
    This Streamlit instance may show **simulated data** when the host developer workstation is offline 
    (nights, weekends, travel). The [GitHub repository](https://github.com/idaakiwumi/frame-pulse-mcp) 
    contains full instructions to run on your own hardware with live telemetry.
    """)

with about_cols[1]:
    st.markdown("### 🎬 Built By")
    st.markdown("""
    **Ida Akiwumi**
    
    Lead Product Designer · Creative Technologist · Narrative Strategist
    
    Translating user friction into product opportunities across film, gaming, and immersive media.
    """)
    
    st.markdown("""
    [🐙 github.com/idaakiwumi](https://github.com/idaakiwumi)  
    [💼 linkedin.com/in/idaa11](https://www.linkedin.com/in/idaa11/)
    """)
    
    st.divider()
    
    st.markdown("### 📈 Repository Stats")
    st.caption("⭐ Star and fork on GitHub to track updates")

# Footer with dense keywords
st.divider()
st.caption("""
**Frame Pulse MCP** · AI-native creative workstation telemetry · 
Python MCP server for Blender, Unreal Engine, Houdini, Maya monitoring · 
Model Context Protocol tools for technical directors · 
Built with Streamlit, psutil, FastMCP by Ida Akiwumi · 
[GitHub](https://github.com/idaakiwumi/frame-pulse-mcp) · 
[LinkedIn](https://www.linkedin.com/in/idaa11/)
""")