import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://127.0.0.1:8000/api'; // Replace with your actual backend API URL

export const postBlogUrl = async (url: string) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/extract`, { url });
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            throw new Error('Axios error: ' + error.message);
        }
        throw new Error('Unknown error occurred');
    }

};

export const checkStatus = async (jobId: string) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/status/${jobId}`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            throw new Error('Axios error: ' + error.message);
        }
        throw new Error('Unknown error occurred');
    }

};

export const fetchResults = async (jobId: string) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/results/${jobId}`);
        return response.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
            throw new Error('Axios error: ' + error.message);
        }
        throw new Error('Unknown error occurred');
    }

};