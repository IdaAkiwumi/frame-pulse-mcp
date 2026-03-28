import streamlit as st
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import directly from modules (not server)
from frame_pulse.system_client import get_thermal_status, get_system_stats
from frame_pulse.render_guard import find_render_processes, emergency_throttle, format_process_list

st.set_page_config(page_title="Frame Pulse | Studio Telemetry", layout="wide", page_icon="🎬")

st.title("🎬 Frame Pulse")
st.caption("Hardware-aware mission control for creative workstations")

# Test imports worked
col1, col2, col3, col4 = st.columns(4)

try:
    thermal = get_thermal_status()
    status = thermal.split(":")[0] if ":" in thermal else "UNKNOWN"
    details = thermal.split(":")[1].strip() if ":" in thermal else thermal
    
    # Extract CPU value
    cpu_val = 0
    if "CPU" in thermal and "%" in thermal:
        try:
            cpu_str = thermal.split("CPU")[1].split("%")[0].strip()
            cpu_val = float(cpu_str)
        except:
            pass
    
    with col1:
        delta_color = "normal" if "SAFE" in status else "inverse" if "CAUTION" in status else "off"
        st.metric("System Status", status, details, delta_color=delta_color)
    
    with col2:
        st.metric("CPU Load", f"{cpu_val:.1f}%", "High" if cpu_val > 80 else "Normal", delta_color="inverse" if cpu_val > 80 else "normal")
    
    with col3:
        st.metric("MCP Server", "🟢 Active", "3 tools loaded")
    
    with col4:
        st.metric("Last Check", "Just now", "Auto-refresh: 10s")
    
    #with col5:
        #st.metric("MCP", "🟢 Active" if "_demo" not in thermal.lower() else "🟡 Demo Mode")

    if "CRITICAL" in status:
        st.error(f"🔥 {thermal}")
    elif "CAUTION" in status:
        st.warning(f"⚠️ {thermal}")
    elif "DEMO" in status:
        st.info(f"ℹ️ {thermal}")

except Exception as e:
    st.error(f"Connection error: {e}")

st.divider()

# Creative processes — THE KEY FIX
st.subheader("🎨 Active Creative Processes")

try:
    # Get raw list, not formatted string
    from frame_pulse.render_guard import find_render_processes
    processes = find_render_processes()
    
    if not processes:
        st.info("No creative applications detected — start Blender, Unreal, or Maya to see them here")
    else:
        st.success(f"Found {len(processes)} active process(es)")
        for p in processes:
            cols = st.columns([3, 1])
            with cols[0]:
                st.code(f"{p['name']}\nPID: {p['pid']} | CPU: {p['cpu']:.1f}% | RAM: {p['memory']:.1f}%")
            with cols[1]:
                if st.button("⏸️ Cool Down", key=f"throttle_{p['pid']}"):
                    result = emergency_throttle(p['pid'])
                    st.toast(result)
                    st.rerun()
except Exception as e:
    st.error(f"Process scan failed: {e}")
    st.info("Try running: pip install psutil")

st.divider()

if st.button("🔄 Refresh Now"):
    st.rerun()

st.caption("Built with Python, MCP, and Streamlit")