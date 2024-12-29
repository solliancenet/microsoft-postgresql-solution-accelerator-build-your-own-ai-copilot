const apiConfig = require('./APIConfig'); // Assuming apiConfig is in the same directory

const apiVersion = 'v1';

const fetchData = async (url) => {
    try {
        const response = await fetch(`${apiConfig.APIUrl}/${apiVersion}${url}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
};


/* *************** */
/* Status API */
/* *************** */

const getStatus = async () => {
    return await fetchData(`/status`);
};

/* *************** */
/* Documents API */
/* *************** */

const listDocuments = async () => {
    return await fetchData(`/documents`);
};

const getDocumentDownloadUrl = (blobName) => {
    return `${apiConfig.APIUrl}/${apiVersion}/documents/${blobName}`;
}

const uploadDocument = async (file) => {
    if (!file) return;

    console.info('Uploading document:', file);

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${apiConfig.APIUrl}/${apiVersion}/documents`, {
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
}

const deleteDocument = async (blobName) => {
    try {
        const response = await fetch(`${apiConfig.APIUrl}/${apiVersion}/documents/${blobName}`, {
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
}

/* *************** */
/* Companies API */
/* *************** */

// Function to fetch companies with pagination
const listCompanies = async (skip = 0, limit = 10, sortBy = '', search = '') => {
    return await fetchData(`/company?skip=${skip}&limit=${limit}&sortby=${sortBy}&search=${search}`);
};

/* *************** */
/* Vendors API */
/* *************** */

// Function to fetch companies with pagination
const listVendors = async (skip = 0, limit = 10, sortBy = '', search = '') => {
    return await fetchData(`/vendor?skip=${skip}&limit=${limit}&sortby=${sortBy}&search=${search}`);
};

/* *************** */
/* SOW API */
/* *************** */

const listSOWs = async (skip = 0, limit = 10, sortBy = '', search = '') => {
    return await fetchData(`/sows?skip=${skip}&limit=${limit}&sortby=${sortBy}&search=${search}`);
};

const createSOW = async (file, sowTitle, startDate, endDate, budget) => {
    if (!file) return;

    console.info('Creating SOW:', file);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('sow_title', sowTitle);
    formData.append('start_date', startDate);
    formData.append('end_date', endDate);
    formData.append('budget', budget);

    try {
        const response = await fetch(`${apiConfig.APIUrl}/${apiVersion}/sows/create`, {
            method: 'POST',
            body: formData,
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return;
    } catch (error) {
        console.error('Error creating SOW:', error);
        throw error;
    }
}


/* *************** */
/* Invoice API */
/* *************** */

const listInvoices = async (skip = 0, limit = 10, sortBy = '', search = '') => {
    return await fetchData(`/invoices?skip=${skip}&limit=${limit}&sortby=${sortBy}&search=${search}`);
};




/* *************** */
/* Exported API */
/* *************** */

module.exports = {
    getStatus,
    documents: {
        list: listDocuments,
        getUrl: getDocumentDownloadUrl,
        upload: uploadDocument,
        delete: deleteDocument,
    },
    companies: {
        list: listCompanies,
    },
    vendors: {
        list: listVendors,
    },
    sows: {
        list: listSOWs,
        create: createSOW,
    },
    invoices: {
        list: listInvoices,
    }
};