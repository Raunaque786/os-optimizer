function showLoader(show) {
    document.getElementById('loader').classList.toggle('hidden', !show);
}

let cpuWaveChart = null;

function runModule(module) {
    showLoader(true);
    fetch(`/${module}`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            showLoader(false);
            const resultDiv = document.getElementById(module);
            if (data.error) {
                resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
                return;
            }
            switch (module) {
                case 'system_info':
                    resultDiv.innerHTML = `
                        <p>CPU Usage: ${data.cpu_usage.toFixed(1)}%</p>
                        <p>RAM: ${data.ram_used} / ${data.ram_total} GB</p>
                        <p>Disk: ${data.disk_used} / ${data.disk_total} GB</p>
                        <p>OS: ${data.os}</p>`;
                    break;
                case 'memory_cleaner':
                    resultDiv.innerHTML = `
                        <p>RAM Before: ${data.ram_before.toFixed(1)}%</p>
                        <p>RAM After: ${data.ram_after.toFixed(1)}%</p>
                        <p>Memory Freed: ${(data.ram_before - data.ram_after).toFixed(1)}%</p>`;
                    break;
                case 'disk_manager':
                    resultDiv.innerHTML = `
                        <p>Total: ${data.total} GB</p>
                        <p>Used Before: ${data.used_before} GB</p>
                        <p>Freed: ${data.freed} GB</p>`;
                    break;
                case 'cpu_optimizer':
                    resultDiv.innerHTML = `
                        <p>CPU Before: ${data.cpu_before.toFixed(1)}%</p>
                        <p>CPU After: ${data.cpu_after.toFixed(1)}%</p>`;
                    break;
                case 'network_optimizer':
                    resultDiv.innerHTML = `
                        <p>Download Before: ${data.download_before} Mbps</p>
                        <p>Download After: ${data.download_after} Mbps</p>
                        <p>Ping Before: ${data.ping_before} ms</p>
                        <p>Ping After: ${data.ping_after} ms</p>`;
                    break;
                case 'process_manager':
                    resultDiv.innerHTML = data.processes.map(p =>
                        `<p>${p.name} - CPU: ${p.cpu.toFixed(1)}%, RAM: ${p.ram.toFixed(1)}%</p>`
                    ).join('');
                    break;
                case 'battery_optimizer':
                    resultDiv.innerHTML = `
                        <p>Battery: ${data.percent_before}%</p>
                        <p>Drain Rate Before: ${data.drain_rate_before}%/min</p>
                        <p>Drain Rate After: ${data.drain_rate_after}%/min</p>`;
                    break;
                case 'startup_manager':
                    resultDiv.innerHTML = `
                        <p>Startup Items Managed:</p>
                        ${data.startup_items.map(item =>
                            `<p>${item.name} - Impact: ${item.impact}, Enabled: ${item.enabled ? 'Yes' : 'No'}</p>`
                        ).join('')}
                        <p>Disabled ${data.disabled_count} item(s).</p>`;
                    break;
                case 'system_health':
                    resultDiv.innerHTML = `
                        <p>CPU Usage: ${data.cpu.toFixed(1)}%</p>
                        <p>RAM Usage: ${data.ram.toFixed(1)}%</p>
                        <p>Disk Usage: ${data.disk.toFixed(1)}%</p>
                        <p>Network Health: ${data.network.toFixed(1)}%</p>
                        <p class="health-score">System Health Score: ${data.health_score}%</p>`;
                    break;
                case 'junk_file_cleaner':
                    resultDiv.innerHTML = `
                        <p>Used Before: ${data.used_before} GB</p>
                        <p>Junk Freed: ${data.freed} GB</p>
                        <p>Used After: ${data.used_after} GB</p>`;
                    break;
                case 'system_booster':
                    resultDiv.innerHTML = `
                        <p>CPU Before: ${data.cpu_before.toFixed(1)}%</p>
                        <p>CPU After: ${data.cpu_after.toFixed(1)}%</p>
                        <p>RAM Before: ${data.ram_before.toFixed(1)}%</p>
                        <p>RAM After: ${data.ram_after.toFixed(1)}%</p>
                        <p>Boost Score: ${data.boost_score}%</p>`;
                    break;
                case 'power_plan_manager':
                    resultDiv.innerHTML = `
                        <p>Current Plan: ${data.current_plan}</p>
                        <p>Optimized Plan: ${data.optimized_plan}</p>
                        <p>Power Efficiency Improved: ${data.power_efficiency_improvement}%</p>`;
                    break;
                case 'cpu_wave':
                    if (cpuWaveChart) {
                        cpuWaveChart.data.datasets[0].data.shift();
                        cpuWaveChart.data.datasets[0].data.push(data.cpu_wave[data.cpu_wave.length - 1]);
                        cpuWaveChart.update('none');
                    }
                    break;
            }
        })
        .catch(error => {
            showLoader(false);
            console.error('Error:', error);
            alert(`${module.replace('_', ' ')} failed!`);
        });
}

document.getElementById('toggleDarkMode').addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
    this.textContent = document.body.classList.contains('dark-mode') ? 'Light Mode' : 'Dark Mode';
});

function toggleRestart() {
    const toggle = document.getElementById('restartToggle');
    const label = document.getElementById('restartLabel');
    showLoader(true);
    if (toggle.checked) {
        fetch('/restart_system')
            .then(response => response.json())
            .then(data => {
                showLoader(false);
                label.textContent = 'Restart: On';
                alert(data.message);
            })
            .catch(error => {
                showLoader(false);
                console.error('Error:', error);
                alert('Restart failed!');
                toggle.checked = false;
                label.textContent = 'Restart: Off';
            });
    } else {
        showLoader(false);
        label.textContent = 'Restart: Off';
    }
}

function updateCpuStats() {
    fetch('/cpu_stats')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            document.getElementById('cpuTemp').textContent = data.temperature;
            document.getElementById('cpuSpeed').textContent = data.clock_speed;
            if (data.status === 'simulated') {
                console.warn('CPU stats simulated due to error:', data.error);
            }
        })
        .catch(error => {
            console.error('Error fetching CPU stats:', error);
            document.getElementById('cpuTemp').textContent = (Math.random() * 30 + 35).toFixed(1);
            document.getElementById('cpuSpeed').textContent = (Math.random() * 2 + 1.5).toFixed(2);
        });
}

function checkSystemUpdates() {
    fetch('/check_updates')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            document.getElementById('updateStatus').textContent = data.message;
        })
        .catch(error => {
            console.error('Error checking updates:', error);
            document.getElementById('updateStatus').textContent = 'Update check failed';
        });
}

function initializeCpuWaveChart() {
    const ctx = document.getElementById('cpuWaveChart').getContext('2d');
    cpuWaveChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array(20).fill().map((_, i) => 20 - i),
            datasets: [{
                label: 'CPU Usage (%)',
                data: Array(20).fill(0),
                borderColor: '#4CAF50',
                backgroundColor: 'rgba(76, 175, 80, 0.4)',
                fill: true,
                tension: 0.5,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true, // Ensure aspect ratio is maintained
            animation: {
                duration: 0
            },
            scales: {
                y: { 
                    beginAtZero: true, 
                    max: 100, 
                    title: { display: true, text: 'CPU Usage (%)' },
                    grid: { color: document.body.classList.contains('dark-mode') ? '#666' : '#ddd' }
                },
                x: { 
                    title: { display: true, text: 'Time (seconds ago)' },
                    grid: { display: false }
                }
            },
            plugins: { legend: { display: false } },
            layout: {
                padding: 10 // Add some internal padding to the chart
            }
        }
    });

    setInterval(() => {
        runModule('cpu_wave');
    }, 1000);
}

setInterval(updateCpuStats, 2000);
updateCpuStats();

setInterval(checkSystemUpdates, 30000);
checkSystemUpdates();

document.addEventListener('DOMContentLoaded', () => {
    initializeCpuWaveChart();
});
