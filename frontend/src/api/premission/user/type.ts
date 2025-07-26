
// // basic response data structure
// export interface ResponseDataBlock {
//     code: number;
//     message: string;
//     ok: boolean;
// }

// account info get from back
export interface AccountInfo {
    id?: string
    username: string
    email: string
    password?: string
    roleId: number 
    
    avatar?: string
    createTime?: string
    updateTime?: string
}

export type AccountList = AccountInfo[];
export interface UserData {
    records: AccountList;
    total: number;
}