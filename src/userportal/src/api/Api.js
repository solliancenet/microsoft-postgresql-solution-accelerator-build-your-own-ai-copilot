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
            const chat_history = [];
            if (history && history.length > 0){
                for(let i in history) {
                    chat_history.push(history[i].text);
                }
            }

            return await RESTHelper.post(getUrl(`/completions/chat`), {
                message,
                chat_history,
            });
        },
    },
    documents: {
        list: async () => {
            return await RESTHelper.get(getUrl(`/documents/documents`));
        },
        getUrl: (blobName) => {
            return getUrl(`/documents/documents/${blobName}`);
        },
        upload: async (file) => {
            if (!file) return;
        
            console.info('Uploading document:', file);
        
            const formData = new FormData();
            formData.append('file', file);
        
            try {
                const response = await fetch(getUrl(`/documents/documents`), {
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
                const response = await fetch(getUrl(`/documents/documents/${blobName}`), {
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
        list: async (skip = 0, limit = 10, sortBy = '', search = '') => {
            return await RESTHelper.get(getUrl(`/invoices?skip=${skip}&limit=${limit}&sortby=${sortBy}&search=${search}`));
        },
        get: async (id) => {
            return await RESTHelper.get(getUrl(`/invoices/${id}`));
        },
        create: async (file, invoice_number, amount, invoice_date, payment_status) => {
            if (!file) return;
        
            console.info('Creating invoice:', file);
        
            const formData = new FormData();
            formData.append('file', file);
            formData.append('invoice_number', invoice_number);
            formData.append('amount', amount);
            formData.append('invoice_date', invoice_date);
            formData.append('payment_status', payment_status);
        
            try {
                const response = await fetch(getUrl(`/invoices`), {
                    method: 'POST',
                    body: formData,
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                return data;
            } catch (error) {
                console.error('Error creating invoice:', error);
                throw error;
            }
        },
        update: async (id, invoice_number, amount, invoice_date, payment_status) => {
            return await RESTHelper.update(getUrl(`/invoices/${id}`), {
                invoice_number: invoice_number,
                amount: amount,
                invoice_date: invoice_date,
                payment_status: payment_status,
            });
        },
        delete: async (id) => {
            return await RESTHelper.delete(getUrl(`/invoices/${id}`));
        }
    },
    msas: {
        list: async (skip = 0, limit = 10, sortBy = '', search = '') => {
            return await RESTHelper.get(getUrl(`/msas?skip=${skip}&limit=${limit}&sortby=${sortBy}&search=${search}`));
        },
        get: async (msaId) => {
            return await RESTHelper.get(getUrl(`/msas/${msaId}`));
        },
        create: async (file, msa_title, start_date, end_date) => {
            if (!file) return;

            console.info('Creating MSA:', file);
        
            const formData = new FormData();
            formData.append('file', file);
            formData.append('msa_title', msa_title);
            formData.append('start_date', start_date);
            formData.append('end_date', end_date);
        
            try {
                const response = await fetch(getUrl(`/msas`), {
                    method: 'POST',
                    body: formData,
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                return data;
            } catch (error) {
                console.error('Error creating MSA:', error);
                throw error;
            }
        },
        update: async(id, msa_title, start_date, end_date) => {
            return await RESTHelper.update(getUrl(`/msas/${id}`), {
                msa_title: msa_title,
                start_date: start_date,
                end_date: end_date,
            });
        },
        delete: async (id) => {
            return await RESTHelper.delete(getUrl(`/msas/${id}`));
        }
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
            formData.append('title', sowTitle);
            formData.append('start_date', startDate);
            formData.append('end_date', endDate);
            formData.append('budget', budget);
        
            try {
                const response = await fetch(getUrl(`/sows`), {
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
        update: async (sowId, title, startDate, endDate, budget) => {
            return await RESTHelper.update(getUrl(`/sows/${sowId}`), {
                title: title,
                start_date: startDate,
                end_date: endDate,
                budget: budget,
            });
        },
        delete: async (sowId) => {
            return await RESTHelper.delete(getUrl(`/sows/${sowId}`));
        }
    },
    vendors: {
        list: async (skip = 0, limit = 10, sortBy = '', search = '') => {
            return await RESTHelper.get(getUrl(`/vendors?skip=${skip}&limit=${limit}&sortby=${sortBy}&search=${search}`));
        },
        get: async (vendorId) => {
            return await RESTHelper.get(getUrl(`/vendors/${vendorId}`));
        },
        create: async (name, address, contact_name, contact_email, contact_phone, type) => {
            console.info('Creating vendor');

            const formData = new FormData();
            formData.append('name', name);
            formData.append('address', address);
            formData.append('contact_name', contact_name);
            formData.append('contact_email', contact_email);
            formData.append('contact_phone', contact_phone);
            formData.append('contact_type', type);

            try {
                const response = await fetch(getUrl(`/vendors`), {
                    method: 'POST',
                    body: formData,
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                return data;
            } catch (error) {
                console.error('Error creating vendor:', error);
                throw error;
            }
        },
        update: async (id, name, address, contact_name, contact_email, contact_phone, type) => {
            return await RESTHelper.update(getUrl(`/vendors/${id}`), {
                name: name,
                address: address,
                contact_name: contact_name,
                contact_email: contact_email,
                contact_phone: contact_phone,
                type: type,
            });
        }, 
        delete: async (vendorId) => {
            return await RESTHelper.delete(getUrl(`/vendors/${vendorId}`));
        }
    }
};