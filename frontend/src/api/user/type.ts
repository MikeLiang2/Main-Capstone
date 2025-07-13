export interface loginData {
    username: string
    password: string
}

export interface tokenData {
    token?: string
    message?: string
} 

// export interface loginResponseData {
//     code: number
//     data: tokenData
// }

export interface user {
    id: number
    avatar: string
    username: string
    password: string
    email: string
    roles: string[]
    buttonPermissions: string[]
    routePermissions: string[]
    token: string
}

// export interface userResponseData {
//     code: number
//     data: user
// }

