import request from '@/utils/request';
import type { AssignedRole, RoleList } from '@/api/premission/role/types';

// get all roles
export function getAllRoles() {
  return request<RoleList>({
    url: '/roles',
    method: 'get',
  });
}

export const assignRole = (data: AssignedRole) => {
  return request({
    url: '/roles/assign',
    method: 'post',
    data
  });
};
