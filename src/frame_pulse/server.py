from mcp.server.fastmcp import FastMCP
import psutil
from typing import Optional

mcp = FastMCP("ProductionPulse")

@mcp.tool()
def get_thermal_status():
    """Check system thermal/load before starting a render."""
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    
    temp = 0
    if hasattr(psutil, "sensors_temperatures"):
        temps = psutil.sensors_temperatures()
        if temps and 'coretemp' in temps:
            temp = max([t.current for t in temps['coretemp']])
    
    status = "SAFE"
    if cpu > 90 or temp > 85:
        status = "CRITICAL"
    elif cpu > 75 or temp > 75:
        status = "CAUTION"
    
    return f"{status}: CPU {cpu}%, Temp {temp}°C"

@mcp.tool()
def find_render_processes(app_name: Optional[str] = None):
    """Scan for creative apps with resource usage."""
    targets = ['blender', 'unreal', 'unity', 'maya', 'afterfx', 'houdini', 'cinema']
    if app_name:
        targets = [app_name.lower()]
    
    found = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            name = proc.info['name'].lower()
            if any(t in name for t in targets):
                found.append(f"{proc.info['name']} (PID {proc.info['pid']}): {proc.info['cpu_percent']:.1f}% CPU, {proc.info['memory_percent']:.1f}% RAM")
        except:
            continue
    
    return "\n".join(found) if found else "No active render processes"

@mcp.tool()
def emergency_throttle(target_pid: Optional[int] = None):
    """Reduce process priority to prevent thermal damage."""
    # Windows-safe implementation
    try:
        if target_pid:
            p = psutil.Process(target_pid)
            p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if hasattr(psutil, 'BELOW_NORMAL_PRIORITY_CLASS') else 10)
            return f"Throttled PID {target_pid}"
        
        # Auto-detect highest consumer
        highest = None
        max_cpu = 0
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            if proc.info['cpu_percent'] > max_cpu and proc.info['name'] not in ['System', 'Registry', 'svchost']:
                max_cpu = proc.info['cpu_percent']
                highest = proc.info['pid']
        
        if highest and max_cpu > 80:
            p = psutil.Process(highest)
            p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if hasattr(psutil, 'BELOW_NORMAL_PRIORITY_CLASS') else 10)
            return f"Auto-throttled PID {highest} using {max_cpu:.1f}% CPU"
        
        return "No throttling needed"
    except Exception as e:
        return f"Throttle failed: {e}"

# THIS IS THE CRITICAL FIX
if __name__ == "__main__":
    mcp.run()