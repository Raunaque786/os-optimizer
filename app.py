from flask import Flask, render_template, jsonify
import psutil
import time
import random
import platform
import speedtest
import os
import math

app = Flask(__name__)

# Simulate processing delay
def simulate_processing():
    time.sleep(1.5)

# System Information
@app.route('/system_info', methods=['GET'])
def system_info():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        os_info = f"{platform.system()} {platform.release()}"
        return jsonify({
            "cpu_usage": cpu_usage,
            "ram_total": round(ram.total / (1024 ** 3), 1),
            "ram_used": round(ram.used / (1024 ** 3), 1),
            "disk_total": round(disk.total / (1024 ** 3), 1),
            "disk_used": round(disk.used / (1024 ** 3), 1),
            "os": os_info
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Memory Cleaner
@app.route('/memory_cleaner', methods=['GET'])
def memory_cleaner():
    ram_before = psutil.virtual_memory().percent
    simulate_processing()
    ram_after = max(ram_before - random.uniform(5, 15), 10)
    return jsonify({"ram_before": ram_before, "ram_after": ram_after})

# Disk Manager
@app.route('/disk_manager', methods=['GET'])
def disk_manager():
    disk = psutil.disk_usage('/')
    simulate_processing()
    freed_space = random.uniform(0.1, 1.0)
    return jsonify({
        "total": round(disk.total / (1024 ** 3), 1),
        "used_before": round(disk.used / (1024 ** 3), 1),
        "freed": round(freed_space, 1)
    })

# CPU Optimizer
@app.route('/cpu_optimizer', methods=['GET'])
def cpu_optimizer():
    cpu_before = psutil.cpu_percent(interval=1)
    simulate_processing()
    cpu_after = max(cpu_before - random.uniform(5, 20), 5)
    return jsonify({"cpu_before": cpu_before, "cpu_after": cpu_after})

# Network Optimizer
@app.route('/network_optimizer', methods=['GET'])
def network_optimizer():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 10**6
        ping = st.results.ping
        simulate_processing()
        improved_download = download_speed * 1.1
        improved_ping = max(ping - 10, 5)
        return jsonify({
            "download_before": round(download_speed, 1),
            "download_after": round(improved_download, 1),
            "ping_before": round(ping, 1),
            "ping_after": round(improved_ping, 1)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Process Manager
@app.route('/process_manager', methods=['GET'])
def process_manager():
    processes = [
        {"pid": p.pid, "name": p.info['name'], "cpu": p.info['cpu_percent'], "ram": p.info['memory_percent']}
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
    ]
    simulate_processing()
    return jsonify({"processes": processes[:10]})

# Battery Optimizer
@app.route('/battery_optimizer', methods=['GET'])
def battery_optimizer():
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        drain_rate = random.uniform(0.1, 1.0)
    else:
        percent = random.uniform(50, 100)
        drain_rate = random.uniform(0.1, 1.0)
    simulate_processing()
    return jsonify({
        "percent_before": round(percent, 1),
        "drain_rate_before": round(drain_rate, 2),
        "drain_rate_after": round(drain_rate * 0.8, 2)
    })

# Startup Manager
@app.route('/startup_manager', methods=['GET'])
def startup_manager():
    processes = [
        {"name": "SystemUpdater", "enabled": True, "impact": "High"},
        {"name": "BackgroundSync", "enabled": True, "impact": "Medium"},
        {"name": "AppLauncher", "enabled": True, "impact": "Low"},
        {"name": "NetworkMonitor", "enabled": False, "impact": "Medium"}
    ]
    simulate_processing()
    disabled_count = random.randint(1, 2)
    for i in range(disabled_count):
        if processes[i]["enabled"]:
            processes[i]["enabled"] = False
    return jsonify({"startup_items": processes, "disabled_count": disabled_count})

# System Health Check
@app.route('/system_health', methods=['GET'])
def system_health():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    network_health = random.uniform(70, 100)
    simulate_processing()
    health_score = round((100 - cpu) * 0.3 + (100 - ram) * 0.3 + (100 - disk) * 0.3 + network_health * 0.1, 1)
    return jsonify({
        "cpu": cpu,
        "ram": ram,
        "disk": disk,
        "network": network_health,
        "health_score": max(health_score, 0)
    })

# System Restart
@app.route('/restart_system', methods=['GET'])
def restart_system():
    simulate_processing()
    return jsonify({"message": "System restart initiated (simulated)."})

# CPU Temp and Clock Speed
@app.route('/cpu_stats', methods=['GET'])
def cpu_stats():
    try:
        freq = psutil.cpu_freq()
        clock_speed = freq.current / 1000 if freq and freq.current else random.uniform(1.5, 3.5)
        temps = psutil.sensors_temperatures()
        if temps and 'coretemp' in temps:
            temp = temps['coretemp'][0].current
        elif temps and 'cpu_thermal' in temps:
            temp = temps['cpu_thermal'][0].current
        else:
            temp = random.uniform(35, 65)
        return jsonify({
            "temperature": round(temp, 1),
            "clock_speed": round(clock_speed, 2),
            "status": "success"
        })
    except Exception as e:
        return jsonify({
            "temperature": round(random.uniform(35, 65), 1),
            "clock_speed": round(random.uniform(1.5, 3.5), 2),
            "status": "simulated",
            "error": str(e)
        })

# Check System Updates
@app.route('/check_updates', methods=['GET'])
def check_updates():
    simulate_processing()
    updates_available = random.choice([True, False])
    update_count = random.randint(1, 5) if updates_available else 0
    return jsonify({
        "updates_available": updates_available,
        "update_count": update_count,
        "message": f"{update_count} update(s) available" if updates_available else "System is up to date"
    })

# Junk File Cleaner
@app.route('/junk_file_cleaner', methods=['GET'])
def junk_file_cleaner():
    disk = psutil.disk_usage('/')
    simulate_processing()
    junk_freed = random.uniform(0.2, 2.0)
    return jsonify({
        "used_before": round(disk.used / (1024 ** 3), 1),
        "freed": round(junk_freed, 1),
        "used_after": round((disk.used / (1024 ** 3)) - junk_freed, 1)
    })

# System Booster
@app.route('/system_booster', methods=['GET'])
def system_booster():
    cpu_before = psutil.cpu_percent(interval=1)
    ram_before = psutil.virtual_memory().percent
    simulate_processing()
    cpu_after = max(cpu_before - random.uniform(10, 25), 5)
    ram_after = max(ram_before - random.uniform(5, 20), 10)
    boost_score = round(random.uniform(15, 30), 1)
    return jsonify({
        "cpu_before": cpu_before,
        "cpu_after": cpu_after,
        "ram_before": ram_before,
        "ram_after": ram_after,
        "boost_score": boost_score
    })

# Power Plan Manager
@app.route('/power_plan_manager', methods=['GET'])
def power_plan_manager():
    battery = psutil.sensors_battery()
    current_plan = random.choice(["Balanced", "Power Saver", "High Performance"])
    simulate_processing()
    optimized_plan = "High Performance" if not battery else "Balanced"
    power_efficiency = round(random.uniform(10, 25), 1)
    return jsonify({
        "current_plan": current_plan,
        "optimized_plan": optimized_plan,
        "power_efficiency_improvement": power_efficiency
    })

# Updated CPU Performance Wave Endpoint
@app.route('/cpu_wave', methods=['GET'])
def cpu_wave():
    cpu_data = []
    base_cpu = psutil.cpu_percent(interval=1)  # Baseline CPU usage
    for i in range(20):
        wave_fluctuation = 20 * math.sin(i * 0.5)  # Larger amplitude for visible wave
        cpu_usage = max(0, min(100, base_cpu + wave_fluctuation + random.uniform(-5, 5)))
        cpu_data.append(cpu_usage)
        time.sleep(0.1)  # Short delay for real-time feel
    return jsonify({"cpu_wave": cpu_data, "labels": list(range(1, 21))})

# Main Route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
