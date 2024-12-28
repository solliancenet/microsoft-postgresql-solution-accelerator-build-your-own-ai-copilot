const apiConfig = require('./APIConfig'); // Assuming apiConfig is in the same directory

const fetchData = async (url) => {
    try {
        const response = await fetch(`${apiConfig.APIUrl}${url}`);
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
    return await fetchData(`/v1/status`);
};

/* *************** */
/* Documents API */
/* *************** */

const listDocuments = async () => {
    return await fetchData(`/v1/documents`);
};

const getDocumentDownloadUrl = (blobName) => {
    return `${apiConfig.APIUrl}/v1/documents/${blobName}`;
}

const uploadDocument = async (file) => {
    if (!file) return;

    console.info('Uploading document:', file);

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${apiConfig.APIUrl}/v1/documents`, {
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
        const response = await fetch(`${apiConfig.APIUrl}/v1/documents/${blobName}`, {
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
    return await fetchData(`/v1/company?skip=${skip}&limit=${limit}&sortby=${sortBy}&search=${search}`);
};

/* *************** */
/* Vendors API */
/* *************** */

// Function to fetch companies with pagination
const listVendors = async (skip = 0, limit = 10, sortBy = '', search = '') => {
    return await fetchData(`/v1/vendor?skip=${skip}&limit=${limit}&sortby=${sortBy}&search=${search}`);
};

/* *************** */
/* SOW API */
/* *************** */

const listSOWs = async (skip = 0, limit = 10, sortBy = '', search = '') => {
    return await fetchData(`/v1/sows?skip=${skip}&limit=${limit}&sortby=${sortBy}&search=${search}`);
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
    }
};