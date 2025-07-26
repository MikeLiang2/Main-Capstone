import { ElMessage } from 'element-plus'

export function showError(error: any, fallback = 'Operation failed') {
  const detail = error?.response?.data?.detail || error?.message || fallback
  ElMessage.error(detail)
}