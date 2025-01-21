
module.exports = {
    get: async (url) => {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const returnData = await response.json();
            return returnData;
        } catch (error) {
            console.error('Error fetching data:', error);
            throw error;
        }
    },
    post: async (url, data) => {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const returnData = await response.json();
            return returnData;
        } catch (error) {
            console.error('Error posting data:', error);
            throw error;
        }
    },
    update: async (url, data) => {
        try {
            const response = await fetch(url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const returnData = await response.json();
            return returnData;
        }
        catch (error) {
            console.error('Error updating SOW:', error);
            throw error;
        }
    },
    delete: async (url) => {
        try {
            const response = await fetch(url, {
                method: 'DELETE',
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return;
        }
        catch (error) {
            console.error('Error deleting:', error);
            throw error;
        }
    }
};