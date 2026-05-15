const InfrastructureAPI = {
    BASE_URL: 'https://findmyproject.com/api/v1', 
    async getAuditReport() {
        try {
            const response = await fetch(`${this.BASE_URL}/secure-data`);
            if (!response.ok) throw new Error('Security Audit Fetch Failed');
            return await response.json();
        } catch (error) {
            console.error("Audit Error:", error);
            return { openPorts: 8, securePorts: 92 };
        }
    },

    
    async getTrafficData() {
        try {
            const response = await fetch(`${this.BASE_URL}/public`);
            if (!response.ok) throw new Error('Traffic Data Fetch Failed');
            return await response.json();
        } catch (error) {
            console.error("Traffic Error:", error);
            return { allowed: 1500, blocked: 400 };
        }
    },

    
    async checkHealth() {
        try {
            const response = await fetch(`${this.BASE_URL}/health`);
            if (!response.ok) throw new Error('Health Check Failed');
            return await response.json();
        } catch (error) {
            console.error("Health Check Error:", error);
            return { status: "offline", cluster: "devsecops-eks" };
        }
    }
};