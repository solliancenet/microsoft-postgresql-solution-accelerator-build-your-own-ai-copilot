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

const listDocuments = async () => {
    try {
        const response = await fetch(`${apiConfig.APIUrl}/v1/documents`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching documents:', error);
        throw error;
    }
};

const getDocumentDownloadUrl = (blobName) => {
    return `${apiConfig.APIUrl}/v1/documents/${blobName}`;
}

const uploadDocument = async (file) => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${apiConfig.APIUrl}/v1/documents`, {
            method: 'POST',
            headers: {
                'Content-Type': 'multipart/form-data',
            },
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


module.exports = {
    getStatus,
    documents: {
        list: listDocuments,
        getUrl: getDocumentDownloadUrl,
        upload: uploadDocument,
    }
};