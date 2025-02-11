import axios from 'axios';

// create an instance of axios

const api = axios.create({
    baseURL : 'http://localhost:8000',
});

export default api;
