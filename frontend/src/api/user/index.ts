import request from "@/utils/request";
// API FUNCTIONALITY HERE QwQ
// note 统一管理请求地址

// Update the path below to the correct relative path if needed, e.g. '../utils/request'
import type { loginData, user } from '@/api/user/type'
import { GET_TOKEN } from "@/utils/token";


// login
export const Mylogin = (user: loginData) => {
  return request<user>({
    url: '/login',
    method: 'post',
    data: user
  });
};

// get user info
export const getUserInfo = () => {
  console.log('getUserInfo called',GET_TOKEN());
  return request<user>({
    url: '/user/info',
    method: 'get',
    headers: {
      Authorization: `Bearer ${GET_TOKEN()}`
    }
  });
};

// // check token
// export const checkToken = (username: string) => {
//   return request<{ valid: boolean }>({
//     url: '/user/token/validate',
//     method: 'get',
//     params: { username }  // if username is needed as query param
//   });
// };