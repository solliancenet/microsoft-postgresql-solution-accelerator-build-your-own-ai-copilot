const apiConfig = require('./APIConfig'); // Assuming apiConfig is in the same directory

const apiVersion = 'v1';

const RESTHelper = require('./RESTHelper');

const getUrl = (url) => {
    return `${apiConfig.APIUrl}/${apiVersion}${url}`;
};

/* *************** */
/* Exported API */
/* *************** */

module.exports = {
    getStatus: async () => {
        return await RESTHelper.get(getUrl(`/status`));
    },
    documents: {
        list: async () => {
            return await RESTHelper.get(getUrl(`/documents`));
        },
        getUrl: (blobName) => {
            return getUrl(`/documents/${blobName}`);
        },
        upload: async (file) => {
            if (!file) return;
        
            console.info('Uploading document:', file);
        
            const formData = new FormData();
            formData.append('file', file);
        
            try {
                const response = await fetch(getUrl(`/documents`), {
                    method: 'POST',
                    body: formData,
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return;
            } catch (error) {
                console.error('Error uploading document:', error);
                throw error;
            }
        },
        delete: async (blobName) => {
            try {
                const response = await fetch(getUrl(`/documents/${blobName}`), {
                    method: 'DELETE',
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return;
            } catch (error) {
                console.error('Error deleting document:', error);
                throw error;
            }
        },
    },
    companies: {
        list: async (skip = 0, limit = 10, sortBy = '', search = '') => {
            return await RESTHelper.get(getUrl(`/company?skip=${skip}&limit=${limit}&sortby=${sortBy}&search=${search}`));
        },
    },
    vendors: {
        list: async (skip = 0, limit = 10, sortBy = '', search = '') => {
            return await RESTHelper.get(getUrl(`/vendor?skip=${skip}&limit=${limit}&sortby=${sortBy}&search=${search}`));
        },
    },
    sows: {
        list: async (skip = 0, limit = 10, sortBy = '', search = '') => {
            return await RESTHelper.get(getUrl(`/sows?skip=${skip}&limit=${limit}&sortby=${sortBy}&search=${search}`));
        },
        get: async (sowId) => {
            return await RESTHelper.get(getUrl(`/sows/${sowId}`));
        },
        create: async (file, sowTitle, startDate, endDate, budget) => {
            if (!file) return;
        
            console.info('Creating SOW:', file);
        
            const formData = new FormData();
            formData.append('file', file);
            formData.append('sow_title', sowTitle);
            formData.append('start_date', startDate);
            formData.append('end_date', endDate);
            formData.append('budget', budget);
        
            try {
                const response = await fetch(getUrl(`/sows/create`), {
                    method: 'POST',
                    body: formData,
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                return data;
            } catch (error) {
                console.error('Error creating SOW:', error);
                throw error;
            }
        },
        update: async (sowId, sowTitle, startDate, endDate, budget) => {
            return await RESTHelper.update(getUrl(`/sows/${sowId}`), {
                sow_title: sowTitle,
                start_date: startDate,
                end_date: endDate,
                budget: budget,
            });
        },
        delete: async (sowId) => {
            return await RESTHelper.delete(getUrl(`/sows/${sowId}`));
        }
    },
    invoices: {
        list: async (skip = 0, limit = 10, sortBy = '', search = '') => {
            return await RESTHelper.get(getUrl(`/invoices?skip=${skip}&limit=${limit}&sortby=${sortBy}&search=${search}`));
        },
    }
};