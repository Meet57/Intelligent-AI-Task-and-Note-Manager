const API_BASE = 'http://127.0.0.1:5000';

// Generic API request function
export const apiRequest = async (url: string, options: RequestInit = {}) => {
  try {
    const response = await fetch(`${API_BASE}${url}`, {
      headers: {
        'Content-Type': 'application/json',
      },
      ...options,
    });
    
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

// Task API functions
export const taskAPI = {
  getAll: () => apiRequest('/tasks/'),
  
  getById: (id: number) => apiRequest(`/tasks/${id}`),
  
  create: (taskData: any) => 
    apiRequest('/tasks/', {
      method: 'POST',
      body: JSON.stringify(taskData),
    }),
  
  update: (id: number, taskData: any) =>
    apiRequest(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    }),
  
  delete: (id: number) =>
    apiRequest(`/tasks/${id}`, { method: 'DELETE' }),
  
  addNote: (taskId: number, noteId: number) =>
    apiRequest(`/tasks/${taskId}/notes/${noteId}`, { method: 'POST' }),
  
  removeNote: (taskId: number, noteId: number) =>
    apiRequest(`/tasks/${taskId}/notes/${noteId}`, { method: 'DELETE' }),
};

// Note API functions
export const noteAPI = {
  getAll: () => apiRequest('/notes/'),
  
  getById: (id: number) => apiRequest(`/notes/${id}`),
  
  create: (noteData: any) =>
    apiRequest('/notes/', {
      method: 'POST',
      body: JSON.stringify(noteData),
    }),
  
  update: (id: number, noteData: any) =>
    apiRequest(`/notes/${id}`, {
      method: 'PUT',
      body: JSON.stringify(noteData),
    }),
  
  delete: (id: number) =>
    apiRequest(`/notes/${id}`, { method: 'DELETE' }),
  
  addTask: (noteId: number, taskId: number) =>
    apiRequest(`/notes/${noteId}/tasks/${taskId}`, { method: 'POST' }),
  
  removeTask: (noteId: number, taskId: number) =>
    apiRequest(`/notes/${noteId}/tasks/${taskId}`, { method: 'DELETE' }),
};

// Health check
export const healthAPI = {
  check: () => apiRequest('/health'),
};

// Agent API functions
export const agentAPI = {
  sendMessage: (message: string) =>
    apiRequest('/agents/agent', {
      method: 'POST',
      body: JSON.stringify({ message }),
    }),
};

// Agent service
export const agentService = {
  send: async (message: string) => {
    try {
      const response = await agentAPI.sendMessage(message);
      return { messages: response.messages, type: 'success' as const };
    } catch (error) {
      console.error('Error sending message to agent:', error);
      throw new Error('Failed to get response from agent');
    }
  },
};

// Higher-level service functions
export const taskService = {
  // Load all tasks
  loadAll: async () => {
    try {
      return await taskAPI.getAll();
    } catch (error) {
      console.error('Error loading tasks:', error);
      throw new Error('Failed to load tasks');
    }
  },

  // Save task (create or update)
  save: async (taskData: any, editingTask: any = null) => {
    try {
      if (editingTask) {
        await taskAPI.update(editingTask.id, taskData);
        return { message: 'Task updated successfully', type: 'success' as const };
      } else {
        await taskAPI.create(taskData);
        return { message: 'Task created successfully', type: 'success' as const };
      }
    } catch (error) {
      console.error('Error saving task:', error);
      throw new Error('Failed to save task');
    }
  },

  // Delete task
  remove: async (id: number) => {
    try {
      await taskAPI.delete(id);
      return { message: 'Task deleted successfully', type: 'success' as const };
    } catch (error) {
      console.error('Error deleting task:', error);
      throw new Error('Failed to delete task');
    }
  },

  // Add note to task
  addNote: async (taskId: number, noteId: number) => {
    try {
      await taskAPI.addNote(taskId, noteId);
      return { message: 'Note added to task successfully', type: 'success' as const };
    } catch (error) {
      console.error('Error adding note to task:', error);
      throw new Error('Failed to add note to task');
    }
  },

  // Remove note from task
  removeNote: async (taskId: number, noteId: number) => {
    try {
      await taskAPI.removeNote(taskId, noteId);
      return { message: 'Note removed from task successfully', type: 'success' as const };
    } catch (error) {
      console.error('Error removing note from task:', error);
      throw new Error('Failed to remove note from task');
    }
  },
};

export const noteService = {
  // Load all notes
  loadAll: async () => {
    try {
      return await noteAPI.getAll();
    } catch (error) {
      console.error('Error loading notes:', error);
      throw new Error('Failed to load notes');
    }
  },

  // Save note (create or update)
  save: async (noteData: any, editingNote: any = null) => {
    try {
      if (editingNote) {
        await noteAPI.update(editingNote.id, noteData);
        return { message: 'Note updated successfully', type: 'success' as const };
      } else {
        await noteAPI.create(noteData);
        return { message: 'Note created successfully', type: 'success' as const };
      }
    } catch (error) {
      console.error('Error saving note:', error);
      throw new Error('Failed to save note');
    }
  },

  // Delete note
  remove: async (id: number) => {
    try {
      await noteAPI.delete(id);
      return { message: 'Note deleted successfully', type: 'success' as const };
    } catch (error) {
      console.error('Error deleting note:', error);
      throw new Error('Failed to delete note');
    }
  },

  // Add task to note
  addTask: async (noteId: number, taskId: number) => {
    try {
      await noteAPI.addTask(noteId, taskId);
      return { message: 'Task added to note successfully', type: 'success' as const };
    } catch (error) {
      console.error('Error adding task to note:', error);
      throw new Error('Failed to add task to note');
    }
  },

  // Remove task from note
  removeTask: async (noteId: number, taskId: number) => {
    try {
      await noteAPI.removeTask(noteId, taskId);
      return { message: 'Task removed from note successfully', type: 'success' as const };
    } catch (error) {
      console.error('Error removing task from note:', error);
      throw new Error('Failed to remove task from note');
    }
  },
};