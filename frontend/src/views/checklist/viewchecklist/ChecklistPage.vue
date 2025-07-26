<template>
  <div style="max-width: 800px; margin: auto;">
    <el-card :header="process.name">
      <p>分类：{{ process.category.name }}</p>
      <div v-for="stage in process.stages" :key="stage.id" class="stage">
        <el-divider>{{ stage.name }}</el-divider>

        <div v-for="step in stage.steps" :key="step.id" style="margin-bottom: 0.5rem;">
          <el-checkbox v-model="step.completed" @change="onCheckChange(step)">
            {{ step.name }}
            <a v-if="step.resourceUrl" :href="step.resourceUrl" target="_blank" style="margin-left: 10px;">
              [参考资料1]
            </a>

          </el-checkbox>
        </div>

      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { ChecklistStep, ProcessInstance } from '@/api/checklist/type'

const process = ref<ProcessInstance>({
  id: 1,
  name: '签证申请流程',
  description: '帮助用户逐步完成签证申请',
  category: { id: 1, name: '签证' },
  owner: { id: '1', username: 'admin', email: 'admin@example.com', avatar: '' },
  shared_users: [],
  stages: [
    {
      id: 1,
      name: '材料准备',
      order: 1,
      steps: [
        {
          id: 11, name: '上传身份证', completed: true,
          description: '',
          resourceUrl: ''
        },
        {
          id: 12, name: '上传护照', completed: false,
          description: '',
          resourceUrl: ''
        }
      ]
    },
    {
      id: 2,
      name: '表格填写',
      order: 2,
      steps: [
        {
          id: 13, name: '填写在线表格', completed: false, resourceUrl: 'https://gov.example.com/form',
          description: ''
        }
      ]
    }
  ]
})



const onCheckChange = async (step: ChecklistStep) => {
  console.log(`Step ${step.id} is now:`, step.completed)
  // 可调用后端 API 保存
  // await axios.put(`/api/steps/${step.id}`, { completed: step.completed })
}
</script>

<style scoped>
.stage {
  margin-top: 1rem;
  padding-left: 1rem;
  border-left: 2px solid #ccc;
}
</style>
