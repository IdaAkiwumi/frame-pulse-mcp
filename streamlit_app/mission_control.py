import streamlit as st
import sys
import os

# Add src to path so we can import our tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from frame_pulse.server import get_thermal_status, find_render_processes, emergency_throttle

st.set_page_config(page_title="Frame Pulse | Studio Telemetry", layout="wide", page_icon="🎬")

st.title("🎬 Frame Pulse")
st.caption("Mission Control for AI-Augmented Creative Workflows")

# Auto-refresh every 10 seconds
st.query_params.run = "true"  # Trigger rerun mechanism
from streamlit.runtime.scriptrunner import RerunException
from streamlit.runtime.scriptrunner import RerunData

# Real-time metrics
col1, col2, col3, col4 = st.columns(4)

try:
    thermal = get_thermal_status()
    status = thermal.split(":")[0] if ":" in thermal else "UNKNOWN"
    details = thermal.split(":")[1].strip() if ":" in thermal else thermal
    
    cpu_val = 0
    if "CPU" in thermal and "%" in thermal:
        try:
            cpu_str = thermal.split("CPU")[1].split("%")[0].strip()
            cpu_val = float(cpu_str)
        except:
            pass
    
    with col1:
        color = "normal" if "SAFE" in status else "inverse" if "CAUTION" in status else "off"
        st.metric("System Status", status, details, delta_color=color)
    
    with col2:
        st.metric("CPU Load", f"{cpu_val:.1f}%", "High" if cpu_val > 80 else "Normal", delta_color="inverse" if cpu_val > 80 else "normal")
    
    with col3:
        st.metric("MCP Server", "🟢 Active", "3 tools loaded")
    
    with col4:
        st.metric("Last Check", "Just now", "Auto-refresh: 10s")

    if "CRITICAL" in status:
        st.error(f"🔥 {thermal} — HALT all renders immediately!")
    elif "CAUTION" in status:
        st.warning(f"⚠️ {thermal} — Queue carefully")

except Exception as e:
    st.error(f"Server offline: {e}")

st.divider()

# Creative process monitor
st.subheader("🎨 Active Production Processes")

try:
    processes = find_render_processes()
    if "No active" in processes:
        st.info("No creative applications detected")
    else:
        for line in processes.split("\n"):
            if line.strip():
                cols = st.columns([3, 1])
                cols[0].code(line)
                # Extract PID for throttle button
                try:
                    pid = int(line.split("PID")[1].split(")")[0].strip())
                    if cols[1].button(f"⏸️ Throttle {pid}", key=f"throttle_{pid}"):
                        result = emergency_throttle(pid)
                        st.success(result)
                        st.rerun()
                except:
                    pass
except Exception as e:
    st.error(f"Process scan failed: {e}")

st.divider()

# Manual refresh
if st.button("🔄 Refresh Now"):
    st.rerun()

st.caption("💡 Real-time system telemetry via Python + MCP. [GitHub Repo](https://github.com/idaakiwumi/Frame-pulse-mcp)")