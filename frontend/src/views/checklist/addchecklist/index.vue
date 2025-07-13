<template>
  <div style="max-width: 800px; margin: auto;">
    <el-card>
      <h2>新增流程</h2>
      <el-form label-position="top" :model="form">
        <el-form-item label="流程名称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="form.category.id" placeholder="请选择分类">
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" />
        </el-form-item>

        <el-divider>添加阶段</el-divider>
        <div v-for="(stage, index) in form.stages" :key="index" style="margin-bottom: 20px;">
          <el-form-item :label="`阶段名称 ${index + 1}`">
            <el-input v-model="stage.name" />
          </el-form-item>
          <el-form-item :label="`阶段顺序 ${index + 1}`">
            <el-input-number v-model="stage.order" :min="1" />
          </el-form-item>
          <el-button type="primary" plain size="small" @click="() => addStep(index)">添加步骤</el-button>

          <div v-for="(step, sIndex) in stage.steps" :key="sIndex" style="margin-left: 1em;">
            <el-form-item :label="`步骤 ${sIndex + 1} 名称`">
              <el-input v-model="step.name" />
            </el-form-item>
            <el-form-item label="描述">
              <el-input v-model="step.description" />
            </el-form-item>
            <el-form-item label="参考链接">
              <el-input v-model="step.resourceUrl" />
            </el-form-item>
          </div>
        </div>

        <el-form-item>
          <el-button @click="addStage">添加阶段</el-button>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submit">提交</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getChecklistById, updateChecklist } from '@/api/checklist'

const route = useRoute()

const categories = ref([
  { id: 1, name: '签证' },
  { id: 2, name: '入职' }
])

const timestampId = Date.now();

const form = ref({
  id: timestampId,
  name: '',
  description: '',
  category: { id: 1, name: '签证' },
  stages: [] as any[]
})

let stepIdCounter = 1;
let stageIdCounter = 1;

const addStage = () => {
  form.value.stages.push({
    id: stageIdCounter++,
    name: '',
    order: form.value.stages.length + 1,
    steps: []
  });
};

const addStep = (stageIndex: number) => {
  form.value.stages[stageIndex].steps.push({
    id: stepIdCounter++,
    name: '',
    description: '',
    resourceUrl: '',
    completed: false
  });
};

import { createChecklist } from '@/api/checklist/index'
import type { ProcessInstance } from '@/api/checklist/type'
import { id } from 'element-plus/es/locales.mjs'

const isEditMode = !!route.params.id

onMounted(async () => {
  if (isEditMode) {
    const data = await getChecklistById(Number(route.params.id))
    form.value = data.data
  }
})

const submit = async () => {

  const payload: ProcessInstance = {
    id: form.value.id,
    name: form.value.name,
    description: form.value.description,
    category: form.value.category,
    stages: form.value.stages
  };

  try {
    if (isEditMode) {
      await updateChecklist(payload.id, payload)
      alert("更新成功")
    } else {
      console.log('提交数据:', payload);
      const result = await createChecklist(payload);
      alert('创建成功：' + JSON.stringify(result));
    }

  } catch (error: any) {
    alert('提交失败：' + error.message);
  }
};
</script>