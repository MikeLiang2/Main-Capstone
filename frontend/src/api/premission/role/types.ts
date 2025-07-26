// each role has an id, name, and optional description
export interface Role {
  id: number;
  name: string;
  description?: string;
}

// role list structure
export interface RoleList {
  roles: Role[];
  total: number;
}

// // role assignment request structure
// export interface AssignedRole {
//   userId: number;
//   roleId: number;
// }

export interface RoleCreate {
  name: string;
  description?: string;

  addPeople: boolean;
  deletePeople: boolean;
  editPeople: boolean;
  editPassword: boolean;
  addRole: boolean;
  editRole: boolean;
  shareChecklist: boolean;
  shareAnyChecklist: boolean;
  editChecklist: boolean;
  editAnyChecklist: boolean;
  deleteChecklist: boolean;
  deleteAnyChecklist: boolean;
  addChecklist: boolean;
}