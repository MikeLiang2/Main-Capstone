// user management
import request from "@/utils/request";
import type { AccountInfo, UserData } from "./type";


// GET user info
// return { code, message, ok, data: { records: [], total } }）
export function getUserList(page: number, limit: number) {
  return request<UserData>({
    url: `/premission/user/${page}/${limit}`,
    method: 'get'
  })
}

// GET single user by ID
export function getUser(userId: number) {
  return request<AccountInfo>({
    url: `/premission/user/${userId}`,
    method: 'get'
  })
}

// POST - add new user
export function addUser(data: AccountInfo) {
  return request({
    url: '/premission/user',
    method: 'post',
    data
  })
}

// DELETE - delete user by ID
export function deleteUser(userId: number) {
  return request({
    url: `/premission/user/delete/${userId}`,
    method: 'delete'
  })
}

// PUT - update user
export function updateUser(userId: number, data: AccountInfo) {
  return request({
    url: `/premission/user/update/${userId}`,
    method: 'put',
    data
  });
}