import request from '@/utils/request';
import type { Role, RoleCreate, RoleList } from '@/api/premission/role/types';

// get all roles
export function getAllRoles() {
  return request<Role[]>({
    url: '/roles',
    method: 'get',
  });
}

export function addRoleApi(data: Partial<Role>) {
  return request({
    url: '/role',
    method: 'post',
    data,
  });
}


export function getRoleList(page: number, limit: number, name?: string) {
  return request({
    url: '/role',
    method: 'get',
    params: {
      page,
      limit,
      ...(name ? { name } : {})
    }
  });
}

// PUT - update role
export function updateRoleApi(id: number, data: RoleCreate) {
  return request({
    url: `/role/${id}`,
    method: 'put',
    data
  });
}

// DELETE - delete role
export function deleteRoleApi(id: number) {
  return request({
    url: `/role/${id}`,
    method: 'delete'
  });
}