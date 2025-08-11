<template>
    <!-- Search Module -->
    <el-card>
        <el-form class="search-form" :inline="true">
            <el-form-item label="Role Name:">
                <el-input placeholder="Enter and search role" v-model="searchinfo" />
            </el-form-item>

            <el-form-item class="form-buttons">
                <el-button type="primary" icon="Search" :disabled="!searchinfo" @click="handleSearch">Search</el-button>
                <el-button type="danger" icon="CircleClose" @click="handleReset">Reset</el-button> </el-form-item>
        </el-form>
    </el-card>

    <!-- Add Role Drawer -->
    <el-drawer v-model="drawerVisible" title="Add Role" direction="rtl" size="30%">
        <el-form :model="addForm" :rules="formRules" ref="formRef" label-width="120px" class="user-form">


            <el-form-item label="Role Name" prop="name" :rules="formRules.name">
                <el-input v-model="addForm.name" placeholder="Enter role name" />
            </el-form-item>

            <el-form-item label="Description">
                <el-input v-model="addForm.description" placeholder="Optional description" />
            </el-form-item>

            <!-- People Permissions -->
            <el-divider content-position="left">People Permissions</el-divider>
            <el-form-item>
                <el-checkbox-group v-model="selectedPermissions">
                    <el-checkbox label="addPeople">Add People</el-checkbox>
                    <el-checkbox label="deletePeople">Delete People</el-checkbox>
                    <el-checkbox label="editPeople">Edit People</el-checkbox>
                    <el-checkbox label="editPassword">Edit Password</el-checkbox>
                </el-checkbox-group>
            </el-form-item>

            <!-- Role Permissions -->
            <el-divider content-position="left">Role Permissions</el-divider>
            <el-form-item>
                <el-checkbox-group v-model="selectedPermissions">
                    <el-checkbox label="addRole">Add Role</el-checkbox>
                    <el-checkbox label="editRole">Edit Role</el-checkbox>
                </el-checkbox-group>
            </el-form-item>

            <!-- Checklist Permissions -->
            <el-divider content-position="left">Checklist Permissions</el-divider>
            <el-form-item>
                <el-checkbox-group v-model="selectedPermissions">
                    <el-checkbox label="shareChecklist">Share</el-checkbox>
                    <el-checkbox label="shareAnyChecklist">Share Any</el-checkbox>
                    <el-checkbox label="editChecklist">Edit</el-checkbox>
                    <el-checkbox label="editAnyChecklist">Edit Any</el-checkbox>
                    <el-checkbox label="deleteChecklist">Delete</el-checkbox>
                    <el-checkbox label="deleteAnyChecklist">Delete Any</el-checkbox>
                    <el-checkbox label="addChecklist">Add</el-checkbox>
                </el-checkbox-group>
            </el-form-item>

            <!-- Submit/Cancel -->
            <el-form-item style="margin-top: 20px; justify-content: center;">
                <el-button type="primary" @click="submitAddRole">Submit</el-button>
                <el-button @click="drawerVisible = false">Cancel</el-button>
            </el-form-item>

        </el-form>
    </el-drawer>



    <!-- User Table and Actions -->
    <el-card style="margin-top: 20px;">
        <div class="action-buttons">
            <el-button type="primary" icon="Plus" @click="addRole">Add Role</el-button>
            <el-button type="danger" icon="Delete">Delete Role</el-button>
        </div>
        <!-- 
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
} -->

        <!-- users -->
        <el-table :fit="true" style="width: 100%; margin: 15px 0;" :data="roleList">
            <el-table-column type="selection" width="30" />
            <el-table-column align="center" prop="id" label="#" show-overflow-tooltip sortable />
            <el-table-column align="center" prop="name" label="Role Name" show-overflow-tooltip sortable />
            <el-table-column align="center" width="255" prop="Operations" label="Operations" sortable>
                <template #="{ row }">
                    <div style="display: flex; flex-wrap: wrap; gap: 4px; justify-content: center;">
                        <el-button type="primary" size="small" @click="() => update(row)">Edit</el-button>
                        <!-- <el-button type="primary" size="small" @click="() => setPermission(row)"></el-button> -->
                        <!-- <el-icon>
                                <Lock />
                            </el-icon> -->
                        <!-- <span style="margin-left: 4px;">Pass</span> -->

                        <!-- <el-button type="primary" size="small" @click="() => setRole(row)">Role</el-button> -->
                        <el-button type="danger" size="small" @click="() => deleteRole(row)">Delete</el-button>
                    </div>
                </template>
            </el-table-column>

        </el-table>

        <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :disabled="false"
            :background="true" layout="prev, pager, next, jumper" :total="total"
            @current-change="handleCurrentChange" />
    </el-card>
</template>

<script setup lang="ts">

import { reactive, ref, onMounted } from 'vue';
import { addRoleApi, deleteRoleApi, getRoleList, updateRoleApi } from '@/api/premission/role';
import type { Role, RoleCreate } from '@/api/premission/role/types';
import { ElMessage, ElMessageBox } from 'element-plus';

// paging
let currentPage = ref<number>(1);
let pageSize = ref<number>(10);
const total = ref(0);
const searchinfo = ref('');
const roleList = ref<Role[]>([]);
const drawerVisible = ref(false);

// role result control
const receiveRoleList = async (page = 1) => {
    try {
        const res = await getRoleList(page, pageSize.value, searchinfo.value);
        if (res.status === 200) {
            roleList.value = res.data.roles;
            total.value = res.data.total;
        }
    } catch (error) {
        console.error('Error loading role list:', error);
    }
};

// form rules
const formRules = {
    name: [
        { required: true, message: 'Role name is required', trigger: 'blur' }
    ],
}

// add role
const addForm = reactive({
    name: '',
    description: ''
});
const selectedPermissions = ref<string[]>([]);

// Drawer
const addRole = () => {
    addForm.name = '';
    addForm.description = '';
    selectedPermissions.value = [];
    drawerVisible.value = true;
};


const deleteRole = async (row: Role) => {
    try {
        await ElMessageBox.confirm(
            `Are you sure you want to delete the role "${row.name}"?`,
            'Confirm Deletion',
            {
                confirmButtonText: 'Confirm',
                cancelButtonText: 'Cancel',
                type: 'warning',
            }
        );

        await deleteRoleApi(row.id);
        ElMessage.success('Role deleted');
        receiveRoleList(currentPage.value);
    } catch (err: any) {
        if (err === 'cancel') {
            // 用户点击了 Cancel，不做任何提示
            return;
        }

        console.error('Submit role failed', err);

        const detail = err?.response?.data?.detail;

        if (typeof detail === 'string') {
            ElMessage.error(detail);
        } else if (Array.isArray(detail)) {
            const messages = detail.map((d: any) => d.msg).join('; ');
            ElMessage.error(messages);
        } else {
            ElMessage.error('Failed to submit role');
        }
    }
};

const isEditMode = ref(false);
const currentEditRoleId = ref<number | null>(null);

const update = (row: Role) => {
    isEditMode.value = true;
    drawerVisible.value = true;
    currentEditRoleId.value = row.id;
    addForm.name = row.name;
    addForm.description = row.description || '';
    selectedPermissions.value = allPermissions.filter((perm) => (row as any)[perm]);
};

const submitAddRole = async () => {
    if (!addForm.name) {
        ElMessage.error('Role name is required');
        return;
    }

    const payload: RoleCreate = {
        name: addForm.name,
        description: addForm.description,
        addPeople: selectedPermissions.value.includes('addPeople'),
        deletePeople: selectedPermissions.value.includes('deletePeople'),
        editPeople: selectedPermissions.value.includes('editPeople'),
        editPassword: selectedPermissions.value.includes('editPassword'),
        addRole: selectedPermissions.value.includes('addRole'),
        editRole: selectedPermissions.value.includes('editRole'),
        shareChecklist: selectedPermissions.value.includes('shareChecklist'),
        shareAnyChecklist: selectedPermissions.value.includes('shareAnyChecklist'),
        editChecklist: selectedPermissions.value.includes('editChecklist'),
        editAnyChecklist: selectedPermissions.value.includes('editAnyChecklist'),
        deleteChecklist: selectedPermissions.value.includes('deleteChecklist'),
        deleteAnyChecklist: selectedPermissions.value.includes('deleteAnyChecklist'),
        addChecklist: selectedPermissions.value.includes('addChecklist'),
    };
    try {
        if (isEditMode.value && currentEditRoleId.value !== null) {
            const res = await updateRoleApi(currentEditRoleId.value, payload);
            if (res.status === 200) {
                ElMessage.success('Role updated successfully');
            }
        } else {
            const res = await addRoleApi(payload);
            if (res.status === 200 || res.status === 201) {
                ElMessage.success('Role added successfully');
            }
        }

        drawerVisible.value = false;
        isEditMode.value = false;
        currentEditRoleId.value = null;
        receiveRoleList(1);
    } catch (err: any) {
        console.error('Submit role failed', err);
        // 尝试从后端响应中提取详细错误信息
        const detail = err?.response?.data?.detail;

        if (typeof detail === 'string') {
            ElMessage.error(detail);
        } else if (Array.isArray(detail)) {
            // FastAPI validation error 格式为 array
            const messages = detail.map((d: any) => d.msg).join('; ');
            ElMessage.error(messages);
        } else {
            ElMessage.error('Failed to submit role');
        }
    }
};

const allPermissions = [
    'addPeople', 'deletePeople', 'editPeople', 'editPassword',
    'addRole', 'editRole',
    'shareChecklist', 'shareAnyChecklist',
    'editChecklist', 'editAnyChecklist',
    'deleteChecklist', 'deleteAnyChecklist',
    'addChecklist'
];

///////
// search
const handleSearch = () => {
    receiveRoleList(1);
};

// reset search
const handleReset = () => {
    searchinfo.value = '';
    receiveRoleList(1);
};

// page control
const handleCurrentChange = (val: number) => {
    currentPage.value = val;
    receiveRoleList(currentPage.value);
};

onMounted(() => {
    receiveRoleList(1);
});
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

.el-divider {
    margin-top: 20px;
    margin-bottom: 10px;
}

.el-form-item {
    .el-checkbox-group {
        display: flex;
        flex-wrap: wrap;
        gap: 10px 20px;
    }
}
</style>