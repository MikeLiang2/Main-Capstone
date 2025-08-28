<template>
  <el-card>
    <el-form :model="form" label-position="top">
      <el-form-item label="Prompt">
        <el-input type="textarea" v-model="form.prompt" placeholder="Describe the checklist you want to create today..."
          :autosize="{ minRows: 3, maxRows: 40 }" />
      </el-form-item>
      <el-form-item class="form-buttons">
        <el-button type="primary" :loading="loading" :disabled="loading" @click="generateChecklist">
          Generate
        </el-button>

        <el-button type="success" v-if="process" @click="saveChecklist">
          Save
        </el-button>
      </el-form-item>

    </el-form>
  </el-card>

  <el-empty v-if="process?.stages?.length === 0" description="No checklist generated yet" />

  <div v-else>
    <el-card v-for="(stage, index) in process?.stages || []" :key="index" class="result-card" shadow="hover">
      <template #header>
        <div class="stage-header">
          <span> Stage {{ index + 1 }}: {{ stage.name }}</span>
        </div>
      </template>

      <el-timeline>
        <el-timeline-item v-for="(step, i) in stage.steps" :key="i" :timestamp="step.name" placement="top">
          <div class="step-description">
            {{ step.description }}
          </div>
          <div v-if="step.resourceUrl" class="step-url">
            <a :href="step.resourceUrl" target="_blank">{{ step.resourceUrl }}</a>
          </div>
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>

<script setup lang="ts">

import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import axios from '@/utils/request'

interface Step {
  name: string
  description: string
  resourceUrl: string
  completed: boolean
}

interface Stage {
  name: string
  order: number
  steps: Step[]
}

interface Process {
  name: string
  description: string
  category_id: number
  stages: Stage[]
}

const form = ref({
  prompt: ''
})
const loading = ref(false)

const process = ref<Process | null>(null)

const generateChecklist = async () => {
  if (!form.value.prompt) {
    ElMessage.warning('Please enter a prompt')
    return
  }

  if (loading.value) return  // 防止重复点击
  loading.value = true

  try {
    const res = await axios.post('/checklist/generate', { prompt: form.value.prompt })
    process.value = res.data
  } catch (error) {
    console.error(error)
    ElMessage.error('Failed to generate checklist from AI, maybe change your prompt and try again?')
  } finally {
    loading.value = false  // 请求完成后可再次点击
  }
}

const saveChecklist = async () => {
  if (!process.value) {
    ElMessage.warning('No checklist to save')
    return
  }

  try {
    await axios.post('/checklist', process.value)
    ElMessage.success('Checklist saved successfully')
    process.value = null
    form.value.prompt = ''
  } catch (error) {
    console.error(error)
    ElMessage.error('Failed to save checklist')
  }
}

</script>
<style scoped lang="scss">
.result-card {
  margin-top: 20px;
}

.stage-header {
  font-weight: bold;
  font-size: 16px;
  color: #2c3e50;
}

.step-description {
  white-space: pre-line;
  margin-bottom: 4px;
}

.step-url {
  font-size: 13px;
  color: #409eff;
  margin-top: 2px;
}

.form-buttons {
  margin-top: 12px;
}
</style>
