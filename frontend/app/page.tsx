"use client";

import React, { useState, useEffect } from 'react';
import Navigation from '../components/Navigation';
import { Task, Note } from '../types';
import TaskForm from '@/components/TaskForm';
import TaskTable from '@/components/TaskTable';
import NoteForm from '@/components/NoteForm';
import NoteTable from '@/components/NoteTable';
import AgentChat from '@/components/AgentChat';
import { taskService, noteService } from '../utils/api';

export default function Home() {
  const [currentView, setCurrentView] = useState<'tasks' | 'notes' | 'agents'>('tasks');
  const [tasks, setTasks] = useState<Task[]>([]);
  const [notes, setNotes] = useState<Note[]>([]);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [editingNote, setEditingNote] = useState<Note | null>(null);
  const [message, setMessage] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  const showMessage = (text: string, type: 'success' | 'error') => {
    setMessage({ text, type });
    setTimeout(() => setMessage(null), 3000);
  };

  // Task functions
  const loadTasks = async () => {
    try {
      const tasksData = await taskService.loadAll();
      setTasks(tasksData);
    } catch (error) {
      showMessage('Failed to load tasks', 'error');
    }
  };

  const saveTask = async (taskData: Partial<Task>) => {
    try {
      const result = await taskService.save(taskData, editingTask);
      showMessage(result.message, result.type);
      setEditingTask(null);
      loadTasks();
    } catch (error) {
      showMessage('Failed to save task', 'error');
    }
  };

  const deleteTask = async (id: number) => {
    try {
      const result = await taskService.remove(id);
      showMessage(result.message, result.type);
      loadTasks();
    } catch (error) {
      showMessage('Failed to delete task', 'error');
    }
  };

  const addNoteToTask = async (taskId: number, noteId: number) => {
    try {
      const result = await taskService.addNote(taskId, noteId);
      showMessage(result.message, result.type);
      loadTasks();
      loadNotes();
    } catch (error) {
      showMessage('Failed to add note to task', 'error');
    }
  };

  const removeNoteFromTask = async (taskId: number, noteId: number) => {
    try {
      const result = await taskService.removeNote(taskId, noteId);
      showMessage(result.message, result.type);
      loadTasks();
      loadNotes();
    } catch (error) {
      showMessage('Failed to remove note from task', 'error');
    }
  };

  // Note functions
  const loadNotes = async () => {
    try {
      const notesData = await noteService.loadAll();
      setNotes(notesData);
    } catch (error) {
      showMessage('Failed to load notes', 'error');
    }
  };

  const saveNote = async (noteData: Partial<Note>) => {
    try {
      const result = await noteService.save(noteData, editingNote);
      showMessage(result.message, result.type);
      setEditingNote(null);
      loadNotes();
    } catch (error) {
      showMessage('Failed to save note', 'error');
    }
  };

  const deleteNote = async (id: number) => {
    try {
      const result = await noteService.remove(id);
      showMessage(result.message, result.type);
      loadNotes();
    } catch (error) {
      showMessage('Failed to delete note', 'error');
    }
  };

  const addTaskToNote = async (noteId: number, taskId: number) => {
    try {
      const result = await noteService.addTask(noteId, taskId);
      showMessage(result.message, result.type);
      loadTasks();
      loadNotes();
    } catch (error) {
      showMessage('Failed to add task to note', 'error');
    }
  };

  const removeTaskFromNote = async (noteId: number, taskId: number) => {
    try {
      const result = await noteService.removeTask(noteId, taskId);
      showMessage(result.message, result.type);
      loadTasks();
      loadNotes();
    } catch (error) {
      showMessage('Failed to remove task from note', 'error');
    }
  };

  // Effects
  useEffect(() => {
    loadTasks();
    loadNotes();
  }, []);

  // Render the selected view (switch-style instead of ternary)
  let viewContent: React.ReactNode = null;
  switch (currentView) {
    case 'tasks':
      viewContent = (
        <>
          <TaskForm
            task={editingTask}
            onSave={saveTask}
            onCancel={() => setEditingTask(null)}
          />
          <TaskTable
            tasks={tasks}
            onEdit={setEditingTask}
            onDelete={deleteTask}
            allNotes={notes}
            onAddNote={addNoteToTask}
            onRemoveNote={removeNoteFromTask}
          />
        </>
      );
      break;
    case 'notes':
      viewContent = (
        <>
          <NoteForm
            note={editingNote}
            onSave={saveNote}
            onCancel={() => setEditingNote(null)}
          />
          <NoteTable
            notes={notes}
            onEdit={setEditingNote}
            onDelete={deleteNote}
            allTasks={tasks}
            onAddTask={addTaskToNote}
            onRemoveTask={removeTaskFromNote}
          />
        </>
      );
      break;
    case 'agents':
      viewContent = <AgentChat />;
      break;
    default:
      viewContent = null;
  }

  return (
    <div className="bg-gray-50 min-h-screen">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-3xl font-bold text-gray-900">Task & Notes Manager</h1>
        </div>
      </header>

      {/* Navigation */}
      <Navigation currentView={currentView} onViewChange={setCurrentView} />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-2 pb-8">
        {viewContent}
      </main>

      {/* Message */}
      {message && (
        <div
          className={`fixed top-4 right-4 px-4 py-2 rounded-md text-white font-medium ${
            message.type === 'success' ? 'bg-green-500' : 'bg-red-500'
          }`}
        >
          {message.text}
        </div>
      )}
    </div>
  );
}
