function showLoader(show) {
    document.getElementById('loader').classList.toggle('hidden', !show);
}

function runModule(module) {
    showLoader(true);
    fetch(`/${module}`)
        .then(response => response.json())
        .then(data => {
            showLoader(false);
            const resultDiv = document.getElementById(module);
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
            }
        })
        .catch(error => {
            showLoader(false);
            console.error('Error:', error);
            alert(`${module.replace('_', ' ')} failed!`);
        });
}

// Dark Mode Toggle
document.getElementById('toggleDarkMode').addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
    this.textContent = document.body.classList.contains('dark-mode') ? 'Light Mode' : 'Dark Mode';
});
