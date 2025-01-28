
module.exports = {
    get: async (url) => {
        const tryGet = async () => {
            const response = await fetch(url, {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                }
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const returnData = await response.json();
            return returnData;
        };

        const retries = 3;
        const delay = 400;
        for(let attempts = 1; attempts <= retries; attempts++) {
            try {
                return await tryGet();
            } catch (error) {
                if (attempts === retries) {
                    console.error(`Error fetching data after multiple attempts(${attempts}):`, error);
                    throw error;
                }
                console.warn(`Error fetching data, Retrying in ${delay}ms...`, error);
                await new Promise(resolve => setTimeout(resolve, delay));
            }
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