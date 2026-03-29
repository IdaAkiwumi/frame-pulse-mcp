"""
Frame Pulse MCP Server
MCP tools for AI agents to monitor and govern creative workstations.
"""

import sys
import os

# Add parent to path for absolute imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP
from typing import Optional

# Absolute imports (work when run directly)
from frame_pulse.system_client import get_thermal_status
from frame_pulse.render_guard import find_render_processes, format_process_list, emergency_throttle

mcp = FastMCP("FramePulse")

@mcp.tool()
def check_system_health():
    """Check if workstation is safe for heavy creative workloads."""
    return get_thermal_status()

@mcp.tool()
def scan_creative_apps(app_name: Optional[str] = None):
    """Find active creative applications (Blender, Unreal, Maya, etc.)."""
    processes = find_render_processes(app_name)
    return format_process_list(processes)

@mcp.tool()
def throttle_process(target_pid: Optional[int] = None):
    """Reduce CPU priority of a process to prevent overheating."""
    return emergency_throttle(target_pid)

# Backward compatible aliases
@mcp.tool()
def get_thermal_status_alias():
    """Alias for check_system_health."""
    return get_thermal_status()

@mcp.tool()
def find_render_processes_alias(app_name: Optional[str] = None):
    """Alias for scan_creative_apps."""
    processes = find_render_processes(app_name)
    return format_process_list(processes)

@mcp.tool()
def emergency_throttle_alias(target_pid: Optional[int] = None):
    """Alias for throttle_process."""
    return emergency_throttle(target_pid)

if __name__ == "__main__":
    mcp.run()