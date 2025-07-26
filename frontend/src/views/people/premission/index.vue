<template>
    <!-- Search Module -->
    <el-card>
        <el-form class="search-form" :inline="true">
            <el-form-item label="User Name:" prop="name">
                <el-input placeholder="Enter name" v-model="searchinfo" />
            </el-form-item>

            <el-form-item class="form-buttons">
                <el-button type="primary" icon="Search" :disabled="!searchinfo" @click="handleSearch">Search</el-button>
                <el-button type="danger" icon="CircleClose" @click="handleReset">Reset</el-button>
            </el-form-item>
        </el-form>

    </el-card>

    <!-- User Table and Actions -->
    <el-card style="margin-top: 20px;">
        <div class="action-buttons">
            <el-button type="primary" icon="Plus" @click="addUser">Add User</el-button>
            <el-button type="danger" icon="Delete">Delete User</el-button>
        </div>

        <!-- users -->
        <el-table :fit="true" style="width: 100%; margin: 15px 0;" :data="userList">
            <el-table-column type="selection" width="30" />
            <el-table-column align="center" prop="id" label="#" show-overflow-tooltip sortable/>
            <el-table-column align="center" prop="username" label="Name" show-overflow-tooltip sortable/>
            <el-table-column align="center" prop="email" label="Email" show-overflow-tooltip sortable/>
            <el-table-column align="center" label="Role" show-overflow-tooltip sortable>
                <template #="{ row }">
                    {{ roleMap[row.roleId] || 'Unknown' }}
                </template>
            </el-table-column>
            <el-table-column align="center" prop="createTime" label="Create Date" show-overflow-tooltip sortable/>
            <el-table-column align="center" prop="updateTime" label="Update Date" show-overflow-tooltip sortable/>
            <el-table-column align="center" width="300" prop="Operations" label="Operations">
                <template #="{ row }">
                    <div style="display: flex; flex-wrap: wrap; gap: 4px; justify-content: center;">
                        <el-button type="primary" size="small" @click="() => update(row)">Edit</el-button>
                        <el-button type="primary" size="small" @click="() => setPass(row)">
                            <el-icon>
                                <Lock />
                            </el-icon>
                            <span style="margin-left: 4px;">Pass</span>
                        </el-button>
                        <!-- <el-button type="primary" size="small" @click="() => setRole(row)">Role</el-button> -->
                        <el-button type="danger" size="small" @click="() => deleteUser(row)">Delete</el-button>
                    </div>
                </template>
            </el-table-column>

        </el-table>

        <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :disabled="false"
            :background="true" layout="prev, pager, next, jumper" :total="total"
            @current-change="handleCurrentChange" />
    </el-card>

    <el-drawer v-model="showDrawer" :title="isEditMode ? 'Edit User' : 'Add User'">
        <template #default>
            <!-- <span>Hi, there!</span> -->
            <el-form ref="userFormRef" :model="userForm" :rules="formRules" label-width="80px" class="user-form"
                label-position="top">
                <el-form-item label="User Name" prop="username" :rules="formRules.username">
                    <el-input placeholder="Enter user name" v-model="userForm.username" />
                </el-form-item>
                <el-form-item label="Email" prop="email" :rules="formRules.email">
                    <el-input placeholder="Enter email" v-model="userForm.email" />
                </el-form-item>
                <el-form-item v-if="!isEditMode" label="Password" prop="password" :rules="formRules.password">
                    <el-input type="password" placeholder="Enter password" v-model="userForm.password" />
                </el-form-item>
                <el-form-item v-if="isEditMode" label="Role" :rules="formRules.role">
                    <el-select v-model="userForm.roleId" placeholder="Select role">
                        <el-option v-for="role in roleList" :key="role.id" :label="role.name" :value="role.id" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Avatar" prop="avatar">
                    <el-input placeholder="Enter avatar" v-model="userForm.avatar" />
                </el-form-item>

                <!-- 表单项 -->
                <el-form-item style="text-align: right;">
                    <el-button type="primary" @click="submitUser">Confirm</el-button>
                    <el-button @click="showDrawer = false">Cancel</el-button>
                </el-form-item>
            </el-form>

        </template>

        <!-- <template #footer>
            <el-button type="primary" @click="submitUser">Confirm</el-button>
            <el-button @click="showDrawer = false">Cancel</el-button>
        </template> -->
    </el-drawer>
    <!-- interface user {
    id: number
    avatar: string
    username: string
    password: string
    email: string
    roles: string[]
    buttonPermissions: string[]
    routePermissions: string[]
    token: string
} -->

    <!-- For role allocation -->
    <el-drawer v-model="drawerPass" size="400px" :with-header="false">
        <div class="drawer-pass-container">
            <div class="drawer-pass-header">
                <h3>Change Password</h3>
            </div>

            <el-form ref="userFormRef" :model="userForm" :rules="formRules" label-width="80px" class="user-form">
                <el-form-item label="User Name">
                    <div class="plain-text">{{ userForm.username }}</div>
                </el-form-item>

                <el-form-item label="Password" prop="password" :rules="formRules.password">
                    <el-input type="password" placeholder="Enter password" v-model="userForm.password" />
                </el-form-item>

            </el-form>

            <div class="drawer-pass-footer">
                <!-- @click="submitRole" -->
                <el-button type="primary" @click="submitPass">Submit</el-button>
                <el-button @click="drawerPass = false">Close</el-button>
            </div>
        </div>
    </el-drawer>


</template>

<script setup lang="ts">

//default page
import { ref, onMounted, reactive, computed } from 'vue';
import type { AccountInfo, UserData, AccountList } from '@/api/premission/user/type';
import { getUserList, updateUser, updateUserPassword } from '@/api/premission/user/index';
import type { AxiosResponse } from 'axios';
import { ElMessageBox, ElMessage } from 'element-plus'
import { deleteUser as deleteUserApi } from '@/api/premission/user/index';
import type { FormInstance } from 'element-plus';
import { showSuccessAndReload } from '@/views/people/premission/autoreloder/autorelod';
import type { Role } from '@/api/premission/role/types';
import { getAllRoles } from '@/api/premission/role';
import { registerApi } from '@/api/user';


//search info
const searchinfo = ref('');

let isEditMode = ref(false);

// import type { DrawerProps } from 'element-plus'
let currentPage = ref(1);

// number data on each page
let pageSize = ref(10);

// Total number of items
let total = ref(0);

let showDrawer = ref(false);

// drawer for password change
let drawerPass = ref(false);

let userList = ref<AccountList>([]);

let currentEditUserId = ref<string | null>(null);
//For User add and data collection 
let userForm = reactive<AccountInfo>({
    username: '',
    email: '',
    password: '',
    roleId: 1,

    avatar: '',
    createTime: '',
    updateTime: '',
});

const roleList = ref<Role[]>([])
const roleMap = computed(() => {
    const map: Record<number, string> = {}
    roleList.value.forEach(role => {
        map[role.id] = role.name
    })
    return map
})

// Form reference for validation
const userFormRef = ref<FormInstance>();
// Form validation rules
const formRules = {
    username: [
        { required: true, message: 'Username is required', trigger: 'blur' }
    ],
    email: [
        { required: true, message: 'Email is required', trigger: 'blur' },
        {
            validator: (rule: any, value: string, callback: any) => {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (value && !emailRegex.test(value)) {
                    callback(new Error('Email format is invalid'));
                } else {
                    callback();
                }
            },
            trigger: ['blur', 'change']
        }
    ],
    password: [
        { required: true, message: 'Password is required', trigger: 'blur' }
    ],
    role: [
        { required: true, message: 'Role is required', trigger: 'blur' }
    ],
};

onMounted(() => {
    receiveUserList();
    fetchRoles();
});

// Fetch user list
const receiveUserList = async (page = 1) => {
    currentPage.value = page;
    try {
        const res: AxiosResponse<UserData> = await getUserList(currentPage.value, pageSize.value, searchinfo.value);

        // console.log(res);
        if (res.status === 200) {
            userList.value = res.data.records;
            total.value = res.data.total;
            // console.log("User list fetched successfully:", userList.value);
            // console.log("Total users:", total.value);
        } else {
            console.error("Failed to fetch user list");
        }
    } catch (error) {
        console.error('Error fetching user list:', error);
    }
}


const fetchRoles = async () => {
    const res = await getAllRoles()
    if (res.status === 200) {
        roleList.value = res.data;
    }
}

/////////////////////////////////////Password Change
const setPass = (row: AccountInfo) => {
    resetForm();
    currentEditUserId.value = row.id!;
    drawerPass.value = true;

    userForm.username = row.username;
};

// const onRoleChange = (value: string) => {
//     userRole.value = value;
// };

async function submitPass() {
    if (!userFormRef.value) {
        console.error('Form ref is not set');
        return;
    }

    userFormRef.value.validate(async (valid: boolean) => {
        if (!valid) {
            ElMessageBox.alert('Please fix form errors before submitting.', 'Validation Failed');
            return;
        }
        try {
            // Your API call here
            const res = await updateUserPassword(currentEditUserId.value, userForm.password);
            if (res.status === 200) {
                // handle success
            } else {
                ElMessageBox.alert('Failed to update user password', 'Error');
            }
            drawerPass.value = false;
            // reload list, reset form etc.
        } catch (error: any) {
            ElMessageBox.alert(error.response?.data?.detail || 'Unexpected error occurred', 'Error');
        }
    });
}

///////////////////////////////
const resetForm = () => {
    userForm.username = '';
    userForm.email = '';
    userForm.password = '';
    userForm.roleId = 1;

    userForm.avatar = '';

    isEditMode.value = false;
    currentEditUserId.value = null;
};

// Current page number change (handleCurrentChange).
const handleCurrentChange = (val: number) => {
    // console.log(`current page: ${val}`)
    currentPage.value = val;
    receiveUserList(currentPage.value);
}

const addUser = () => {
    resetForm();
    showDrawer.value = true;
    // console.log("Add user button clicked");
}

const update = (row: AccountInfo) => {
    resetForm();
    currentEditUserId.value = row.id!;
    isEditMode.value = true;
    showDrawer.value = true;

    // 预填表单
    userForm.username = row.username;
    userForm.email = row.email;
    // userForm.password = row.password;
    userForm.roleId = row.roleId;

    userForm.avatar = row.avatar ?? "";
};

// delete user
const currentUserId = localStorage.getItem('userId');
const deleteUser = (row: AccountInfo) => {
    if (row.id === currentUserId) {
        ElMessage.warning('You cannot delete your own account!');
        return;
    }

    ElMessageBox.confirm(`Are you sure you want to delete user "${row.username}"?`, 'Warning', {
        confirmButtonText: 'Yes',
        cancelButtonText: 'No',
        type: 'warning',
    })
        .then(async () => {
            try {
                await deleteUserApi(row.id!);
                ElMessage.success('User deleted successfully!');
                receiveUserList();
            } catch (error: any) {
                console.error('Delete error:', error);
                ElMessage.error(error.response?.data?.detail || 'Failed to delete user');
            }
        })
        .catch(() => {
        });
};



// submit user form
const submitUser = async () => {
    if (!userFormRef.value) return;

    userFormRef.value.validate(async (valid) => {
        if (!valid) {
            ElMessageBox.alert('Please fix form errors before submitting.', 'Validation Failed');
            return;
        }

        try {
            if (isEditMode.value && currentEditUserId.value !== null) {
                // update existing user
                const res = await updateUser(currentEditUserId.value, userForm);
                if (res.status === 200) {
                    showSuccessAndReload('User updated successfully!');
                } else {
                    ElMessageBox.alert('Failed to update user', 'Error');
                }
            } else {
                // add new user
                // console.log("Registering new user:", userForm);
                const registerRes = await registerApi({
                    email: userForm.email,
                    password: userForm.password || '',
                    username: userForm.username,
                    avatar: userForm.avatar || '',
                });

                if (registerRes.status === 201 || registerRes.status === 200) {
                    const newUserId = registerRes.data.id;
                    if (!newUserId) {
                        throw new Error('User registration did not return a valid user ID.');
                    }
                } else {
                    ElMessageBox.alert('User registration failed', 'Error');
                }
            }

            showDrawer.value = false;
            receiveUserList();
            resetForm();
        } catch (error: any) {
            console.error("Submit error:", error);
            ElMessageBox.alert(error.response?.data?.detail || 'Unexpected error occurred', 'Error');
        }
    });
};


////////////////// SEARCHING MODULE
// searching module
const handleSearch = () => {
    receiveUserList(1);
};

// reset search
const handleReset = () => {
    searchinfo.value = '';
    receiveUserList(1);
};

</script>

<style scoped lang="scss">
@use '@/styles/global_var.scss' as *;

.search-form {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

// seach buttons
.form-buttons {
    display: flex;
    gap: 10px;
}

.action-buttons {
    display: flex;
    gap: 10px;
}

.el-button {
    background-color: #7559b6;
    color: white;
    border: 1px solid #9b59b6;
    transition: all 0.3s ease;

    &:hover,
    &:focus {
        background-color: #9e98e6;
        border-color: #9e98e6;
        color: white;
    }

    &.is-disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
}

.user-form {
    padding: 10px;

    .el-form-item {
        margin-bottom: 10px;

        .el-input,
        .el-select {
            width: 100%;
        }
    }
}


// drawer styles
.drawer-pass-container {
    padding: 24px;
}

.drawer-pass-header {
    margin-bottom: 20px;

    h3 {
        margin: 0;
        font-size: 18px;
        font-weight: 600;
    }
}

.drawer-pass-form {
    .el-form-item {
        margin-bottom: 20px;
    }

    .plain-text {
        line-height: 32px;
        font-size: 14px;
        padding-left: 4px;
    }
}
</style>
