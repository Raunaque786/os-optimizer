from flask import Flask, render_template, jsonify
import psutil
import time
import random
import platform
import speedtest
import os

app = Flask(__name__)

# Simulate processing delay
def simulate_processing():
    time.sleep(1.5)

# System Information
@app.route('/system_info', methods=['GET'])
def system_info():
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
    freed_space = random.uniform(0.1, 1.0)  # Simulated freed space in GB
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
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 10**6  # Mbps
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

# Process Manager
@app.route('/process_manager', methods=['GET'])
def process_manager():
    processes = [
        {"pid": p.pid, "name": p.info['name'], "cpu": p.info['cpu_percent'], "ram": p.info['memory_percent']}
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
    ]
    simulate_processing()
    return jsonify({"processes": processes[:10]})  # Top 10 processes

# Battery Optimizer
@app.route('/battery_optimizer', methods=['GET'])
def battery_optimizer():
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        drain_rate = random.uniform(0.1, 1.0)  # Simulated drain rate
    else:
        percent = random.uniform(50, 100)
        drain_rate = random.uniform(0.1, 1.0)
    simulate_processing()
    return jsonify({
        "percent_before": round(percent, 1),
        "drain_rate_before": round(drain_rate, 2),
        "drain_rate_after": round(drain_rate * 0.8, 2)
    })

# Main Route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)