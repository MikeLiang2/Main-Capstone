// user management
import request from "@/utils/request";
import type { AccountInfo, UserData } from "./type";


// GET user info
export function getUserList(page: number, limit: number, name?: string) {
  return request<UserData>({
    url: '/users',
    method: 'get',
    params: {
      page,
      limit,
      ...(name ? { name } : {})
    }
  });
}
 
// // GET single user by ID
// export function getUser(userId: number) {
//   return request<AccountInfo>({
//     url: `/users/${userId}`,
//     method: 'get'
//   })
// }

// // POST - add new user
// export function addUser(data: AccountInfo) {
//   return request({
//     url: '/premission/user',
//     method: 'post',
//     data
//   })
// }

// DELETE - delete user by ID
export const deleteUser = (userId: string) => {
  return request({
    url: `/userstmp/${userId}`,
    method: 'delete',
  });
};

// PUT - update user
export function updateUser(userId: string, data: AccountInfo) {
  return request({
    url: `/userstmp/${userId}`,
    method: 'patch',
    data
  });
}

export function updateUserPassword(userId: string, password: string) {
  return request({
    url: `/users/${userId}/password`,
    method: 'patch',
    data: { password }, 
  });
}