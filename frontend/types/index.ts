export interface Task {
  id: number;
  title: string;
  description?: string;
  status: 'pending' | 'in-progress' | 'completed';
  deadline?: string;
  notes?: Note[];
}

export interface Note {
  id: number;
  title: string;
  content?: string;
  created_at: string;
  tasks?: Task[];
}