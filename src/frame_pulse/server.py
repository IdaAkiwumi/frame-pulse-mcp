"""
Frame Pulse MCP Server
MCP tools for AI agents to monitor and govern creative workstations.
"""

import sys
import os

# CRITICAL: Set path BEFORE any frame_pulse imports
# Use absolute path to work regardless of working directory
sys.path.insert(0, r"C:\Users\kemia\OneDrive\Documents\GitHub\frame-pulse-mcp\src")

# Now safe to import project modules
import logging
import traceback

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(r"C:\Users\kemia\OneDrive\Documents\GitHub\frame-pulse-mcp\frame_pulse.log"),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger("frame-pulse")

from mcp.server.fastmcp import FastMCP
from typing import Optional

from frame_pulse.system_client import get_thermal_status
from frame_pulse.render_guard import find_render_processes, format_process_list, emergency_throttle

mcp = FastMCP("FramePulse")

THROTTLE_EXPLANATION = """
WHAT THROTTLING/DEPRIORITIZING DOES:
- Reduces the target process's CPU priority (Windows: BELOW_NORMAL, Linux: nice +10)
- Process keeps running but yields CPU to higher-priority work
- Renders complete faster, system stays responsive, thermals stay controlled
- REVERSIBLE: You can restore normal priority later if needed

WHEN TO USE:
- Background apps competing with your main render
- Thermal CAUTION state (CPU 75-90%, Temp 75-85°C)
- Not responding to a render farm deadline

WHEN NOT TO USE:
- The process IS your main render (throttle something else instead)
- CRITICAL thermal state (use emergency throttle or pause entirely)
"""


@mcp.tool()
def check_system_health():
    """Check if workstation is safe for heavy creative workloads."""
    try:
        return get_thermal_status()
    except Exception as e:
        logger.error(f"check_system_health failed: {e}")
        logger.error(traceback.format_exc())
        return {"error": str(e), "status": "degraded"}


@mcp.tool()
def scan_creative_apps(app_name: Optional[str] = None):
    """Find active creative applications (Blender, Unreal, Maya, etc.)."""
    try:
        processes = find_render_processes(app_name)
        return format_process_list(processes)
    except Exception as e:
        logger.error(f"scan_creative_apps failed: {e}")
        logger.error(traceback.format_exc())
        return {"error": str(e), "processes": []}


@mcp.tool()
def throttle_process(target_pid: Optional[int] = None):
    """
    Reduce CPU priority of a process to prevent overheating.
    
    ALIASES: Also responds to "deprioritize" for clarity.
    
    Args:
        target_pid: Process ID to throttle. If None, auto-throttles highest CPU consumer.
    
    Returns:
        Confirmation message with explanation of what was done.
    """
    try:
        result = emergency_throttle(target_pid)
        return f"{result}\n\n{THROTTLE_EXPLANATION}"
    except Exception as e:
        logger.error(f"throttle_process failed: {e}")
        return {"error": str(e)}


@mcp.tool()
def deprioritize_process(target_pid: Optional[int] = None):
    """
    SAME AS THROTTLE — reduces CPU priority of a process.
    
    Use this if "throttle" sounds too aggressive. Same function, clearer language.
    
    Args:
        target_pid: Process ID to deprioritize. If None, auto-selects highest CPU consumer.
    
    Returns:
        Confirmation with full explanation of effects.
    """
    result = emergency_throttle(target_pid)
    return f"{result}\n\nTHROTTLING = DEPRIORITIZING: Same function, clearer name for non-technical users.\n\n{THROTTLE_EXPLANATION}"


@mcp.tool()
def emergency_throttle_process(target_pid: Optional[int] = None):
    """
    EMERGENCY: Immediately reduce priority without confirmation.
    
    Use when:
    - System in CRITICAL thermal state (CPU >90%, Temp >85°C)
    - Render farm node about to shut down from overheating
    - No time for explanation
    
    Returns:
        Action taken, minimal explanation.
    """
    try:
        return emergency_throttle(target_pid)
    except Exception as e:
        logger.error(f"emergency_throttle_process failed: {e}")
        return f"FAILED: {e}"


@mcp.tool()
def restore_priority(target_pid: int):
    """
    Restore a throttled process to normal CPU priority.
    
    Use this to 'undo' a throttle/deprioritize if you throttled the wrong process
    or if your main render finished and you want full performance back.
    
    Args:
        target_pid: Process ID to restore to normal priority (REQUIRED, no auto-detect for safety)
    
    Returns:
        Confirmation of priority restoration.
    """
    try:
        import psutil
        p = psutil.Process(target_pid)
        
        if hasattr(psutil, 'NORMAL_PRIORITY_CLASS'):
            p.nice(psutil.NORMAL_PRIORITY_CLASS)
        else:
            p.nice(0)  # Unix normal priority
        
        return f"Restored {p.name()} (PID {target_pid}) to normal priority\n\nProcess will now compete equally for CPU resources."
    except Exception as e:
        logger.error(f"restore_priority failed: {e}")
        return f"Failed to restore priority: {e}"


@mcp.tool()
def prioritize_process(target_pid: int):
    """
    Give a process HIGHER than normal CPU priority.
    
    WARNING: Use sparingly. High priority can make system unresponsive.
    
    Use only when:
    - A critical render must finish by deadline
    - System is otherwise idle
    - You accept risk of temporary unresponsiveness
    
    Args:
        target_pid: Process ID to boost (REQUIRED)
    
    Returns:
        Confirmation with warning about side effects.
    """
    try:
        import psutil
        p = psutil.Process(target_pid)
        
        if hasattr(psutil, 'HIGH_PRIORITY_CLASS'):
            p.nice(psutil.HIGH_PRIORITY_CLASS)
            warning = "HIGH PRIORITY SET: This process will preempt most others. System may feel sluggish."
        elif hasattr(psutil, 'ABOVE_NORMAL_PRIORITY_CLASS'):
            p.nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS)
            warning = "Above-normal priority set. Monitor system responsiveness."
        else:
            p.nice(-10)  # Unix high priority (negative = higher)
            warning = "High nice value set (-10). Monitor system load."
        
        return f"Prioritized {p.name()} (PID {target_pid})\n\n{warning}\n\nUse 'restore_priority' to undo if system becomes unresponsive."
    except Exception as e:
        logger.error(f"prioritize_process failed: {e}")
        return f"Failed to prioritize: {e}"


# Backward compatible aliases
@mcp.tool()
def get_thermal_status_alias():
    """Alias for check_system_health."""
    return check_system_health()


@mcp.tool()
def find_render_processes_alias(app_name: Optional[str] = None):
    """Alias for scan_creative_apps."""
    return scan_creative_apps(app_name)


@mcp.tool()
def emergency_throttle_alias(target_pid: Optional[int] = None):
    """Alias for throttle_process."""
    return throttle_process(target_pid)


if __name__ == "__main__":
    mcp.run()