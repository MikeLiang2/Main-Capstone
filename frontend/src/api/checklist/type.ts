// types used by checklists APIsexport 
// 
// 单个步骤
export interface ChecklistStep {
  id: number;
  name: string;
  description: string;
  completed: boolean;
  resourceUrl: string;
}

// 创建用步骤
export interface ChecklistStepCreate {
  name: string;
  description: string;
  completed?: boolean;
  resourceUrl: string;
}

// 阶段（含 ID）
export interface ChecklistStage {
  id: number;
  name: string;
  order: number;
  steps: ChecklistStep[];
}

// 创建阶段（不含 ID）
export interface ChecklistStageCreate {
  name: string;
  order: number;
  steps: ChecklistStepCreate[];
}

// 类别
export interface ProcessCategory {
  id: number;
  name: string;
}

// 获取用：完整流程实例
export interface ProcessInstance {
  id: number;
  name: string;
  description: string;
  category: ProcessCategory;
  stages: ChecklistStage[];
  owner: UserBrief;
  shared_users: ChecklistShare[];
}

// 创建/更新流程用：
export interface ProcessInstanceCreate {
  name: string;
  description: string;
  category_id?: number;
  stages: ChecklistStageCreate[];
}

export interface UserBrief {
  id: string;
  username: string;
  email: string;
  avatar?: string | null;
}

export interface ChecklistShare {
  user: UserBrief;
  can_edit: boolean;
  can_share: boolean;
}
