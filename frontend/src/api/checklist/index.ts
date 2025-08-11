import request from '@/utils/request';
import type {
  ProcessInstance,
  ProcessInstanceCreate
} from './type';

const BASE_PATH = '/checklist';

export function createChecklist(process: ProcessInstanceCreate) {
  return request.post<ProcessInstance>(BASE_PATH, process);
}


export function getChecklistById(id: number) {
  return request.get<ProcessInstance>(`${BASE_PATH}/${id}`);
}


export const getAllChecklists = (params: { page: number; limit: number; name?: string }) => {
  return request.get<{ records: ProcessInstance[]; total: number }>(BASE_PATH, { params });
}


export function updateChecklist(id: number, data: ProcessInstanceCreate) {
  return request.put<ProcessInstance>(`${BASE_PATH}/${id}`, data);
}

export function deleteChecklistApi(id: number) {
  return request.delete(`${BASE_PATH}/${id}`);
}

export const getCategories = () => {
  return request({
    url: '/category',
    method: 'get'
  })
}

export const shareChecklist = (checklistId: number, data: {
  email: string
  can_edit: boolean
  can_share: boolean
}) => {
  return request.post(`/processes/${checklistId}/share`, data)
}

export const copyChecklist = (id: number) => {
  return request.post(`/checklist/${id}/copy`)
}

export const deleteShare = (checklistId: number, userId: string) => {
  return request.delete(`/processes/${checklistId}/share/${userId}`)
}