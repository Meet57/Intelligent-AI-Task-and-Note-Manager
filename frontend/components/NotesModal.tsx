import { Note } from '../types';
import { useState } from 'react';

interface NotesModalProps {
  isOpen: boolean;
  onClose: () => void;
  notes: Note[];
  taskTitle: string;
  taskId: number;
  availableNotes: Note[];
  onAddNote: (taskId: number, noteId: number) => void;
  onRemoveNote: (taskId: number, noteId: number) => void;
}

export default function NotesModal({ 
  isOpen, 
  onClose, 
  notes, 
  taskTitle, 
  taskId, 
  availableNotes, 
  onAddNote, 
  onRemoveNote 
}: NotesModalProps) {
  const [selectedNoteId, setSelectedNoteId] = useState<string>('');
  
  if (!isOpen) return null;

  const handleAddNote = () => {
    if (selectedNoteId) {
      onAddNote(taskId, parseInt(selectedNoteId));
      setSelectedNoteId('');
    }
  };

  const unassociatedNotes = availableNotes.filter(
    availableNote => !notes.some(note => note.id === availableNote.id)
  );

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full mx-4 max-h-[80vh] overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h2 className="text-xl font-semibold text-gray-900">
            Notes for "{taskTitle}"
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Add Note Section */}
        {unassociatedNotes.length > 0 && (
          <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
            <h3 className="text-sm font-medium text-gray-900 mb-3">Add Note to Task</h3>
            <div className="flex space-x-3">
              <select
                value={selectedNoteId}
                onChange={(e) => setSelectedNoteId(e.target.value)}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-md bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select a note to add...</option>
                {unassociatedNotes.map((note) => (
                  <option key={note.id} value={note.id}>
                    {note.title}
                  </option>
                ))}
              </select>
              <button
                onClick={handleAddNote}
                disabled={!selectedNoteId}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                Add Note
              </button>
            </div>
          </div>
        )}

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[60vh]">
          {notes && notes.length > 0 ? (
            <div className="space-y-4">
              {notes.map((note) => (
                <div key={note.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900">{note.title}</h3>
                      <span className="text-sm text-gray-500">
                        {note.created_at ? new Date(note.created_at).toLocaleDateString() : 'No date'}
                      </span>
                    </div>
                    <button
                      onClick={() => onRemoveNote(taskId, note.id)}
                      className="ml-3 text-red-600 hover:text-red-800 text-sm font-medium"
                      title="Remove note from task"
                    >
                      Remove
                    </button>
                  </div>
                  {note.content && (
                    <p className="text-gray-700 text-sm whitespace-pre-wrap">{note.content}</p>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <p>No notes associated with this task.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}