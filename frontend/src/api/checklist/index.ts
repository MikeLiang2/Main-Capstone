// checklists API
import service from '@/utils/request'; // Adjust path as needed
import type { ProcessInstance } from './type';
import request from "@/utils/request";
// Base path (no need to duplicate host/port if baseURL is set in axios config)

const BASE_PATH = '/checklist';

export function createChecklist(process: ProcessInstance) {
  return service.post<ProcessInstance>(BASE_PATH, process);
}

export function getChecklist(processId: number) {
  return service.get<ProcessInstance>(`${BASE_PATH}/${processId}`);
}

export async function getAllChecklists() {
  return service.get<ProcessInstance[]>(BASE_PATH);
}

export function getChecklistById(id: number) {
  return service.get<ProcessInstance>(`${BASE_PATH}/${id}`);
}



export function updateChecklist(id: number, data: ProcessInstance) {
  return service.put<ProcessInstance>(`${BASE_PATH}/${id}`, data);
}


export function deleteChecklistApi(id: number) {
  return request({
    url: `/checklists/${id}`,
    method: 'delete'
  })
}