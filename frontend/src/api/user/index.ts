import request from "@/utils/request";
// API FUNCTIONALITY HERE QwQ
// note 统一管理请求地址

// Update the path below to the correct relative path if needed, e.g. '../utils/request'
import type { loginData, user } from '@/api/user/type'
import { GET_TOKEN } from "@/utils/token";
import axios from 'axios';
import type { AccountInfo } from "../premission/user/type";

// login
export const Mylogin = (user: loginData) => {
  const params = new URLSearchParams();
  params.append('username', user.username);
  params.append('password', user.password);

  return request({
    url: '/auth/jwt/login',
    method: 'post',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    data: params,
  });
};

// get user info
export const getUserInfo = () => {
  // console.log('getUserInfo called', GET_TOKEN());
  return request<user>({
    url: '/users/me',
    method: 'get',
    headers: {
      Authorization: `Bearer ${GET_TOKEN()}`
    }
  });
};



export const registerApi = (payload: {
  email: string;
  password: string;
  username: string;
  avatar?: string;
}) => {
  return request<AccountInfo>({
    url: '/auth/register',
    method: 'post',
    data: payload
  });
};