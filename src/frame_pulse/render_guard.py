import psutil

CREATIVE_APPS = [
    'blender', 'blender.exe',
    'unreal', 'unrealeditor', 'ue4editor', 'ue5editor',
    'unity', 'unity.exe',
    'maya', 'mayabatch', 'mayapy',
    'houdini', 'houdinifx', 'houdini.exe',
    'afterfx', 'afterfx.exe',
    'cinema', 'c4d',
    'nuke', 'nuke.exe',
    'resolve', 'resolve.exe',
    'premiere', 'premiere.exe',
    'substance', 'substance painter',
    'zbrush', 'zbrush.exe'
]

def find_render_processes(app_name=None):
    """Scan for active creative applications."""
    targets = [app_name.lower()] if app_name else CREATIVE_APPS
    
    found = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            name = proc.info['name'].lower()
            if any(t in name for t in targets):
                cpu = proc.info['cpu_percent'] or 0
                mem = proc.info['memory_percent'] or 0
                found.append({
                    'name': proc.info['name'],
                    'pid': proc.info['pid'],
                    'cpu': cpu,
                    'memory': mem,
                    'status': proc.info['status']
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return found

def format_process_list(processes):
    """Pretty print for display."""
    if not processes:
        return "No active render processes detected"
    
    lines = []
    for p in processes:
        lines.append(f"{p['name']} (PID {p['pid']}): {p['cpu']:.1f}% CPU, {p['memory']:.1f}% RAM")
    return "\n".join(lines)

def emergency_throttle(target_pid=None):
    """Reduce process priority to prevent thermal damage."""
    try:
        if target_pid:
            p = psutil.Process(int(target_pid))
            # Cross-platform priority reduction
            if hasattr(psutil, 'BELOW_NORMAL_PRIORITY_CLASS'):  # Windows
                p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
            else:  # Unix
                p.nice(10)
            return f"Throttled {p.name()} (PID {target_pid})"
        
        # Auto-detect highest CPU consumer
        highest = None
        max_cpu = 0
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                if proc.info['cpu_percent'] > max_cpu and proc.info['name'] not in ['System', 'Registry', 'svchost.exe', 'wininit.exe']:
                    max_cpu = proc.info['cpu_percent']
                    highest = proc.info['pid']
            except:
                continue
        
        if highest and max_cpu > 80:
            p = psutil.Process(highest)
            if hasattr(psutil, 'BELOW_NORMAL_PRIORITY_CLASS'):
                p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
            else:
                p.nice(10)
            return f"Auto-throttled {p.name()} (PID {highest}) using {max_cpu:.1f}% CPU"
        
        return "No throttling needed — system stable"
        
    except Exception as e:
        return f"Throttle failed: {e}"