import { Note, Task } from '../types';
import { useState, useEffect } from 'react';
import TasksModal from './TasksModal';

interface NoteTableProps {
  notes: Note[];
  onEdit: (note: Note) => void;
  onDelete: (id: number) => void;
  allTasks: Task[];
  onAddTask: (noteId: number, taskId: number) => void;
  onRemoveTask: (noteId: number, taskId: number) => void;
}

export default function NoteTable({ notes, onEdit, onDelete, allTasks, onAddTask, onRemoveTask }: NoteTableProps) {
  const [selectedNote, setSelectedNote] = useState<Note | null>(null);
  const [isTasksModalOpen, setIsTasksModalOpen] = useState(false);

  const handleViewTasks = (note: Note) => {
    setSelectedNote(note);
    setIsTasksModalOpen(true);
  };

  const closeTasksModal = () => {
    setIsTasksModalOpen(false);
    setSelectedNote(null);
  };

  // Update selected note when notes array changes
  useEffect(() => {
    if (selectedNote) {
      const updatedNote = notes.find(n => n.id === selectedNote.id);
      if (updatedNote) {
        setSelectedNote(updatedNote);
      }
    }
  }, [notes, selectedNote]);

  const handleAddTask = async (noteId: number, taskId: number) => {
    await onAddTask(noteId, taskId);
  };

  const handleRemoveTask = async (noteId: number, taskId: number) => {
    await onRemoveTask(noteId, taskId);
  };
  if (!notes || notes.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b">
          <h3 className="text-lg font-medium">Notes</h3>
        </div>
        <div className="px-6 py-8 text-center text-gray-500">
          No notes found. Create your first note above.
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="px-6 py-4 border-b">
        <h3 className="text-lg text-black font-medium">Notes</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Title
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Content
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Created
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Tasks
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {notes.map((note) => (
              <tr key={note.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 font-medium text-gray-900">
                  {note.title}
                </td>
                <td className="px-6 py-4 text-sm text-gray-500 max-w-xs">
                  <div className="truncate">
                    {note.content || 'No content'}
                  </div>
                </td>
                <td className="px-6 py-4 text-sm text-gray-500">
                  {note.created_at ? new Date(note.created_at).toLocaleDateString() : '-'}
                </td>
                <td className="px-6 py-4">
                  <button
                    onClick={() => handleViewTasks(note)}
                    className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 hover:bg-green-200"
                  >
                    {note.tasks ? note.tasks.length : 0} tasks
                  </button>
                </td>
                <td className="px-6 py-4">
                  <div className="flex space-x-2">
                    <button
                      onClick={() => onEdit(note)}
                      className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => onDelete(note.id)}
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
      
      {/* Tasks Modal */}
      {selectedNote && (
        <TasksModal
          isOpen={isTasksModalOpen}
          onClose={closeTasksModal}
          tasks={selectedNote.tasks || []}
          noteTitle={selectedNote.title}
          noteId={selectedNote.id}
          availableTasks={allTasks}
          onAddTask={handleAddTask}
          onRemoveTask={handleRemoveTask}
        />
      )}
    </div>
  );
}