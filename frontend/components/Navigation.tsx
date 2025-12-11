interface NavigationProps {
  currentView: 'tasks' | 'notes' | 'agents';
  onViewChange: (view: 'tasks' | 'notes' | 'agents') => void;
}

export default function Navigation({ currentView, onViewChange }: NavigationProps) {
  return (
    <nav className="bg-white border-b">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex space-x-8">
          <button
            onClick={() => onViewChange('tasks')}
            className={`py-4 px-2 border-b-2 font-medium text-sm ${
              currentView === 'tasks'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Tasks
          </button>
          <button
            onClick={() => onViewChange('notes')}
            className={`py-4 px-2 border-b-2 font-medium text-sm ${
              currentView === 'notes'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Notes
          </button>
          <button
            onClick={() => onViewChange('agents')}
            className={`py-4 px-2 border-b-2 font-medium text-sm ${
              currentView === 'agents'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Agents
          </button>
        </div>
      </div>
    </nav>
  );
}