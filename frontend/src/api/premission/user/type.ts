
// // basic response data structure
// export interface ResponseDataBlock {
//     code: number;
//     message: string;
//     ok: boolean;
// }

// account info get from back
export interface AccountInfo {
    id?: number
    createTime?: string
    updateTime?: string
    email?: string
    username: string
    password: string
    roleId?: number // role ID, optional
}

export type AccountList = AccountInfo[];
export interface UserData {
    records: AccountList;
    total: number;
}