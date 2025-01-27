const { data } = require('react-router-dom');
const RESTHelper = require('./RESTHelper');

const APIUrl = process.env.REACT_APP_SERVICE_API_ENDPOINT_URL || 'http://localhost:8000';

const getUrl = (url) => {
    return `${APIUrl}${url}`;
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
        validations: async (id) => {
            return await RESTHelper.get(getUrl(`/invoices/${id}/validations`));
        },
        analyze: async (file, data) => {
            if (!file) return;

            console.info('Analyzing invoice:', file);

            const formData = new FormData();
            formData.append('file', file);
            for(var key in data){
                formData.append(key, data[key]);
            }

            try {
                const response = await fetch(getUrl(`/invoices/`), {
                    method: 'POST',
                    body: formData,
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const result = await response.json();
                return result;
            } catch (error) {
                console.error('Error analyzing invoice:', error);
                throw error;
            }
        },
        validate: async (id) => {
            console.info('Validating invoice:', id);
            
            try {
                const response = await fetch(getUrl(`/validation/invoice/${id}`), {
                    method: 'POST',
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return;
            } catch (error) {
                console.error('Error validating invoice:', error);
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
    invoiceLineItems: {
        list: async (invoiceId = -1, skip = 0, limit = 10, sortBy = '') => {
            return await RESTHelper.get(getUrl(`/invoice_line_items?invoice_id=${invoiceId}&skip=${skip}&limit=${limit}&sortby=${sortBy}`));
        },
        get: async (id) => {
            return await RESTHelper.get(getUrl(`/invoice_line_items/${id}`));
        },
        create: async (data) => {
            console.info('Creating invoice line item');
        
            const formData = new FormData();
            for(var key in data){
                formData.append(key, data[key]);
            }
        
            try {
                const response = await fetch(getUrl(`/invoice_line_items`), {
                    method: 'POST',
                    body: formData,
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const result = await response.json();
                return result;
            } catch (error) {
                console.error('Error creating invoice line item:', error);
                throw error;
            }
        },
        update: async (id, data) => {
            return await RESTHelper.update(getUrl(`/invoice_line_items/${id}`), data);
        },
        delete: async (id) => {
            return await RESTHelper.delete(getUrl(`/invoice_line_items/${id}`));
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
    sows: {
        list: async (vendor_id = -1, skip = 0, limit = 10, sortBy = '') => {
            return await RESTHelper.get(getUrl(`/sows?vendor_id=${vendor_id}&skip=${skip}&limit=${limit}&sortby=${sortBy}`));
        },
        get: async (id) => {
            return await RESTHelper.get(getUrl(`/sows/${id}`));
        },
        analyze: async(file, data) => {
            if (!file) return;
        
            console.info('Analyzing SOW:', file);
        
            const formData = new FormData();
            formData.append('file', file);
            for (var key in data) {
                formData.append(key, data[key]);
            }

            try {
                const response = await fetch(getUrl(`/sows/`), {
                    method: 'POST',
                    body: formData,
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const result = await response.json();
                return result;
            } catch (error) {
                console.error('Error analyzing SOW:', error);
                throw error;
            }
        },
        validate: async (id) => {
            console.info('Validating SOW:', id);
        
            try {
                const response = await fetch(getUrl(`/valiation/sow/${id}`), {
                    method: 'POST',
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return;
            } catch (error) {
                console.error('Error validating SOW:', error);
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
        }
    }
};