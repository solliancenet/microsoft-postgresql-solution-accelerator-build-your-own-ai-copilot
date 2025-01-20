const { data } = require('react-router-dom');
const apiConfig = require('./APIConfig'); // Assuming apiConfig is in the same directory

const RESTHelper = require('./RESTHelper');

const getUrl = (url) => {
    return `${apiConfig.APIUrl}${url}`;
};

/* *************** */
/* Exported API */
/* *************** */

module.exports = {
    getStatus: async () => {
        return await RESTHelper.get(getUrl(`/status`));
    },
    completions: {
        chat: async (message, history) => {
            const chat_history = history || [];
            return await RESTHelper.post(getUrl(`/completions/chat`), {
                message,
                chat_history,
            });
        },
    },
    deliverables: {
        list: async (milestoneId = -1, skip = 0, limit = 10, sortBy = '') => {
            return await RESTHelper.get(getUrl(`/deliverables?milestone_id=${milestoneId}&skip=${skip}&limit=${limit}&sortby=${sortBy}`));
        },
        get: async (id) => {
            return await RESTHelper.get(getUrl(`/deliverables/${id}`));
        },
        create: async (id, data) => {       
            console.info('Creating deliverable:');
        
            const formData = new FormData();

            formData.append('milestone_id', id);
            for(var key in data){
                formData.append(key, data[key]);
            }
        
            try {
                const response = await fetch(getUrl(`/deliverables`), {
                    method: 'POST',
                    body: formData,
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const result = await response.json();
                return result;
            } catch (error) {
                console.error('Error creating deliverable:', error);
                throw error;
            }
        },
        update: async (id, data) => {
            return await RESTHelper.update(getUrl(`/deliverables/${id}`), data);
        },
        delete: async (id) => {
            return await RESTHelper.delete(getUrl(`/deliverables/${id}`));
        }
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
    invoices: {
        list: async (skip = 0, limit = 10, sortBy = '') => {
            return await RESTHelper.get(getUrl(`/invoices?skip=${skip}&limit=${limit}&sortby=${sortBy}`));
        },
        get: async (id) => {
            return await RESTHelper.get(getUrl(`/invoices/${id}`));
        },
        create: async (file, data) => {
            if (!file) return;
        
            console.info('Creating invoice:', file);
        
            const formData = new FormData();
            formData.append('file', file);
            for(var key in data){
                formData.append(key, data[key]);
            }
        
            try {
                const response = await fetch(getUrl(`/invoices`), {
                    method: 'POST',
                    body: formData,
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const result = await response.json();
                return result;
            } catch (error) {
                console.error('Error creating invoice:', error);
                throw error;
            }
        },
        update: async (id, data) => {
            return await RESTHelper.update(getUrl(`/invoices/${id}`), data);
        },
        delete: async (id) => {
            return await RESTHelper.delete(getUrl(`/invoices/${id}`));
        }
    },
    milestones: {
        list: async (sowId = -1, skip = 0, limit = 10, sortBy = '') => {
            return await RESTHelper.get(getUrl(`/milestones?sow_id=${sowId}&skip=${skip}&limit=${limit}&sortby=${sortBy}`));
        },
        get: async (id) => {
            return await RESTHelper.get(getUrl(`/milestones/${id}`));
        },
        create: async (data) => {
            console.info('Creating milestone');
        
            const formData = new FormData();
            for(var key in data){
                formData.append(key, data[key]);
            }
        
            try {
                const response = await fetch(getUrl(`/milestones`), {
                    method: 'POST',
                    body: formData,
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const result = await response.json();
                return result;
            } catch (error) {
                console.error('Error creating milestone:', error);
                throw error;
            }
        },
        update: async (id, data) => {
            return await RESTHelper.update(getUrl(`/milestones/${id}`), data);
        },
        delete: async (id) => {
            return await RESTHelper.delete(getUrl(`/milestones/${id}`));
        }
    },
    msas: {
        list: async (vendor_id = -1, skip = 0, limit = 10, sortBy = '') => {
            return await RESTHelper.get(getUrl(`/msas?vendor_id=${vendor_id}&skip=${skip}&limit=${limit}&sortby=${sortBy}`));
        },
        get: async (id) => {
            return await RESTHelper.get(getUrl(`/msas/${id}`));
        },
        create: async (file, data) => {
            if (!file) return;

            console.info('Creating MSA');
        
            const formData = new FormData();
            formData.append('file', file);
            for(var key in data) {
                formData.append(key, data[key]);
            }
        
            try {
                const response = await fetch(getUrl(`/msas`), {
                    method: 'POST',
                    body: formData,
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const result = await response.json();
                return result;
            } catch (error) {
                console.error('Error creating MSA:', error);
                throw error;
            }
        },
        update: async(id, data) => {
            return await RESTHelper.update(getUrl(`/msas/${id}`), data);
        },
        delete: async (id) => {
            return await RESTHelper.delete(getUrl(`/msas/${id}`));
        }
    },
    sows: {
        list: async (msa_id = -1, skip = 0, limit = 10, sortBy = '') => {
            return await RESTHelper.get(getUrl(`/sows?msa_id=${msa_id}&skip=${skip}&limit=${limit}&sortby=${sortBy}`));
        },
        get: async (id) => {
            return await RESTHelper.get(getUrl(`/sows/${id}`));
        },
        create: async (file, data) => {
            if (!file) return;
        
            console.info('Creating SOW:', file);
        
            const formData = new FormData();
            formData.append('file', file);
            for (var key in data) {
                formData.append(key, data[key]);
            }

            try {
                const response = await fetch(getUrl(`/sows`), {
                    method: 'POST',
                    body: formData,
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const result = await response.json();
                return result;
            } catch (error) {
                console.error('Error creating SOW:', error);
                throw error;
            }
        },
        update: async (id, data) => {
            return await RESTHelper.update(getUrl(`/sows/${id}`), data);
        },
        delete: async (id) => {
            return await RESTHelper.delete(getUrl(`/sows/${id}`));
        }
    },
    statuses: {
        list: async () => {
            return await RESTHelper.get(getUrl(`/statuses`));
        }
    },
    vendors: {
        list: async (skip = 0, limit = 10, sortBy = '') => {
            return await RESTHelper.get(getUrl(`/vendors?skip=${skip}&limit=${limit}&sortby=${sortBy}`));
        },
        get: async (id) => {
            return await RESTHelper.get(getUrl(`/vendors/${id}`));
        },
        create: async (data) => {
            console.info('Creating vendor');

            const formData = new FormData();
            for(var key in data){
                formData.append(key, data[key]);
            }

            try {
                const response = await fetch(getUrl(`/vendors`), {
                    method: 'POST',
                    body: formData,
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const result = await response.json();
                return result;
            } catch (error) {
                console.error('Error creating vendor:', error);
                throw error;
            }
        },
        update: async (id, data) => {
            return await RESTHelper.update(getUrl(`/vendors/${id}`), data);
        }, 
        delete: async (id) => {
            return await RESTHelper.delete(getUrl(`/vendors/${id}`));
        }
    }
};