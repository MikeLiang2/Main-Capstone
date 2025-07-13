// types used by checklists APIsexport 
// 
export interface ChecklistStep {
    id: number;
    name: string;
    description: string;
    completed: boolean;
    resourceUrl: string;
  }
  
  export interface ChecklistStage {
    id: number;
    name: string;
    order: number;
    steps: ChecklistStep[];
  }
  
  export interface ProcessCategory {
    id: number;
    name: string;
  }
  
  export interface ProcessInstance {
    id: number;
    name: string;
    description: string;
    category: ProcessCategory;
    stages: ChecklistStage[];
  }
  