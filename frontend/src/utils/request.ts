//axios
import axios from 'axios';
import useUserStore from '@/store/modules/user';

//access address
// 好像也可以配置多个地址，暂时用不到
let service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL, // Base URL for the API
  //  baseURL: 'http://127.0.0.1:8000', // Base URL for the API, change as needed
  timeout: 5000, // Request timeout in milliseconds
});


//request interceptor
// what to do before sending a request
service.interceptors.request.use(
  (config) => {
    const userStore = useUserStore();

    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);


//response interceptor
// what to do after receiving a response
// success and failure
service.interceptors.response.use(
  (response) => {
    // Handle the response data success
    return response;
  },
  (error) => {
    // Handle the error response failure
    // 404, 500 add later
    return Promise.reject(error);
  }
);

// Export the service instance for use in other parts of the application
export default service;
