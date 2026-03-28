import psutil
from mcp.server.fastmcp import FastMCP
from typing import Optional

# Import from our new modules
from .system_client import get_thermal_status, get_system_stats
from .render_guard import find_render_processes, format_process_list, emergency_throttle

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

# Backward compatible aliases for old tool names
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