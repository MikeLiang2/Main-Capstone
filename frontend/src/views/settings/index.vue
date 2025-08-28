<template>
  <el-card class="avatar-settings-card">
    <div class="card-content">

      <!-- Left: Avatar Preview -->
      <div class="avatar-preview">
        <el-avatar :size="256" :src="previewUrl || userStore.userimage || defaultAvatar" />
      </div>

      <!-- Right: Prompt & Style -->
      <div class="avatar-controls">
        <el-form :model="form" label-position="top">
          <el-form-item label="Prompt">
            <el-input type="textarea" v-model="form.prompt" placeholder="Describe your avatar..." :rows="4" />
          </el-form-item>

          <el-form-item label="Style">
            <div class="style-toggle">
              <div class="option" :class="{ active: form.styleValue === 0 }" @click="form.styleValue = 0">
                Natural
              </div>
              <div class="option" :class="{ active: form.styleValue === 1 }" @click="form.styleValue = 1">
                Vivid
              </div>
              <div class="slider-indicator" :class="{ vivid: form.styleValue === 1 }"></div>
            </div>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" :loading="loading" @click="generateAvatar">
              Generate
            </el-button>
            <el-button type="success" :disabled="!previewUrl" @click="approveAvatar">
              Approve
            </el-button>
          </el-form-item>
        </el-form>
      </div>

    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import useUserStore from "@/store/modules/user";
import type { ApproveRequest, AvatarPrompt } from "@/api/settings/avatar/type";
import { generateAvatar as apiGenerateAvatar, approveAvatar as apiApproveAvatar } from "@/api/settings/avatar/index";

const userStore = useUserStore();
const defaultAvatar = "/assets/default-avatar.png";

const form = ref({
  prompt: "",
  styleValue: 1, // 0 = natural, 1 = vivid
});

const previewUrl = ref<string | null>(null);
const loading = ref(false);

// Convert slider value to style string
const selectedStyle = computed(() => (form.value.styleValue === 1 ? "vivid" : "natural"));

// Generate avatar
async function generateAvatar() {
  if (!form.value.prompt) return;

  loading.value = true;
  previewUrl.value = null;

  const payload: AvatarPrompt = {
    prompt: form.value.prompt,
    style: selectedStyle.value,
  };

  try {
    const response = await apiGenerateAvatar(payload);
    console.log(response)
    previewUrl.value = response.data.url;
  } catch (error: any) {
    console.error("Avatar generation failed:", error);
  } finally {
    loading.value = false;
  }
}

// Approve avatar
async function approveAvatar() {
  if (!previewUrl.value) return;

  try {
    const payload: ApproveRequest = { temp_url: previewUrl.value };
    await apiApproveAvatar(payload);
    userStore.fetchUserData();
    previewUrl.value = null;
  } catch (error: any) {
    console.error("Avatar approval failed:", error);
  }
}
</script>

<style scoped lang="scss">
.avatar-settings-card {
  max-width: 800px;
  margin: 40px auto;
  border-radius: 12px;
  background-color: #f8fafc;
  padding: 20px;

  .card-content {
    display: flex;
    gap: 30px;

    .avatar-preview {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: flex-start;

      h4 {
        margin-bottom: 10px;
        font-weight: 600;
        font-size: 16px;
      }

      .el-avatar {
        border: 2px solid #ddd;
      }
    }

    .avatar-controls {
      flex: 1.2;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;

      .style-toggle {
        position: relative;
        display: flex;
        border-radius: 10px; // pill shape
        overflow: hidden;
        cursor: pointer;
        user-select: none;
        font-size: 16px;
        height: 50px;
        width: 100%;
        background-color: white;

        .option {
          flex: 1;
          text-align: center;
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 2;
          transition: color 0.3s;
          color: #4b5563; // dark gray for inactive
          font-weight: 500;
          letter-spacing: 0.5px;

          &.active {
            color: #ffffff; // white for active
            font-weight: 600;
          }
        }

        .slider-indicator {
          position: absolute;
          top: 2px; // slight padding inside border
          bottom: 2px;
          width: 50%;
          background-color: #3b82f6; // professional blue
          border-radius: 10px;
          transition: transform 0.3s ease;

          &.vivid {
            transform: translateX(100%);
          }
        }
      }

      .style-labels {
        display: flex;
        justify-content: space-between;
        font-size: 14px;
        color: #6b7280; // lighter gray
        margin-top: 4px;
        padding: 0 8px;
      }


      .el-form-item {
        margin-bottom: 20px;
      }

      .el-button {
        font-weight: 600;
        border-radius: 8px;
        padding: 10px 24px;
        font-size: 14px;
        transition: all 0.3s;
        color: white;

        &.generate {
          background-color: #409eff;
          color: #fff;
        }

        &.approve {
          background-color: #67c23a;
          color: #fff;
        }

        &:hover {
          opacity: 0.9;
        }
      }
    }
  }
}
</style>
