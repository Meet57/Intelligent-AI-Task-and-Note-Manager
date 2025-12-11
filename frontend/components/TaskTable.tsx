import { Task, Note } from '../types';
import { useState, useEffect } from 'react';
import NotesModal from './NotesModal';

interface TaskTableProps {
  tasks: Task[];
  onEdit: (task: Task) => void;
  onDelete: (id: number) => void;
  allNotes: Note[];
  onAddNote: (taskId: number, noteId: number) => void;
  onRemoveNote: (taskId: number, noteId: number) => void;
}

const getStatusClass = (status: string) => {
  switch (status?.toLowerCase()) {
    case 'completed': return 'bg-green-100 text-green-800';
    case 'in-progress': return 'bg-blue-100 text-blue-800';
    case 'pending': return 'bg-yellow-100 text-yellow-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

export default function TaskTable({ tasks, onEdit, onDelete, allNotes, onAddNote, onRemoveNote }: TaskTableProps) {
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [isNotesModalOpen, setIsNotesModalOpen] = useState(false);

  const handleViewNotes = (task: Task) => {
    setSelectedTask(task);
    setIsNotesModalOpen(true);
  };

  const closeNotesModal = () => {
    setIsNotesModalOpen(false);
    setSelectedTask(null);
  };

  // Update selected task when tasks array changes
  useEffect(() => {
    if (selectedTask) {
      const updatedTask = tasks.find(t => t.id === selectedTask.id);
      if (updatedTask) {
        setSelectedTask(updatedTask);
      }
    }
  }, [tasks, selectedTask]);

  const handleAddNote = async (taskId: number, noteId: number) => {
    await onAddNote(taskId, noteId);
  };

  const handleRemoveNote = async (taskId: number, noteId: number) => {
    await onRemoveNote(taskId, noteId);
  };
  if (!tasks || tasks.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b">
          <h3 className="text-lg font-medium">Tasks</h3>
        </div>
        <div className="px-6 py-8 text-center text-gray-500">
          No tasks found. Create your first task above.
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="px-6 py-4 border-b">
        <h3 className="text-lg text-black font-medium">Tasks</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Title
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Deadline
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Notes
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {tasks.map((task) => (
              <tr key={task.id} className="hover:bg-gray-50">
                <td className="px-6 py-4">
                  <div className="font-medium text-gray-900">{task.title}</div>
                  {task.description && (
                    <div className="text-sm text-gray-500 truncate max-w-xs">
                      {task.description}
                    </div>
                  )}
                </td>
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusClass(task.status)}`}>
                    {task.status}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-gray-500">
                  {task.deadline ? new Date(task.deadline).toLocaleDateString() : '-'}
                </td>
                <td className="px-6 py-4">
                  <button
                    onClick={() => handleViewNotes(task)}
                    className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 hover:bg-blue-200"
                  >
                    {task.notes ? task.notes.length : 0} notes
                  </button>
                </td>
                <td className="px-6 py-4">
                  <div className="flex space-x-2">
                    <button
                      onClick={() => onEdit(task)}
                      className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => onDelete(task.id)}
                      className="text-red-600 hover:text-red-800 text-sm font-medium"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {/* Notes Modal */}
      {selectedTask && (
        <NotesModal
          isOpen={isNotesModalOpen}
          onClose={closeNotesModal}
          notes={selectedTask.notes || []}
          taskTitle={selectedTask.title}
          taskId={selectedTask.id}
          availableNotes={allNotes}
          onAddNote={handleAddNote}
          onRemoveNote={handleRemoveNote}
        />
      )}
    </div>
  );
}