<template>
  <!-- Checklist Management Page -->
  <div class="checklist-container">
    <!-- Title and Action Bar -->
    <el-card>
      <div class="card-header">
        <h2>Checklist Management</h2>
        <el-button type="primary" icon="Plus" @click="addChecklist">Add Checklist</el-button>
      </div>

      <!-- Checklist Table -->
      <el-table :data="checklistList" style="width: 100%" :fit="true" @row-click="row => openChecklistDrawer(row.id)">
        <el-table-column type="index" label="#" width="50" align="center" />
        <el-table-column prop="name" label="Name" show-overflow-tooltip align="center" />
        <el-table-column prop="category.name" label="Category" show-overflow-tooltip align="center" />
        <el-table-column label="Actions" align="center" width="240">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="editChecklist(row.id)">Edit</el-button>
            <el-button type="danger" size="small" @click="deleteChecklist(row.id)">Delete</el-button>
            <!-- <el-button type="success" size="small" @click="openChecklistDrawer(row.id)">View</el-button> -->
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Checklist Drawer -->
    <el-drawer v-model="showDrawer" size="600px" title="Checklist Detail" :before-close="() => (showDrawer = false)">
      <!-- Drawer 内容展示 -->
      <template #default>
        <div v-if="selectedChecklist">
          <h3 class="checklist-title">{{ selectedChecklist.name }}</h3>
          <p class="checklist-meta"><strong>Category:</strong> {{ selectedChecklist.category.name }}</p>
          <p class="checklist-meta"><strong>Description:</strong> {{ selectedChecklist.description }}</p>

          <!-- ✅ Progress -->
          <el-progress :percentage="calculateProgress(selectedChecklist)" status="success" style="margin: 16px 0;" />

          <!-- ✅ Stage List -->
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


  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getAllChecklists } from '@/api/checklist'
import type { ProcessInstance } from '@/api/checklist/type'
import { ElMessageBox, ElMessage } from 'element-plus'
import { deleteChecklistApi } from '@/api/checklist'

//////
import { getChecklistById, updateChecklist } from '@/api/checklist'
import type { ChecklistStep } from '@/api/checklist/type'



const showDrawer = ref(false)
const selectedChecklist = ref<ProcessInstance | null>(null)

const openChecklistDrawer = async (id: number) => {
  try {
    const res = await getChecklistById(id)
    selectedChecklist.value = res.data
    showDrawer.value = true
  } catch (error) {
    console.error('Failed to fetch checklist detail:', error)
    ElMessage.error('Failed to load checklist detail')
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
    await updateChecklist(selectedChecklist.value.id, selectedChecklist.value)
    ElMessage.success('Step updated')
  } catch (error) {
    ElMessage.error('Update failed')
  }
}
////


const checklistList = ref<ProcessInstance[]>([])
const router = useRouter()

const loadChecklists = async () => {
  try {
    const res = await getAllChecklists()
    checklistList.value = res.data
  } catch (error) {
    console.error('Failed to fetch checklist:', error)
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
        ElMessage.error('Failed to delete checklist')
      }
    })
    .catch(() => { })
}


// const viewChecklist = (row: ProcessInstance) => {
//   router.push({ name: 'ViewChecklist', params: { id: row.id } })
// }


onMounted(loadChecklists)
</script>

<style scoped lang="scss">
.checklist-container {
  max-width: 1000px;
  margin: 40px auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.el-button {
  background-color: #64b5f6;
  color: white;
  border: 1px solid #64b5f6;

  &:hover {
    background-color: #90caf9;
    border-color: #90caf9;
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
</style>
