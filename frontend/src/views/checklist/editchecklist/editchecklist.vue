<template>
  <!-- Checklist Management Page -->
  <div class="checklist-container">

    <!-- Search Module -->
    <el-card>
      <el-form class="search-form" :inline="true">
        <el-form-item label="Checklist Name:">
          <el-input placeholder="Search checklist" v-model="searchinfo" />
        </el-form-item>

        <el-form-item class="form-buttons">
          <el-button type="primary" icon="Search" :disabled="!searchinfo" @click="handleSearch">Search</el-button>
          <el-button type="danger" icon="CircleClose" @click="handleReset">Reset</el-button> </el-form-item>
      </el-form>
    </el-card>

    <div style="height: 20px;"></div>

    <!-- Title and Action Bar -->
    <el-card>
      <div class="card-header">
        <h2>Checklist Management</h2>
        <el-button type="primary" icon="Plus" @click="addChecklist">Add Checklist</el-button>
      </div>

      <!-- Checklist Table -->
      <el-table :data="checklistList" style="width: 100%" :fit="true" @row-click="row => openChecklistDrawer(row.id)">
        <el-table-column prop="id" label="ID" width="80" align="center" sortable />
        <el-table-column prop="name" label="Name" show-overflow-tooltip align="center" sortable />
        <el-table-column prop="category.name" label="Category" show-overflow-tooltip align="center" sortable />
        <el-table-column prop="owner.username" label="Owner" align="center" sortable />
        <el-table-column label="Shared With" align="center">
          <template #default="{ row }">
            <span class="share-link" @click.stop="openEditShareDialog(row)">
              {{row.shared_users.map((s: any) => s.user.username).join(', ') || '-'}}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="Actions" align="center" width="350">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="editChecklist(row.id)">Edit</el-button>
            <el-button type="danger" size="small" @click.stop="deleteChecklist(row.id)">Delete</el-button>
            <el-button type="success" size="small" @click.stop="openShareDialog(row)">Share</el-button>
            <el-button type="warning" size="small" @click.stop="copyChecklistAction(row.id)">Copy</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination style="margin-top: 16px;" v-model:current-page="currentPage" v-model:page-size="pageSize"
        :disabled="false" :background="true" layout="prev, pager, next, jumper" :total="total"
        @current-change="handleCurrentChange" />
    </el-card>


    <!-- Checklist Drawer -->
    <el-drawer v-model="showDrawer" size="600px" title="Checklist Detail" :before-close="() => (showDrawer = false)">
      <!-- Drawer 内容展示 -->
      <template #default>
        <div v-if="selectedChecklist">
          <h3 class="checklist-title">{{ selectedChecklist.name }}</h3>
          <p class="checklist-meta"><strong>Category:</strong> {{ selectedChecklist.category.name }}</p>
          <p class="checklist-meta"><strong>Owner:</strong> {{ selectedChecklist.owner.username }}</p>
          <p class="checklist-meta"><strong>Shared With:</strong>
            {{selectedChecklist.shared_users.map(s => s.user.username).join(', ')}}
          </p>
          <p class="checklist-meta"><strong>Description:</strong> {{ selectedChecklist.description }}</p>

          <!-- Progress -->
          <el-progress :percentage="calculateProgress(selectedChecklist)" status="success" style="margin: 16px 0;" />

          <!-- Stage List -->
          <div v-for="(stage, sIndex) in selectedChecklist.stages" :key="stage.id" class="stage-block">
            <el-divider>{{ stage.name }}</el-divider>

            <div v-for="step in stage.steps" :key="step.id" class="step-block">
              <el-checkbox v-model="step.completed" @change="() => toggleStep(step)">
                {{ step.name }}
                <a v-if="step.resourceUrl" :href="step.resourceUrl" target="_blank"
                  style="margin-left: 8px; font-size: 12px">
                  [Resource]
                </a>
              </el-checkbox>
              <div class="step-description">
                {{ step.description }}
              </div>
            </div>
          </div>
        </div>
      </template>
    </el-drawer>

    <el-dialog v-model="showShareDialog" title="Share Checklist" width="500px">
      <el-form :model="shareForm" :rules="rules" label-position="top" ref="shareFormRef">
        <el-form-item label="User Email" prop="email">
          <el-input v-model="shareForm.email" placeholder="Enter user email to share with" />
        </el-form-item>
        <el-form-item style="margin-top: 10px;">
          <el-checkbox v-model="shareForm.can_edit">Can Edit</el-checkbox>
          <el-checkbox v-model="shareForm.can_share" style="margin-left: 12px">Can Share</el-checkbox>
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showShareDialog = false">Cancel</el-button>
          <el-button type="primary" @click="submitShare">Confirm</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog v-model="showEditShareDialog" title="Edit Shares" width="500px">
      <el-table :data="editShares" style="width: 100%">
        <el-table-column prop="user.username" label="User" />
        <el-table-column label="Can Edit" width="100">
          <template #default="{ row }">
            <el-checkbox v-model="row.can_edit" @change="() => updateSharePermission(row)" />
          </template>
        </el-table-column>
        <el-table-column label="Can Share" width="110">
          <template #default="{ row }">
            <el-checkbox v-model="row.can_share" @change="() => updateSharePermission(row)" />
          </template>
        </el-table-column>
        <el-table-column width="80" label="Delete">
          <template #default="{ row }">
            <el-button type="danger" size="small" @click="deleteShareAction(row)">Delete</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getAllChecklists, shareChecklist, deleteShare } from '@/api/checklist'
import type { ProcessInstance, ChecklistShare } from '@/api/checklist/type'
import { ElMessageBox, ElMessage, type FormRules } from 'element-plus'
import { deleteChecklistApi } from '@/api/checklist'

//////
import { getChecklistById, updateChecklist } from '@/api/checklist'
import type { ChecklistStep } from '@/api/checklist/type'
import { showError } from '@/utils/error'
import { copyChecklist } from '@/api/checklist'

// paging
let currentPage = ref<number>(1);
let pageSize = ref<number>(10);
let total = ref<number>(100);

const showDrawer = ref(false)
const selectedChecklist = ref<ProcessInstance | null>(null)

const rules: FormRules = {
  email: [
    { required: true, message: 'Email is required', trigger: 'blur' },
    { type: 'email', message: 'Please enter a valid email', trigger: 'blur' }
  ]
}

const openChecklistDrawer = async (id: number) => {
  try {
    const res = await getChecklistById(id)
    selectedChecklist.value = res.data
    console.log('Checklist loaded:', selectedChecklist.value)
    showDrawer.value = true
  } catch (error) {
    console.error('Failed to fetch checklist detail:', error)
    showError(error, 'Failed to load checklist detail')
  }
}


const calculateProgress = (checklist: ProcessInstance): number => {
  const allSteps = checklist.stages.flatMap(s => s.steps)
  const total = allSteps.length
  const done = allSteps.filter(s => s.completed).length
  return total === 0 ? 0 : Math.round((done / total) * 100)
}

// 更新勾选状态
const toggleStep = async (step: ChecklistStep) => {
  if (!selectedChecklist.value) return
  try {
    const payload = formatChecklistForUpdate(selectedChecklist.value)
    await updateChecklist(selectedChecklist.value.id, payload)
    ElMessage.success('Step updated')
  } catch (error) {
    console.error('Update failed:', error)
    showError(error, 'Update failed')
  }
}
////


const checklistList = ref<ProcessInstance[]>([])
const router = useRouter()

const loadChecklists = async (page = currentPage.value) => {
  try {
    const res = await getAllChecklists({
      page,
      limit: pageSize.value,
      name: searchinfo.value || undefined
    })

    checklistList.value = res.data.records
    total.value = res.data.total
  } catch (error) {
    console.error('Failed to fetch checklist:', error)
    showError(error, 'Failed to load checklist list')
  }
}

const editChecklist = (id: number) => {
  router.push({ name: 'EditChecklist', params: { id } })
}

const addChecklist = () => {
  router.push({ name: 'AddChecklist' })
}

const deleteChecklist = (id: number) => {
  ElMessageBox.confirm('Are you sure you want to delete this checklist?', 'Warning', {
    confirmButtonText: 'Yes',
    cancelButtonText: 'No',
    type: 'warning'
  })
    .then(async () => {
      try {
        await deleteChecklistApi(id)
        ElMessage.success('Checklist deleted successfully')
        loadChecklists()
      } catch (error) {
        console.error('Delete failed:', error)
        showError(error, 'Failed to delete checklist')
      }
    })
    .catch(() => { })
}

const formatChecklistForUpdate = (checklist: ProcessInstance) => {
  return {
    name: checklist.name,
    description: checklist.description,
    category_id: checklist.category.id,
    stages: checklist.stages.map(stage => ({
      name: stage.name,
      order: stage.order,
      steps: stage.steps.map(step => ({
        name: step.name,
        description: step.description,
        completed: step.completed,
        resourceUrl: step.resourceUrl
      }))
    }))
  }
}

////
const showShareDialog = ref(false)
const shareForm = ref({
  email: '',
  can_edit: false,
  can_share: false
})
const selectedChecklistId = ref<number | null>(null)
const showEditShareDialog = ref(false)
const editShares = ref<ChecklistShare[]>([])

const openShareDialog = (row: ProcessInstance) => {
  selectedChecklistId.value = row.id
  shareForm.value = { email: '', can_edit: false, can_share: false }
  showShareDialog.value = true
}

const openEditShareDialog = (row: ProcessInstance) => {
  selectedChecklistId.value = row.id
  editShares.value = row.shared_users.map(s => ({ ...s }))
  showEditShareDialog.value = true
}

const updateSharePermission = async (share: ChecklistShare) => {
  if (!selectedChecklistId.value) return
  try {
    await shareChecklist(selectedChecklistId.value, {
      email: share.user.email,
      can_edit: share.can_edit,
      can_share: share.can_share
    })
    ElMessage.success('Share updated')
    await loadChecklists(currentPage.value)
  } catch (error) {
    showError(error, 'Failed to update share')
  }
}

const deleteShareAction = async (share: ChecklistShare) => {
  if (!selectedChecklistId.value) return
  try {
    await deleteShare(selectedChecklistId.value, share.user.id)
    ElMessage.success('Share deleted')
    await loadChecklists(currentPage.value)
    showEditShareDialog.value = false
  } catch (error) {
    showError(error, 'Failed to delete share')
  }
}

const submitShare = async () => {
  try {
    if (!selectedChecklistId.value) return

    if (!shareForm.value.email || !shareForm.value.email.includes('@')) {
      ElMessage.warning('Please enter a valid email address')
      return
    }

    await shareChecklist(selectedChecklistId.value, shareForm.value)
    ElMessage.success('Shared successfully')
    await loadChecklists(currentPage.value)
  } catch (error: any) {
    console.error('Share failed:', error)
    const detail = error?.response?.data?.detail || error?.message || 'Share failed'
    ElMessage.error(detail)
  } finally {
    showShareDialog.value = false
  }
}

const copyChecklistAction = async (id: number) => {
  try {
    await copyChecklist(id)
    ElMessage.success('Checklist copied successfully')
    loadChecklists()
  } catch (error) {
    showError(error, 'Failed to copy checklist')
  }
}

// const viewChecklist = (row: ProcessInstance) => {
//   router.push({ name: 'ViewChecklist', params: { id: row.id } })
// }

// search

const searchinfo = ref('');

const handleSearch = () => {
  loadChecklists(1);
};

// reset search
const handleReset = () => {
  searchinfo.value = '';
  loadChecklists(1);
};

// page control
const handleCurrentChange = (val: number) => {
  currentPage.value = val;
  loadChecklists(currentPage.value);
};


onMounted(loadChecklists)
</script>

<style scoped lang="scss">
.checklist-container {
  width: 100%;
  max-width: none;
  padding: 0 10px;

}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
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

.checklist-title {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.checklist-meta {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.checklist-meta strong {
  color: #333;
  margin-right: 4px;
}

.stage-block {
  margin-top: 20px;
}

.stage-block ::v-deep(.el-divider__text) {
  font-weight: 600;
  font-size: 15px;
  color: #34495e;
}

.step-block {
  margin: 10px 0;
}

.step-description {
  margin-left: 26px;
  font-size: 13px;
  color: #888;
  line-height: 1.4;
}

.share-link {
  cursor: pointer;
  color: #409eff;
}

.search-form {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
