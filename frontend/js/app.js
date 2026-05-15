document.addEventListener('DOMContentLoaded', () => {
    const terminal = document.getElementById('terminal-output');
    const btnAudit = document.getElementById('btn-audit');
    const btnHealth = document.getElementById('btn-health');

    const logToTerminal = (message, type = 'info') => {
        const p = document.createElement('p');
        p.className = 'log-entry';
        const time = new Date().toLocaleTimeString();
        p.innerHTML = `<span style="color: #8b949e">[${time}]</span> ${message}`;
        terminal.appendChild(p);
        terminal.scrollTop = terminal.scrollHeight;
    };

    
    btnAudit.addEventListener('click', async () => {
        logToTerminal('ACCESSING: https://findmyproject.com/api/v1/secure-data');
        logToTerminal('INITIATING GLOBAL SECURITY SCAN...', 'warn');
        
        const newData = await InfrastructureAPI.getAuditReport();
        
        setTimeout(() => {
            if (window.auditChart) {
                window.auditChart.data.datasets[0].data = [newData.openPorts, newData.securePorts];
                window.auditChart.update();
            }
            logToTerminal('SCAN COMPLETE: INFRASTRUCTURE SECURE.', 'success');
        }, 1200);
    });

    
    btnHealth.addEventListener('click', async () => {
        logToTerminal('QUERYING CLUSTER STATUS...');
        const health = await InfrastructureAPI.checkHealth();
        logToTerminal(`SYSTEM: ${health.status.toUpperCase()} | ENDPOINT: findmyproject.com`, 'success');
    });

    logToTerminal('Production Monitor ready at findmyproject.com');
});