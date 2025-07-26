<template>
  <div style="max-width: 800px; margin: auto;">
    <el-card>
      <h2>{{ isEditMode ? 'Edit Checklist' : 'Create New Process' }}</h2>
      <el-form :model="form" :rules="rules" ref="formRef" label-position="top">
        <el-form-item label="Process Name" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="Category">
          <el-select v-model="form.category.id" placeholder="Select a category">
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="Description">
          <el-input v-model="form.description" type="textarea" />
        </el-form-item>

        <el-divider>Add Stages</el-divider>
        <div v-for="(stage, index) in form.stages" :key="index" style="margin-bottom: 20px;">
          <el-form-item :label="`Stage Name ${index + 1}`">
            <el-input v-model="stage.name" />
          </el-form-item>
          <el-form-item :label="`Stage Order ${index + 1}`">
            <el-input-number v-model="stage.order" :min="1" />
          </el-form-item>
          <el-button type="primary" plain size="small" @click="() => addStep(index)">Add Step</el-button>

          <div v-for="(step, sIndex) in stage.steps" :key="sIndex" style="margin-left: 1em;">
            <el-form-item :label="`Step ${sIndex + 1} Name`">
              <el-input v-model="step.name" />
            </el-form-item>
            <el-form-item label="Description">
              <el-input v-model="step.description" />
            </el-form-item>
            <el-form-item label="Resource URL">
              <el-input v-model="step.resourceUrl" />
            </el-form-item>
          </div>
        </div>

        <el-form-item>
          <el-button @click="addStage">Add Stage</el-button>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submit">Submit</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getChecklistById, updateChecklist, createChecklist, getCategories } from '@/api/checklist'
import { useRouter } from 'vue-router'
const route = useRoute()
const router = useRouter()
const categories = ref<{ id: number, name: string }[]>([])

const rules = {
  name: [{ required: true, message: 'Checklist name is required', trigger: 'blur' }]
}

const formRef = ref()


// const timestampId = Date.now();

const form = ref({
  // id: undefined,
  name: '',
  description: '',
  category: { id: 1, name: '' },
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

const isEditMode = ref(false)

onMounted(async () => {
  const res = await getCategories()
  categories.value = res.data

  if (route.params.id) {
    isEditMode.value = true
    const data = await getChecklistById(Number(route.params.id))
    form.value = {
      name: data.data.name,
      description: data.data.description,
      category: data.data.category || { id: 1, name: '' },
      stages: data.data.stages
    }
  }
})

const submit = async () => {
  if (!formRef.value) return;

  formRef.value.validate(async (valid: boolean) => {
    if (!valid) return;

    const payload = {
      name: form.value.name,
      description: form.value.description,
      category_id: form.value.category.id,
      stages: form.value.stages
    };

    try {
      if (isEditMode.value) {
        await updateChecklist(Number(route.params.id), payload);
        alert("Successfully updated");
        router.push(`/checklist/editchecklist`);
      } else {
        const result = await createChecklist(payload);
        alert('Created successfully');
        router.push(`/checklist/editchecklist`);
      }
    } catch (error: any) {
      alert('Submission failed: ' + error.message);
    }
  });
};

</script>