<template>
    <div class="view-checklist">
        <el-card v-if="checklist">
            <h2>{{ checklist.name }}</h2>
            <p><strong>Category:</strong> {{ checklist.category.name }}</p>
            <p><strong>Description:</strong> {{ checklist.description }}</p>

            <el-divider />
            <div v-for="stage in checklist.stages" :key="stage.id" class="stage-block">
                <h3>{{ stage.name }}</h3>
                <el-checkbox-group>
                    <el-checkbox v-for="step in stage.steps" :key="step.id" v-model="step.completed"
                        @change="toggleStep(stage.id, step)">
                        <div style="display: flex; flex-direction: column;">
                            <div>
                                {{ step.name }}
                                <a v-if="step.resourceUrl" :href="step.resourceUrl" target="_blank"
                                    style="margin-left: 8px; font-size: 12px">
                                    [Resource]
                                </a>
                            </div>
                            <div style="font-size: 12px; color: #888; margin-left: 2px;">
                                {{ step.description }}
                            </div>
                        </div>
                    </el-checkbox>
                </el-checkbox-group>
            </div>
        </el-card>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getChecklistById, updateChecklist } from '@/api/checklist'
import type { ProcessInstance, ChecklistStep } from '@/api/checklist/type'
import { ElMessage } from 'element-plus'

const route = useRoute()
const checklist = ref<ProcessInstance | null>(null)

const loadChecklist = async () => {
    const id = Number(route.params.id)
    const res = await getChecklistById(id)
    // console.log('Checklist data:')
    checklist.value = res.data
}

// check item status change
// This function toggles the completion status of a checklist step
const toggleStep = async (stageId: number, step: ChecklistStep) => {
    step.completed = !step.completed

    try {
        if (checklist.value) {
            await updateChecklist(checklist.value.id, checklist.value)
            ElMessage.success('Step status updated')
        }
    } catch (error) {
        ElMessage.error('Update failed')
        console.error(error)
    }
}

onMounted(loadChecklist)
</script>

<style scoped lang="scss">
.view-checklist {
    max-width: 1000px;
    margin: 40px auto;

    .stage-block {
        margin-bottom: 20px;
    }

    h3 {
        margin-top: 20px;
        color: #3f51b5;
    }
}
</style>
