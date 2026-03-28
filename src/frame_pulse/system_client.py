import psutil
import os

def get_system_stats():
    """Get core system telemetry."""
    try:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        stats = {
            'cpu': {'percent': cpu, 'cores': psutil.cpu_count()},
            'memory': {
                'percent': mem.percent,
                'used_gb': mem.used // (1024**3),
                'available_gb': mem.available // (1024**3)
            },
            'disk': {
                'percent': disk.percent,
                'free_gb': disk.free // (1024**3)
            }
        }
        
        # Add temps if available
        if hasattr(psutil, 'sensors_temperatures'):
            temps = psutil.sensors_temperatures()
            if temps:
                stats['temperatures'] = {
                    name: [t.current for t in entries if hasattr(t, 'current')]
                    for name, entries in temps.items()
                }
        
        return stats
    except Exception as e:
        # Cloud/demo fallback
        import random
        return {
            'cpu': {'percent': random.randint(20, 45), 'cores': 8},
            'memory': {'percent': random.randint(30, 60), 'used_gb': 16, 'available_gb': 16},
            'disk': {'percent': random.randint(40, 70), 'free_gb': 200},
            '_demo_mode': True,
            '_error': str(e)
        }

def get_thermal_status():
    """Quick status check for MCP tools."""
    stats = get_system_stats()
    cpu = stats['cpu']['percent']
    
    # Check temps if available
    temp = 0
    if 'temperatures' in stats and stats['temperatures']:
        try:
            temp = max([
                t for sublist in stats['temperatures'].values() 
                for t in (sublist if isinstance(sublist, list) else [sublist])
                if isinstance(t, (int, float))
            ])
        except:
            pass
    
    # Demo mode detection
    if stats.get('_demo_mode'):
        return f"DEMO: CPU {cpu}%, Temp {temp or 65}°C — Simulated for preview"
    
    # Real status
    if cpu > 90 or temp > 85:
        return f"CRITICAL: HALT renders immediately"
    elif cpu > 75 or temp > 75:
        return f"CAUTION: Queue carefully"
    return f"SAFE: Ready for production workloads"

  # Real status
   # if cpu > 90 or temp > 85:
   #     return f"CRITICAL: CPU {cpu}%, Temp {temp}°C — HALT renders immediately"
  #  elif cpu > 75 or temp > 75:
  #      return f"CAUTION: CPU {cpu}%, Temp {temp}°C — Queue carefully"
   # return f"SAFE: CPU {cpu}%, Temp {temp}°C — Ready for production workloads" 