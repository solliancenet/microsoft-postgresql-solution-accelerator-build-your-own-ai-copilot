const apiConfig = require('./APIConfig'); // Assuming apiConfig is in the same directory

const getStatus = async () => {
    try {
        const response = await fetch(`${apiConfig.APIUrl}/v1/status`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching status:', error);
        throw error;
    }
};

module.exports = {
    getStatus,
};