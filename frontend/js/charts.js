window.auditChart = null;
window.trafficChart = null;

const renderCharts = async () => {
    console.log("> Syncing charts with findmyproject.com production server...");

    let auditData, trafficData;
    
    try {
        auditData = await InfrastructureAPI.getAuditReport();
        trafficData = await InfrastructureAPI.getTrafficData();
    } catch (error) {
        console.warn("> Using fallback visual data for initial render");
        auditData = { openPorts: 15, securePorts: 85 };
        trafficData = { allowed: 2500, blocked: 600 };
    }

   
    const auditCtx = document.getElementById('auditChart').getContext('2d');
    if (window.auditChart) window.auditChart.destroy();

    window.auditChart = new Chart(auditCtx, {
        type: 'doughnut',
        data: {
            labels: ['Critical Risks', 'Secure Zones'],
            datasets: [{
                data: [auditData.openPorts, auditData.securePorts],
                backgroundColor: ['#f85149', '#3fb950'], 
                borderColor: '#0d1117',
                borderWidth: 5,
                hoverOffset: 12
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#8b949e', font: { family: 'Segoe UI', size: 11 } }
                }
            }
        }
    });

    
    const trafficCtx = document.getElementById('trafficChart').getContext('2d');
    if (window.trafficChart) window.trafficChart.destroy();

    window.trafficChart = new Chart(trafficCtx, {
        type: 'bar',
        data: {
            labels: ['Authorized Traffic', 'Blocked Attacks'],
            datasets: [{
                label: 'Global Requests',
                data: [trafficData.allowed, trafficData.blocked],
                backgroundColor: ['#58a6ff', '#f85149'],
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#30363d' },
                    ticks: { color: '#8b949e' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#8b949e' }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
};

document.addEventListener('DOMContentLoaded', renderCharts);