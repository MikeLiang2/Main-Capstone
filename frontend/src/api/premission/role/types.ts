// each role has an id, name, and optional description
export interface Role {
  id: number;
  name: string;
  description?: string;
}

// role list structure
export interface RoleList {
  roles: Role[];
}

// role assignment request structure
export interface AssignedRole {
  userId: number;
  roleId: number;
}